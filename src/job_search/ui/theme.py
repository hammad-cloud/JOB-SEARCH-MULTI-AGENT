"""Shared dashboard theme: colors, CSS injection, and chart layout defaults."""

from __future__ import annotations

import streamlit as st

from job_search.models.schemas import TrackerStatus

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Epilogue:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');"
)
FONT_BODY = "'Inter', 'Source Sans Pro', sans-serif"
FONT_HEADING = "'Epilogue', 'Inter', sans-serif"

COLORS = {
    "primary": "#4640DE",
    "text": "#25324B",
    "muted": "#7C8493",
    "border": "#D6DDEB",
    "card_blue": "#26A4FF",
    "card_purple": "#9F5BE0",
    "card_orange": "#FFB836",
    "bar_open": "#26A4FF",
    "bar_progress": "#FFB836",
    "up": "#56CDAD",
    "down": "#FF6550",
}

STATUS_COLORS = {
    TrackerStatus.ACTIVE: "#26A4FF",
    TrackerStatus.IN_PROCESS: "#7B61FF",
    TrackerStatus.INTERVIEW: "#FFB836",
    TrackerStatus.OFFER: "#F472B6",
    TrackerStatus.HIRED: "#56CDAD",
    TrackerStatus.REJECTED: "#FF6550",
}

# (status, color, short label) in legend order
STATUS_LEGEND: list[tuple[TrackerStatus, str, str]] = [
    (TrackerStatus.ACTIVE, STATUS_COLORS[TrackerStatus.ACTIVE], "Active"),
    (TrackerStatus.IN_PROCESS, STATUS_COLORS[TrackerStatus.IN_PROCESS], "In process"),
    (TrackerStatus.INTERVIEW, STATUS_COLORS[TrackerStatus.INTERVIEW], "Interview"),
    (TrackerStatus.OFFER, STATUS_COLORS[TrackerStatus.OFFER], "Offer"),
    (TrackerStatus.HIRED, STATUS_COLORS[TrackerStatus.HIRED], "Hired"),
    (TrackerStatus.REJECTED, STATUS_COLORS[TrackerStatus.REJECTED], "Rejected"),
]

