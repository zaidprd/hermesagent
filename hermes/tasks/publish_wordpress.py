"""publish_wordpress task: post a generated article to a WordPress site via REST API."""
import base64

import markdown as md
import requests


def run(payload, gateway):
    title = payload["title"]
    body_markdown = payload.get("body", "")
    meta_description = payload.get("meta_description", "")
    featured_image_url = payload.get("featured_image_url", "")

    wp_site_url = payload["wp_site_url"].rstrip("/")
    wp_username = payload["wp_username"]
    wp_app_password = payload["wp_app_password"]

    body_html = md.markdown(body_markdown, extensions=["extra", "nl2br"])

    credentials = base64.b64encode(
        f"{wp_username}:{wp_app_password}".encode()
    ).decode()

    post_data = {
        "title": title,
        "content": body_html,
        "status": "publish",
        "excerpt": meta_description,
    }

    resp = requests.post(
        f"{wp_site_url}/wp-json/wp/v2/posts",
        json=post_data,
        headers={"Authorization": f"Basic {credentials}"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    return {
        "post_id": data["id"],
        "post_url": data.get("link", ""),
    }
