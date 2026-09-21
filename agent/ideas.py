"""Idea generation.

Two engines:
  * LLM engine  — used automatically when an API key is available (OpenAI / OpenRouter)
  * Offline engine — template-based, free, works with no network at all

Both return the same :class:`Idea` shape.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import random
from dataclasses import dataclass, field

from . import llm

DEFAULT_NICHE = "general"

NICHES: dict[str, dict] = {
    "fitness": {
        "label": "FITNESS",
        "problems": [
            "bad posture", "strength plateaus", "low energy", "gym anxiety",
            "poor sleep", "belly fat", "knee pain", "inconsistent training",
        ],
        "goals": [
            "build real strength", "lose fat", "train pain-free",
            "look 10% stronger", "build a habit that sticks",
        ],
        "habits": [
            "skipping rest days", "crunching for an hour", "training 7 days straight",
            "dieting without tracking", "chasing PRs every session",
        ],
        "tips": [
            "add one rep per week instead of one more weight",
            "eat 25-35g of protein after training",
            "walk 7,000 steps on rest days",
            "sleep 8 hours — it beats most supplements",
            "use a 3-1-1 tempo on your main lifts",
            "deload every 5th week to break plateaus",
            "track every session in a simple logbook",
            "do 10 minutes of mobility before lifting",
        ],
        "story_verbs": [
            "got visibly stronger", "lost 4 kg", "fixed my posture",
            "built a gym habit", "slept through the night",
        ],
        "debates": [
            "cardio vs lifting", "fasting vs regular meals",
            "gym vs home workouts", "protein shakes vs whole food",
        ],
                "wishes": ["built real strength", "lost fat", "trained pain-free", "got 10% stronger", "made the habit stick"],
"hashtags": ["#fitness", "#gymtok", "#dailytips", "#strengthtraining"],
    },
    "tech": {
        "label": "TECH",
        "problems": [
            "tech debt", "burnout", "slow code reviews", "scope creep",
            "imposter syndrome", "meeting overload", "flaky CI", "dead-end projects",
        ],
        "goals": [
            "ship faster", "learn in public", "automate my workflow",
            "get promoted", "build in public",
        ],
        "habits": [
            "context-switching all day", "writing docs nobody reads",
            "debugging without logs", "skipping code review",
        ],
        "tips": [
            "add a 30-second why comment before complex code",
            "profile before you optimize",
            "write the failing test first",
            "keep a decision log for every sprint",
            "turn every repeated task into a script",
            "block 2 hours of deep work daily",
            "review diffs smaller than 400 lines",
            "track flaky tests in one dashboard",
        ],
        "story_verbs": [
            "shipped my side project", "cut build times in half",
            "automated my whole deploy", "learned a new framework",
            "passed my system design interview",
        ],
        "debates": [
            "tabs vs spaces", "monolith vs microservices",
            "JIT vs AOT runtimes", "React vs vanilla JS",
        ],
                "wishes": ["shipped faster", "learned in public", "automated my workflow", "got promoted", "built in public"],
"hashtags": ["#tech", "#coding", "#devlife", "#aibuilding"],
    },
    "finance": {
        "label": "MONEY",
        "problems": [
            "cash flow gaps", "overspending", "tax surprises",
            "under-diversified portfolios", "fee creep", "no emergency fund",
            "subscription bloat",
        ],
        "goals": [
            "save your first 10k", "retire 10 years earlier", "grow passive income",
            "pay off debt faster", "invest without stress",
        ],
        "habits": [
            "checking your balance after a bad week", "paying for 40 subscriptions",
            "chasing last month's hot stock", "carrying a balance past the due date",
        ],
        "tips": [
            "pay yourself first — automate a transfer on payday",
            "use the 72-hour rule for any purchase over $100",
            "move 1% of your portfolio into index funds each quarter",
            "audit subscriptions once a month",
            "keep 3-6 months of expenses in a high-yield account",
            "round up every purchase and invest the change",
            "review your account fees once a year",
            "name every savings goal",
        ],
        "story_verbs": [
            "built a 6-month emergency fund", "paid off $8k of debt",
            "doubled my passive income", "cut my monthly costs by 30%",
            "automated my whole budget",
        ],
        "debates": [
            "index funds vs ETFs", "rent vs buy",
            "Roth vs traditional IRA", "pay debt vs invest",
        ],
                "wishes": ["saved my first 10k", "invested without stress", "paid off my debt", "grew my passive income"],
"hashtags": ["#finance", "#personalfinance", "#moneytips", "#investing"],
    },
    "cooking": {
        "label": "COOKING",
        "problems": [
            "takeout addiction", "meal-prep burnout", "food waste", "bland flavor",
            "no time to cook", "shaky knife skills", "overcrowded grocery lists",
        ],
        "goals": [
            "cook 5 dinners a week", "cut takeout costs in half",
            "meal prep in under an hour", "master one cuisine", "cook with what you have",
        ],
        "habits": [
            "shopping while hungry", "buying produce you'll never use",
            "seasoning at the end only", "washing herbs before storing",
        ],
        "tips": [
            "sear hot and fast — never crowd the pan",
            "finish every dish with acid: lemon, vinegar, or capers",
            "double your aromatics, halve your salt",
            "keep a pantry staples list under $30",
            "marinate proteins overnight in the fridge",
            "sharpen your knife once a month",
            "roast vegetables hot for caramelization",
            "start rice while something else simmers",
        ],
        "story_verbs": [
            "cut takeout in half", "mastered my weeknight routine",
            "wasted 50% less food", "learned 5 quick stir-fries",
            "built a pantry that does the work",
        ],
        "debates": [
            "one-pot vs multi-pot meals", "air fryer vs oven",
            "organic vs seasonal", "cast iron vs nonstick",
        ],
                "wishes": ["cooked 5 dinners a week", "cut my takeout costs in half", "meal prepped in an hour", "mastered one cuisine"],
"hashtags": ["#cooking", "#foodtok", "#mealprep", "#easyrecipes"],
    },
    "travel": {
        "label": "TRAVEL",
        "problems": [
            "jet lag", "overpacking", "tourist-trap menus", "booking stress",
            "missed connections", "hotel markups", "burnout mid-trip",
        ],
        "goals": [
            "travel on a budget", "visit 3 cities in a month",
            "travel solo confidently", "pack in one carry-on", "see more, spend less",
        ],
        "habits": [
            "booking flights at the last second", "carrying 3 pairs of the same thing",
            "only eating where the lines are", "ignoring the local transit app",
        ],
        "tips": [
            "book the return first, then hunt outbound fares",
            "carry one universal adapter and one power bank only",
            "eat where locals queue, not where tourists do",
            "pack one layer per activity, not per day",
            "keep a 12-item packing checklist",
            "sit aisle for extra legroom on long-hauls",
            "keep small local cash for day one",
            "add a 2-night buffer before connections",
        ],
        "story_verbs": [
            "hit 5 countries on one ticket", "packed for 14 days in a carry-on",
            "cut my trip costs by 40%", "traveled solo for the first time",
            "saw the city like a local",
        ],
        "debates": [
            "carry-on only vs checked bags", "hostel vs hotel",
            "guided tours vs free roaming", "peak vs off-season",
        ],
                "wishes": ["traveled on a budget", "packed in one carry-on", "traveled solo confidently", "saw more and spent less"],
"hashtags": ["#travel", "#wanderlust", "#traveltips", "#budgettravel"],
    },
    "general": {
        "label": "DAILY TIPS",
        "problems": [
            "procrastination", "decision fatigue", "phone addiction",
            "chronic tiredness", "messy workspace", "no clear goals",
            "bad mornings", "shiny-object syndrome",
        ],
        "goals": [
            "build a habit that sticks", "reclaim 1 hour a day", "learn a new skill",
            "feel calmer at work", "start something and finish it",
        ],
        "habits": [
            "checking your phone first thing", "saying yes to everything",
            "starting five things at once", "waiting for motivation to act",
        ],
        "tips": [
            "start with two minutes — just open the thing",
            "batch your decisions into one weekly planning slot",
            "put your phone in another room for the first hour",
            "write down the one thing that must happen today",
            "use a body double for hard tasks",
            "take a 10-minute walk before any big meeting",
            "keep a done list next to your to-do list",
            "schedule the finish line — deadlines create momentum",
        ],
        "story_verbs": [
            "built a morning routine that stuck", "reclaimed an hour a day",
            "finished a project I'd dropped", "broke my doomscrolling habit",
            "learned a new skill in 30 days",
        ],
        "debates": [
            "morning routine vs night routine", "analog journal vs app",
            "deep work vs multitasking", "habit stacking vs habit tracking",
        ],
                "wishes": ["built a habit that stuck", "reclaimed an hour a day", "learned a new skill", "finished what I started"],
"hashtags": ["#productivity", "#selfimprovement", "#dailytips", "#mindset"],
    },
}


@dataclass
class Idea:
    title: str
    hook: str
    topic: str
    format: str
    hashtags: list[str] = field(default_factory=list)

    def key(self) -> str:
        return hashlib.sha1(self.title.lower().strip().encode("utf-8")).hexdigest()[:16]


def _fmt_listicle(b: dict, r: random.Random):
    n = r.choice([3, 4, 5, 6, 7])
    title = f"{n} small habits that quietly fix {r.choice(b['problems'])}"
    hook = r.choice([
        "Most people get this wrong.",
        "Save this before you forget it.",
        "The shortcut nobody teaches you.",
    ])
    return title, hook


def _fmt_myth(b: dict, r: random.Random):
    title = f"The {r.choice(b['problems'])} myth you still believe"
    hook = r.choice([
        "Stop doing this right now.",
        "You've been lied to about this one.",
        "Everyone says it. Almost nobody does it right.",
    ])
    return title, hook


def _fmt_story(b: dict, r: random.Random):
    title = f"I {r.choice(b['story_verbs'])} in {r.choice([7, 14, 21, 30, 90])} days"
    hook = r.choice([
        "No crazy hacks. Just this routine.",
        "Here's the exact plan, step by step.",
        "You can do the same. It's simpler than you think.",
    ])
    return title, hook


def _fmt_mistake(b: dict, r: random.Random):
    title = f"Stop {r.choice(b['habits'])} — it's costing you"
    hook = r.choice([
        "This one habit is holding you back.",
        "Unpopular opinion, but it's true.",
        "If you're doing this, keep watching.",
    ])
    return title, hook


def _fmt_debate(b: dict, r: random.Random):
    title = f"{r.choice(b['debates'])} — which one actually works?"
    hook = r.choice([
        "Let's settle this argument once.",
        "3 points, then you decide.",
        "The answer surprises most people.",
    ])
    return title, hook


def _fmt_beginner(b: dict, r: random.Random):
    title = f"Beginner mistakes that cause {r.choice(b['problems'])}"
    hook = r.choice([
        "New to this? Watch before your next session.",
        "These 2-minute fixes save you months.",
        "Start here before you go any further.",
    ])
    return title, hook


def _fmt_wish(b: dict, r: random.Random):
    title = f"Things I wish I knew before I {r.choice(b['wishes'])}"
    hook = r.choice([
        "I lost months to these. Don't.",
        "Nobody tells you this part.",
        "Reading this now saves you a year.",
    ])
    return title, hook


FORMATS: list[tuple[str, callable]] = [
    ("listicle", _fmt_listicle),
    ("myth", _fmt_myth),
    ("story", _fmt_story),
    ("mistake", _fmt_mistake),
    ("debate", _fmt_debate),
    ("beginner", _fmt_beginner),
    ("wish", _fmt_wish),
]


def _local_ideas(niche_key: str, count: int, rng: random.Random, exclude: set[str]) -> list[Idea]:
    bank = NICHES.get(niche_key, NICHES[DEFAULT_NICHE])
    out: list[Idea] = []
    seen = set(exclude)
    tries = 0
    while len(out) < count and tries < 200:
        tries += 1
        name, fn = rng.choice(FORMATS)
        title, hook = fn(bank, rng)
        k = Idea(title, hook, name, name).key()
        if k in seen:
            continue
        seen.add(k)
        out.append(Idea(
            title=title,
            hook=hook,
            topic=name,
            format=name,
            hashtags=list(dict.fromkeys(list(bank["hashtags"])[:3] + [f"#{niche_key}"]))[:5],
        ))
    return out


def _llm_ideas(cfg, count: int) -> list[Idea]:
    niche = cfg.get("agent.niche", DEFAULT_NICHE)
    model = cfg.get("llm.model", "gpt-4o-mini")
    system = "You are a viral short-form video strategist. Reply with JSON only."
    user = (
        f"Generate {count} short-form video ideas (TikTok / YouTube Shorts / Reels) "
        f"for a {niche} creator. "
        'Return JSON: {"ideas":[{"title": "...", "hook": "...", "topic": "...", '
        '"format": "listicle|myth|story|mistake|debate|beginner", "hashtags": ["#a", "#b"]}]}. '
        "Titles under 60 chars, hooks under 45 chars. Punchy, specific, honest — no clickbait lies."
    )
    data = llm.parse_json(llm.chat(model, system, user))
    out = []
    for item in data.get("ideas", [])[:count]:
        idea = Idea(
            title=str(item.get("title", "")).strip(),
            hook=str(item.get("hook") or item.get("title") or "").strip(),
            topic=str(item.get("topic", "")).strip(),
            format=str(item.get("format", "tip")).strip(),
            hashtags=[str(h) for h in item.get("hashtags", [])][:5],
        )
        if idea.title and idea.hook:
            out.append(idea)
    return out


def generate_ideas(
    cfg,
    count: int = 3,
    exclude: set[str] | None = None,
    use_llm: bool | None = None,
) -> list[Idea]:
    """Generate *count* fresh ideas, skipping any whose key is in *exclude*."""
    exclude = set(exclude or ())
    provider = str(cfg.get("llm.provider", "auto")).lower()
    if use_llm is None:
        use_llm = provider in ("auto", "openai") and llm.available()
    if use_llm:
        try:
            fresh = [i for i in _llm_ideas(cfg, count) if i.key() not in exclude][:count]
            if fresh:
                return fresh
        except Exception as exc:  # noqa: BLE001 — fall back to the offline engine
            print(f"  ! LLM idea generation failed ({exc}); using offline engine.")
    seed = f"{dt.date.today().isoformat()}:{len(exclude)}"
    return _local_ideas(cfg.get("agent.niche", DEFAULT_NICHE), count, random.Random(seed), exclude)
