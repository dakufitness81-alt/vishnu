"""Compose caption-style vertical videos from a Script.

Slides (PIL-rendered PNGs) → ffmpeg concat → H.264 MP4, optionally muxed with
narration audio so slide timing follows the voiceover length.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = {
    True: [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ],
    False: [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ],
}

PALETTES = [
    ((10, 15, 30), (56, 189, 248)),
    ((12, 12, 20), (163, 230, 53)),
    ((15, 12, 26), (236, 72, 153)),
    ((14, 14, 16), (251, 191, 36)),
    ((8, 30, 26), (45, 212, 191)),
]
ACCENTS = [(56, 189, 248), (163, 230, 53), (236, 72, 153), (251, 191, 36), (45, 212, 191)]
SHADOW = (0, 0, 0)
WHITE = (245, 247, 250)
GREY = (203, 210, 220)
TRACK = (44, 48, 60)


def slugify(text: str, max_len: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].rstrip("-") or "post"


def _font(size: int, bold: bool = True) -> ImageFont.ImageFont:
    for path in FONT_CANDIDATES[bold]:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:  # noqa: BLE001
                pass
    return ImageFont.load_default()


def _sanitize(text: str) -> str:
    """Keep characters the bundled font can render (drop emoji & exotic glyphs)."""
    return re.sub(
        r"[^\x09\x0A\x20-\x7E\u00A0-\u024F\u2000-\u206F\u20AC\u2190-\u21FF\u2200-\u22FF\u25A0-\u25FF]",
        "",
        text,
    ).strip()


def _center_crop(img: Image.Image, w: int, h: int) -> Image.Image:
    target = w / h
    src = img.width / img.height
    if src > target:
        new_w = int(img.height * target)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    elif src < target:
        new_h = int(img.width / target)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))
    return img.resize((w, h), Image.LANCZOS)


def _background(w: int, h: int, index: int, assets: list[Path]) -> Image.Image:
    if assets:
        img = Image.open(assets[index % len(assets)]).convert("RGB")
        img = _center_crop(img, w, h)
        return Image.blend(img, Image.new("RGB", (w, h), (8, 10, 16)), 0.45)
    c1, c2 = PALETTES[index % len(PALETTES)]
    small = Image.new("RGB", (64, 114))
    for y in range(114):
        t = y / 113
        color = tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
        for x in range(64):
            small.putpixel((x, y), color)
    return small.resize((w, h), Image.BICUBIC)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: float) -> list[str]:
    lines: list[str] = []
    cur = ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def _draw_block(
    draw: ImageDraw.ImageDraw,
    cx: int,
    center_y: int,
    text: str,
    font,
    fill,
    max_width: float,
    gap: int = 14,
) -> int:
    lines = _wrap(draw, text, font, max_width)
    line_h = font.size + gap
    total = line_h * len(lines) - gap
    y = int(center_y - total / 2)
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text((cx - w / 2 + 4, y + 4), line, font=font, fill=SHADOW)
        draw.text((cx - w / 2, y), line, font=font, fill=fill)
        y += line_h
    return y


def _slide_image(cfg, w: int, h: int, kind: str, text: str, num: int, total: int, idx: int, assets: list[Path]) -> Image.Image:
    from .ideas import DEFAULT_NICHE, NICHES

    img = _background(w, h, idx, assets).convert("RGB")
    draw = ImageDraw.Draw(img)
    accent = ACCENTS[idx % len(ACCENTS)]
    handle = str(cfg.get("agent.handle", "@yourhandle"))
    niche = str(cfg.get("agent.niche", DEFAULT_NICHE))
    label = NICHES.get(niche, NICHES[DEFAULT_NICHE])["label"]
    brand = f"{label}  •  DAILY TIPS"
    text = _sanitize(text)

    if kind == "hook":
        draw.text((w // 2, 150), brand, font=_font(34, bold=False), fill=accent, anchor="mt")
        _draw_block(draw, w // 2, int(h * 0.44), text, _font(92), WHITE, w - 200, gap=18)
        draw.text((w // 2, h - 170), handle, font=_font(46), fill=GREY, anchor="mm")

    elif kind == "point":
        r, cxc, cyc = 58, 140, 300
        draw.ellipse([cxc - r, cyc - r, cxc + r, cyc + r], fill=accent)
        draw.text((cxc, cyc + 2), str(num), font=_font(64), fill=(10, 10, 15), anchor="mm")
        draw.text((230, cyc), f"OF {total}", font=_font(42), fill=accent, anchor="lm")
        draw.text((w - 120, 170), brand, font=_font(30, bold=False), fill=(150, 158, 172), anchor="rm")
        _draw_block(draw, w // 2, int(h * 0.5), text, _font(64), WHITE, w - 220, gap=14)
        pad, bar_y = 120, h - 140
        total_w = w - 2 * pad
        draw.rounded_rectangle([pad, bar_y, pad + total_w, bar_y + 14], radius=7, fill=TRACK)
        draw.rounded_rectangle([pad, bar_y, pad + int(total_w * num / total), bar_y + 14], radius=7, fill=accent)
        draw.text((w // 2, h - 90), handle, font=_font(36, bold=False), fill=GREY, anchor="mm")

    else:  # cta
        draw.text((w // 2, 150), brand, font=_font(34, bold=False), fill=accent, anchor="mt")
        _draw_block(draw, w // 2, int(h * 0.40), text, _font(84), WHITE, w - 180, gap=16)
        draw.text((w // 2, int(h * 0.56)), handle, font=_font(64), fill=accent, anchor="mm")
        hashtags = "  ".join(str(h) for h in list(cfg.get("video.hashtags", []))[:2])
        if hashtags:
            draw.text((w // 2, int(h * 0.63)), hashtags, font=_font(34, bold=False), fill=GREY, anchor="mm")

    return img


def render(cfg, idea, script, audio: Path | None, out_path: Path) -> Path:
    """Render the video for *script*; returns the output path."""
    w = int(cfg.get("video.width", 1080))
    h = int(cfg.get("video.height", 1920))
    fps = int(cfg.get("video.fps", 30))
    crf = int(cfg.get("video.crf", 20))

    assets_dir = cfg.root / "assets"
    assets = (
        sorted(a for a in assets_dir.glob("bg*") if a.suffix.lower() in {".jpg", ".jpeg", ".png"})
        if assets_dir.exists()
        else []
    )

    slides: list[tuple[str, str, int, int]] = [("hook", script.hook, 0, 0)]
    slides += [("point", b, i + 1, len(script.beats)) for i, b in enumerate(script.beats)]
    slides.append(("cta", script.cta, 0, 0))

    mins = float(cfg.get("video.min_slide_seconds", 2.2))
    maxs = float(cfg.get("video.max_slide_seconds", 6.0))
    durs = [
        2.0 if kind == "hook" else max(mins, min(maxs, 1.2 + 0.45 * len(text.split())))
        for kind, text, _, _ in slides
    ]
    if audio:
        adur = _probe(audio)
        if adur > 0.5:
            scale = adur / sum(durs)
            durs = [d * scale for d in durs]
    total = sum(durs)

    workdir = out_path.parent / "frames"
    workdir.mkdir(parents=True, exist_ok=True)

    frame_paths: list[Path] = []
    for i, (kind, text, num, tot) in enumerate(slides):
        p = workdir / f"slide_{i:02d}.png"
        _slide_image(cfg, w, h, kind, text, num, tot, i, assets).save(p)
        frame_paths.append(p)

    # Encode with dense per-slide inputs (each image looped for exactly its
    # duration) joined by the concat *filter* — the concat *demuxer* emits one
    # frame per slide, which breaks fade filters and duration math.
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y", "-hide_banner", "-loglevel", "error"]
    for p, d in zip(frame_paths, durs):
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-r", str(fps), "-i", str(p)]
    if audio:
        cmd += ["-i", str(audio)]
    n = len(slides)
    labels = "".join(f"[{i}:v]" for i in range(n))
    vf = (
        f"{labels}concat=n={n}:v=1:a=0,"
        f"fade=t=in:st=0:d=0.4,"
        f"fade=t=out:st={max(0.0, total - 0.6):.3f}:d=0.6,"
        f"format=yuv420p[v]"
    )
    cmd += ["-filter_complex", vf, "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-r", str(fps)]
    if audio:
        cmd += ["-map", f"{n}:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += [str(out_path)]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {proc.stderr[-800:]}")
    return out_path


def _probe(path: Path) -> float:
    from .voice import probe_duration

    return probe_duration(path)
