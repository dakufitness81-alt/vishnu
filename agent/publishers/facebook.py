"""Meta publishers: Facebook Page video posts + Instagram Reels.

Setup (Meta for Developers → create an app with Facebook Login / Instagram API):
  * Facebook Page:  FACEBOOK_PAGE_ID + FACEBOOK_PAGE_TOKEN in .env
    (the token needs pages_manage_posts / pages_read_engagement)
  * Instagram:      INSTAGRAM_BUSINESS_ACCOUNT_ID + INSTAGRAM_ACCESS_TOKEN in .env
    (business/creator IG account linked to that Page; token needs
    instagram_content_publish)
"""
from __future__ import annotations

import os

import requests

from .base import PublishResult, Publisher


def _graph_version() -> str:
    return os.environ.get("GRAPH_VERSION", "v20.0")


class FacebookPagePublisher(Publisher):
    name = "facebook"

    def publish(self, cfg, bundle) -> PublishResult:
        page = os.environ.get("FACEBOOK_PAGE_ID")
        token = os.environ.get("FACEBOOK_PAGE_TOKEN")
        if not page or not token:
            return PublishResult(
                "facebook", False,
                "Set FACEBOOK_PAGE_ID and FACEBOOK_PAGE_TOKEN in .env",
            )
        try:
            with open(bundle.video_path, "rb") as f:
                resp = requests.post(
                    f"https://graph.facebook.com/{_graph_version()}/{page}/videos",
                    data={
                        "access_token": token,
                        "title": bundle.title,
                        "description": self.caption_for(cfg, bundle, 4000),
                    },
                    files={"video": (bundle.video_path.name, f, "video/mp4")},
                    timeout=600,
                )
            body = resp.json() if resp.text else {}
            if resp.status_code >= 300:
                return PublishResult("facebook", False, f"API error {resp.status_code}: {resp.text[:200]}")
            post_id = body.get("post_id") or body.get("id")
            return PublishResult(
                "facebook", True, "Video posted to Page",
                url=f"https://facebook.com/v/{post_id}" if post_id else None,
            )
        except Exception as exc:  # noqa: BLE001
            return PublishResult("facebook", False, f"error: {exc}")


class InstagramPublisher(Publisher):
    name = "instagram"

    def publish(self, cfg, bundle) -> PublishResult:
        ig = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
        if not ig or not token:
            return PublishResult(
                "instagram", False,
                "Set INSTAGRAM_BUSINESS_ACCOUNT_ID and INSTAGRAM_ACCESS_TOKEN in .env",
            )
        try:
            with open(bundle.video_path, "rb") as f:
                create = requests.post(
                    f"https://graph.facebook.com/{_graph_version()}/{ig}/media",
                    data={
                        "media_type": "REELS",
                        "caption": self.caption_for(cfg, bundle, 2100),
                        "access_token": token,
                    },
                    files={"video": (bundle.video_path.name, f, "video/mp4")},
                    timeout=600,
                )
            if create.status_code >= 300:
                return PublishResult("instagram", False, f"container failed: {create.text[:200]}")
            container_id = create.json().get("id")
            pub = requests.post(
                f"https://graph.facebook.com/{_graph_version()}/{ig}/media_publish",
                data={"creation_id": container_id, "access_token": token},
                timeout=60,
            )
            if pub.status_code >= 300:
                return PublishResult("instagram", False, f"publish failed: {pub.text[:200]}")
            return PublishResult("instagram", True, "Reel published")
        except Exception as exc:  # noqa: BLE001
            return PublishResult("instagram", False, f"error: {exc}")
