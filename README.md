# Multi-Agent Job Search

Local pipeline that turns a resume and search preferences into ranked jobs and application drafts. Specialized agents handle profile extraction, search, matching, research, writing, and tracking.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
```

Edit `.env` with your LLM key. Leave `USE_MOCK_JOBS=true` until a job API is configured.

## Run

```bash
# CLI
job-search --help
job-search --resume data/resumes/sample.txt

# UI
streamlit run src/job_search/app.py
```

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
    pages/       Pipeline, Design resume, Find jobs tabs
    state.py     fresh-session bootstrap + cross-tab helpers
    theme.py     dashboard CSS and chart styling
    seed.py      demo tracker data for first run
tests/
```

Pipeline: **Profile → Search → Match → Research → Writer → Tracker**.
