"""Shared dashboard theme: colors, CSS injection, and chart layout defaults."""

from __future__ import annotations

import streamlit as st

from job_search.models.schemas import TrackerStatus

# Metric accent colors (match dashboard screenshot)
COLORS = {
    "total": "#e5e7eb",
    "in_process": "#22d3ee",
    "active": "#3b82f6",
    "interview": "#fbbf24",
    "offer": "#a78bfa",
    "hired": "#22c55e",
    "rejected": "#ef4444",
    "sector_bar": "#3b82f6",
    "channel_bar": "#a78bfa",
    "funnel_bar": "#3b82f6",
}

STATUS_CHART_COLORS = {
    "Applied / Active": COLORS["active"],
    "In process": COLORS["in_process"],
    "Interview": COLORS["interview"],
    "Offer": COLORS["offer"],
    "Hired": COLORS["hired"],
    "Rejected/Closed": COLORS["rejected"],
}

# Legend order matching the dashboard screenshot (colored dots)
STATUS_LEGEND: list[tuple[TrackerStatus, str, str]] = [
    (TrackerStatus.ACTIVE, COLORS["active"], "Active"),
    (TrackerStatus.INTERVIEW, COLORS["interview"], "Interview"),
    (TrackerStatus.OFFER, COLORS["offer"], "Offer"),
    (TrackerStatus.HIRED, COLORS["hired"], "Hired"),
    (TrackerStatus.REJECTED, COLORS["rejected"], "Rejected/Closed"),
]

DASHBOARD_CSS = """
<style>
  .block-container {
    padding-top: 1.2rem;
    max-width: 1400px;
  }

  /* Navigation tabs — sober style, no blue flash */
  .stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: transparent;
    border-bottom: 1px solid #30363d;
    padding-bottom: 0;
  }
  .stTabs [data-baseweb="tab-highlight"],
  .stTabs [data-baseweb="tab-border"] {
    display: none !important;
    background-color: transparent !important;
    opacity: 0 !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    border-radius: 8px 8px 0 0;
    color: #9ca3af;
    padding: 10px 18px;
    font-weight: 500;
    font-size: 14px;
    letter-spacing: 0.01em;
    transition: none !important;
    box-shadow: none !important;
    outline: none !important;
  }
  .stTabs [data-baseweb="tab"]:hover {
    color: #e5e7eb;
    background: rgba(255, 255, 255, 0.04);
  }
  .stTabs [aria-selected="true"] {
    background: #161b22 !important;
    color: #f3f4f6 !important;
    border: 1px solid #30363d !important;
    border-bottom-color: #161b22 !important;
    margin-bottom: -1px;
    font-weight: 600;
  }
  .stTabs button,
  .stTabs button:focus,
  .stTabs button:focus-visible,
  .stTabs button:active,
  .stTabs [data-baseweb="tab"]:focus,
  .stTabs [data-baseweb="tab"]:active {
    outline: none !important;
    box-shadow: none !important;
  }
  .stTabs [data-baseweb="tab-panel"] {
    padding-top: 16px;
    border: none;
    background: transparent;
  }

  /* Upload button styling */
  [data-testid="stFileUploader"] section {
    padding: 0;
  }
  [data-testid="stFileUploader"] button {
    background: #374151;
    color: #f3f4f6;
    border: 1px solid #4b5563;
    border-radius: 8px;
    font-weight: 600;
  }
  [data-testid="stFileUploader"] button:hover {
    background: #4b5563;
    color: #ffffff;
    border-color: #6b7280;
  }

  /* Primary buttons — muted instead of bright red/blue flash */
  .stButton > button[kind="primary"] {
    background: #374151;
    border: 1px solid #4b5563;
    color: #f9fafb;
    font-weight: 600;
    transition: background 0.15s ease, border-color 0.15s ease;
  }
  .stButton > button[kind="primary"]:hover {
    background: #4b5563;
    border-color: #6b7280;
    color: #ffffff;
  }
  .stButton > button[kind="primary"]:focus,
  .stButton > button[kind="primary"]:active {
    outline: none !important;
    box-shadow: none !important;
    background: #4b5563;
  }

  /* Secondary buttons */
  .stButton > button[kind="secondary"] {
    background: #161b22;
    border: 1px solid #30363d;
    color: #e5e7eb;
    border-radius: 8px;
    font-weight: 500;
  }
  .stButton > button[kind="secondary"]:hover {
    background: #1f2937;
    border-color: #4b5563;
    color: #f3f4f6;
  }
  .stButton > button:focus,
  .stButton > button:focus-visible {
    outline: none !important;
    box-shadow: none !important;
  }

  /* Bordered chart containers */
  [data-testid="stVerticalBlockBorderWrapper"] {
    background: #161b22;
    border-color: #30363d !important;
    border-radius: 12px;
    padding: 8px 12px 4px;
  }
  [data-testid="stVerticalBlockBorderWrapper"] p {
    color: #f3f4f6;
    font-weight: 600;
    margin-bottom: 0;
  }

  /* Hide plotly mode bar for cleaner cards */
  .js-plotly-plot .plotly .modebar { display: none !important; }

  /* Find jobs */
  .jobs-found {
    color: #9ca3af;
    font-size: 14px;
    margin: 12px 0 10px;
  }
  div[data-testid="stMarkdownContainer"] a {
    color: #60a5fa;
    font-size: 18px;
    font-weight: 600;
    text-decoration: underline;
  }
</style>
"""


def inject_dashboard_theme() -> None:
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def plotly_layout(**overrides) -> dict:
    base = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#9ca3af", "size": 12},
        "margin": {"l": 12, "r": 12, "t": 12, "b": 12},
        "showlegend": False,
        "xaxis": {"gridcolor": "#30363d", "zerolinecolor": "#30363d"},
        "yaxis": {"gridcolor": "#30363d", "zerolinecolor": "#30363d"},
    }
    base.update(overrides)
    return base
