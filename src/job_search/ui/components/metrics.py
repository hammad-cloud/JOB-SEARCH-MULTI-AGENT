"""Top-row metric cards for the pipeline dashboard."""

from __future__ import annotations

import streamlit.components.v1 as components

from job_search.models.schemas import TrackerStatus
from job_search.ui.theme import COLORS

METRIC_CARDS = [
    ("TOTAL", "total", COLORS["total"]),
    ("IN PROCESS", "in_process", COLORS["in_process"]),
    ("ACTIVE", TrackerStatus.ACTIVE.value, COLORS["active"]),
    ("INTERVIEW", TrackerStatus.INTERVIEW.value, COLORS["interview"]),
    ("OFFER", TrackerStatus.OFFER.value, COLORS["offer"]),
    ("HIRED", TrackerStatus.HIRED.value, COLORS["hired"]),
    ("REJECTED/CLOSED", TrackerStatus.REJECTED.value, COLORS["rejected"]),
]


def build_display_counts(counts: dict[str, int]) -> dict[str, int]:
    """Derive the aggregate IN PROCESS metric shown in the dashboard."""
    in_process = (
        counts.get(TrackerStatus.ACTIVE.value, 0)
        + counts.get(TrackerStatus.INTERVIEW.value, 0)
        + counts.get(TrackerStatus.OFFER.value, 0)
    )
    display = dict(counts)
    display["in_process"] = in_process
    return display


def render_metrics(counts: dict[str, int]) -> None:
    display = build_display_counts(counts)
    cards = "".join(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{display.get(key, 0)}</div>
          <div class="metric-bar" style="background:{color};"></div>
        </div>
        """
        for label, key, color in METRIC_CARDS
    )
    html = f"""
    <style>
      .metric-row {{
        display: grid;
        grid-template-columns: repeat(7, minmax(0, 1fr));
        gap: 12px;
        font-family: "Source Sans Pro", sans-serif;
      }}
      .metric-card {{
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 14px 12px 10px;
      }}
      .metric-label {{
        color: #9ca3af;
        font-size: 11px;
        letter-spacing: 0.08em;
        font-weight: 600;
      }}
      .metric-value {{
        color: #f3f4f6;
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
        margin: 4px 0 8px;
      }}
      .metric-bar {{
        height: 3px;
        border-radius: 999px;
      }}
      @media (max-width: 1100px) {{
        .metric-row {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
      }}
    </style>
    <div class="metric-row">{cards}</div>
    """
    components.html(html, height=110)
