"""
tab_overview.py — Tab 1: KPI cards, donut chart, top genres, ratings, duration.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from collections import Counter

from src.utils.theme import (
    NETFLIX_RED, DARK_BG, CARD_BG, CARD2_BG,
    TEXT_PRIMARY, TEXT_MUTED, ACCENT_BLUE, ACCENT_GOLD,
    apply_netflix_theme,
)
from src.components.ui_components import kpi_card


def _genre_counter(df: pd.DataFrame) -> Counter:
    all_g = []
    for row in df["listed_in"].dropna():
        all_g.extend([g.strip() for g in row.split(",")])
    return Counter(all_g)


def render(df: pd.DataFrame) -> None:
    """Render the Overview tab."""

    # ── KPI row ───────────────────────────────────────────────────────────────
    total    = len(df)
    n_movies = (df["type"] == "Movie").sum()
    n_shows  = (df["type"] == "TV Show").sum()

    kpis = [
        (f"{total:,}",    "Total Titles",   None),
        (f"{n_movies:,}", "Movies",         f"{n_movies/total*100:.0f}%"),
        (f"{n_shows:,}",  "TV Shows",       f"{n_shows/total*100:.0f}%"),
        (str(df[df["country"] != "Unknown"]["country"].nunique()), "Countries", None),
        (str(df["rating"].nunique()), "Ratings", None),
    ]
    cols = st.columns(5)
    for col, (val, lbl, dlt) in zip(cols, kpis):
        col.markdown(kpi_card(val, lbl, dlt), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Donut + Top genres ────────────────────────────────────────────────────
    col_a, col_b = st.columns([1, 2])

    with col_a:
        tc = df["type"].value_counts()
        fig = go.Figure(go.Pie(
            labels=tc.index, values=tc.values,
            hole=0.62,
            marker=dict(
                colors=[NETFLIX_RED, ACCENT_BLUE],
                line=dict(color=DARK_BG, width=3),
            ),
            textfont=dict(color=TEXT_PRIMARY, size=12),
        ))
        fig.add_annotation(
            text=f"<b>{total:,}</b><br>TITLES",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=TEXT_PRIMARY),
        )
        fig.update_layout(
            title="Content Mix", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_PRIMARY),
            margin=dict(t=50, b=20, l=20, r=20),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.05),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        gc    = _genre_counter(df)
        top_g = pd.Series(gc).sort_values(ascending=False).head(12)
        fig   = go.Figure(go.Bar(
            x=top_g.values[::-1], y=top_g.index[::-1],
            orientation="h",
            marker=dict(
                color=top_g.values[::-1],
                colorscale=[[0, "#5a0009"], [0.5, NETFLIX_RED], [1, "#ff6b6b"]],
                showscale=False,
            ),
            text=top_g.values[::-1], textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=11),
        ))
        fig = apply_netflix_theme(fig, "Top 12 Genres")
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    # ── Ratings + Duration histogram ──────────────────────────────────────────
    col_c, col_d = st.columns(2)

    with col_c:
        rc  = df["rating"].value_counts().head(10)
        fig = px.bar(
            x=rc.index, y=rc.values,
            color=rc.values,
            color_continuous_scale=["#5a0009", NETFLIX_RED, "#ff6b6b"],
        )
        fig = apply_netflix_theme(fig, "Content Ratings Distribution")
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        fig.update_traces(
            text=rc.values, textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        mv = df[df["type"] == "Movie"].dropna(subset=["duration_min"])
        fig = go.Figure(go.Histogram(
            x=mv["duration_min"], nbinsx=40,
            marker=dict(color=NETFLIX_RED, line=dict(color=DARK_BG, width=0.5)),
            opacity=0.9,
        ))
        mean_d, med_d = mv["duration_min"].mean(), mv["duration_min"].median()
        fig.add_vline(x=mean_d, line_dash="dash", line_color=ACCENT_GOLD,
                      annotation_text=f"Mean {mean_d:.0f}m",
                      annotation_font_color=ACCENT_GOLD)
        fig.add_vline(x=med_d, line_dash="dot", line_color="#2ecc71",
                      annotation_text=f"Median {med_d:.0f}m",
                      annotation_font_color="#2ecc71")
        fig = apply_netflix_theme(fig, "Movie Duration Distribution (minutes)")
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)
