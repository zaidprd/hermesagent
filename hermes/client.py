import requests

from . import config


class BackendClient:
    """Thin HTTP client for the Hermes job API."""

    def __init__(self, base_url=None, token=None):
        self.base = (base_url or config.BACKEND_URL).rstrip("/")
        self.token = token or config.HERMES_API_TOKEN
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self.token}"

    def claim_job(self):
        r = self.session.post(f"{self.base}/api/hermes/jobs/claim/", timeout=35)
        if r.status_code == 204:
            return None
        r.raise_for_status()
        return r.json()

    def complete_job(self, job_id, result):
        r = self.session.post(
            f"{self.base}/api/hermes/jobs/{job_id}/complete/",
            json={"result": result},
            timeout=35,
        )
        r.raise_for_status()
        return r.json()

    def fail_job(self, job_id, error):
        r = self.session.post(
            f"{self.base}/api/hermes/jobs/{job_id}/fail/",
            json={"error": str(error)},
            timeout=35,
        )
        r.raise_for_status()
        return r.json()
