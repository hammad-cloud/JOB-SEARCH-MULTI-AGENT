# Multi-Agent Job Search

Local pipeline that turns a resume and search preferences into ranked jobs and application drafts. Specialized agents handle profile extraction, search, matching, research, writing, and tracking.

## Agents

| Agent | Role |
|-------|------|
| **Profile** | Turns resume text into a structured candidate profile |
| **Search** | Finds jobs from the Adzuna API, or sample listings when no key is set |
| **Match** | Scores each job against the candidate profile |
| **Research** | Writes a short company and role brief for the top matches |
| **Writer** | Drafts cover letters and resume bullets for the top matches |
| **Tracker** | Saves results and tracks applications for later review |
| **Resume design** | Reorders a real resume toward a target job without inventing experience |

## Tech stack

Python 3.11, Pydantic, OpenAI-compatible LLM API, Adzuna Jobs API (httpx), Streamlit, Plotly, Pytest, Ruff, GitHub Actions CI.

## Setup

```bash
git clone https://github.com/hammad-cloud/JOB-SEARCH-MULTI-AGENT.git
cd JOB-SEARCH-MULTI-AGENT
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

## Folder structure

```
JOB-SEARCH-MULTI-AGENT/
.github/workflows/ CI: Ruff lint + Pytest on every push
config/          non-secret defaults (settings.yaml)
data/            resumes, cached jobs, application drafts, tracker.json
prompts/         agent prompt templates
src/job_search/
  agents/        profile, search, match, research, writer, tracker, resume design
  orchestrator/  pipeline.py: runs the agents in order
  tools/         job board API, resume parser, storage, tracker
  llm/           OpenAI-compatible client
  models/        Pydantic schemas
  main.py        CLI entry point (job-search)
  app.py         Streamlit entry point
  ui/
    components/  metrics, charts, header, applications, jobs/
      jobs/      search form, job cards, results list
    services/    CV text load + keyword extraction for Find jobs
    pages/       Dashboard, Design resume, Find jobs pages
    state.py     fresh-session bootstrap + cross-page helpers
    theme.py     dashboard CSS and chart styling
    seed.py      demo tracker data for first run
tests/           unit tests with fixtures
```

Pipeline: **Profile → Search → Match → Research → Writer → Tracker**.

## License

[MIT](LICENSE) © 2026 Muhammad Hammad
