"""Dashboard charts: job statistics card, response rate, and status summary."""

from __future__ import annotations

from collections import Counter
from datetime import date, timedelta

import plotly.graph_objects as go
import streamlit as st

from job_search.models.schemas import TrackedApplication, TrackerChannel, TrackerStatus
from job_search.ui.theme import COLORS, STATUS_LEGEND, plotly_layout

PROGRESSED = (TrackerStatus.INTERVIEW, TrackerStatus.OFFER, TrackerStatus.HIRED)
PERIODS = ["Week", "Month", "Year"]

Bucket = tuple[str, date, date]  # (label, first day, last day) inclusive


def period_buckets(period: str, today: date) -> list[Bucket]:
    """Week = last 7 days, Month = last 4 weeks, Year = last 12 calendar months."""
    if period == "Week":
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        return [(d.strftime("%a"), d, d) for d in days]
    if period == "Month":
        buckets = []
        for i in range(3, -1, -1):
            end = today - timedelta(days=7 * i)
            start = end - timedelta(days=6)
            buckets.append((start.strftime("%b %d"), start, end))
        return buckets
    buckets = []
    year, month = today.year, today.month
    for _ in range(12):
        start = date(year, month, 1)
        next_start = date(year + (month == 12), month % 12 + 1, 1)
        buckets.append((start.strftime("%b"), start, next_start - timedelta(days=1)))
        year, month = (year, month - 1) if month > 1 else (year - 1, 12)
    return buckets[::-1]


def _item_date(item: TrackedApplication) -> date | None:
    try:
        return date.fromisoformat(item.date[:10])
    except ValueError:
        return None


def _in_range(items: list[TrackedApplication], start: date, end: date) -> list[TrackedApplication]:
    return [item for item in items if (d := _item_date(item)) and start <= d <= end]


def _change_html(current: int, previous: int) -> str:
    if previous == 0:
        return f'<span style="color:{COLORS["muted"]}">no prior data</span>'
    pct = (current - previous) / previous * 100
    color, arrow = (COLORS["up"], "&#9650;") if pct >= 0 else (COLORS["down"], "&#9660;")
    return f'<span style="color:{color}">{abs(pct):.1f}% {arrow}</span>'


def _stacked_bars(items: list[TrackedApplication], buckets: list[Bucket]) -> go.Figure:
    labels, open_counts, progressed_counts = [], [], []
    for label, start, end in buckets:
        window = _in_range(items, start, end)
        progressed = sum(item.status in PROGRESSED for item in window)
        labels.append(label)
        progressed_counts.append(progressed)
        open_counts.append(len(window) - progressed)
    fig = go.Figure(
        [
            go.Bar(name="Applied", x=labels, y=open_counts, marker_color=COLORS["bar_open"]),
            go.Bar(
                name="Reached interview",
                x=labels,
                y=progressed_counts,
                marker_color=COLORS["bar_progress"],
            ),
        ]
    )
    fig.update_traces(
        marker_line_width=0, hovertemplate="%{x}: %{y}<extra>%{fullData.name}</extra>"
    )
    fig.update_layout(
        **plotly_layout(
            height=280,
            barmode="stack",
            bargap=0.25,
            showlegend=True,
            legend={"orientation": "h", "y": -0.15, "x": 0},
            yaxis={"visible": False},
        )
    )
    return fig


def _horizontal_bar(labels: list[str], values: list[int], color: str) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker={"color": color, "line": {"width": 0}},
            text=[str(value) for value in values],
            textposition="outside",
            hovertemplate="%{y}: %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        **plotly_layout(
            height=280,
            yaxis={"categoryorder": "total ascending", "tickfont": {"color": COLORS["text"]}},
            xaxis={"visible": False},
            margin={"l": 8, "r": 36, "t": 8, "b": 8},
        )
    )
    return fig


def _plot(fig: go.Figure) -> None:
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _mini_card(title: str, value: int, period: str, change_html: str) -> None:
    with st.container(border=True):
        st.markdown(
            f"""
            <p class="card-title" style="font-size:16px">{title}</p>
            <div class="big-num" style="font-size:28px">{value}</div>
            <p class="card-caption">This {period.lower()} {change_html}</p>
            """,
            unsafe_allow_html=True,
        )


