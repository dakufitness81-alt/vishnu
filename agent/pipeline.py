"""The full agent pipeline: idea → script → voice → video → publish → state."""
from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import ideas as ideas_mod
from . import llm
from . import scripts as scripts_mod
from . import video
from . import voice
from .ideas import Idea
from .publishers import get_publisher
from .scripts import Script
from .state import State


@dataclass
class PostBundle:
    post_id: str
    title: str
    idea: Idea
    script: Script
    video_path: Path
    caption: str
    results: list = field(default_factory=list)

    def metadata(self) -> dict:
        return {
            "post_id": self.post_id,
            "title": self.title,
            "idea": asdict(self.idea),
            "beats": list(self.script.beats),
            "cta": self.script.cta,
            "hashtags": list(self.script.hashtags),
            "caption": self.caption,
            "video": str(self.video_path),
            "results": [asdict(r) for r in self.results],
        }


def build_caption(cfg, idea: Idea, script: Script) -> str:
    lines = [script.title.strip(), ""]
    lines += [f"- {b}" for b in script.beats]
    lines += ["", script.cta.strip(), ""]
    if script.hashtags:
        lines.append(" ".join(script.hashtags))
    return "\n".join(lines).strip()


def run(
    cfg,
    idea: str | Idea | None = None,
    platforms: list[str] | None = None,
    count: int = 1,
) -> list[PostBundle]:
    """Run the pipeline *count* time(s); returns the produced bundles."""
    platforms = platforms or [str(p) for p in cfg.get("agent.platforms", ["local"])]
    state = State(cfg.root / "state.json")
    bundles: list[PostBundle] = []

    for i in range(max(1, count)):
        print(f"\n==== Post {i + 1}/{max(1, count)} " + "=" * 40)

        # 1 ─ Idea
        if isinstance(idea, str):
            chosen = Idea(
                title=idea, hook=idea, topic="custom", format="custom",
                hashtags=list(cfg.get("video.hashtags", [])),
            )
            print(f"  [idea]    yours: {chosen.title}")
            idea = None  # any further posts in this run are auto-generated
        elif idea is not None:
            chosen = idea
            idea = None
        else:
            candidates = ideas_mod.generate_ideas(
                cfg,
                count=int(cfg.get("agent.ideas_per_run", 3)),
                exclude=state.idea_keys(),
            )
            chosen = candidates[0]
            print(f"  [idea]    {chosen.title}  (format: {chosen.format})")

        # 2 ─ Script
        script = scripts_mod.generate_script(cfg, chosen)
        engine = "LLM" if llm.available() else "offline engine"
        print(f"  [script]  {len(script.beats)} beats via {engine}")

        # 3 ─ Video
        post_id = f"{dt.datetime.now():%Y%m%d-%H%M%S}-{video.slugify(chosen.title, 28)}"
        outdir = cfg.output_dir / "posts" / post_id
        outdir.mkdir(parents=True, exist_ok=True)
        audio = voice.synthesize(cfg, script, outdir)
        mode = "voiced" if audio else "silent + captions"
        print(f"  [video]   rendering ({mode})...")
        video_path = video.render(cfg, chosen, script, audio, outdir / "video.mp4")
        caption = build_caption(cfg, chosen, script)
        bundle = PostBundle(
            post_id=post_id,
            title=chosen.title,
            idea=chosen,
            script=script,
            video_path=video_path,
            caption=caption,
        )

        # 4 ─ Publish
        ok_any = False
        for name in platforms:
            publisher = get_publisher(name)
            print(f"  [publish] {name} ...")
            res = publisher.publish(cfg, bundle)
            bundle.results.append(res)
            url = f"  -> {res.url}" if res.url else ""
            print(f"            {'OK ' if res.ok else 'FAIL'} {res.message}{url}")
            ok_any = ok_any or res.ok

        # 5 ─ State
        if ok_any:
            state.record({
                "post_id": post_id,
                "idea_key": chosen.key(),
                "idea_title": chosen.title,
                "posted_at": dt.datetime.now().isoformat(timespec="seconds"),
                "platforms_ok": [r.platform for r in bundle.results if r.ok],
                "video": str(video_path),
            })
        else:
            print("  [state]   nothing accepted — not recorded (will retry next run)")

        bundles.append(bundle)
    return bundles