DASHBOARD_CSS = f"""
<style>
  {FONT_IMPORT}
  html, body, .stApp {{ font-family: {FONT_BODY}; }}
  h1, h2, h3, .dash-greeting {{ font-family: {FONT_HEADING} !important; color: {COLORS["text"]}; }}

  .block-container {{ padding-top: 1.6rem; max-width: 1400px; }}
  [data-testid="stHeader"] {{ background: transparent; }}

  /* Purple sidebar */
  [data-testid="stSidebar"] {{ background: {COLORS["primary"]}; }}
  [data-testid="stSidebar"] * {{ color: #FFFFFF; }}
  [data-testid="stSidebar"] .brand {{
    font-family: {FONT_HEADING}; font-size: 22px; font-weight: 700; margin: 0 0 18px 6px;
  }}
  [data-testid="stSidebar"] .side-section {{
    font-size: 12px; letter-spacing: 0.08em; opacity: 0.75; margin: 22px 0 6px 6px;
    padding-top: 18px; border-top: 1px solid rgba(255,255,255,0.18);
  }}

  /* Sidebar nav: radio rendered as menu items */
  [data-testid="stSidebar"] [role="radiogroup"] {{ gap: 4px; width: 100%; }}
  [data-testid="stSidebar"] [role="radiogroup"] label {{
    width: 100%; padding: 9px 14px; border-radius: 6px; margin: 0;
  }}
  [data-testid="stSidebar"] [role="radiogroup"] > div {{ width: 100%; }}
  [data-testid="stSidebar"] [role="radiogroup"] label > div > div:first-child {{ display: none; }}
  [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
    background: rgba(255,255,255,0.10);
  }}
  [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{ background: #FFFFFF; }}
  [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * {{
    color: {COLORS["primary"]} !important; font-weight: 600;
  }}

  /* Sidebar CV uploader */
  [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
    background: rgba(255,255,255,0.10); border: 1px dashed rgba(255,255,255,0.45);
  }}
  [data-testid="stSidebar"] [data-testid="stFileUploader"] button {{
    background: #FFFFFF; border: none;
  }}
  [data-testid="stSidebar"] [data-testid="stFileUploader"] button * {{
    color: {COLORS["primary"]};
  }}

  /* Header */
  .dash-greeting {{ font-size: 24px; font-weight: 700; margin: 0; }}
  .dash-sub {{ color: {COLORS["muted"]}; font-size: 14px; margin: 4px 0 0; }}
  .date-chip {{
    float: right; border: 1px solid {COLORS["border"]}; padding: 10px 14px;
    font-size: 14px; color: {COLORS["text"]}; white-space: nowrap;
  }}

  /* Cards */
  [data-testid="stVerticalBlockBorderWrapper"] {{
    background: #FFFFFF; border-color: {COLORS["border"]} !important; border-radius: 4px;
  }}
  .card-title {{
    font-family: {FONT_HEADING};
    font-weight: 600;
    font-size: 18px;
    color: {COLORS["text"]};
    margin: 0;
  }}
  .card-caption {{ color: {COLORS["muted"]}; font-size: 13px; margin: 2px 0 0; }}
  .big-num {{
    font-family: {FONT_HEADING}; font-size: 52px; font-weight: 600; color: {COLORS["text"]};
    margin: 10px 0 6px; line-height: 1.1;
  }}
  .big-num span {{
    font-family: {FONT_BODY};
    font-size: 17px;
    font-weight: 400;
    color: {COLORS["muted"]};
  }}
  .seg-bar {{ display: flex; height: 10px; margin: 14px 0 16px; }}
  .legend-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px 12px;
    font-size: 13px; color: {COLORS["muted"]};
  }}
  .legend-grid b {{ color: {COLORS["text"]}; }}
  .legend-grid .dot {{
    display: inline-block; width: 14px; height: 14px; border-radius: 3px;
    margin-right: 8px; vertical-align: -2px;
  }}

  /* Tabs (inside Job statistics) */
  .stTabs [data-baseweb="tab-list"] {{ gap: 24px; border-bottom: 1px solid {COLORS["border"]}; }}
  .stTabs [data-baseweb="tab"] {{ color: {COLORS["muted"]}; padding: 8px 2px; font-weight: 500; }}
  .stTabs [aria-selected="true"] {{ color: {COLORS["text"]} !important; font-weight: 600; }}
  .stTabs [data-baseweb="tab-highlight"] {{ background-color: {COLORS["primary"]} !important; }}

  /* Week / Month / Year toggle */
  [data-testid="stButtonGroup"] {{
    background: #E9EBFD;
    padding: 4px;
    border-radius: 2px;
    float: right;
  }}
  [data-testid="stButtonGroup"] button {{
    border: none !important;
    background: transparent;
    color: {COLORS["primary"]};
  }}
  [data-testid="stButtonGroup"] button[kind="segmented_controlActive"] {{ background: #FFFFFF; }}

  .stButton > button[kind="primary"] {{ border-radius: 2px; font-weight: 600; }}
  .js-plotly-plot .plotly .modebar {{ display: none !important; }}

  /* Find jobs */
  .jobs-found {{ color: {COLORS["muted"]}; font-size: 14px; margin: 12px 0 10px; }}
  div[data-testid="stMarkdownContainer"] a {{
    color: {COLORS["primary"]}; font-size: 18px; font-weight: 600; text-decoration: underline;
  }}
</style>
"""


def inject_dashboard_theme() -> None:
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def plotly_layout(**overrides) -> dict:
    base = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": COLORS["muted"], "size": 12, "family": "Inter, sans-serif"},
        "margin": {"l": 8, "r": 8, "t": 8, "b": 8},
        "showlegend": False,
        "xaxis": {"gridcolor": "rgba(0,0,0,0)", "zerolinecolor": COLORS["border"]},
        "yaxis": {"gridcolor": "rgba(0,0,0,0)", "zerolinecolor": COLORS["border"]},
    }
    base.update(overrides)
    return base
