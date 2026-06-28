import hashlib
import hmac
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.accounts.models import User

from .models import Subscription


@login_required
def billing_overview(request):
    sub, _ = Subscription.objects.get_or_create(tenant=request.user.tenant)
    sub._maybe_reset_quota()
    return render(request, "billing/overview.html", {
        "sub": sub,
        "mayar_url": getattr(settings, "MAYAR_PRO_PAYMENT_URL", ""),
    })


@csrf_exempt
@require_POST
def mayar_webhook(request):
    secret = getattr(settings, "MAYAR_WEBHOOK_SECRET", "").encode()
    if secret:
        signature = request.headers.get("X-MAYAR-SIGNATURE", "")
        expected = hmac.new(secret, request.body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return HttpResponse(status=400)

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return HttpResponse(status=400)

    event = payload.get("event", "")
    if event != "payment.paid":
        return HttpResponse(status=200)

    data = payload.get("data") or {}
    customer = data.get("customer") or {}
    customer_email = customer.get("email", "").lower().strip()
    order_id = data.get("id", "")

    if not customer_email:
        return HttpResponse(status=200)

    try:
        user = User.objects.select_related("tenant").get(email__iexact=customer_email)
        sub, _ = Subscription.objects.get_or_create(tenant=user.tenant)
        sub.activate_pro(order_id=order_id)
    except User.DoesNotExist:
        pass

    return HttpResponse(status=200)
