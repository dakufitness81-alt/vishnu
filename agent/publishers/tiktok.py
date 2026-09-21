"""TikTok Content Posting API publisher.

Requires an approved TikTok developer app with the Content Posting API scope
(https://developers.tiktok.com). Set TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET
in .env. Note: on a brand-new app TikTok typically starts posts in a private
queue for review.
"""
from __future__ import annotations

import os

import requests

from .base import PublishResult, Publisher

BASE = "https://open.tiktokapis.com"


def _basic_auth(cfg):
    k = os.environ.get("TIKTOK_CLIENT_KEY")
    s = os.environ.get("TIKTOK_CLIENT_SECRET")
    return (k, s) if k and s else None


def _token(auth) -> str:
    resp = requests.post(
        f"{BASE}/v2/oauth2/token/",
        auth=auth,
        data={"grant_type": "client_credentials"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


class TikTokPublisher(Publisher):
    name = "tiktok"

    def publish(self, cfg, bundle) -> PublishResult:
        auth = _basic_auth(cfg)
        if not auth:
            return PublishResult(
                "tiktok", False,
                "Set TIKTOK_CLIENT_KEY/TIKTOK_CLIENT_SECRET in .env "
                "(approved Content Posting API app required)",
            )
        try:
            token = _token(auth)
            headers = {"Authorization": f"Bearer {token}"}
            data = bundle.video_path.read_bytes()
            init = requests.post(
                f"{BASE}/v2/post/publish/video/init/",
                headers=headers,
                json={
                    "video_size": len(data),
                    "video_title": bundle.title[:2200],
                    "source_info": {"source": "PULL_FROM_URL", "video_url": ""},
                },
                timeout=60,
            )
            if init.status_code >= 300:
                return PublishResult("tiktok", False, f"init failed: {init.text[:200]}")
            d = init.json()["data"]
            requests.put(d["upload_url"], data=data, timeout=600)
            complete = requests.post(
                f"{BASE}/v2/post/publish/video/complete/",
                headers=headers,
                json={
                    "publish_id": d["publish_id"],
                    "post_info": {
                        "title": bundle.title,
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                    },
                },
                timeout=60,
            )
            if complete.status_code >= 300:
                return PublishResult("tiktok", False, f"complete failed: {complete.text[:200]}")
            return PublishResult("tiktok", True, "Video queued on TikTok (may need review)")
        except Exception as exc:  # noqa: BLE001
            return PublishResult("tiktok", False, f"error: {exc}")
