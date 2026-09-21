"""Command-line interface:  python -m agent <command>

Commands:
  run       full pipeline: idea -> script -> video -> publish   (default)
  ideas     print generated video ideas
  video     render one video without publishing
  publish   publish an existing post bundle (dir with video.mp4)
  loop      keep posting every N seconds (daemon mode)
  status    posting history from state.json
  auth      interactive auth for a platform (x | youtube)
  init      create .env from the template
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from . import __version__
from . import pipeline
from . import voice as voice_mod
from .config import Config
from .ideas import Idea
from .publishers import list_platforms
from .scripts import Script
from .state import State


def _split(s: str | None) -> list[str] | None:
    return [p.strip() for p in s.split(",") if p.strip()] if s else None


def _summary(bundles: list[pipeline.PostBundle]) -> None:
    print("\n" + "=" * 52)
    print("  Done.")
    for b in bundles:
        print(f"  - {b.title}")
        print(f"    video:   {b.video_path}")
        for r in b.results:
            extra = f"  -> {r.url}" if r.url else ""
            print(f"    {r.platform:<11} {'[ok]' if r.ok else '[--]'} {r.message}{extra}")


# ── commands ────────────────────────────────────────────────────────────────


def cmd_run(args) -> None:
    cfg = Config.load(args.config)
    platforms = _split(args.platforms)
    if args.dry_run:
        platforms = ["local"]
    bundles = pipeline.run(cfg, idea=args.idea, platforms=platforms, count=args.count)
    _summary(bundles)


def cmd_ideas(args) -> None:
    from . import ideas as ideas_mod

    cfg = Config.load(args.config)
    state = State(cfg.root / "state.json")
    ideas = ideas_mod.generate_ideas(cfg, count=args.count, exclude=state.idea_keys())
    print(f"\n  {len(ideas)} fresh ideas (niche: {cfg.get('agent.niche')}):\n")
    for n, i in enumerate(ideas, 1):
        print(f"  {n}. [{i.format}] {i.title}")
        print(f"     hook: {i.hook}")
        print(f"     tags: {' '.join(i.hashtags)}")
        print()


def cmd_video(args) -> None:
    from . import scripts as scripts_mod
    from . import video as video_mod
    from .ideas import Idea as _Idea

    cfg = Config.load(args.config)
    if args.idea:
        idea = _Idea(title=args.idea, hook=args.idea, topic="custom", format="custom",
                     hashtags=list(cfg.get("video.hashtags", [])))
    else:
        from . import ideas as ideas_mod

        idea = ideas_mod.generate_ideas(cfg, count=1)[0]
    print(f"  Idea: {idea.title}")
    script = scripts_mod.generate_script(cfg, idea)
    import datetime as dt

    post_id = f"{dt.datetime.now():%Y%m%d-%H%M%S}-{video_mod.slugify(idea.title, 28)}"
    outdir = cfg.output_dir / "posts" / post_id
    outdir.mkdir(parents=True, exist_ok=True)
    audio = voice_mod.synthesize(cfg, script, outdir)
    print(f"  Rendering ({'voiced' if audio else 'silent + captions'})...")
    out = video_mod.render(cfg, idea, script, audio, outdir / "video.mp4")
    print(f"  Video: {out}")


def cmd_publish(args) -> None:
    from .publishers import get_publisher

    cfg = Config.load(args.config)
    src = Path(args.bundle).expanduser().resolve()
    video_path = src / "video.mp4"
    if not video_path.exists():
        raise SystemExit(f"No video.mp4 found in {src}")
    caption = (src / "caption.txt").read_text(encoding="utf-8") if (src / "caption.txt").exists() else ""
    meta: dict = {}
    if (src / "metadata.json").exists():
        meta = json.loads((src / "metadata.json").read_text(encoding="utf-8"))
    idea = Idea(**meta["idea"]) if "idea" in meta else Idea(
        title=meta.get("title", src.name), hook=meta.get("title", src.name),
        topic="custom", format="custom", hashtags=[],
    )
    script = Script(
        title=meta.get("title", idea.title),
        hook=idea.hook,
        beats=meta.get("beats", []),
        cta=meta.get("cta", ""),
        hashtags=meta.get("hashtags", []),
    )
    bundle = pipeline.PostBundle(
        post_id=src.name, title=idea.title, idea=idea, script=script,
        video_path=video_path, caption=caption or idea.title,
    )
    platforms = _split(args.platforms) or [str(p) for p in cfg.get("agent.platforms", ["local"])]
    for name in platforms:
        res = get_publisher(name).publish(cfg, bundle)
        url = f"  -> {res.url}" if res.url else ""
        print(f"  {name:<11} {'[ok]' if res.ok else '[--]'} {res.message}{url}")


def cmd_loop(args) -> None:
    cfg = Config.load(args.config)
    platforms = _split(args.platforms)
    print(f"  Looping every {args.interval}s"
          f" ({'forever' if args.count == 0 else f'{args.count} posts'}). Ctrl-C to stop.")
    n = 0
    while True:
        try:
            bundles = pipeline.run(cfg, platforms=platforms, count=1)
            _summary(bundles)
        except Exception as exc:  # noqa: BLE001 — keep the daemon alive
            print(f"  [loop] run failed: {exc}")
        n += 1
        if args.count and n >= args.count:
            break
        sleep_for = args.interval + random.uniform(0, min(3600, args.interval * 0.1))
        print(f"  Next run in ~{int(sleep_for)}s (Ctrl-C to stop)")
        try:
            _sleep_in_chunks(sleep_for)
        except KeyboardInterrupt:
            print("\n  Stopped.")
            break


def _sleep_in_chunks(seconds: float) -> None:
    end = time.time() + seconds
    while time.time() < end:
        time.sleep(min(5, max(0.1, end - time.time())))


def cmd_status(args) -> None:
    cfg = Config.load(args.config)
    state = State(cfg.root / "state.json")
    if not state.posts:
        print("  Nothing posted yet. Try:  python -m agent run")
        return
    print(f"\n  Last {min(20, len(state.posts))} posts:")
    for p in state.posts[-20:]:
        plats = ", ".join(p.get("platforms_ok", [])) or "-"
        print(f"  {p.get('posted_at', '?')}  {plats:<16} {p.get('idea_title', '?')}")
    last = state.last_posted_at()
    if last:
        print(f"\n  Last post: {last}")


def cmd_auth(args) -> None:
    cfg = Config.load(args.config)
    if args.platform == "x":
        from .publishers.x_twitter import auth_x

        auth_x(cfg)
    elif args.platform == "youtube":
        from .publishers.youtube import auth_youtube

        auth_youtube(cfg)


def cmd_init(args) -> None:
    cfg = Config.load(args.config)
    env_path = cfg.root / ".env"
    template = cfg.root / ".env.example"
    if env_path.exists():
        print(f"  .env already exists at {env_path}")
    else:
        env_path.write_text(
            template.read_text(encoding="utf-8") if template.exists() else "# add your API keys here\n",
            encoding="utf-8",
        )
        print(f"  Created {env_path}")
    print("\n  Next steps:")
    print("    1) Edit .env — leave it empty to stay 100% offline, or add API keys")
    print("    2) Edit config.yaml — set your niche, handle, and target platforms")
    print("    3) python -m agent run        (makes a video and posts it)")


# ── entry point ─────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="agent",
        description=f"Vishnu AutoPilot v{__version__} — AI agent: ideas -> videos -> social media",
    )
    parser.add_argument("--config", default=None, help="path to config.yaml")
    sub = parser.add_subparsers(dest="command")

    s = sub.add_parser("run", help="full pipeline (default)")
    s.add_argument("--idea", help="use your own idea instead of generating one")
    s.add_argument("--platforms", help=f"comma list; options: {', '.join(list_platforms())}")
    s.add_argument("--count", type=int, default=1, help="posts to make this run")
    s.add_argument("--dry-run", action="store_true", help="publish to local only")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("ideas", help="print generated ideas")
    s.add_argument("--count", type=int, default=5)
    s.set_defaults(func=cmd_ideas)

    s = sub.add_parser("video", help="render a video without publishing")
    s.add_argument("--idea", help="use your own idea")
    s.set_defaults(func=cmd_video)

    s = sub.add_parser("publish", help="publish an existing bundle dir")
    s.add_argument("bundle", help="directory containing video.mp4 (+ caption.txt, metadata.json)")
    s.add_argument("--platforms", help=f"comma list; options: {', '.join(list_platforms())}")
    s.set_defaults(func=cmd_publish)

    s = sub.add_parser("loop", help="post automatically every N seconds")
    s.add_argument("--interval", type=int, default=86400, help="seconds between posts (default: daily)")
    s.add_argument("--count", type=int, default=0, help="stop after N posts (0 = forever)")
    s.add_argument("--platforms", help="comma list")
    s.set_defaults(func=cmd_loop)

    s = sub.add_parser("status", help="posting history")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("auth", help="interactive platform auth")
    s.add_argument("platform", choices=["x", "youtube"])
    s.set_defaults(func=cmd_auth)

    s = sub.add_parser("init", help="create .env from template")
    s.set_defaults(func=cmd_init)

    args = parser.parse_args(argv)
    if args.command is None:  # bare `python -m agent` == run
        args = parser.parse_args(["run"])
    args.func(args)
