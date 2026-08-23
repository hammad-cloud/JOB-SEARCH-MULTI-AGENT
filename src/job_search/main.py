"""CLI entry: job-search --resume path/to/resume.txt"""

from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from job_search.models.schemas import SearchPreferences
from job_search.orchestrator.pipeline import JobSearchPipeline

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the multi-agent job search pipeline.")
    parser.add_argument("--resume", required=True, type=Path, help="Path to a .txt or .md resume")
    parser.add_argument("--keywords", default="", help="Comma-separated search keywords")
    parser.add_argument("--location", default="Remote")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--onsite", action="store_true", help="Include non-remote roles")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    preferences = SearchPreferences(
        keywords=[item.strip() for item in args.keywords.split(",") if item.strip()],
        location=args.location,
        remote_only=not args.onsite,
        results_limit=args.limit,
    )
    result = JobSearchPipeline().run(args.resume, preferences)

    skill_count = len(result.profile.skills)
    console.print(f"\n[bold]{result.profile.name}[/bold] · {skill_count} skills extracted")
    table = Table(title="Ranked jobs")
    table.add_column("Score")
    table.add_column("Title")
    table.add_column("Company")
    table.add_column("Location")
    for match in result.matches:
        job = match.job
        if not job:
            continue
        table.add_row(str(match.score), job.title, job.company, job.location)
    console.print(table)
    console.print(f"[green]Saved {len(result.drafts)} draft(s) to data/applications/[/green]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
