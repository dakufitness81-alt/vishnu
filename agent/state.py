"""Posting history and dedupe, persisted to state.json in the project root."""
from __future__ import annotations

import json
from pathlib import Path


class State:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.data: dict = {"posts": []}
        self.load()

    def load(self) -> None:
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8")) or {"posts": []}
            except json.JSONDecodeError:
                self.data = {"posts": []}
        self.data.setdefault("posts", [])

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    def idea_keys(self) -> set[str]:
        return {p.get("idea_key", "") for p in self.data["posts"] if p.get("idea_key")}

    def record(self, entry: dict) -> None:
        self.data["posts"].append(entry)
        self.save()

    @property
    def posts(self) -> list[dict]:
        return self.data["posts"]

    def last_posted_at(self, platform: str | None = None) -> str | None:
        for p in reversed(self.data["posts"]):
            if platform is None or platform in (p.get("platforms_ok") or []):
                return p.get("posted_at")
        return None
