"""Narration for videos.

Provider resolution (voice.provider):
  auto   → OpenAI TTS if OPENAI_API_KEY/OPENROUTER_API_KEY is set,
           else espeak-ng if installed, else silent (captions carry the message)
  openai → force OpenAI-compatible /v1/audio/speech
  espeak → force local espeak-ng / espeak
  none   → always silent
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from . import llm


def script_to_text(script) -> str:
    parts = [script.hook, *script.beats, script.cta]
    return ". ".join(p.strip().rstrip(".") for p in parts if p and p.strip())


def synthesize(cfg, script, workdir: Path) -> Path | None:
    """Create narration audio next to the video if a provider is available."""
    provider = str(cfg.get("voice.provider", "auto")).lower()
    if provider == "none":
        return None
    if provider in ("auto", "openai") and llm.available():
        out = _openai_tts(cfg, script, workdir)
        if out:
            return out
    if provider in ("auto", "espeak"):
        exe = shutil.which("espeak-ng") or shutil.which("espeak")
        if exe:
            out = _espeak(exe, script, workdir)
            if out:
                return out
    return None


def _openai_tts(cfg, script, workdir: Path) -> Path | None:
    import requests

    try:
        base, key = llm._endpoint()
        model = os.environ.get("TTS_MODEL") or str(cfg.get("voice.openai_model", "tts-1"))
        voice = os.environ.get("TTS_VOICE") or str(cfg.get("voice.openai_voice", "alloy"))
        resp = requests.post(
            f"{base}/audio/speech",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": model, "voice": voice, "input": script_to_text(script)[:4000]},
            timeout=120,
        )
        if resp.status_code != 200:
            print(f"  ! TTS failed ({resp.status_code}): {resp.text[:200]}")
            return None
        out = workdir / "narration.mp3"
        out.write_bytes(resp.content)
        return out
    except Exception as exc:  # noqa: BLE001
        print(f"  ! TTS unavailable: {exc}")
        return None


def _espeak(exe: str, script, workdir: Path) -> Path | None:
    try:
        out = workdir / "narration.wav"
        subprocess.run(
            [exe, "-v", "en-us", "-s", "168", "-w", str(out), script_to_text(script)],
            check=True,
            timeout=180,
            capture_output=True,
        )
        return out if out.exists() else None
    except Exception as exc:  # noqa: BLE001
        print(f"  ! espeak failed: {exc}")
        return None


def probe_duration(path: Path) -> float:
    """Read media duration in seconds using ffmpeg (last ``time=`` stamp)."""
    import imageio_ffmpeg

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.run(
        [ff, "-hide_banner", "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    best = 0.0
    for token in proc.stderr.split():
        if token.startswith("time="):
            try:
                h, m, s = token[5:].split(":")
                best = float(h) * 3600 + float(m) * 60 + float(s)
            except ValueError:
                pass
    return best
