# Multi-Agent Job Search

Local pipeline that turns a resume and search preferences into ranked jobs and application drafts. Specialized agents handle profile extraction, search, matching, research, writing, and tracking.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
```

Edit `.env`:

- **LLM (optional):** set `OPENAI_API_KEY` (any OpenAI-compatible endpoint via `OPENAI_BASE_URL`) and `USE_LLM=true`. Profile extraction, resume design, cover letters and company briefs then use the LLM; otherwise they use built-in heuristics.
- **Live jobs (optional):** get free keys at [developer.adzuna.com](https://developer.adzuna.com), set `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` and `USE_MOCK_JOBS=false`. Without them, searches use sample listings. If the API call fails, the app falls back to the sample listings.

## Run

```bash
# CLI
job-search --help
job-search --resume data/resumes/sample.txt

# UI (http://localhost:8501)
streamlit run src/job_search/app.py
```

The UI has three pages in the sidebar: **Dashboard** (stats, charts, application tracker), **Design resume**, and **Find jobs**.

```bash
pytest
ruff check src tests
```

## Layout

```
config/          non-secret defaults
data/            resumes, cached jobs, application drafts, tracker.json
prompts/         agent prompt templates
src/job_search/  package (agents, tools, orchestrator, UI)
  ui/
    components/  metrics, charts, header, applications, jobs/
      jobs/      search form, job cards, results list
    services/    CV text load + keyword extraction for Find jobs
    pages/       Dashboard, Design resume, Find jobs pages
    state.py     fresh-session bootstrap + cross-page helpers
    theme.py     dashboard CSS and chart styling
    seed.py      demo tracker data for first run
tests/
```

Pipeline: **Profile → Search → Match → Research → Writer → Tracker**.
