"""Configuration: config.yaml + .env loading with sane defaults."""
from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any

import yaml

DEFAULTS: dict[str, Any] = {
    "agent": {
        "name": "Vishnu AutoPilot",
        "niche": "fitness",
        "handle": "@yourhandle",
        "platforms": ["local"],
        "ideas_per_run": 3,
    },
    "video": {
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "crf": 20,
        "beats": 4,
        "min_slide_seconds": 2.2,
        "max_slide_seconds": 6.0,
        "cta": "Follow for one tip like this every day.",
        "hashtags": ["#fitness", "#dailytips"],
    },
    "voice": {
        "provider": "auto",  # auto | openai | espeak | none
        "openai_model": "tts-1",
        "openai_voice": "alloy",
    },
    "llm": {
        "provider": "auto",  # auto | openai | none
        "model": "gpt-4o-mini",
    },
    "output": {
        "dir": "output",
    },
}


def deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def find_project_root(start: str | os.PathLike | None = None) -> Path:
    """Walk up from *start* (default: cwd) until we find config.yaml or the package."""
    current = Path(start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "config.yaml").exists() or (candidate / "agent").is_dir():
            return candidate
    return current


def load_env_file(path: Path) -> None:
    """Load KEY=VALUE pairs from .env without overriding the real environment."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


class Config:
    def __init__(self, raw: dict[str, Any], root: Path):
        self.raw = raw
        self.root = Path(root)

    @classmethod
    def load(cls, path: str | os.PathLike | None = None) -> "Config":
        if path is None:
            root = find_project_root()
            path = root / "config.yaml"
        else:
            path = Path(path).resolve()
            root = path.parent
        data: dict[str, Any] = {}
        if path.exists():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        cfg = cls(deep_merge(DEFAULTS, data), root)
        load_env_file(cfg.root / ".env")
        return cfg

    def get(self, dotted: str, default: Any = None) -> Any:
        node: Any = self.raw
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    @property
    def output_dir(self) -> Path:
        d = self.root / self.get("output.dir", "output")
        d.mkdir(parents=True, exist_ok=True)
        return d
