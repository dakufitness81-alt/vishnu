"""X (Twitter) publisher + OAuth 2.0 authorization-code (PKCE) helper.

Setup:
  1. Create an app at https://developer.x.com (OAuth redirect: http://localhost:8080/callback)
  2. Put X_CLIENT_ID / X_CLIENT_SECRET in .env
  3. Run:  python -m agent auth x
Tokens are stored in secrets/x_tokens.json (git-ignored).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import time

import requests

from .base import PublishResult, Publisher

API = "https://api.x.com/2"


def _secrets_dir(cfg):
    d = cfg.root / "secrets"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _token_file(cfg):
    return _secrets_dir(cfg) / "x_tokens.json"


def load_token(cfg) -> dict | None:
    f = _token_file(cfg)
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
    env = os.environ.get("X_API_TOKEN")
    return {"access_token": env} if env else None


def auth_x(cfg) -> None:
    cid = os.environ.get("X_CLIENT_ID")
    csec = os.environ.get("X_CLIENT_SECRET")
    if not cid or not csec:
        raise SystemExit("Set X_CLIENT_ID and X_CLIENT_SECRET in .env first.")
    redirect = os.environ.get("X_REDIRECT_URI", "http://localhost:8080/callback")
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    url = (
        f"{API}/oauth2/authorize?response_type=code&client_id={cid}&redirect_uri={redirect}"
        f"&scope=tweets.read%20tweets.write%20users.read%20offline.access"
        f"&code_challenge={challenge}&code_challenge_method=S256"
    )
    print(f"\n1) Open this URL in your browser and approve access:\n\n   {url}\n")
    code = input("2) Paste the authorization code from the redirect page: ").strip()
    if not code:
        raise SystemExit("No code provided.")
    resp = requests.post(
        f"{API}/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect,
            "client_id": cid,
            "client_secret": csec,
            "code_verifier": verifier,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    _token_file(cfg).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("   X token saved to secrets/x_tokens.json")


def _upload_video(headers: dict, path) -> str:
    """Single-step v2 media upload (videos are kept under 5 MB by _shrink)."""
    b64 = base64.b64encode(path.read_bytes()).decode()
    resp = requests.post(
        f"{API}/media/upload",
        headers=headers,
        data={"media_category": "tweet_video", "media": b64, "media_type": "video/mp4"},
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()
    if "media_id" not in data:
        raise RuntimeError(f"Media init failed: {data}")
    media_id = data["media_id"]
    for _ in range(30):
        st = requests.get(f"{API}/media/upload/{media_id}", headers=headers, timeout=30).json()
        payload = st.get("data", st)
        state = payload.get("state")
        if state == "succeeded":
            return media_id
        if state in ("expired", "failed"):
            raise RuntimeError(f"Media processing {state}: {payload}")
        time.sleep(2)
    raise RuntimeError("Media processing timed out")


def _shrink(cfg, bundle):
    """Re-encode to stay under X's 5 MB upload limit."""
    import subprocess

    import imageio_ffmpeg

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    out = bundle.video_path.parent / "video_small.mp4"
    has_audio = (bundle.video_path.parent / "narration.mp3").exists() or (
        bundle.video_path.parent / "narration.wav"
    ).exists()
    for crf in (24, 27, 30, 33):
        cmd = [
            ff, "-y", "-hide_banner", "-loglevel", "error", "-i", str(bundle.video_path),
            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
        ]
        cmd += ["-c:a", "copy"] if has_audio else ["-an"]
        cmd.append(str(out))
        subprocess.run(cmd, check=True, capture_output=True)
        if out.stat().st_size <= 4_400_000:
            return out
    return out


class XPublisher(Publisher):
    name = "x"

    def publish(self, cfg, bundle) -> PublishResult:
        tok = load_token(cfg)
        if not tok or not tok.get("access_token"):
            return PublishResult(
                "x", False,
                "No X token. Set X_CLIENT_ID/X_CLIENT_SECRET in .env then run: python -m agent auth x",
            )
        headers = {"Authorization": f"Bearer {tok['access_token']}"}
        try:
            vid = bundle.video_path
            if vid.stat().st_size > 4_500_000:
                vid = _shrink(cfg, bundle)
            media_id = _upload_video(headers, vid)
            resp = requests.post(
                f"{API}/tweets",
                headers=headers,
                json={"text": self.caption_for(cfg, bundle, 275), "media": {"media_ids": [media_id]}},
                timeout=60,
            )
            if resp.status_code >= 300:
                return PublishResult("x", False, f"API error {resp.status_code}: {resp.text[:200]}")
            tweet_id = resp.json().get("data", {}).get("id", "?")
            return PublishResult("x", True, "Tweet posted", url=f"https://x.com/i/status/{tweet_id}")
        except Exception as exc:  # noqa: BLE001
            return PublishResult("x", False, f"error: {exc}")
