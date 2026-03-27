"""
app.py — Entry point for the Netflix EDA Streamlit Dashboard.

Run:
    streamlit run app.py
"""

import streamlit as st

# ── Page config — MUST be first Streamlit call ────────────────────────────────
st.set_page_config(
    page_title="Netflix EDA Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal imports (after set_page_config) ──────────────────────────────────
from src.utils.theme import inject_css
from src.utils.data_loader import load_data
from src.components.sidebar import render_sidebar
from src.components.ui_components import page_header
from src.tabs import (
    tab_overview,
    tab_content,
    tab_geography,
    tab_timeline,
    tab_deepdive,
    tab_recommender,
)

# ── Inject global CSS ─────────────────────────────────────────────────────────
inject_css()

# ── Load raw data (sidebar provides the path) ─────────────────────────────────
# We need df_raw before the sidebar can populate filter options,
# so we load it with the default path first, then the sidebar may override it.
_DEFAULT_PATH = "../dataset/netflix_titles.csv"

try:
    df_raw = load_data(_DEFAULT_PATH)
except FileNotFoundError:
    df_raw = None

# ── Sidebar (filters + author card) ──────────────────────────────────────────
if df_raw is not None:
    df_filtered, data_path = render_sidebar(df_raw)

    # If the user changed the path, reload
    if data_path != _DEFAULT_PATH:
        try:
            df_raw = load_data(data_path)
            from src.utils.data_loader import apply_filters
            # Re-apply filters with new data — sidebar re-renders on next run
        except FileNotFoundError:
            st.error(f"❌ File not found: `{data_path}`")
            st.stop()
else:
    # No data yet — show setup instructions
    st.error("❌ Dataset not found at `../dataset/netflix_titles.csv`")
    st.info(
        "**Setup:**\n"
        "1. Download the dataset from "
        "[Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)\n"
        "2. Place `netflix_titles.csv` inside the `dataset/` folder at the repo root\n"
        "3. Refresh this page"
    )
    st.stop()

# ── Page header ───────────────────────────────────────────────────────────────
page_header(len(df_filtered))

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊  Overview",
    "🎭  Content",
    "🌍  Geography",
    "📅  Timeline",
    "🔍  Deep Dive",
    "🔮  Recommender",
])

with tab1:
    tab_overview.render(df_filtered)

with tab2:
    tab_content.render(df_filtered)

with tab3:
    tab_geography.render(df_filtered)

with tab4:
    tab_timeline.render(df_filtered)

with tab5:
    tab_deepdive.render(df_filtered, df_raw)

with tab6:
    tab_recommender.render(df_raw)
