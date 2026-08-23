"""Dashboard charts: status donut, sector, channel, and funnel."""

from __future__ import annotations

from collections import Counter

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from job_search.models.schemas import TrackedApplication, TrackerChannel, TrackerStatus
from job_search.ui.theme import COLORS, STATUS_LEGEND, plotly_layout


def _chart_card(title: str, fig: go.Figure, height: int = 260) -> None:
    fig.update_layout(**plotly_layout(height=height))
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _horizontal_bar(
    labels: list[str],
    values: list[int],
    color: str,
    *,
    show_values: bool = True,
) -> go.Figure:
    text = [str(value) for value in values] if show_values else None
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker={"color": color, "line": {"width": 0}},
            text=text,
            textposition="outside",
            textfont={"color": "#e5e7eb", "size": 12},
            hovertemplate="%{y}: %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending",
            "tickfont": {"color": "#d1d5db", "size": 12},
            "gridcolor": "rgba(0,0,0,0)",
        },
        xaxis={
            "showgrid": True,
            "gridcolor": "#30363d",
            "tickfont": {"color": "#9ca3af"},
            "zeroline": False,
        },
        margin={"l": 8, "r": 36, "t": 8, "b": 8},
    )
    return fig


def _status_donut(counts: dict[str, int], total: int) -> go.Figure:
    labels: list[str] = []
    values: list[int] = []
    colors: list[str] = []
    for status, color, short_label in STATUS_LEGEND:
        value = counts.get(status.value, 0)
        if value <= 0:
            continue
        labels.append(short_label)
        values.append(value)
        colors.append(color)

    if not values:
        labels, values, colors = ["No data"], [1], ["#374151"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.62,
                marker={"colors": colors, "line": {"color": "#161b22", "width": 2}},
                textinfo="none",
                hovertemplate="%{label}: %{value}<extra></extra>",
                sort=False,
                showlegend=False,
            )
        ]
    )
    fig.update_layout(
        margin={"l": 8, "r": 8, "t": 8, "b": 8},
        showlegend=False,
        annotations=[
            {
                "text": (
                    f"{total}<br>"
                    "<span style='font-size:12px;color:#9ca3af'>applications</span>"
                ),
                "x": 0.5,
                "y": 0.5,
                "font": {"size": 22, "color": "#f3f4f6"},
                "showarrow": False,
            }
        ],
    )
    return fig


def _status_legend_html(counts: dict[str, int]) -> str:
    rows = "".join(
        f"""
        <div class="legend-row">
          <span class="legend-dot" style="background:{color};"></span>
          <span class="legend-label">{label}: {counts.get(status.value, 0)}</span>
        </div>
        """
        for status, color, label in STATUS_LEGEND
    )
    return f"""
    <style>
      .status-legend {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 10px;
        height: 220px;
        font-family: "Source Sans Pro", sans-serif;
        padding-left: 8px;
      }}
      .legend-row {{
        display: flex;
        align-items: center;
        gap: 10px;
      }}
      .legend-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
      }}
      .legend-label {{
        color: #d1d5db;
        font-size: 13px;
      }}
    </style>
    <div class="status-legend">{rows}</div>
    """


def _funnel_counts(items: list[TrackedApplication]) -> dict[str, int]:
    total = len(items)
    interview_plus = sum(
        1
        for item in items
        if item.status
        in (TrackerStatus.INTERVIEW, TrackerStatus.OFFER, TrackerStatus.HIRED)
    )
    offer_plus = sum(
        1 for item in items if item.status in (TrackerStatus.OFFER, TrackerStatus.HIRED)
    )
    hired = sum(1 for item in items if item.status == TrackerStatus.HIRED)
    return {
        "Applied": total,
        "Interview": interview_plus,
        "Offer": offer_plus,
        "Hired": hired,
    }


def render_dashboard_charts(items: list[TrackedApplication], counts: dict[str, int]) -> None:
    total = counts.get("total", 0)
    top_left, top_right = st.columns(2)
    with top_left:
        with st.container(border=True):
            st.markdown("**Status breakdown**")
            donut_col, legend_col = st.columns([1.35, 1])
            with donut_col:
                fig = _status_donut(counts, total)
                fig.update_layout(**plotly_layout(height=240))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with legend_col:
                components.html(_status_legend_html(counts), height=240)
    with top_right:
        sectors = Counter(item.sector.strip() or "Unspecified" for item in items)
        if sectors:
            labels = list(sectors.keys())
            values = list(sectors.values())
            _chart_card(
                "By sector",
                _horizontal_bar(labels, values, COLORS["sector_bar"]),
            )
        else:
            with st.container(border=True):
                st.markdown("**By sector**")
                st.caption("No applications yet.")

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        channels = Counter(
            (item.channel.value if item.channel else TrackerChannel.ONLINE.value)
            for item in items
        )
        if channels:
            labels = list(channels.keys())
            values = list(channels.values())
            _chart_card(
                "By channel",
                _horizontal_bar(labels, values, COLORS["channel_bar"]),
                height=240,
            )
        else:
            with st.container(border=True):
                st.markdown("**By channel**")
                st.caption("No applications yet.")
    with bottom_right:
        funnel = _funnel_counts(items)
        _chart_card(
            "Application funnel",
            _horizontal_bar(
                list(funnel.keys()),
                list(funnel.values()),
                COLORS["funnel_bar"],
            ),
            height=240,
        )
