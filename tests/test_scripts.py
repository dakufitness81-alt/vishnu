import random

from agent import ideas as I
from agent import scripts as S


def _idea():
    return I._local_ideas("fitness", 1, random.Random(3), set())[0]


def test_local_script_shape(cfg):
    s = S._local_script(cfg, _idea())
    assert s.title and s.hook
    assert 1 <= len(s.beats) <= 6
    assert len(set(s.beats)) == len(s.beats), "beats must be unique"
    assert s.cta
    assert s.hashtags


def test_script_stable_for_same_idea(cfg):
    idea = _idea()
    a = S._local_script(cfg, idea)
    b = S._local_script(cfg, idea)
    assert a.beats == b.beats


def test_generate_script_without_key_uses_offline(cfg, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    s = S.generate_script(cfg, _idea())
    assert s.beats
