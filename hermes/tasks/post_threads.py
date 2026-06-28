"""post_threads task: post an article summary to Threads via Graph API."""
import requests


def run(payload, gateway):
    user_id = payload["threads_user_id"]
    access_token = payload["threads_access_token"]
    text = payload["text"]

    # Step 1: create media container
    resp = requests.post(
        f"https://graph.threads.net/v1.0/{user_id}/threads",
        params={
            "media_type": "TEXT",
            "text": text,
            "access_token": access_token,
        },
        timeout=30,
    )
    resp.raise_for_status()
    creation_id = resp.json()["id"]

    # Step 2: publish container
    resp2 = requests.post(
        f"https://graph.threads.net/v1.0/{user_id}/threads_publish",
        params={
            "creation_id": creation_id,
            "access_token": access_token,
        },
        timeout=30,
    )
    resp2.raise_for_status()
    post_id = resp2.json()["id"]

    # Step 3: get permalink
    resp3 = requests.get(
        f"https://graph.threads.net/v1.0/{post_id}",
        params={"fields": "permalink", "access_token": access_token},
        timeout=30,
    )
    post_url = ""
    if resp3.ok:
        post_url = resp3.json().get("permalink", "")

    return {"post_id": post_id, "post_url": post_url}
