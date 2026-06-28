"""Hermes worker loop: claim a job, run the matching task, report result."""
import time
import traceback

from . import config
from .client import BackendClient
from .gateway import AIGateway
from .tasks import generate_article, generate_title, publish_wordpress

TASKS = {
    "generate_title": generate_title.run,
    "generate_article": generate_article.run,
    "publish_wordpress": publish_wordpress.run,
}


def main():
    client = BackendClient()
    gateway = AIGateway()
    print(
        f"[hermes] worker started — backend={config.BACKEND_URL} "
        f"model={config.AI_TEXT_MODEL}"
    )

    while True:
        try:
            job = client.claim_job()
        except Exception as exc:  # backend unreachable, etc.
            print(f"[hermes] claim error: {exc}")
            time.sleep(config.POLL_INTERVAL)
            continue

        if not job:
            time.sleep(config.POLL_INTERVAL)
            continue

        job_id = job["id"]
        agent_type = job["agent_type"]
        payload = job.get("payload") or {}
        print(f"[hermes] job #{job_id} -> {agent_type}")

        task = TASKS.get(agent_type)
        if task is None:
            client.fail_job(job_id, f"unknown agent_type: {agent_type}")
            continue

        try:
            result = task(payload, gateway)
            client.complete_job(job_id, result)
            print(f"[hermes] job #{job_id} done")
        except Exception as exc:
            traceback.print_exc()
            try:
                client.fail_job(job_id, str(exc))
            except Exception as report_exc:
                print(f"[hermes] failed to report failure: {report_exc}")


if __name__ == "__main__":
    main()
