"""Optional LLM access (OpenAI or any OpenAI-compatible endpoint, e.g. OpenRouter).

The agent is fully functional without an LLM (offline idea/script engine);
this module is only used when an API key is present in the environment.
"""
from __future__ import annotations

import json
import os
import re

import requests


def api_key() -> str | None:
    return os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY")


def available() -> bool:
    return bool(api_key())


def _endpoint() -> tuple[str, str]:
    """Return (base_url, api_key) for the configured provider."""
    if os.environ.get("OPENAI_API_KEY"):
        return "https://api.openai.com/v1", os.environ["OPENAI_API_KEY"]
    if os.environ.get("OPENROUTER_API_KEY"):
        return "https://openrouter.ai/api/v1", os.environ["OPENROUTER_API_KEY"]
    raise RuntimeError(
        "No LLM API key found. Add OPENAI_API_KEY (or OPENROUTER_API_KEY) to .env, "
        "or set llm.provider: none to use the offline engine only."
    )


def chat(
    model: str,
    system: str,
    user: str,
    max_tokens: int = 900,
    temperature: float = 0.9,
    timeout: int = 90,
) -> str:
    base, key = _endpoint()
    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    resp = requests.post(
        f"{base}/chat/completions",
        json=payload,
        headers={"Authorization": f"Bearer {key}"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def parse_json(text: str):
    """Extract the first JSON object/array from a (possibly fenced) model reply."""
    text = (text or "").strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fence:
        text = fence.group(1).strip()
    for open_ch, close_ch in (("{", "}"), ("[", "]")):
        start, end = text.find(open_ch), text.rfind(close_ch)
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError(f"No JSON found in model reply: {text[:200]!r}")
