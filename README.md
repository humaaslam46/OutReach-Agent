# SafeX Outreach Assistant

A tool to make daily outreach faster and better-tracked — **without automating any actual
sending**. It drafts personalized message openers using Gemini, and tracks your logged
outreach against daily targets, all in one small web app.

## Why it works this way (read this first)

Automating direct messages on Instagram, X, Facebook, TikTok, or Telegram violates those
platforms' Terms of Service and typically gets accounts suspended — the platforms'
anti-spam systems are specifically built to catch this pattern. Automated bulk email (e.g.
BCC-blasting dozens of cold recipients daily) also carries real legal risk under anti-spam
laws depending on where recipients are.

So this tool deliberately does **not** connect to any social platform or email API to send
anything. It does two things well instead:

1. **Drafts** a personalized, on-brief opening message for a specific business — you review,
   edit, and send it yourself, from your own account, one real conversation at a time.
2. **Tracks** what you've actually sent, so you can see daily progress toward your targets
   without maintaining a spreadsheet by hand.

## Features

- Generates a draft message tailored to a business's name, industry, city, and platform —
  the prompt enforces the outreach brief's own rules automatically (no links in the first
  message, identifies you as a SafeX intern, professional tone, no pressure)
- Daily progress bars per platform against your targets (Instagram 30, X 30, Facebook 30,
  Email 40, TikTok 30, Telegram 50)
- A searchable log of everything you've sent, with response status

## Running it locally

```bash
pip install -r requirements.txt
# create .env from .env.example and add your real GEMINI_API_KEY
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000` — the app loads directly (frontend is served by the backend,
same pattern as the SafeX chatbot project).

**Note:** the tracker (logging, progress bars) works even without a Gemini key set — only
the "Generate draft" button needs it. This is intentional (see `backend/drafting.py`) so a
missing/invalid key doesn't take down the whole tool.

## Project structure

```
backend/
  main.py         # FastAPI app: /api/draft, /api/log, /api/progress, /api/platforms
  drafting.py      # Gemini-powered message drafting, with the brief's rules baked into the prompt
  storage.py       # JSON-file based log storage (same lightweight pattern as the SafeX chatbot's analytics)
  schemas.py       # request/response models + daily targets
  static/index.html # the single-file frontend (Draft tab + Tracker tab)
```

## Deploying

Same approach as the SafeX chatbot — this is structured identically (FastAPI serving its
own static frontend at `/`), so it deploys the same way: a single Hugging Face Space
(Docker SDK), with `GEMINI_API_KEY` set as a Space secret. See your Task 1 `DEPLOY.md` for
the exact steps — they apply unchanged here.

## What this doesn't do (on purpose)

- Doesn't log into or post to any social platform
- Doesn't send email
- Doesn't scrape contact info without you providing it
- Doesn't auto-follow-up — that decision (and every send) stays entirely manual, yours
