"""
tab_geography.py — Tab 3: World choropleth, top countries, Movie vs TV stacked.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.utils.theme import (
    NETFLIX_RED, DARK_BG, CARD_BG, ACCENT_BLUE, TEXT_MUTED,
    apply_netflix_theme,
)


def render(df) -> None:
    """Render the Geography tab."""

    country_counts = (
        df[df["country"] != "Unknown"]["country"]
        .value_counts()
        .reset_index()
    )
    country_counts.columns = ["country", "count"]

    # ── Choropleth world map ──────────────────────────────────────────────────
    fig_map = px.choropleth(
        country_counts.head(50),
        locations="country",
        locationmode="country names",
        color="count",
        color_continuous_scale=["#1a0004", "#5a0009", NETFLIX_RED, "#ff6b6b"],
        hover_name="country",
        hover_data={"count": True},
    )
    fig_map.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
        geo=dict(
            bgcolor=DARK_BG, landcolor="#1e1e1e",
            oceancolor="#0d1117", showocean=True,
            coastlinecolor="#333", countrycolor="#2d2d2d", showframe=False,
        ),
        font=dict(color="#fff"),
        title="Global Content Distribution",
        coloraxis_colorbar=dict(
            title="Titles", tickcolor="#B3B3B3",
            title_font=dict(color="#B3B3B3"),
        ),
        margin=dict(t=50, b=0, l=0, r=0),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col_a, col_b = st.columns(2)

    # ── Top 10 horizontal bar ─────────────────────────────────────────────────
    with col_a:
        top10 = country_counts.head(10)
        fig   = go.Figure(go.Bar(
            x=top10["count"][::-1],
            y=top10["country"][::-1],
            orientation="h",
            marker=dict(
                color=top10["count"][::-1],
                colorscale=[[0, "#5a0009"], [1, NETFLIX_RED]],
                showscale=False,
            ),
            text=top10["count"][::-1], textposition="outside",
            textfont=dict(color=TEXT_MUTED),
        ))
        fig = apply_netflix_theme(fig, "Top 10 Content-Producing Countries")
        st.plotly_chart(fig, use_container_width=True)

    # ── Country × Type stacked bar ────────────────────────────────────────────
    with col_b:
        top8 = country_counts.head(8)["country"].tolist()
        ct   = (
            df[df["country"].isin(top8)]
            .groupby(["country", "type"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            ct, x="country", y="count", color="type",
            barmode="stack",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
        )
        fig = apply_netflix_theme(fig, "Top Countries: Movies vs TV Shows")
        fig.update_xaxes(tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)
