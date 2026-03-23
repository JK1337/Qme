# Qme

Qme is built around one goal: **find your dream job**. Play-to-learn modules earn **credits** and certificates; once a target role is in sight, those credits feed premium tools (CV alignment, polish, reQme) — the demo accrues credits only; spending them on actions can be wired next.

## What it offers

- **Dream job first** — narrative and `/dream-job` page state the product intent.
- **Browse roles** — `/jobs` with filters, shortlist (session), detail pages, and “Tailor CV” deep-links to `/cv?job=…` with the description pre-filled.
- **Play to learn** — complete modules to earn **credits** and certificates. **Signed-in** CV rewrites cost `REWRITE_COST` credits (see `qme/services/credits.py`); guests can try rewrites without spending.
- **reQme** — stable `/r/{token}` per account; rotate invalidates old links. Public page shows certificates and CV/life-story excerpts.
- **Account + CV rewrite** — create an account with an optional **main CV** and **life story**. While signed in, job-targeted rewrites use your main CV by default (you can paste a one-off override) and always incorporate your life story as narrative strength. The same context is intended to power future AI job search across the app. Wire a real LLM via `QME_LLM_PROVIDER` and your keys (see `qme/services/cv_rewrite.py`).
- **Sessions** — set `QME_SECRET_KEY` in production for signed cookies (`itsdangerous`).
- **Styling & reQme** — the UI sketches multiple CV styles and a **reQme** share link (`/r/{token}`) for a recipient-facing profile view.

## Requirements

- Python 3.11+

## Run locally

```bash
cd Qme
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
uvicorn qme.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Optional: copy `.env.example` to `.env` and adjust variables.

## Create the GitHub repository

Git is initialized in this folder. To create the remote repo named **Qme** and push:

1. Log in to GitHub CLI: `gh auth login -h github.com` (or create the repo in the GitHub web UI).
2. From this directory:

```bash
git remote add origin git@github.com:YOUR_USER/Qme.git
git branch -M main
git push -u origin main
```

Or with a authenticated `gh`:

```bash
gh repo create Qme --private --source=. --remote=origin --push
```

## License

MIT
