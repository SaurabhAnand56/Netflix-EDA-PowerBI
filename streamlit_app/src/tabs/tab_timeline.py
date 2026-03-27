"""
tab_timeline.py — Tab 4: Growth line chart, release year bar, monthly heatmap.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.utils.theme import (
    NETFLIX_RED, CARD_BG, TEXT_PRIMARY, TEXT_MUTED, ACCENT_BLUE,
    apply_netflix_theme,
)


def render(df) -> None:
    """Render the Timeline tab."""

    # ── Growth line chart ─────────────────────────────────────────────────────
    yearly = (
        df.dropna(subset=["year_added"])
        .groupby(["year_added", "type"])
        .size()
        .reset_index(name="count")
    )
    yearly = yearly[yearly["year_added"] >= 2010]

    fig = px.line(
        yearly, x="year_added", y="count", color="type",
        markers=True,
        color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
    )
    fig.update_traces(line_width=2.5, marker_size=7)
    for trace in fig.data:
        trace.update(fill="tozeroy", fillcolor=(
            "rgba(229,9,20,0.12)" if trace.name == "Movie"
            else "rgba(52,152,219,0.12)"
        ))
    fig = apply_netflix_theme(fig, "Netflix Content Library Growth Over Time")
    fig.update_layout(xaxis_title="Year Added", yaxis_title="Titles Added",
                      hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    # ── Release year bar ──────────────────────────────────────────────────────
    with col_a:
        yr  = df["release_year"].value_counts().sort_index()
        yr  = yr[yr.index >= 2000]
        fig = go.Figure(go.Bar(
            x=yr.index, y=yr.values,
            marker=dict(color=NETFLIX_RED, opacity=0.85),
        ))
        fig = apply_netflix_theme(fig, "Titles by Release Year (2000+)")
        st.plotly_chart(fig, use_container_width=True)

    # ── Per-year grouped bar ──────────────────────────────────────────────────
    with col_b:
        yt  = (
            df.dropna(subset=["year_added"])
            .groupby(["year_added", "type"])
            .size()
            .reset_index(name="count")
        )
        yt  = yt[yt["year_added"] >= 2015]
        fig = px.bar(
            yt, x="year_added", y="count", color="type",
            barmode="group",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
        )
        fig = apply_netflix_theme(fig, "Titles Added Per Year (2015+)")
        st.plotly_chart(fig, use_container_width=True)

    # ── Monthly heatmap ───────────────────────────────────────────────────────
    heat  = df.dropna(subset=["year_added", "month_added"])
    heat  = heat[heat["year_added"] >= 2016]
    pivot = heat.groupby(["year_added", "month_added"]).size().unstack(fill_value=0)
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot.columns = [MONTHS[int(m) - 1] for m in pivot.columns]

    fig = px.imshow(
        pivot,
        color_continuous_scale=[[0,"#0d0d0d"],[0.4,"#5a0009"],[0.7,NETFLIX_RED],[1,"#ff6b6b"]],
        text_auto=True, aspect="auto",
    )
    fig.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_PRIMARY),
        title="Monthly Titles Added to Netflix (Heatmap)",
        margin=dict(t=50, b=40, l=60, r=20),
        xaxis_title="Month", yaxis_title="Year",
        coloraxis_colorbar=dict(title="Titles"),
    )
    fig.update_traces(textfont=dict(color=TEXT_PRIMARY, size=11))
    st.plotly_chart(fig, use_container_width=True)
