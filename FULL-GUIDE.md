# THE FULL GUIDE — everything, in easy words 📘

This is **everything** you need to know, from zero. No experience needed.
Every step says: **what to do → what you'll see → what it means.**

If a sentence has a word you don't know, the guide explains it right there.

---

## Table of contents

1. [What this is](#1-what-this-is)
2. [What you need before starting](#2-what-you-need-before-starting)
3. [Install Python](#3-install-python)
4. [Get the vishnu folder](#4-get-the-vishnu-folder)
5. [Install the agent (one time)](#5-install-the-agent-one-time)
6. [Setup: your name, topic, rules](#6-setup-your-name-topic-rules)
7. [Make your first video](#7-make-your-first-video)
8. [Every command explained](#8-every-command-explained)
9. [Connect your accounts (YouTube, X, TikTok, Facebook, Instagram)](#9-connect-your-accounts)
10. [Make videos better: AI writing + voice (optional)](#10-make-videos-better)
11. [Make it yours: your own topics, backgrounds, style](#11-make-it-yours)
12. [Post automatically every day](#12-post-automatically-every-day)
13. [Your daily routine](#13-your-daily-routine)
14. [Troubleshooting: every common problem + fix](#14-troubleshooting)
15. [Map of your files](#15-map-of-your-files)
16. [Safety: what stays private, what to watch out for](#16-safety)

---

## 1. What this is

It's a **program (an "agent") that makes social media videos for you by itself.**

When you run it, it does 4 things in a row:

```
 1. IDEA      →  "5 small habits that quietly fix bad posture"
 2. SCRIPT    →  hook + 4 tips + "follow for more"
 3. VIDEO     →  25-second vertical video (TikTok/Shorts/Reels style)
 4. PUBLISH   →  posts it to the accounts you connected
```

Key facts:

- **It never repeats an idea.** It remembers everything it made.
- **It's free to start.** No card, no paid accounts.
- **Your accounts stay yours.** It uses a "key" you create (called a
  *token* — explained in Part 9). Nothing is shared anywhere.
- **You are the boss.** You choose topic, accounts, and schedule.

**What is an "agent"?** Just a fancy word for "a program that does a whole
job by itself, step by step, without you clicking through a website."

---

## 2. What you need before starting

| Thing | Why |
|---|---|
| A computer (Windows, Mac, or Linux) | runs the program |
| Internet | to install packages and post |
| Python (free) | the language the program is written in |
| About 15 minutes | total setup time |

That's it. No paid software. No special hardware.

**Useful words you'll meet (mini-dictionary):**

- **Terminal** — a small black/white window where you type commands
  (instructions). Nothing else runs from it.
- **Command** — one line you type into the terminal, then press Enter.
- **Folder (directory)** — where files live, like a drawer.
- **File** — one piece of data (the program, a video, your settings).
- **API** — the "door" a company (YouTube, X…) opens so approved programs
  can do things for you, like posting a video.
- **Token** — a long code that says "this program is allowed to post as me."
  You create it on the company's website. It's like a password.
  ⚠️ Never send tokens to anyone.

---

## 3. Install Python

**Python** is free software that runs our program. Install it once.

### Windows
1. Go to **https://www.python.org/downloads/** and click the big yellow
   **Download Python** button.
2. Run the file you downloaded.
3. ⚠️⚠️ **At the bottom of the first window, tick the box
   "Add python.exe to PATH"** — this is the box people miss most often.
   (If you miss it: uninstall, reinstall, tick the box.)
4. Click **Install Now**, wait, click Close.

### Mac
1. Download from **https://www.python.org/downloads/**
2. Open the file → click through the installer screens (agree, install).
3. *(Optional shortcut: on newer Macs, typing `python3` in the terminal may
   already work — test it first.)*

### Linux (Ubuntu etc.)
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip
```

### ✅ Check it worked
Open a terminal (how? → Part 4), type:
```bash
python --version
```
If it prints something like `Python 3.11.2` → you're good. 🎉
(If Windows says "not recognized" → you missed the PATH box. Reinstall.)

---

## 4. Get the vishnu folder

The program lives in a **folder called `vishnu`**. Two ways to get it:

### Option A — use this workspace (easiest, zero setup)
If you're reading this while chatting with me on Arena: **it's already
installed and running here.** You can skip Parts 3–5 and just ask me:
*"make today's video"*. You can also run commands yourself in the terminal
provided in this workspace.

### Option B — on your own computer
You need a free tool called **Git** to copy the folder from the internet:

1. Install Git: **https://git-scm.com/downloads** (Windows: just click Next
   through the installer. Mac: `brew install git` or it installs itself on
   first use. Linux: `sudo apt install git`.)
2. Open a terminal **anywhere** (e.g. Documents folder) and type:
   ```bash
   git clone -b arena/01a0c2aa-vishnu https://github.com/dakufitness81-alt/vishnu.git
   ```
   What this does: copies the vishnu folder (with my branch that has all the
   new agent code) to your computer.
3. You now have a `vishnu` folder. **Open a terminal INSIDE it:**
   - **Windows:** open the folder in File Explorer → click the address bar →
     type `cmd` → Enter. (The window's title will say "…\vishnu".)
   - **Mac:** right-click the folder → **New Terminal from Folder**.

✅ *You know you're in the right place when you type `ls` (Mac/Linux) or
`dir` (Windows) and see `config.yaml`, `agent`, `assets`, `tests`… in the
list.*

> **Important rule for the whole guide:** every command below must be typed
> from INSIDE the vishnu folder. If in doubt, open a new terminal inside the
> folder and try again.

---

## 5. Install the agent (one time)

"Install the agent" = give it the extra free packages it needs (one is a
mini video-maker). It takes 1–2 minutes.

- **Mac / Linux:**
  ```bash
  bash setup.sh
  ```
- **Windows:**
  ```bat
  setup.bat
  ```

**What it does:** creates a private mini-Python called `.venv` (so it never
breaks other things on your computer) and downloads the packages listed in
`requirements.txt`.

**What you'll see:** lines like `Collecting requests… Installing collected
packages…` and finally:

```
✅ Done! Next steps: ...
```

✅ That `✅ Done!` means everything installed. If it errors, jump to
Part 14 (troubleshooting) — usually it's the Python PATH box from Part 3.

> If `bash`/Git etc. feel scary: in this Arena workspace you can also just
> ask me to "install it" and I'll run it for you.

---

## 6. Setup: your name, topic, rules

Two small files control everything: **`config.yaml`** (the rules) and
**.env** (your secret codes). Let's set both.

### 6a. The rules — `config.yaml`
Open `config.yaml` with any text editor:
- Windows: right-click → Open with → **Notepad**
- Mac: right-click → Open with → **TextEdit** (or any editor)

Here's the file, with **every line explained**:

```yaml
agent:
  niche: fitness        # THE TOPIC of the ideas. Pick ONE:
                        #   fitness, tech, finance, cooking, travel, general
                        #   (you can invent your own — see Part 11)
  handle: "@yourhandle" #  ← WRITE YOUR REAL HANDLE HERE, e.g. @dakufitness81
                        #   It's shown on every video.
  platforms: [local]    # WHERE to post. "local" = don't post anywhere,
                        #   just save the video (perfect for testing).
                        #   Later change to e.g. [youtube] or [youtube, x]
  ideas_per_run: 3      # how many idea candidates it brainstorms per run
                        #   (it picks the best fresh one; you can leave as-is)

video:
  width: 1080           # video size — leave 1080×1920 (vertical).
  height: 1920          #   9:16 vertical is what Shorts/Reels/TikTok want.
  fps: 30               # smoothness — leave as-is
  crf: 20               # quality vs file size — leave as-is
  beats: 4              # number of tip-slides in the middle (3–6 works)
  min_slide_seconds: 2.2  # don't make any slide shorter than this
  max_slide_seconds: 6.0  # …or longer than this
  cta: "Follow for one tip like this every day."
                        #   "Call to action" — the closing line. Make it yours!
  hashtags: ["#fitness", "#dailytips"]
                        #   hashtags shown on the CTA slide + in captions.
                        #   Change to YOUR hashtags.

voice:
  provider: auto        # "auto" = use AI voice if you add a key (Part 10),
                        #   otherwise silent video (captions do the talking).
  openai_model: tts-1   #   leave as-is
  openai_voice: alloy   #   the voice, if you use AI (options in Part 10)

llm:
  provider: auto        # "auto" = use AI writing if you add a key,
                        #   otherwise the built-in free idea engine.
  model: gpt-4o-mini    #   leave as-is

output:
  dir: output           # where finished videos are saved. Leave as-is.
```

**Do these three changes now:**
1. `handle:` → your real handle
2. `hashtags:` → your hashtags
3. `cta:` → something you'd actually say

Save the file. (Don't change the other lines for now.)

### 6b. Your secret codes — `.env`
The `.env` file is where tokens (Part 2 dictionary) go. Make it:

- Mac/Linux: `./.venv/bin/python -m agent init`
- Windows: `.venv\Scripts\python -m agent init`

It creates `.env` from a template. **You can leave it 100% empty and everything
still works** (no AI, no real posting). You only fill in lines when you
connect an account (Part 9).

> ⚠️ The `.env` file is **secret**. It's automatically excluded from the
> project (git-ignored). Never share it, never upload it anywhere.

---

## 7. Make your first video 🎬

Ready? Type (inside the vishnu folder):

- Mac/Linux:
  ```bash
  ./.venv/bin/python -m agent run
  ```
- Windows:
  ```bat
  .venv\Scripts\python -m agent run
  ```

> Short version everyone uses after this: on Mac/Linux the prefix is
> `./.venv/bin/python -m agent` and on Windows it's `.venv\Scripts\python -m agent`.
> In the rest of this guide I'll write just `agent run`, `agent ideas`…
> **you** add the prefix. 🙂

**What you'll see (and what each line means):**

```
==== Post 1/1 ============================================
  [idea]    I fixed my posture in 30 days  (format: story)
              ↑ it picked a fresh idea (never used before)
  [script]  4 beats via offline engine
              ↑ it wrote 4 tip-lines ("beats")
  [video]   rendering (silent + captions)...
              ↑ making the video — take 15–60 seconds
  [publish] local ...
              ↑ where it's going: "local" = saved, not posted
            OK  Saved to .../output/published/20260921-...
              ↑ ✅ success. It tells you exactly where.

====================================================
  Done.
  - I fixed my posture in 30 days
    video:   .../output/posts/20260921-.../video.mp4
    local       [ok] Saved to ...
```

✅ **Now watch your first video!**
- **Windows:** File Explorer → `vishnu` → `output` → `posts` → the newest
  folder → double-click `video.mp4`.
- **Mac:** Finder → vishnu → output → posts → newest folder → double-click.

That video — idea, script, design, music-free render — **was made by the
agent, by itself, in one command.** 🎉

**Where do finished videos go?**
- `output/posts/<date>-<name>/video.mp4` — the working copy
- `output/published/<date>-<name>/` — the "published" package: video +
  `caption.txt` (ready to paste anywhere) + `metadata.json`

**The idea repeats?** It shouldn't. If it does, delete the file `state.json`
in the vishnu folder and run again.

---

## 8. Every command explained

*(Always run from inside the vishnu folder. Add your prefix — see Part 7.)*

### `agent run` — make + post one video
The main command. Brainstorm → script → video → publish to the platforms in
`config.yaml` → remember it.

Useful extras:
```
agent run --idea "best breakfasts for gym people"
        ↑ use YOUR idea instead of generating one
agent run --count 2
        ↑ make 2 videos right now (different ideas)
agent run --platforms youtube,x
        ↑ post to these today, whatever config says
agent run --dry-run
        ↑ make the video but NEVER post (safest mode)
```

### `agent ideas` — just see ideas, make nothing
```
agent ideas            → 5 fresh ideas (title + hook + hashtags)
agent ideas --count 10 → 10 of them
```
Great for picking a good one: then copy it into `agent run --idea "..."`.

### `agent video` — just make a video, don't post
```
agent video --idea "my own idea"
```
Saves to `output/posts/...` for you to grab by hand.

### `agent publish` — post an old video now
You already have a bundle folder (one of those in `output/published/`)?
```
agent publish output/published/20260921-064254-i-fixed-my-posture-in-30-day --platforms youtube
```
On Mac/Linux the easier way is to drag the folder into the terminal:
`agent publish ` then drag the folder from Finder, then ` --platforms youtube`.

### `agent loop` — the never-stop mode
```
agent loop --interval 86400
        ↑ post 1 video every 86400 seconds (= every 24 h). Runs forever.
agent loop --interval 3600 --count 6
        ↑ 6 posts, one every hour, then stops.
```
Stop it: press **Ctrl+C** in its terminal (or see Part 12 for background
version).

### `agent status` — what has it made?
```
agent status
```
Shows the last 20 posts: date, which platforms succeeded, title.

### `agent auth x` / `agent auth youtube` — one-time account connection
Interactive: prints a link, you approve in the browser, paste a code back.
(Only needed once per account — details in Part 9.)

### `agent init` — create the .env file
Run once. You already did it in Part 6.

---

## 9. Connect your accounts

This is the part that lets it **post for you**. You connect **one account at
a time** — start with the one you care about most. YouTube is the best first
choice (unlimited free posting).

**How it works (10-second version):** each company has an "app system." You
create a tiny app there, it gives your program a **token** (a password-like
code that says "this program may post as me"), you put that token in `.env`,
and the agent uses it. The token is stored ONLY on your computer
(`.env` and `secrets/` folder — both are hidden from the project).

### 9a. 📺 YouTube (recommended first) — ~15 minutes

1. Go to **https://console.cloud.google.com** and sign in with the Google
   account that owns your channel.
2. Top-left: **New Project** → name it anything ("MyVideos") → **Create**.
3. In the search bar at top: type **YouTube Data API v3** → open it →
   **Enable**. (This turns on the "door" — free.)
4. Left menu → **APIs & Services → OAuth consent screen**:
   - User type: **External** → Create
   - Fill: App name "MyVideos", your email → Save
   - Next screen, section **Test users** → Add your email → Save.
   *(Test users = accounts allowed to use this while it's in "testing".
   You are the only test user you need.)*
5. Left menu → **APIs & Services → Credentials** → top button
   **+ Create Credentials → OAuth client ID**:
   - Application type: **Desktop app** → **Create**
6. A little **JSON file downloads** (e.g. `client_secret_123....json`).
   This file contains your app's secret. **Rename it to `client_secret.json`**
   and put it in the folder **`vishnu/secrets/`** (create the `secrets`
   folder if it doesn't exist).
   → Your structure: `vishnu/secrets/client_secret.json`
7. Open `.env` and write (your real path — drag the folder into a text
   editor or type carefully):
   ```
   YOUTUBE_CLIENT_SECRET_JSON=/your/path/vishnu/secrets/client_secret.json
   ```
   Windows example: `C:\Users\you\vishnu\secrets\client_secret.json`
   Optional: `YOUTUBE_PRIVACY=unlisted` while you check the first few videos
   (remove that line when you're happy → posts go public).
8. Install the YouTube helper (one time, in the vishnu folder):
   ```
   ./.venv/bin/pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
   (Windows: `.venv\Scripts\pip install ...` same packages)
9. **Connect your account** (one time):
   ```
   agent auth youtube
   ```
   What happens: it prints a link → you open it → Google asks
   *"MyVideos wants to upload videos"* → **Continue → Choose account →
   Allow** → Google shows a **code** on a page → copy that code → paste it
   into the terminal → Enter.
   You'll see: `YouTube token saved to secrets/youtube_token.json` ✅
10. In `config.yaml`: `platforms: [youtube]`
11. **THE MOMENT OF TRUTH:**
    ```
    agent run
    ```
    Wait 30–60 s, then open your YouTube Studio → your video is there.
    Vertical videos under 60 s automatically appear as a **Short**.

### 9b. 🐦 X (Twitter) — ~10 minutes

1. Go to **https://developer.x.com**, sign in, click **Projects and Apps**
   → **Create Project & App** (name: anything).
2. Open your app → **Settings** tab → **Redirect URIs** → add:
   `http://localhost:8080/callback` → Save.
3. **Keys and tokens** tab → copy **Client ID** and **Client Secret**.
4. In `.env`:
   ```
   X_CLIENT_ID=your-client-id-here
   X_CLIENT_SECRET=your-client-secret-here
   ```
5. Connect (one time): `agent auth x`
   → it prints a link → open → approve → the redirect page shows
   **?code=abc123…** → copy that code (the part after `code=`) → paste in
   terminal → Enter → `X token saved` ✅
6. `config.yaml`: `platforms: [x]` → `agent run` → your tweet is posted
   (video + caption, auto-trimmed to X's 280 characters).

   ⚠️ **Know the limit:** X's **free** plan allows only a small number of
   posts per month. For daily X posting you'd need X's paid API tier —
   so a common setup is `[youtube, x]` where YouTube is your daily platform.

### 9c. 🎵 TikTok — needs an approved developer app (~30 min + review)

1. Go to **https://developers.tiktok.com**, sign in, **Create App**.
2. In the app: **Request API Access** → **Content Posting** → apply for the
   **Content Posting API**. TikTok reviews apps (can take a few days; new
   apps often start with posts going to a private review queue).
3. Once approved: copy **Client Key** and **Client Secret** from the app
   page into `.env`:
   ```
   TIKTOK_CLIENT_KEY=...
   TIKTOK_CLIENT_SECRET=...
   ```
4. `config.yaml`: `platforms: [tiktok]` → `agent run`.
   No `auth` command needed — the agent exchanges the key/secret for a
   token automatically each time.

### 9d. 📘 Facebook (your Page) — ~20 minutes

1. Go to **https://developers.facebook.com**, **Create App** → type:
   *Business* (or *Developer* if that's the only option; pick a name).
2. In the app dashboard, add the product **"Facebook Login for Business"**
   (or Instagram Graph API — both come from the same app).
3. You need a **Facebook Page** that's linked to your personal profile
   (facebook.com → Pages → create/join one).
4. Generate a **Page Access Token**: app dashboard → **Graph API Explorer**
   → pick your Page → permissions `pages_manage_posts`,
   `pages_read_engagement`, `pages_show_list` → **Generate Token**.
   Copy the token (long string).
5. In `.env`:
   ```
   FACEBOOK_PAGE_ID=your-page-id        (from your Page's URL or the app dashboard)
   FACEBOOK_PAGE_TOKEN=the-long-token
   ```
6. `config.yaml`: `platforms: [facebook]` → `agent run`.

### 9e. 📸 Instagram (Reels) — needs a business account

1. Your Instagram must be a **Professional (business) account**, linked to
   a **Facebook Page** (Instagram → Settings → Account type and tools →
   Switch to professional → link Page).
2. Use the same Meta app as Part 9d. In **Graph API Explorer**, generate a
   token with **instagram_content_publish** (+ instagram_basic).
3. Get your **Instagram business account ID**: app dashboard → *Instagram*
   → *Get Instagram Business Account ID* (or the token introspection API).
4. In `.env`:
   ```
   INSTAGRAM_BUSINESS_ACCOUNT_ID=...
   INSTAGRAM_ACCESS_TOKEN=...
   ```
5. `config.yaml`: `platforms: [instagram]` → `agent run` → posts as a **Reel**.

### 9f. Post to several at once
Just list them: `platforms: [youtube, facebook, x]` — the agent posts the
same video to all, and handles each platform's caption limit automatically.
One failure doesn't stop the others — `status` shows which succeeded.

---

## 10. Make videos better (optional, ~1 cent/video)

Everything works without this. Adding an OpenAI key upgrades two things:

1. **AI-written ideas & scripts** (more creative, fully custom to your brand)
2. **A spoken voiceover** on every video (5 different voices)

### Steps (5 minutes)
1. Go to **https://platform.openai.com** → sign in → **Billing → add credit**
   ($5 ≈ a few hundred videos with voice).
2. **API keys** (left menu) → **Create new secret key** → copy it (`sk-...`).
3. In `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
4. That's it. Run `agent run` — the output now says
   `4 beats via LLM` and the video has a voice.

**Change the voice** (in `.env`):
```
TTS_VOICE=nova      # female, bright
TTS_VOICE=fable     # female, warm
TTS_VOICE=onyx      # male, deep
TTS_VOICE=alloy     # neutral (default)
```

Prefer a free alternative? Any **OpenRouter** key works too:
`OPENROUTER_API_KEY=...` (and set `llm.model` in config.yaml to a model of
your choice).

---

## 11. Make it yours

### 11a. Your own topic (niche)
Open `agent/ideas.py` and look for `NICHES = {`. You'll see blocks like
`"fitness": {...}` with lists: `problems`, `goals`, `habits`, `tips`,
`story_verbs`, `debates`, `hashtags`, `label`.

**Copy one block, rename it, and rewrite the lists with YOUR words.**
Example — copy the whole `fitness` block, change its name to `"bodybuilding"`
and swap in your own tips/problems/goals. Then in `config.yaml`:
`niche: bodybuilding`. Done — the agent now makes bodybuilding content.

### 11b. Your own background art
The agent looks for files in the `assets/` folder that start with **`bg`**:
`bg1.jpg`, `bg2.jpg`, `bg3.jpg` … (any size, it crops them to vertical).
Replace those three files with **your** images — a gym wall, your logo
background, a photo you own — and every video uses them automatically.
(If the folder is empty, it falls back to clean gradients.)

### 11c. Your style
- Video length: more/fewer `beats` in config.yaml
- Closing line: `cta:`
- Look: colors are in `agent/video.py` (`PALETTES`, `ACCENTS`) — pick hex
  colors that match your brand
- Captions in `output/published/*/caption.txt` are ready to paste into any
  other platform you post manually

---

## 12. Post automatically every day

"Automatic" just means: **the computer runs `agent run` on a schedule, by
itself, every day.** Three ways, pick ONE:

### Option A — Windows Task Scheduler (recommended on Windows)
1. Press the Windows key, type **Task Scheduler**, open it.
2. Right side: **Create Basic Task…**
3. Name: `Vishnu AutoPilot` → Next
4. Trigger: **Daily** → pick the time (e.g. 07:30) → Next
5. Action: **Start a program**
   - *Program/script:* your full path to python, i.e.
     `C:\Users\you\vishnu\.venv\Scripts\python.exe`
   - *Add arguments:* `-m agent run`
   - *Start in:* `C:\Users\you\vishnu`
   → Next → Finish
✅ Done. Every day at 07:30 it makes and posts a new video — even if the
terminal isn't open. (The computer must be **on** at that time.)

### Option B — cron (recommended on Mac/Linux)
1. In a terminal: `crontab -e` (if it asks for an editor, pick `nano`)
2. Add this ONE line (fix the path to your real vishnu folder):
   ```
   30 7 * * * cd /home/you/vishnu && ./.venv/bin/python -m agent run >> autopilot.log 2>&1
   ```
   Reading it: `30 7` = 7:30 · `* * *` = every day · `cd …` = go to the
   folder · `>> autopilot.log` = write what happened into a log file.
3. Save (in nano: Ctrl+O, Enter, Ctrl+X) and exit the terminal.
✅ Done — this survives restarts too.

### Option C — the built-in daemon (simple to understand)
```
agent loop --interval 86400
```
It keeps running in that terminal and posts once per day (with a little
random delay so it doesn't look robotic). To run it in the background
(Mac/Linux):
```bash
nohup ./.venv/bin/python -m agent loop --interval 86400 >> autopilot.log 2>&1 &
```
Stop it: `pkill -f "agent loop"`. (Windows: keep it in a terminal and close
with Ctrl+C, or use Option A/B instead — cleaner.)

### What happens on a bad day?
- A platform is down or a token expires → that post is marked failed,
  **NOT recorded** → the next day's run automatically tries a new post.
- The computer was off at 07:30 → nothing posts that day (Task Scheduler
  can be set to "run as soon as possible after a missed start" if you want).
- You can always check: `agent status` and the `autopilot.log` file.

---

## 13. Your daily routine (2 minutes a day)

1. **(Morning)** Open YouTube/TikTok — your new video is there. 👀
2. **`agent status`** — one line per post, tells you where it landed.
3. Video bad? Ideas: change `niche`/`handle`/`cta` in config.yaml, or feed it
   your own idea: `agent run --idea "..."`.
4. **Weekly:** scroll your posts, note which ideas got views, and add more
   of those words to your niche banks (Part 11a). The more your words, the
   more *you* the content becomes.

---

## 14. Troubleshooting

**Each entry: what you see → what it means → the fix.**

1. **`python` is not recognized / `python: command not found`**
   → Python isn't installed (or on Windows you missed the PATH box).
   → Fix: reinstall from python.org, tick **Add python.exe to PATH**,
   restart the terminal, test with `python --version`.

2. **`No module named agent`**
   → Your terminal isn't inside the vishnu folder.
   → Fix: open a new terminal INSIDE the folder (Part 4) and retry.

3. **`bash: ./.venv/bin/python: No such file or directory`**
   → You haven't run the setup yet (or you're on Windows).
   → Fix: run `bash setup.sh` (Mac/Linux) or `setup.bat` (Windows) once.

4. **Setup fails with "externally-managed-environment"**
   → Your system Python is protected. The setup scripts use `.venv`, so just
   make sure you ran `setup.sh`/`setup.bat` from inside the vishnu folder.

5. **A platform prints `[--] … No token` or `Set X_… in .env`**
   → You're trying to post somewhere not connected yet.
   → Fix: follow that platform's steps in Part 9, or change `platforms:`
   back to `[local]` to just make videos.

6. **YouTube: `Missing SDK — run: pip install …`**
   → Step 8 of Part 9a wasn't done. Run that pip install line.

7. **YouTube: `No credentials. Set YOUTUBE_CLIENT_SECRET_JSON`**
   → Step 7 of Part 9a: the line in `.env` is missing or the path is wrong.
   Check the path character-by-character (Windows paths use `\`).

8. **YouTube post never appears**
   → You set `YOUTUBE_PRIVACY=unlisted` — delete that line from `.env`.
   → Or the video is still processing (YouTube takes a few minutes).

9. **X says `error 401` or token problems**
   → The token is stale/typoed. Delete `secrets/x_tokens.json` and re-run
   `agent auth x`.

10. **TikTok: `init failed`**
    → Your app doesn't have Content Posting access yet (Part 9c review).

11. **Video looks ugly / text cut off**
    → You edited something in config.yaml (size?) — keep 1080×1920.
    → Or you replaced background images with very bright ones — the text
    sits on a dark overlay anyway; try different `assets/bg*.jpg` images.

12. **Same idea keeps appearing**
    → Delete `state.json` from the vishnu folder and run again.

13. **`state.json` or `.env` missing / accidentally deleted**
    → `.env`: run `agent init` and re-paste your tokens (Part 9 steps 3–7
    are all still valid — you only re-type what you had).
    → `state.json`: it recreates itself; worst case, an idea repeats once.

14. **The video has no sound**
    → Expected! By default videos are silent + captions (that's how most
    Shorts are made). Add a voice: Part 10.

15. **Nothing posts on a scheduled day**
    → Was the computer on at that time? Check `autopilot.log` (or the Task
    Scheduler "last run result") — it records exactly what happened.

16. **Anything else** → the agent prints the reason in plain English in the
    line after `[--]`. Copy that line and send it to me — I'll fix it.

---

## 15. Map of your files

```
vishnu/
├── config.yaml      ← YOUR SETTINGS (niche, handle, platforms, style)
├── .env             ← YOUR SECRET TOKENS (never share!) — created by agent init
├── requirements.txt ← the free packages (you don't touch)
├── setup.sh / setup.bat ← one-time installers (you don't touch after step 5)
├── README.md        ← technical manual (for curious humans)
├── START-HERE.md    ← the short guide
├── FULL-GUIDE.md    ← you are here
├── agent/           ← the brain (code — don't edit unless you want to)
│   └── publishers/  ← one file per social platform
├── assets/          ← YOUR background images (bg1.jpg, bg2.jpg, bg3.jpg)
├── tests/           ← the quality checks (14 of them — all passing)
├── secrets/         ← OAuth tokens (auto-created, never shared)
├── output/          ← EVERYTHING IT MAKES
│   ├── posts/       ← working videos
│   └── published/   ← finished packages (video + caption + metadata)
├── state.json       ← its memory of posted ideas (auto-created)
├── .venv/           ← its private Python (never touch, never delete)
└── autopilot.log    ← daily automation diary (if you use Part 12)
```

**You'll edit:** `config.yaml`, `.env`, `assets/` (images).
**You'll read:** `output/`, `autopilot.log`.
**You won't touch:** the rest.

---

## 16. Safety

**What stays 100% on your computer:**
- Your tokens (`.env`, `secrets/`) — hidden from the project, never uploaded
- Your videos (`output/`)
- Your history (`state.json`)

**What talks to the internet, and why:**
- When you connect an account → it posts **only to your own account**, with
  **only your own content**, using the token you created. You can revoke any
  token at any time on the company's website (and the agent stops working
  there immediately — that's your emergency brake).
- If you add an OpenAI key → your idea text goes to OpenAI to be written
  (that's how the upgrade works). Without the key, no such calls happen.

**Sensible habits:**
- Start with `YOUTUBE_PRIVACY=unlisted` for the first week; when the videos
  look right, make them public.
- Respect platform rules: no fake claims in ideas, and keep posting rates
  within each platform's limits (the agent already stays within sane limits:
  1 video/run by default).
- The emergency brakes:
  - Stop one platform → remove it from `platforms:`
  - Stop everything → `platforms: [local]`
  - Stop a token → revoke it on the company's site
  - Stop the whole schedule → delete the cron line / Task Scheduler task

---

## 🏁 That's everything.

Your first two commands, again, so you can start today:

```bash
agent run          # make + post today's video
agent status       # see what it did
```

(Add your prefix: `./.venv/bin/python -m agent` on Mac/Linux,
`.venv\Scripts\python -m agent` on Windows — or just ask me and I'll run it.)
