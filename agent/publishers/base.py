"""Publisher interface shared by all platform integrations."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PublishResult:
    platform: str
    ok: bool
    message: str
    url: str | None = None


class Publisher(ABC):
    name = "base"

    @abstractmethod
    def publish(self, cfg, bundle) -> PublishResult:
        """Publish *bundle* (idea + script + video.mp4 + caption) to this platform."""

    def caption_for(self, cfg, bundle, limit: int) -> str:
        """Truncate the caption for platforms with strict limits (e.g. X: 280)."""
        text = bundle.caption
        if len(text) <= limit:
            return text
        return text[: limit - 1].rstrip() + "…"
