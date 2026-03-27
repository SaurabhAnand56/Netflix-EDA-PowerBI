"""
tab_content.py — Tab 2: Rating breakdown, TV seasons, boxplot, avg duration.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.utils.theme import (
    NETFLIX_RED, ACCENT_BLUE, TEXT_MUTED,
    apply_netflix_theme,
)


def render(df) -> None:
    """Render the Content tab."""

    col_a, col_b = st.columns(2)

    # ── Rating vs Type grouped bar ────────────────────────────────────────────
    with col_a:
        top_r = df["rating"].value_counts().head(8).index
        rt    = (
            df[df["rating"].isin(top_r)]
            .groupby(["rating", "type"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            rt, x="rating", y="count", color="type",
            barmode="group",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
        )
        fig = apply_netflix_theme(fig, "Ratings: Movies vs TV Shows")
        st.plotly_chart(fig, use_container_width=True)

    # ── TV Show seasons ───────────────────────────────────────────────────────
    with col_b:
        shows = df[df["type"] == "TV Show"].dropna(subset=["seasons"])
        sc    = shows["seasons"].value_counts().sort_index().head(10)
        fig   = go.Figure(go.Bar(
            x=sc.index.astype(int), y=sc.values,
            marker=dict(
                color=sc.values,
                colorscale=[[0, "#1a3a5c"], [1, ACCENT_BLUE]],
                showscale=False,
            ),
            text=sc.values, textposition="outside",
            textfont=dict(color=TEXT_MUTED),
        ))
        fig = apply_netflix_theme(fig, "TV Shows by Number of Seasons")
        fig.update_xaxes(title="Seasons", tickmode="linear")
        st.plotly_chart(fig, use_container_width=True)

    # ── Box plot: duration by rating ──────────────────────────────────────────
    movies = df[df["type"] == "Movie"].dropna(subset=["duration_min"])
    top6   = movies["rating"].value_counts().head(6).index
    fig    = px.box(
        movies[movies["rating"].isin(top6)],
        x="rating", y="duration_min",
        color="rating",
        color_discrete_sequence=px.colors.sequential.Reds,
        points="outliers",
    )
    fig = apply_netflix_theme(fig, "Movie Duration Spread by Rating")
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="Duration (minutes)")
    st.plotly_chart(fig, use_container_width=True)

    # ── Avg duration by rating ────────────────────────────────────────────────
    avg = movies[movies["rating"].isin(top6)].groupby("rating")["duration_min"].mean().sort_values(ascending=False)
    fig = px.bar(
        x=avg.index, y=avg.values,
        color=avg.values,
        color_continuous_scale=["#5a0009", NETFLIX_RED, "#F5C518"],
        text=[f"{v:.0f}m" for v in avg.values],
    )
    fig = apply_netflix_theme(fig, "Average Movie Duration by Rating")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_traces(textposition="outside", textfont=dict(color=TEXT_MUTED))
    st.plotly_chart(fig, use_container_width=True)
