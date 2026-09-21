import random
import wave

from agent import ideas, scripts, video
from agent.voice import probe_duration


def _script(cfg):
    idea = ideas._local_ideas("fitness", 1, random.Random(11), set())[0]
    return idea, scripts._local_script(cfg, idea)


def test_render_silent_video(cfg, tmp_path):
    idea, s = _script(cfg)
    out = video.render(cfg, idea, s, None, tmp_path / "video.mp4")
    assert out.exists()
    assert out.stat().st_size > 20_000


def test_render_with_audio_tracks_voice_length(cfg, tmp_path):
    idea, s = _script(cfg)
    wav = tmp_path / "narration.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(22050)
        w.writeframes(b"".join(
            (8000 if (i % 200) < 100 else 0).to_bytes(2, "little", signed=True)
            for i in range(22050 * 6)
        ))
    out = video.render(cfg, idea, s, wav, tmp_path / "video.mp4")
    assert out.exists()
    assert probe_duration(out) > 4.0


def test_slugify():
    assert video.slugify("Hello, World! This is a test") == "hello-world-this-is-a-test"
    assert video.slugify("!!!") == "post"
