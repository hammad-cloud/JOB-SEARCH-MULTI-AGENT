"""Top-row colored stat cards for the pipeline dashboard."""

from __future__ import annotations

import streamlit.components.v1 as components

from job_search.models.schemas import TrackerStatus
from job_search.ui.theme import COLORS, FONT_BODY, FONT_IMPORT

METRIC_CARDS = [
    ("in_process", "Applications in process", COLORS["card_blue"]),
    (TrackerStatus.INTERVIEW.value, "Interviews scheduled", COLORS["card_purple"]),
    (TrackerStatus.OFFER.value, "Offers received", COLORS["card_orange"]),
]


def build_display_counts(counts: dict[str, int]) -> dict[str, int]:
    """Derive the aggregate IN PROCESS metric shown in the dashboard."""
    in_process = (
        counts.get(TrackerStatus.ACTIVE.value, 0)
        + counts.get(TrackerStatus.IN_PROCESS.value, 0)
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
        <div class="metric-card" style="background:{color};">
          <div class="metric-value">{display.get(key, 0)}</div>
          <div class="metric-label">{label}</div>
        </div>
        """
        for key, label, color in METRIC_CARDS
    )
    html = f"""
    <style>
      {FONT_IMPORT}
      body {{ margin: 0; }}
      .metric-row {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 18px;
        font-family: {FONT_BODY};
      }}
      .metric-card {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 20px 22px;
        color: #FFFFFF;
      }}
      .metric-value {{ font-family: 'Epilogue', sans-serif; font-size: 40px; font-weight: 600; }}
      .metric-label {{ font-size: 17px; font-weight: 500; line-height: 1.3; }}
      @media (max-width: 700px) {{
        .metric-row {{ grid-template-columns: 1fr; }}
      }}
    </style>
    <div class="metric-row">{cards}</div>
    """
    components.html(html, height=100)
