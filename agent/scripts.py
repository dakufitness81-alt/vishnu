"""Turn an Idea into a slide-by-slide video script.

Offline engine: deterministic per idea (same idea → same script), uses the
niche tip bank. LLM engine (optional) writes custom beats when a key exists.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from . import llm
from .ideas import DEFAULT_NICHE, Idea, NICHES

CTAS = [
    "Follow for one tip like this every day.",
    "Save this and try it this week.",
    "Share it with someone who needs it.",
    "Comment TIP and I'll send the full routine.",
]


@dataclass
class Script:
    title: str
    hook: str
    beats: list[str]
    cta: str
    hashtags: list[str] = field(default_factory=list)


def _local_script(cfg, idea: Idea) -> Script:
    niche = cfg.get("agent.niche", DEFAULT_NICHE)
    bank = NICHES.get(niche, NICHES[DEFAULT_NICHE])
    rng = random.Random(idea.key())  # stable per idea
    n = max(1, min(6, int(cfg.get("video.beats", 4))))
    beats = rng.sample(bank["tips"], k=min(n, len(bank["tips"])))
    cta = str(cfg.get("video.cta") or "").strip() or rng.choice(CTAS)
    hashtags = list(idea.hashtags or bank["hashtags"])[:4]
    return Script(title=idea.title, hook=idea.hook, beats=beats, cta=cta, hashtags=hashtags)


def _llm_script(cfg, idea: Idea) -> Script | None:
    niche = cfg.get("agent.niche", DEFAULT_NICHE)
    model = cfg.get("llm.model", "gpt-4o-mini")
    system = (
        "You write scripts for 30-second vertical videos. Each beat is one spoken "
        "slide of 5-12 words, plain words only, no emojis, no hashtags."
    )
    user = (
        f"Niche: {niche}\nIdea: {idea.title}\nHook: {idea.hook}\n\n"
        "Write the video script. Return JSON: "
        '{"title": "...", "hook": "...", "beats": ["...", "...", "..."], "cta": "..."} '
        "with 3-5 beats, hook under 45 chars, cta one sentence."
    )
    data = llm.parse_json(llm.chat(model, system, user, max_tokens=700, temperature=0.85))
    beats = [str(b).strip() for b in data.get("beats", []) if str(b).strip()]
    if not beats:
        return None
    return Script(
        title=str(data.get("title") or idea.title).strip()[:80],
        hook=str(data.get("hook") or idea.hook).strip()[:80],
        beats=beats[:5],
        cta=str(data.get("cta") or CTAS[0]).strip()[:120],
        hashtags=list(idea.hashtags)[:4],
    )


def generate_script(cfg, idea: Idea) -> Script:
    provider = str(cfg.get("llm.provider", "auto")).lower()
    if provider in ("auto", "openai") and llm.available():
        try:
            script = _llm_script(cfg, idea)
            if script:
                return script
        except Exception as exc:  # noqa: BLE001 — fall back to offline engine
            print(f"  ! LLM script generation failed ({exc}); using offline engine.")
    return _local_script(cfg, idea)
