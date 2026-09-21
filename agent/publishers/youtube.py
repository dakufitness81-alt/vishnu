"""YouTube (Shorts-friendly) publisher via the official API client.

Setup:
  1. Google Cloud Console → enable YouTube Data API v3 → OAuth client (Desktop)
  2. Download the client_secret JSON and set YOUTUBE_CLIENT_SECRET_JSON in .env
  3. Run:  python -m agent auth youtube
Requires: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""
from __future__ import annotations

import json
import os

from .base import PublishResult, Publisher

EXTRA_DEPS = ("google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _token_file(cfg):
    return cfg.root / "secrets" / "youtube_token.json"


def _load_credentials(cfg):
    from google.oauth2.credentials import Credentials

    tok = json.loads(_token_file(cfg).read_text(encoding="utf-8"))
    creds = Credentials(
        None,
        scopes=SCOPES,
        token=tok.get("token"),
        refresh_token=tok.get("refresh_token"),
        client_id=tok.get("client_id"),
        client_secret=tok.get("client_secret"),
        expiry=tok.get("expiry"),
    )
    if not creds.valid and creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request

        creds.refresh(Request())
        _token_file(cfg).write_text(json.dumps({
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "expiry": str(creds.expiry),
        }, indent=2), encoding="utf-8")
    return creds


def auth_youtube(cfg) -> None:
    js = os.environ.get("YOUTUBE_CLIENT_SECRET_JSON")
    if not js:
        raise SystemExit(
            "Set YOUTUBE_CLIENT_SECRET_JSON in .env (path to the OAuth client JSON "
            "from Google Cloud Console). Then re-run: python -m agent auth youtube"
        )
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(js, SCOPES)
    creds = flow.run_console(message="Open the URL, authorize, then paste the code here: ")
    d = cfg.root / "secrets"
    d.mkdir(parents=True, exist_ok=True)
    _token_file(cfg).write_text(json.dumps({
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "expiry": str(creds.expiry),
    }, indent=2), encoding="utf-8")
    print("   YouTube token saved to secrets/youtube_token.json")


class YouTubePublisher(Publisher):
    name = "youtube"

    def publish(self, cfg, bundle) -> PublishResult:
        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
        except ImportError:
            return PublishResult(
                "youtube", False,
                f"Missing SDK — run: pip install {' '.join(EXTRA_DEPS)}",
            )
        if not _token_file(cfg).exists():
            return PublishResult(
                "youtube", False,
                "No credentials. Set YOUTUBE_CLIENT_SECRET_JSON in .env then run: python -m agent auth youtube",
            )
        try:
            creds = _load_credentials(cfg)
            svc = build("youtube", "v3", credentials=creds, cache_discovery=False)
            body = {
                "snippet": {
                    "title": bundle.title[:100],
                    "description": self.caption_for(cfg, bundle, 4800),
                    "tags": bundle.script.hashtags[:10],
                    "categoryId": "17",
                },
                "status": {
                    "privacyStatus": os.environ.get("YOUTUBE_PRIVACY", "public"),
                    "selfDeclaredMadeForKids": False,
                },
            }
            req = svc.videos().insert(
                part="snippet,status",
                body=body,
                media_body=MediaFileUpload(str(bundle.video_path), mimetype="video/mp4"),
            )
            res = req.execute()
            return PublishResult("youtube", True, "Video uploaded", url=f"https://youtu.be/{res.get('id')}")
        except Exception as exc:  # noqa: BLE001
            return PublishResult("youtube", False, f"error: {exc}")
