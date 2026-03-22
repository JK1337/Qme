# Qme

Qme is a jobs platform with a professional-network feel: it sits between recruiters and job seekers and gives candidates concrete tools to reach a dream role — not just listings.

## What it offers

- **Learn to earn** — complete training modules to earn points and Qme certificates (demo store in this scaffold; swap for a database when you scale).
- **CV aligned to the role** — paste a CV and a job description; get a tailored draft. The API is ready to plug in an LLM via `QME_LLM_PROVIDER` and your keys (see `qme/services/cv_rewrite.py`).
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
