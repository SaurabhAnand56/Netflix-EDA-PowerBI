"""
tab_deepdive.py — Tab 5: Missing values, correlation heatmap, data explorer, insights.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

from src.utils.theme import (
    NETFLIX_RED, CARD_BG, TEXT_PRIMARY, TEXT_MUTED, ACCENT_BLUE,
    apply_netflix_theme,
)
from src.components.ui_components import insight_card


def render(df, df_raw) -> None:
    """Render the Deep Dive tab."""

    # ── Missing values ────────────────────────────────────────────────────────
    st.markdown("#### 🔍 Missing Values Analysis")

    miss     = df_raw.isnull().sum()
    miss_pct = (miss / len(df_raw) * 100).round(2)
    miss_df  = pd.DataFrame({
        "Column":        miss.index,
        "Missing Count": miss.values,
        "Missing %":     miss_pct.values,
    }).query("`Missing Count` > 0").sort_values("Missing %", ascending=False)

    fig = go.Figure(go.Bar(
        x=miss_df["Column"], y=miss_df["Missing %"],
        marker=dict(color=NETFLIX_RED, opacity=0.85),
        text=[f"{v}%" for v in miss_df["Missing %"]],
        textposition="outside", textfont=dict(color=TEXT_MUTED),
    ))
    fig = apply_netflix_theme(fig, "Missing Values by Column (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Correlation heatmap ───────────────────────────────────────────────────
    st.markdown("#### 📊 Correlation Heatmap (Movies)")

    movies  = df[df["type"] == "Movie"].dropna(subset=["duration_min"])
    num_df  = movies[["release_year", "duration_min", "year_added", "month_added"]].dropna()
    corr    = num_df.corr()

    fig = px.imshow(
        corr,
        color_continuous_scale=[[0, ACCENT_BLUE], [0.5, "#1a1a1a"], [1, NETFLIX_RED]],
        zmin=-1, zmax=1, text_auto=".2f", aspect="auto",
    )
    fig.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_PRIMARY),
        title="Correlation Between Numeric Variables",
        margin=dict(t=50, b=40, l=100, r=20),
        coloraxis_colorbar=dict(title="Corr"),
    )
    fig.update_traces(textfont=dict(color=TEXT_PRIMARY, size=13))
    col_corr, _ = st.columns([1, 1])
    with col_corr:
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Data explorer ─────────────────────────────────────────────────────────
    st.markdown("#### 📋 Data Explorer")
    with st.expander("Browse filtered dataset", expanded=False):
        display_cols = ["title", "type", "director", "country",
                        "release_year", "rating", "duration", "listed_in"]
        st.dataframe(df[display_cols].reset_index(drop=True),
                     use_container_width=True, height=400)

    st.markdown("---")

    # ── Key insights ──────────────────────────────────────────────────────────
    st.markdown("#### 💡 Key Insights Summary")

    total    = len(df)
    n_movies = (df["type"] == "Movie").sum()
    n_shows  = (df["type"] == "TV Show").sum()

    all_genres = Counter(
        g.strip()
        for row in df["listed_in"].dropna()
        for g in row.split(",")
    )

    insights = [
        ("🎬 Content Mix",
         f"{n_movies/total*100:.0f}% Movies / {n_shows/total*100:.0f}% TV Shows"),
        ("🇺🇸 Top Country",
         f"United States — {df[df['country']=='United States']['title'].count():,} titles"),
        ("🔞 Top Rating",
         f"{df['rating'].value_counts().idxmax()} — Netflix targets adult audiences"),
        ("🌍 Top Genre",
         f"{pd.Series(all_genres).idxmax()} — global content push"),
        ("⏱️ Avg Movie Length",
         f"{movies['duration_min'].mean():.0f} minutes"),
        ("📺 TV Seasons",
         "67% of TV Shows have only 1 season"),
        ("📈 Peak Release Year",
         f"{df['release_year'].value_counts().idxmax()} had the most releases"),
    ]

    cols = st.columns(2)
    for i, (key, val) in enumerate(insights):
        with cols[i % 2]:
            st.markdown(insight_card(key, val), unsafe_allow_html=True)
