"""HTTP API consumed by the Hermes worker.

Auth is a single static Bearer token (HERMES_API_TOKEN). One trusted worker,
so no need for DRF/JWT yet.
"""
import json
from functools import wraps

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .handlers import handle_completion, handle_failure
from .models import Job


def hermes_auth(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth[7:] if auth.startswith("Bearer ") else ""
        if not settings.HERMES_API_TOKEN or token != settings.HERMES_API_TOKEN:
            return JsonResponse({"detail": "unauthorized"}, status=401)
        return view(request, *args, **kwargs)

    return wrapper


def _load_body(request):
    try:
        return json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None


@csrf_exempt
@require_POST
@hermes_auth
def claim_job(request):
    """Atomically claim the oldest pending job. 204 if none available."""
    with transaction.atomic():
        job = (
            Job.objects.select_for_update(skip_locked=True)
            .filter(status=Job.PENDING)
            .order_by("created_at")
            .first()
        )
        if job is None:
            return HttpResponse(status=204)
        job.status = Job.RUNNING
        job.started_at = timezone.now()
        job.save(update_fields=["status", "started_at", "updated_at"])

    return JsonResponse(
        {"id": job.id, "agent_type": job.agent_type, "payload": job.payload}
    )


@csrf_exempt
@require_POST
@hermes_auth
def complete_job(request, pk):
    body = _load_body(request)
    if body is None:
        return JsonResponse({"detail": "invalid json"}, status=400)
    job = Job.objects.filter(pk=pk).first()
    if job is None:
        return JsonResponse({"detail": "not found"}, status=404)

    job.result = body.get("result", {})
    job.status = Job.COMPLETED
    job.completed_at = timezone.now()
    job.save(update_fields=["result", "status", "completed_at", "updated_at"])
    handle_completion(job)
    return JsonResponse({"ok": True})


@csrf_exempt
@require_POST
@hermes_auth
def fail_job(request, pk):
    body = _load_body(request) or {}
    job = Job.objects.filter(pk=pk).first()
    if job is None:
        return JsonResponse({"detail": "not found"}, status=404)

    job.error_message = (body.get("error") or "")[:5000]
    job.status = Job.FAILED
    job.completed_at = timezone.now()
    job.save(update_fields=["error_message", "status", "completed_at", "updated_at"])
    handle_failure(job)
    return JsonResponse({"ok": True})
