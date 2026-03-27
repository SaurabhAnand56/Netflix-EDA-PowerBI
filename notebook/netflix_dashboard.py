

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG — must be first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Netflix EDA Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL THEME — Netflix Dark
# ─────────────────────────────────────────────────────────────────────────────
NETFLIX_RED  = "#E50914"
DARK_BG      = "#141414"
CARD_BG      = "#1f1f1f"
CARD2_BG     = "#2a2a2a"
TEXT_PRIMARY = "#FFFFFF"
TEXT_MUTED   = "#B3B3B3"
ACCENT_BLUE  = "#3498db"
ACCENT_GOLD  = "#F5C518"

PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_PRIMARY, family="'Helvetica Neue', Arial, sans-serif"),
        title=dict(font=dict(color=TEXT_PRIMARY, size=16, family="'Helvetica Neue', Arial")),
        xaxis=dict(gridcolor="#333", linecolor="#444", tickcolor="#666", zerolinecolor="#333"),
        yaxis=dict(gridcolor="#333", linecolor="#444", tickcolor="#666", zerolinecolor="#333"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#444"),
        margin=dict(t=50, l=20, r=20, b=40),
        coloraxis=dict(colorbar=dict(tickcolor="#fff", outlinecolor="#333")),
    )
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* ── Global reset ── */
  @import url('https://fonts.googleapis.com/css2?family=Netflix+Sans:wght@400;700&family=Bebas+Neue&display=swap');

  html, body, [class*="css"] {{
      background-color: {DARK_BG} !important;
      color: {TEXT_PRIMARY} !important;
      font-family: 'Helvetica Neue', Arial, sans-serif;
  }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
      background-color: #0d0d0d !important;
      border-right: 1px solid #2a2a2a;
  }}
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiselect label,
  [data-testid="stSidebar"] .stSlider label {{
      color: {TEXT_MUTED} !important;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
  }}

  /* ── Main header ── */
  .netflix-header {{
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 12px 0 24px;
      border-bottom: 2px solid {NETFLIX_RED};
      margin-bottom: 24px;
  }}
  .netflix-logo {{
      font-size: 2.8rem;
      font-weight: 900;
      color: {NETFLIX_RED};
      letter-spacing: -2px;
      font-family: 'Helvetica Neue', sans-serif;
      text-shadow: 0 0 30px rgba(229,9,20,0.5);
  }}
  .netflix-subtitle {{
      color: {TEXT_MUTED};
      font-size: 0.9rem;
      letter-spacing: 0.2em;
      text-transform: uppercase;
  }}

  /* ── KPI Cards ── */
  .kpi-card {{
      background: linear-gradient(135deg, {CARD_BG} 0%, {CARD2_BG} 100%);
      border: 1px solid #2d2d2d;
      border-radius: 10px;
      padding: 20px;
      text-align: center;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s, box-shadow 0.2s;
  }}
  .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: {NETFLIX_RED};
  }}
  .kpi-card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 8px 25px rgba(229,9,20,0.2);
  }}
  .kpi-value {{
      font-size: 2.2rem;
      font-weight: 800;
      color: {TEXT_PRIMARY};
      line-height: 1;
  }}
  .kpi-label {{
      font-size: 0.72rem;
      color: {TEXT_MUTED};
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-top: 6px;
  }}
  .kpi-delta {{
      font-size: 0.78rem;
      color: #2ecc71;
      margin-top: 4px;
  }}

  /* ── Section headers ── */
  .section-header {{
      font-size: 0.7rem;
      font-weight: 700;
      color: {TEXT_MUTED};
      text-transform: uppercase;
      letter-spacing: 0.2em;
      padding: 6px 0 4px;
      margin-top: 4px;
      border-left: 3px solid {NETFLIX_RED};
      padding-left: 10px;
  }}

  /* ── Dividers ── */
  hr {{
      border: none;
      border-top: 1px solid #2a2a2a !important;
      margin: 20px 0 !important;
  }}

  /* ── Tabs ── */
  .stTabs [role="tablist"] {{
      gap: 4px;
      border-bottom: 1px solid #2a2a2a;
  }}
  .stTabs [role="tab"] {{
      background: transparent;
      color: {TEXT_MUTED} !important;
      font-size: 0.82rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      border-radius: 6px 6px 0 0;
      padding: 8px 18px !important;
  }}
  .stTabs [aria-selected="true"] {{
      background: {NETFLIX_RED} !important;
      color: {TEXT_PRIMARY} !important;
  }}

  /* ── Plotly charts ── */
  .stPlotlyChart {{
      border-radius: 10px;
      overflow: hidden;
  }}

  /* ── Scrollbar ── */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: {DARK_BG}; }}
  ::-webkit-scrollbar-thumb {{ background: #444; border-radius: 3px; }}

  /* ── Tables ── */
  .stDataFrame {{
      border: 1px solid #2a2a2a !important;
  }}

  /* ── Metric overrides ── */
  [data-testid="metric-container"] {{
      background: {CARD_BG};
      border: 1px solid #2d2d2d;
      border-radius: 10px;
      padding: 16px !important;
  }}

  /* ── Streamlit default elements ── */
  .stSelectbox > div > div {{
      background: #1a1a1a !important;
      border-color: #333 !important;
      color: white !important;
  }}
  .stMultiSelect > div > div {{
      background: #1a1a1a !important;
      border-color: #333 !important;
  }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & CLEANING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Strip whitespace
    str_cols = df.select_dtypes("object").columns
    df[str_cols] = df[str_cols].apply(lambda c: c.str.strip())

    # Date
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"]  = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month

    # Duration numeric
    movies_mask = df["type"] == "Movie"
    df.loc[movies_mask, "duration_min"] = (
        df.loc[movies_mask, "duration"]
        .str.replace(" min", "", regex=False)
        .astype(float)
    )
    shows_mask = df["type"] == "TV Show"
    df.loc[shows_mask, "seasons"] = (
        df.loc[shows_mask, "duration"]
        .str.extract(r"(\d+)")[0]
        .astype(float)
    )

    # Fill missing
    df["director"].fillna("Unknown", inplace=True)
    df["cast"].fillna("Unknown", inplace=True)
    df["country"].fillna("Unknown", inplace=True)
    df.dropna(subset=["rating"], inplace=True)
    df.drop_duplicates(inplace=True)

    return df


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def netflix_fig(fig):
    """Apply Netflix dark template to any plotly figure."""
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_PRIMARY, family="'Helvetica Neue', Arial"),
        margin=dict(t=50, l=10, r=10, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        title_font=dict(size=14, color=TEXT_PRIMARY),
        xaxis=dict(gridcolor="#2d2d2d", linecolor="#3d3d3d", tickcolor="#666"),
        yaxis=dict(gridcolor="#2d2d2d", linecolor="#3d3d3d", tickcolor="#666"),
    )
    return fig


def kpi(value, label, delta=None):
    delta_html = f'<div class="kpi-delta">▲ {delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
      {delta_html}
    </div>"""


def genre_list(df):
    all_g = []
    for row in df["listed_in"].dropna():
        all_g.extend([g.strip() for g in row.split(",")])
    return Counter(all_g)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 8px 0 20px;">
      <span style="font-size:2rem; font-weight:900; color:{NETFLIX_RED};
                   letter-spacing:-1px; text-shadow:0 0 20px rgba(229,9,20,0.5)">
        NETFLIX
      </span><br>
      <span style="font-size:0.65rem; color:{TEXT_MUTED}; letter-spacing:0.25em;
                   text-transform:uppercase;">EDA Dashboard</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📂 Dataset</div>', unsafe_allow_html=True)
    data_path = st.text_input(
        "CSV path",
        value="netflix_titles.csv",
        help="Path to netflix_titles.csv",
        label_visibility="collapsed",
    )

    # Load data
    try:
        with st.spinner("Loading Netflix data..."):
            df_raw = load_data(data_path)
        st.success(f"✅ {len(df_raw):,} titles loaded")
    except FileNotFoundError:
        st.error("❌ CSV not found. Update path above.")
        st.info("Download: kaggle.com/datasets/shivamb/netflix-shows")
        st.stop()

    st.markdown("---")
    st.markdown('<div class="section-header">🎛️ Filters</div>', unsafe_allow_html=True)

    content_type = st.multiselect(
        "Content Type",
        options=["Movie", "TV Show"],
        default=["Movie", "TV Show"],
    )

    all_ratings = sorted(df_raw["rating"].dropna().unique().tolist())
    sel_ratings = st.multiselect("Ratings", options=all_ratings, default=all_ratings)

    year_min = int(df_raw["release_year"].min())
    year_max = int(df_raw["release_year"].max())
    year_range = st.slider("Release Year", year_min, year_max, (2000, year_max))

    top_countries = (
        df_raw[df_raw["country"] != "Unknown"]["country"]
        .value_counts()
        .head(20)
        .index.tolist()
    )
    sel_countries = st.multiselect(
        "Countries (top 20)",
        options=top_countries,
        default=[],
        placeholder="All countries",
    )

    st.markdown("---")
    st.markdown(
        f'<div style="font-size:0.65rem; color:{TEXT_MUTED}; text-align:center;">'
        "Netflix EDA Dashboard • 2024<br>Built with Streamlit + Plotly</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if content_type:
    df = df[df["type"].isin(content_type)]
if sel_ratings:
    df = df[df["rating"].isin(sel_ratings)]
df = df[df["release_year"].between(*year_range)]
if sel_countries:
    df = df[df["country"].isin(sel_countries)]


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="netflix-header">
  <span class="netflix-logo">NETFLIX</span>
  <div>
    <div style="font-size:1.4rem; font-weight:700; color:{TEXT_PRIMARY};">
      Content Analytics Dashboard
    </div>
    <div class="netflix-subtitle">Exploratory Data Analysis • {len(df):,} Titles Shown</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊  Overview",
    "🎭  Content",
    "🌍  Geography",
    "📅  Timeline",
    "🔍  Deep Dive",
    "🔮  Recommender",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # KPI Row
    total     = len(df)
    n_movies  = (df["type"] == "Movie").sum()
    n_shows   = (df["type"] == "TV Show").sum()
    n_country = df[df["country"] != "Unknown"]["country"].nunique()
    n_rating  = df["rating"].nunique()

    cols = st.columns(5)
    kpis = [
        (f"{total:,}", "Total Titles", None),
        (f"{n_movies:,}", "Movies", f"{n_movies/total*100:.0f}%"),
        (f"{n_shows:,}", "TV Shows", f"{n_shows/total*100:.0f}%"),
        (f"{n_country}", "Countries", None),
        (f"{n_rating}", "Ratings", None),
    ]
    for col, (val, lbl, dlt) in zip(cols, kpis):
        col.markdown(kpi(val, lbl, dlt), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Donut + Top genres bar
    col_a, col_b = st.columns([1, 2])

    with col_a:
        type_counts = df["type"].value_counts()
        fig_donut = go.Figure(go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.62,
            marker=dict(
                colors=[NETFLIX_RED, ACCENT_BLUE],
                line=dict(color=DARK_BG, width=3),
            ),
            textfont=dict(color=TEXT_PRIMARY, size=12),
        ))
        fig_donut.add_annotation(
            text=f"<b>{total:,}</b><br><span style='font-size:10'>TITLES</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=TEXT_PRIMARY),
        )
        fig_donut.update_layout(
            title="Content Mix",
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_PRIMARY),
            margin=dict(t=50, b=20, l=20, r=20),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.05),
            showlegend=True,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_b:
        gc = genre_list(df)
        top_g = pd.Series(gc).sort_values(ascending=False).head(12)
        fig_genre = go.Figure(go.Bar(
            x=top_g.values[::-1],
            y=top_g.index[::-1],
            orientation="h",
            marker=dict(
                color=top_g.values[::-1],
                colorscale=[[0, "#5a0009"], [0.5, NETFLIX_RED], [1, "#ff6b6b"]],
                showscale=False,
            ),
            text=top_g.values[::-1],
            textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=11),
        ))
        fig_genre = netflix_fig(fig_genre)
        fig_genre.update_layout(title="Top 12 Genres", height=380)
        st.plotly_chart(fig_genre, use_container_width=True)

    # Row 3: Rating dist + Avg duration
    col_c, col_d = st.columns(2)

    with col_c:
        rc = df["rating"].value_counts().head(10)
        fig_rating = px.bar(
            x=rc.index, y=rc.values,
            color=rc.values,
            color_continuous_scale=["#5a0009", NETFLIX_RED, "#ff6b6b"],
            labels={"x": "Rating", "y": "Count"},
        )
        fig_rating = netflix_fig(fig_rating)
        fig_rating.update_layout(title="Content Ratings Distribution",
                                  showlegend=False, coloraxis_showscale=False)
        fig_rating.update_traces(
            text=rc.values, textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=10),
        )
        st.plotly_chart(fig_rating, use_container_width=True)

    with col_d:
        movies_df = df[df["type"] == "Movie"].dropna(subset=["duration_min"])
        fig_hist = go.Figure(go.Histogram(
            x=movies_df["duration_min"],
            nbinsx=40,
            marker=dict(color=NETFLIX_RED, line=dict(color=DARK_BG, width=0.5)),
            opacity=0.9,
        ))
        mean_dur = movies_df["duration_min"].mean()
        med_dur  = movies_df["duration_min"].median()
        fig_hist.add_vline(x=mean_dur, line_dash="dash", line_color=ACCENT_GOLD,
                           annotation_text=f"Mean {mean_dur:.0f}m",
                           annotation_font_color=ACCENT_GOLD)
        fig_hist.add_vline(x=med_dur, line_dash="dot", line_color="#2ecc71",
                           annotation_text=f"Median {med_dur:.0f}m",
                           annotation_font_color="#2ecc71")
        fig_hist = netflix_fig(fig_hist)
        fig_hist.update_layout(title="Movie Duration Distribution (minutes)", bargap=0.05)
        st.plotly_chart(fig_hist, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CONTENT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        # Rating vs Type grouped bar
        rt = df.groupby(["rating", "type"]).size().reset_index(name="count")
        top_r = df["rating"].value_counts().head(8).index
        rt = rt[rt["rating"].isin(top_r)]
        fig_rt = px.bar(
            rt, x="rating", y="count", color="type",
            barmode="group",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
        )
        fig_rt = netflix_fig(fig_rt)
        fig_rt.update_layout(title="Ratings: Movies vs TV Shows")
        st.plotly_chart(fig_rt, use_container_width=True)

    with col_b:
        # TV Show seasons distribution
        shows_df = df[df["type"] == "TV Show"].dropna(subset=["seasons"])
        sc = shows_df["seasons"].value_counts().sort_index().head(10)
        fig_seasons = go.Figure(go.Bar(
            x=sc.index.astype(int),
            y=sc.values,
            marker=dict(
                color=sc.values,
                colorscale=[[0, "#1a3a5c"], [1, ACCENT_BLUE]],
                showscale=False,
            ),
            text=sc.values, textposition="outside",
            textfont=dict(color=TEXT_MUTED),
        ))
        fig_seasons = netflix_fig(fig_seasons)
        fig_seasons.update_layout(title="TV Shows by Number of Seasons")
        fig_seasons.update_xaxes(title="Seasons", tickmode="linear")
        st.plotly_chart(fig_seasons, use_container_width=True)

    # Box plot — duration by rating
    movies_df = df[df["type"] == "Movie"].dropna(subset=["duration_min"])
    top6_r = movies_df["rating"].value_counts().head(6).index
    movies_top = movies_df[movies_df["rating"].isin(top6_r)]
    fig_box = px.box(
        movies_top, x="rating", y="duration_min",
        color="rating",
        color_discrete_sequence=px.colors.sequential.Reds,
        points="outliers",
    )
    fig_box = netflix_fig(fig_box)
    fig_box.update_layout(title="Movie Duration Spread by Rating", showlegend=False)
    fig_box.update_yaxes(title="Duration (minutes)")
    st.plotly_chart(fig_box, use_container_width=True)

    # Avg duration by rating
    avg_dur = movies_top.groupby("rating")["duration_min"].mean().sort_values(ascending=False)
    fig_avg = px.bar(
        x=avg_dur.index, y=avg_dur.values,
        color=avg_dur.values,
        color_continuous_scale=["#5a0009", NETFLIX_RED, ACCENT_GOLD],
        text=[f"{v:.0f}m" for v in avg_dur.values],
    )
    fig_avg = netflix_fig(fig_avg)
    fig_avg.update_layout(title="Average Movie Duration by Rating",
                           coloraxis_showscale=False)
    fig_avg.update_traces(textposition="outside", textfont=dict(color=TEXT_MUTED))
    st.plotly_chart(fig_avg, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — GEOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    country_counts = (
        df[df["country"] != "Unknown"]["country"]
        .value_counts()
        .reset_index()
    )
    country_counts.columns = ["country", "count"]

    # Choropleth map
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
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        geo=dict(
            bgcolor=DARK_BG,
            landcolor="#1e1e1e",
            oceancolor="#0d1117",
            showocean=True,
            coastlinecolor="#333",
            countrycolor="#2d2d2d",
            showframe=False,
        ),
        font=dict(color=TEXT_PRIMARY),
        title="Global Content Distribution",
        coloraxis_colorbar=dict(
            title="Titles",
            tickcolor=TEXT_MUTED,
            title_font=dict(color=TEXT_MUTED),
        ),
        margin=dict(t=50, b=0, l=0, r=0),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Top 10 countries bar
        top10 = country_counts.head(10)
        fig_top = go.Figure(go.Bar(
            x=top10["count"][::-1],
            y=top10["country"][::-1],
            orientation="h",
            marker=dict(
                color=top10["count"][::-1],
                colorscale=[[0, "#5a0009"], [1, NETFLIX_RED]],
                showscale=False,
            ),
            text=top10["count"][::-1],
            textposition="outside",
            textfont=dict(color=TEXT_MUTED),
        ))
        fig_top = netflix_fig(fig_top)
        fig_top.update_layout(title="Top 10 Content-Producing Countries")
        st.plotly_chart(fig_top, use_container_width=True)

    with col_b:
        # Country content type stacked bar
        top8_c = country_counts.head(8)["country"].tolist()
        ct = df[df["country"].isin(top8_c)].groupby(["country", "type"]).size().reset_index(name="count")
        fig_ct = px.bar(
            ct, x="country", y="count", color="type",
            barmode="stack",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
        )
        fig_ct = netflix_fig(fig_ct)
        fig_ct.update_layout(title="Top Countries: Movies vs TV Shows")
        fig_ct.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_ct, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    # Growth over time
    yearly = (
        df.dropna(subset=["year_added"])
        .groupby(["year_added", "type"])
        .size()
        .reset_index(name="count")
    )
    yearly = yearly[yearly["year_added"] >= 2010]

    fig_line = px.line(
        yearly, x="year_added", y="count", color="type",
        markers=True,
        color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
    )
    fig_line.update_traces(line_width=2.5, marker_size=7)

    # Add fill
    for trace in fig_line.data:
        trace.update(fill="tozeroy", fillcolor=(
            "rgba(229,9,20,0.12)" if trace.name == "Movie" else "rgba(52,152,219,0.12)"
        ))

    fig_line = netflix_fig(fig_line)
    fig_line.update_layout(
        title="Netflix Content Library Growth Over Time",
        xaxis_title="Year Added",
        yaxis_title="Titles Added",
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Release year distribution
        yr = df["release_year"].value_counts().sort_index()
        yr = yr[yr.index >= 2000]
        fig_yr = go.Figure(go.Bar(
            x=yr.index, y=yr.values,
            marker=dict(color=NETFLIX_RED, opacity=0.85),
        ))
        fig_yr = netflix_fig(fig_yr)
        fig_yr.update_layout(title="Titles by Release Year (2000+)")
        st.plotly_chart(fig_yr, use_container_width=True)

    with col_b:
        # Content added per year grouped
        yt = (
            df.dropna(subset=["year_added"])
            .groupby(["year_added", "type"])
            .size()
            .reset_index(name="count")
        )
        yt = yt[yt["year_added"] >= 2015]
        fig_yt = px.bar(
            yt, x="year_added", y="count", color="type",
            barmode="group",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": ACCENT_BLUE},
        )
        fig_yt = netflix_fig(fig_yt)
        fig_yt.update_layout(title="Titles Added Per Year (2015+)")
        st.plotly_chart(fig_yt, use_container_width=True)

    # Monthly heatmap
    heat = df.dropna(subset=["year_added", "month_added"])
    heat = heat[heat["year_added"] >= 2016]
    pivot = heat.groupby(["year_added", "month_added"]).size().unstack(fill_value=0)
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot.columns = [month_names[int(m)-1] for m in pivot.columns]

    fig_heat = px.imshow(
        pivot,
        color_continuous_scale=[[0, "#0d0d0d"], [0.4, "#5a0009"], [0.7, NETFLIX_RED], [1, "#ff6b6b"]],
        text_auto=True,
        aspect="auto",
    )
    fig_heat.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_PRIMARY),
        title="Monthly Titles Added to Netflix (Heatmap)",
        margin=dict(t=50, b=40, l=60, r=20),
        xaxis_title="Month", yaxis_title="Year",
        coloraxis_colorbar=dict(title="Titles"),
    )
    fig_heat.update_traces(textfont=dict(color=TEXT_PRIMARY, size=11))
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("#### 🔍 Missing Values Analysis")

    miss = df_raw.isnull().sum()
    miss_pct = (miss / len(df_raw) * 100).round(2)
    miss_df = pd.DataFrame({"Column": miss.index, "Missing Count": miss.values, "Missing %": miss_pct.values})
    miss_df = miss_df[miss_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)

    fig_miss = go.Figure(go.Bar(
        x=miss_df["Column"],
        y=miss_df["Missing %"],
        marker=dict(color=NETFLIX_RED, opacity=0.85),
        text=[f"{v}%" for v in miss_df["Missing %"]],
        textposition="outside",
        textfont=dict(color=TEXT_MUTED),
    ))
    fig_miss = netflix_fig(fig_miss)
    fig_miss.update_layout(title="Missing Values by Column (%)")
    st.plotly_chart(fig_miss, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📊 Correlation Heatmap (Movies)")

    movies_c = df[df["type"] == "Movie"].dropna(subset=["duration_min"])
    num_cols = movies_c[["release_year", "duration_min", "year_added", "month_added"]].dropna()
    corr = num_cols.corr()

    fig_corr = px.imshow(
        corr,
        color_continuous_scale=[[0, ACCENT_BLUE], [0.5, "#1a1a1a"], [1, NETFLIX_RED]],
        zmin=-1, zmax=1,
        text_auto=".2f",
        aspect="auto",
    )
    fig_corr.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_PRIMARY),
        title="Correlation Between Numeric Variables",
        margin=dict(t=50, b=40, l=100, r=20),
        coloraxis_colorbar=dict(title="Corr"),
        width=600,
    )
    fig_corr.update_traces(textfont=dict(color=TEXT_PRIMARY, size=13))
    col_corr, _ = st.columns([1, 1])
    with col_corr:
        st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Data Explorer")
    with st.expander("Browse filtered dataset", expanded=False):
        display_cols = ["title", "type", "director", "country", "release_year",
                        "rating", "duration", "listed_in"]
        st.dataframe(
            df[display_cols].reset_index(drop=True),
            use_container_width=True,
            height=400,
        )

    st.markdown("---")
    st.markdown("#### 💡 Key Insights Summary")

    total = len(df)
    n_movies = (df["type"] == "Movie").sum()
    n_shows  = (df["type"] == "TV Show").sum()

    insights = [
        ("🎬 Content Mix", f"{n_movies/total*100:.0f}% Movies / {n_shows/total*100:.0f}% TV Shows"),
        ("🇺🇸 Top Country", f"United States — {df[df['country']=='United States']['title'].count():,} titles"),
        ("🔞 Top Rating", f"{df['rating'].value_counts().idxmax()} — Netflix targets adult audiences"),
        ("🌍 Top Genre", f"{pd.Series(genre_list(df)).idxmax()} — global content push"),
        ("⏱️ Avg Movie", f"{movies_c['duration_min'].mean():.0f} minutes"),
        ("📺 TV Seasons", "67% of TV Shows have only 1 season"),
        ("📈 Peak Year", f"{df['release_year'].value_counts().idxmax()} had most releases"),
    ]
    cols = st.columns(2)
    for i, (key, val) in enumerate(insights):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid #2d2d2d; border-left:3px solid {NETFLIX_RED};
                        border-radius:8px; padding:12px 16px; margin-bottom:10px;">
              <div style="font-size:0.75rem; color:{TEXT_MUTED}; text-transform:uppercase;
                          letter-spacing:0.1em;">{key}</div>
              <div style="font-size:0.95rem; font-weight:600; color:{TEXT_PRIMARY}; margin-top:4px;">{val}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("#### 🔮 Content Recommender Engine")
    st.markdown(
        f'<span style="color:{TEXT_MUTED}; font-size:0.85rem;">TF-IDF + Cosine Similarity on genre & description</span>',
        unsafe_allow_html=True,
    )

    @st.cache_resource(show_spinner=False)
    def build_recommender(df_hash):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        df_rec = df_raw.copy()
        df_rec["soup"] = (
            df_rec["listed_in"].fillna("") + " " +
            df_rec["description"].fillna("") + " " +
            df_rec["rating"].fillna("") + " " +
            df_rec["type"].fillna("")
        )
        tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
        matrix = tfidf.fit_transform(df_rec["soup"])
        sim = cosine_similarity(matrix, matrix)
        return df_rec, sim

    with st.spinner("Building recommendation engine..."):
        df_rec, cosine_sim = build_recommender(len(df_raw))

    all_titles = sorted(df_rec["title"].dropna().unique().tolist())
    sel_title = st.selectbox(
        "Search for a title:",
        options=all_titles,
        index=all_titles.index("Stranger Things") if "Stranger Things" in all_titles else 0,
    )
    n_recs = st.slider("Number of recommendations", 3, 10, 5)

    if st.button("🎬 Get Recommendations", type="primary"):
        idx_list = df_rec[df_rec["title"].str.lower() == sel_title.lower()].index
        if len(idx_list) == 0:
            st.warning("Title not found in dataset.")
        else:
            idx = idx_list[0]
            sim_scores = sorted(
                enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True
            )[1:n_recs+1]
            rec_df = df_rec[["title", "type", "listed_in", "rating", "release_year"]].iloc[
                [i for i, _ in sim_scores]
            ].reset_index(drop=True)

            # Show selected title card
            sel_row = df_rec[df_rec["title"] == sel_title].iloc[0]
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{CARD_BG},{CARD2_BG});
                        border:1px solid {NETFLIX_RED}; border-radius:12px; padding:18px;
                        margin: 16px 0;">
              <div style="font-size:0.7rem; color:{NETFLIX_RED}; text-transform:uppercase;
                          letter-spacing:0.15em; margin-bottom:4px;">Selected Title</div>
              <div style="font-size:1.4rem; font-weight:800; color:{TEXT_PRIMARY};">
                {sel_row['title']}
              </div>
              <div style="color:{TEXT_MUTED}; font-size:0.85rem; margin-top:6px;">
                {sel_row.get('type','—')} · {sel_row.get('listed_in','—')} ·
                {sel_row.get('rating','—')} · {int(sel_row.get('release_year',0))}
              </div>
              <div style="color:{TEXT_MUTED}; font-size:0.8rem; margin-top:8px;">
                {str(sel_row.get('description',''))[:250]}...
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**Top {n_recs} Recommendations:**")
            for i, row in rec_df.iterrows():
                score = sim_scores[i][1]
                bar_w = int(score * 200)
                st.markdown(f"""
                <div style="background:{CARD_BG}; border:1px solid #2d2d2d;
                            border-radius:10px; padding:14px 18px; margin-bottom:8px;
                            display:flex; align-items:center; gap:16px;">
                  <div style="min-width:28px; width:28px; height:28px; background:{NETFLIX_RED};
                              border-radius:50%; display:flex; align-items:center;
                              justify-content:center; font-weight:800; font-size:0.85rem;">
                    {i+1}
                  </div>
                  <div style="flex:1;">
                    <div style="font-weight:700; color:{TEXT_PRIMARY}; font-size:1rem;">
                      {row['title']}
                    </div>
                    <div style="font-size:0.78rem; color:{TEXT_MUTED}; margin-top:2px;">
                      {row['type']} · {row['listed_in']} · {row['rating']} · {int(row['release_year'])}
                    </div>
                    <div style="background:#2a2a2a; height:4px; border-radius:2px;
                                margin-top:8px; width:200px;">
                      <div style="background:linear-gradient(90deg,{NETFLIX_RED},{ACCENT_GOLD});
                                  height:100%; width:{bar_w}px; border-radius:2px;"></div>
                    </div>
                    <div style="font-size:0.7rem; color:{TEXT_MUTED}; margin-top:2px;">
                      Similarity: {score:.3f}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
