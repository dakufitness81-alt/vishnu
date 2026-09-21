from agent import pipeline
from agent.state import State


def test_full_run_local_publisher(cfg, root):
    bundles = pipeline.run(cfg, count=1)
    b = bundles[0]
    assert b.video_path.exists() and b.video_path.stat().st_size > 10_000
    pub = root / "output" / "published" / b.post_id
    assert (pub / "video.mp4").exists()
    assert (pub / "caption.txt").exists()
    assert (pub / "metadata.json").exists()
    st = State(root / "state.json")
    assert len(st.posts) == 1
    assert st.posts[0]["idea_title"] == b.title


def test_dedup_across_runs(cfg, root):
    pipeline.run(cfg, count=1)
    pipeline.run(cfg, count=1)
    st = State(root / "state.json")
    titles = [p["idea_title"] for p in st.posts]
    assert len(titles) == 2
    assert len(set(titles)) == 2, "two runs should pick two different ideas"


def test_publish_republish_same_bundle_dir(cfg, root):
    """Re-publishing a bundle that already lives in output/published/ must not
    fail with 'same file' copy errors."""
    bundles = pipeline.run(cfg, count=1)
    b = bundles[0]
    pub = root / "output" / "published" / b.post_id
    b2 = pipeline.PostBundle(
        post_id=b.post_id,
        title=b.title,
        idea=b.idea,
        script=b.script,
        video_path=pub / "video.mp4",  # already inside the publish dir
        caption=b.caption,
    )
    from agent.publishers import get_publisher

    res = get_publisher("local").publish(cfg, b2)
    assert res.ok, res.message


def test_user_idea_is_used(cfg, root):
    bundles = pipeline.run(cfg, idea="My own brilliant idea about deep squats", count=1)
    assert bundles[0].title == "My own brilliant idea about deep squats"
    st = State(root / "state.json")
    assert st.posts[0]["idea_title"] == "My own brilliant idea about deep squats"
