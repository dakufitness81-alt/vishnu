"""Platform registry. Importing this module is safe — heavy SDKs are only
imported lazily inside each publisher's publish()/auth() calls."""
from __future__ import annotations

from .base import PublishResult, Publisher
from .facebook import FacebookPagePublisher, InstagramPublisher
from .local import LocalPublisher
from .tiktok import TikTokPublisher
from .x_twitter import XPublisher
from .youtube import YouTubePublisher

REGISTRY: dict[str, type[Publisher]] = {
    cls.name: cls
    for cls in (
        LocalPublisher,
        YouTubePublisher,
        TikTokPublisher,
        XPublisher,
        FacebookPagePublisher,
        InstagramPublisher,
    )
}

_ALIASES = {
    "twitter": "x",
    "yt": "youtube",
    "ig": "instagram",
    "fb": "facebook",
    "dry-run": "local",
    "dry": "local",
}


def get_publisher(name: str) -> Publisher:
    key = _ALIASES.get(name.lower().strip(), name.lower().strip())
    if key not in REGISTRY:
        raise SystemExit(f"Unknown platform '{name}'. Options: {', '.join(sorted(REGISTRY))}")
    return REGISTRY[key]()


def list_platforms() -> list[str]:
    return sorted(REGISTRY)
