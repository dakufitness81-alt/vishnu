import pytest

from agent.config import Config


@pytest.fixture
def root(tmp_path):
    (tmp_path / "config.yaml").write_text(
        """
agent:
  niche: fitness
  handle: "@testbot"
  platforms: [local]
video:
  width: 480
  height: 854
  fps: 24
  crf: 23
  beats: 3
""",
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture
def cfg(root):
    return Config.load(root / "config.yaml")
