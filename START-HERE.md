# START HERE — the no-experience-needed guide 🚀

This guide assumes you have **never** run code before. Follow the steps in
order. Every command you need to type is shown exactly — copy it, paste it,
press **Enter**.

> **You are reading this inside the Arena workspace?** Great news: everything
> is already installed here. Skip to **Step 2** (or just tell me in chat:
> *"make today's video"* and I'll run it for you).

---

## What is this thing?

A program that, every day (or whenever you run it):

1. Thinks of a video idea (e.g. *"5 small habits that quietly fix bad posture"*)
2. Writes the script
3. Makes a short vertical video (TikTok/Shorts/Reels style, ~25 seconds)
4. Publishes it to the accounts you connect

Everything runs on your own machine. **It is free to start — no account, no
card, no API key needed** for the first videos.

---

## Step 0 — What you need (one-time, only on your own computer)

- A computer (Windows / Mac / Linux)
- **Python 3** installed:
  1. Go to https://www.python.org/downloads/
  2. Download and run the installer
  3. ⚠️ On Windows, **tick the box "Add python.exe to PATH"** at the bottom
     of the first installer screen (it's easy to miss!)
  4. Click "Install Now"

✅ *You know it worked when you open a terminal (a black or white window where
you type) and type `python --version` and it prints something like
`Python 3.11.x`.*

**What is a terminal?** The text window where commands run. To open one **inside
the vishnu folder**:
- **Windows:** open the `vishnu` folder in File Explorer → click the address
  bar at the top → type `cmd` → press Enter.
- **Mac:** right-click the `vishnu` folder → *New Terminal from Folder*.
  (Or: open Terminal app, then type `cd /path/to/vishnu`.)

---

## Step 1 — Install the agent (one-time, ~2 minutes)

Make sure you are in the `vishnu` folder (see above), then:

**Mac / Linux**
```bash
bash setup.sh
```

**Windows** (in the cmd window from Step 0)
```bat
setup.bat
```

That's it. It installs everything the agent needs.

✅ *You'll know it worked when you see* `Done!` *at the end of the output.*

---

## Step 2 — Put your name on the videos

Open the file **`config.yaml`** (any text editor: Notepad, TextEdit, VS Code)
and change this line:

```yaml
  handle: "@yourhandle"      ←  change to your real handle, e.g. "@dakufitness81"
```

Also check the line above it:

```yaml
  niche: fitness             ←  the topic of the ideas. Options:
                                fitness, tech, finance, cooking, travel, general
```

Save the file.

---

## Step 3 — Make your first video (the fun part)

**Mac / Linux**
```bash
./.venv/bin/python -m agent run --dry-run
```

**Windows**
```bat
.venv\Scripts\python -m agent run --dry-run
```

Watch the text scroll:

```
==== Post 1/1 ============================================
  [idea]    I fixed my posture in 30 days  (format: story)
  [script]  4 beats via offline engine
  [video]   rendering (silent + captions)...
  [publish] local ...
            OK  Saved to .../output/published/20260921-...
```

`--dry-run` means "make the video but don't post it anywhere" — perfect for
the first try.

✅ **Watch your first video:** open the **`output/posts`** folder, open the
newest folder inside it, and double-click **`video.mp4`**. That video was
invented, scripted, and produced by the agent, automatically.

More useful commands:

| You want to... | Type (Mac/Linux) | Type (Windows) |
|---|---|---|
| See ideas before making a video | `./.venv/bin/python -m agent ideas` | `.venv\Scripts\python -m agent ideas` |
| See what has been made | `./.venv/bin/python -m agent status` | `.venv\Scripts\python -m agent status` |
| Use your own idea | `./.venv/bin/python -m agent run --idea "Your idea here"` | `.venv\Scripts\python -m agent run --idea "Your idea here"` |

---

## Step 4 — Connect your first social account (optional)

You can skip this and keep making videos with `--dry-run`. When you're ready
to auto-post, connect the account you want. Put your details in the **`.env`**
file (create it once with this command):

```bash
./.venv/bin/python -m agent init        # Windows: .venv\Scripts\python -m agent init
```

Then change **`config.yaml`** → `platforms: [local]` to the account(s) you
connect, e.g. `platforms: [youtube]` or `platforms: [youtube, x]`.

### 📺 YouTube (recommended first account — Shorts)

1. Go to https://console.cloud.google.com (free Google account).
2. Create a project (top-left → name it anything, e.g. "mystuff").
3. Menu → **APIs & Services → Library** → search **"YouTube Data API v3"** →
   **Enable**.
4. Menu → **APIs & Services → OAuth consent screen** → choose *External* →
   fill only the **App name** and **your email** → *Create*. On the next
   screen, under *Test users*, add your own Google email → *Save*.
5. Menu → **APIs & Services → Credentials → + Create Credentials → OAuth
   client ID** → application type **"Desktop app"** → *Create*.
6. A JSON file downloads. **Rename it `client_secret.json`** and put it in a
   new folder called **`secrets`** inside the vishnu folder
   (i.e. `vishnu/secrets/client_secret.json`).
7. In `.env`, set (use your real folder path):
   ```
   YOUTUBE_CLIENT_SECRET_JSON=/home/you/vishnu/secrets/client_secret.json
   ```
   (Windows looks like `C:\Users\you\vishnu\secrets\client_secret.json`)
8. Install the YouTube library (one-time):
   ```bash
   ./.venv/bin/pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
9. Connect your account (one-time, ~1 minute):
   ```bash
   ./.venv/bin/python -m agent auth youtube
   ```
   It prints a link → open it → Google asks permission → click *Continue* →
   a code appears on a Google page → copy it → paste it back in the terminal
   → Enter. You'll see *"YouTube token saved"* ✅
10. Set `platforms: [youtube]` in `config.yaml` and run:
    ```bash
    ./.venv/bin/python -m agent run
    ```
    Your video now appears on your channel. Vertical videos under 60 s show
    as **Shorts** automatically. (Optional: set `YOUTUBE_PRIVACY=unlisted` in
    `.env` while you check the first few.)

### 🐦 X (Twitter)

1. Go to https://developer.x.com → sign in → **Projects and Apps → Create
   Project & App** (any name).
2. In the app → **Settings** → **Redirect URIs**, add:
   `http://localhost:8080/callback`
3. In the app → **Keys and tokens**, copy **Client ID** and **Client Secret**
   into `.env`:
   ```
   X_CLIENT_ID=abc123...
   X_CLIENT_SECRET=xyz789...
   ```
4. Connect (one-time):
   ```bash
   ./.venv/bin/python -m agent auth x
   ```
   It prints a link → open it → approve → the page shows an **authorization
   code** → copy it → paste it in the terminal → Enter. *"X token saved"* ✅
5. Set `platforms: [x]` in `config.yaml` and run `python -m agent run`.
   (Note: X's free plan allows only a small number of posts per month.)

### 📘 Facebook / 📸 Instagram / 🎵 TikTok (short version)

These also need a small "developer app" — the full click-by-click is in
`README.md` (section *Connecting your accounts*). The short version:

| Platform | You need to create | Paste in `.env` |
|---|---|---|
| Facebook Page | a Meta app + a Page access token | `FACEBOOK_PAGE_ID=...` and `FACEBOOK_PAGE_TOKEN=...` |
| Instagram (business) | same Meta app + business account linked to your Page | `INSTAGRAM_BUSINESS_ACCOUNT_ID=...` and `INSTAGRAM_ACCESS_TOKEN=...` |
| TikTok | a TikTok developer app with Content Posting API access (review required) | `TIKTOK_CLIENT_KEY=...` and `TIKTOK_CLIENT_SECRET=...` |

---

## Step 5 — Make it post automatically every day

Pick one option:

### Option A — "keep the program open" (easiest to understand)
```bash
nohup ./.venv/bin/python -m agent loop --interval 86400 >> autopilot.log 2>&1 &
```
It now makes + posts **one video every 24 hours** as long as the computer is
on. (`--interval 3600` = every hour, `--interval 604800` = every week.)
To stop it: press Ctrl+C if it's in front of you, or
`pkill -f "agent loop"`.

### Option B — let the computer do it (runs even after you close things)
**Mac / Linux (cron):**
```bash
crontab -e
```
then add this line (change the path to your real vishnu folder; this posts
daily at 07:30):
```
30 7 * * * cd /home/you/vishnu && ./.venv/bin/python -m agent run >> autopilot.log 2>&1
```
Save and exit. Done — it runs forever, even after restarts.

**Windows (Task Scheduler):**
1. Open **Task Scheduler** (search in Start menu) → *Create Basic Task*.
2. Name: "Vishnu AutoPilot" → trigger: **Daily**, pick the time.
3. Action: **Start a program**
   - Program: `C:\Users\you\vishnu\.venv\Scripts\python.exe`
   - Arguments: `-m agent run`
   - Start in: `C:\Users\you\vishnu`
4. Finish. Done.

✅ *Check it's working the next morning: `python -m agent status` (with your
.venv prefix) shows the new post.*

---

## Step 6 — (Optional) Make the videos even better

Add an **OpenAI API key** to `.env` (buy credits at https://platform.openai.com,
$5 lasts for a long time):

```
OPENAI_API_KEY=sk-...
```

Instantly, with no other changes:
- ideas and scripts are written by a real AI instead of the built-in engine
- every video gets a **spoken voiceover** (you can change the voice:
  `TTS_VOICE=nova` in `.env`)

Everything is optional — without the key, the agent still works fully.

---

## Cheat sheet (everyday commands)

All commands are run from inside the `vishnu` folder.
**Mac/Linux prefix:** `./.venv/bin/python -m agent` — **Windows prefix:**
`.venv\Scripts\python -m agent`

| Do this | Command |
|---|---|
| Make + post today's video | `run` |
| Make a video, don't post | `run --dry-run` |
| Post 2 videos at once | `run --count 2` |
| Only specific accounts | `run --platforms youtube,x` |
| My own idea | `run --idea "best morning meals"` |
| See ideas | `ideas` |
| History of posts | `status` |
| Daily autopilot | `loop --interval 86400` |

Example (Mac/Linux):
```bash
./.venv/bin/python -m agent run --platforms youtube
```

---

## "Something went wrong" — the 5 fixes that solve 95% of problems

1. **`python` is not recognized** → Python isn't installed (or on Windows you
   missed the *Add to PATH* box). Reinstall from python.org with that box
   ticked, then restart the terminal.
2. **`No module named agent`** → your terminal isn't inside the `vishnu`
   folder. Reopen it inside the folder (Step 0) and try again.
3. **A platform shows `[--]` / `FAIL`** → read the message right below it.
   9 times out of 10 it's a missing value in `.env` or the one-time
   `auth` step wasn't run yet.
4. **Video looks generic / wrong topic** → change `niche` and `handle` in
   `config.yaml`, then run again. Ideas repeat? They never should — if they
   do, delete `state.json` and try again.
5. **YouTube post isn't visible** → you probably set
   `YOUTUBE_PRIVACY=unlisted` — remove that line from `.env` to make posts
   public.

Anything else: run the command again and read the message — the agent prints
plain-English explanations of what it needs.

---

## How much does it cost?

| Part | Cost |
|---|---|
| Ideas + scripts (built-in engine) | **free** |
| Video production | **free** |
| Posting to YouTube / TikTok / FB / IG | **free** |
| Posting to X (free plan) | free, limited posts per month |
| LLM writing + voiceover (optional) | a few cents per video (~$5 OpenAI credit ≈ hundreds of videos) |

You are in control of every account, every post, and every setting.
