import random

from agent import ideas as M


def test_generates_unique_ideas():
    out = M._local_ideas("fitness", 6, random.Random(1), set())
    assert len(out) == 6
    keys = {i.key() for i in out}
    assert len(keys) == 6
    for i in out:
        assert i.title and i.hook and i.format and i.hashtags


def test_unknown_niche_falls_back_to_general():
    out = M._local_ideas("underwater_basketball", 3, random.Random(2), set())
    assert len(out) == 3
    for i in out:
        assert i.title


def test_excluded_keys_are_skipped():
    first = M._local_ideas("fitness", 5, random.Random(7), set())
    keys = {i.key() for i in first}
    second = M._local_ideas("fitness", 5, random.Random(7), keys)
    assert {i.key() for i in second}.isdisjoint(keys)
    assert len(second) == 5


def test_generate_ideas_uses_offline_engine_without_key(cfg, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    out = M.generate_ideas(cfg, count=4)
    assert len(out) == 4
    assert len({i.key() for i in out}) == 4