def _funnel_counts(items: list[TrackedApplication]) -> dict[str, int]:
    return {
        "Applied": len(items),
        "Interview": sum(item.status in PROGRESSED for item in items),
        "Offer": sum(item.status in (TrackerStatus.OFFER, TrackerStatus.HIRED) for item in items),
        "Hired": sum(item.status == TrackerStatus.HIRED for item in items),
    }


def _job_statistics(items: list[TrackedApplication]) -> None:
    with st.container(border=True):
        title_col, toggle_col = st.columns([2, 1])
        with toggle_col:
            period = (
                st.segmented_control(
                    "Period",
                    PERIODS,
                    default="Year",
                    key="stats_period",
                    label_visibility="collapsed",
                )
                or "Year"
            )
        buckets = period_buckets(period, date.today())
        start, end = buckets[0][1], min(buckets[-1][2], date.today())
        with title_col:
            st.markdown(
                f"""
                <p class="card-title">Job statistics</p>
                <p class="card-caption">Showing applications {start:%b %d, %Y} – {end:%b %d, %Y}</p>
                """,
                unsafe_allow_html=True,
            )

        overview, sector_tab, channel_tab, funnel_tab = st.tabs(
            ["Overview", "By sector", "By channel", "Funnel"]
        )
        with overview:
            chart_col, side_col = st.columns([1.7, 1])
            with chart_col:
                _plot(_stacked_bars(items, buckets))
            span = end - start + timedelta(days=1)
            current = _in_range(items, start, end)
            previous = _in_range(items, start - span, start - timedelta(days=1))
            cur_prog = sum(item.status in PROGRESSED for item in current)
            prev_prog = sum(item.status in PROGRESSED for item in previous)
            with side_col:
                applied_change = _change_html(len(current), len(previous))
                _mini_card("Applied", len(current), period, applied_change)
                _mini_card("Reached interview", cur_prog, period, _change_html(cur_prog, prev_prog))
        with sector_tab:
            sectors = Counter(item.sector.strip() or "Unspecified" for item in items)
            if sectors:
                _plot(_horizontal_bar(list(sectors), list(sectors.values()), COLORS["primary"]))
            else:
                st.caption("No applications yet.")
        with channel_tab:
            channels = Counter(
                (item.channel.value if item.channel else TrackerChannel.ONLINE.value)
                for item in items
            )
            if channels:
                values = list(channels.values())
                _plot(_horizontal_bar(list(channels), values, COLORS["card_purple"]))
            else:
                st.caption("No applications yet.")
        with funnel_tab:
            funnel = _funnel_counts(items)
            _plot(_horizontal_bar(list(funnel), list(funnel.values()), COLORS["card_blue"]))


def _status_summary(counts: dict[str, int], total: int) -> None:
    segments = "".join(
        f'<div style="flex:{counts.get(status.value, 0)};background:{color}"></div>'
        for status, color, _ in STATUS_LEGEND
        if counts.get(status.value, 0)
    ) or '<div style="flex:1;background:#E9EBFD"></div>'
    legend = "".join(
        f'<div><span class="dot" style="background:{color}"></span>'
        f"{label} : <b>{counts.get(status.value, 0)}</b></div>"
        for status, color, label in STATUS_LEGEND
    )
    with st.container(border=True):
        st.markdown(
            f"""
            <p class="card-title">Status summary</p>
            <div class="big-num">{total} <span>Applications</span></div>
            <div class="seg-bar">{segments}</div>
            <div class="legend-grid">{legend}</div>
            """,
            unsafe_allow_html=True,
        )


def render_dashboard_charts(items: list[TrackedApplication], counts: dict[str, int]) -> None:
    total = counts.get("total", 0)
    left, right = st.columns([2.1, 1], gap="medium")
    with left:
        _job_statistics(items)
    with right:
        rate = round(_funnel_counts(items)["Interview"] / total * 100) if total else 0
        with st.container(border=True):
            st.markdown(
                f"""
                <p class="card-title">Response rate</p>
                <div class="big-num">{rate}% <span>reached interview</span></div>
                """,
                unsafe_allow_html=True,
            )
        _status_summary(counts, total)
