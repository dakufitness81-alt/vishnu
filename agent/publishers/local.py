"""Local (dry-run) publisher — the default.

Saves the finished post (video, caption, metadata) to output/published/<id>/
so the whole pipeline can be tested end-to-end with zero credentials.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from .base import PublishResult, Publisher


class LocalPublisher(Publisher):
    name = "local"

    def publish(self, cfg, bundle) -> PublishResult:
        try:
            dest = cfg.output_dir / "published" / bundle.post_id
            dest.mkdir(parents=True, exist_ok=True)
            dest_video = dest / "video.mp4"
            if Path(bundle.video_path).resolve() != dest_video.resolve():
                shutil.copyfile(bundle.video_path, dest_video)
            (dest / "caption.txt").write_text(bundle.caption, encoding="utf-8")
            (dest / "metadata.json").write_text(
                json.dumps(bundle.metadata(), indent=2, ensure_ascii=False), encoding="utf-8"
            )
            return PublishResult("local", True, f"Saved to {dest}")
        except Exception as exc:  # noqa: BLE001
            return PublishResult("local", False, f"Failed to save locally: {exc}")
