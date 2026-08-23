"""Pipeline dashboard page."""

from __future__ import annotations

from job_search.tools.tracker import TrackerStore
from job_search.ui.components.applications import render_applications_table
from job_search.ui.components.charts import render_dashboard_charts
from job_search.ui.components.metrics import render_metrics


def render_pipeline_page(store: TrackerStore) -> None:
    items = store.list()
    counts = store.counts()
    render_metrics(counts)
    render_dashboard_charts(items, counts)
    render_applications_table(store, items)
