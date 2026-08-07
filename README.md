---
title: SafeX Outreach Assistant
emoji: 🎯
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# 🎯 SafeX Outreach Assistant

A tool to make daily client outreach faster and better-tracked — **without automating any
actual sending**. It drafts personalized message openers using Gemini, and tracks logged
outreach against daily targets, in one small self-contained web app.

**Author:** Huma Aslam · SafeX Solutions AI/ML Intern

---

## ⚠️ Why this doesn't auto-send anything (read first)

Automating direct messages on Instagram, X, Facebook, TikTok, or Telegram violates those
platforms' Terms of Service and typically gets accounts suspended. Automated bulk email
outreach also carries real legal risk under anti-spam laws. So this tool deliberately does
**not** connect to any social platform or email API to send anything.

It does two things instead:
1. **Drafts** a personalized opening message for a specific business — you review, edit,
   and send it yourself, one real conversation at a time.
2. **Tracks** what you've actually sent, with daily progress against your targets.

## ✨ Features

- Gemini-powered draft generation, tailored to business name, industry, city, and platform
- Outreach rules (no links in first message, identifies you as a SafeX intern, low-pressure
  tone) are baked into the prompt automatically
- Daily progress bars per platform (Instagram 30, X 30, Facebook 30, Email 40, TikTok 30,
  Telegram 50)
- Searchable log of everything sent, with response status
- Tracker works even without a Gemini key configured — only drafting needs it

## 🛠️ Tech stack

| Layer | Tech |
|---|---|
| LLM | Google Gemini 2.5 Flash |
| Orchestration | LangChain |
| Backend | FastAPI |
| Storage | JSON file (lightweight, no DB needed at this scale) |
| Frontend | Single-file HTML/CSS/JS, no framework |
| Hosting | Hugging Face Spaces (Docker) |

## 📂 Project structure

```
backend/
  main.py          # FastAPI app: /api/draft, /api/log, /api/progress, /api/platforms
  drafting.py       # Gemini-powered drafting (lazy-loaded — works even without a key set)
  storage.py        # JSON-file based log storage
  schemas.py         # request/response models + daily targets
  static/index.html  # the frontend (Draft tab + Tracker tab)
Dockerfile
requirements.txt
```

## 🚀 Running locally

**Windows note:** if `pip` or `uvicorn` aren't recognized directly, use `python -m pip` /
`python -m uvicorn` instead — routes through Python regardless of PATH setup.

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file (copy `.env.example`) and add your real key:
```
GEMINI_API_KEY=your_actual_key_here
```

Run it:
```bash
python -m uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000` — the app loads directly (frontend served by the backend).

## ☁️ Deploying (Hugging Face Spaces)

GitHub Pages **cannot** host this — it only serves static files and can't run the Python
backend or call the Gemini API server-side. Use Hugging Face Spaces instead:

1. Create a Space at [huggingface.co/new-space](https://huggingface.co/new-space) —
   SDK: **Docker**
2. Clone it locally, copy this project's files into that cloned folder (everything in this
   repo — `backend/`, `Dockerfile`, `requirements.txt`, `README.md` — but **not** `.env`)
3. Push:
   ```bash
   git add .
   git commit -m "Initial deploy"
   git push
   ```
4. On the Space's **Settings → Variables and secrets**, add `GEMINI_API_KEY` with your
   real key
5. Wait for the build to finish (Logs tab) — then it's live at
   `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## 🔒 What this doesn't do (on purpose)

- Doesn't log into or post to any social platform
- Doesn't send email
- Doesn't scrape contact info without you providing it
- Doesn't auto-follow-up — every send stays entirely manual, yours
