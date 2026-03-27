"""
app.py — Netflix EDA Streamlit Dashboard entry point.

Run from the streamlit_app/ folder:
    streamlit run app.py

The dataset is resolved relative to THIS file's location so the path works
both locally (streamlit_app/../dataset/) and on Streamlit Cloud.
"""

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Netflix EDA Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.utils.theme import inject_css
from src.utils.data_loader import load_data
from src.components.sidebar import render_sidebar
from src.components.ui_components import page_header
from src.tabs import tab_overview, tab_content, tab_geography, tab_timeline, tab_deepdive, tab_recommender

inject_css()

# ── Resolve dataset path relative to app.py itself ───────────────────────────
# Works locally AND on Streamlit Cloud — never depends on cwd
THIS_DIR  = Path(__file__).parent          # .../streamlit_app/
DATA_PATH = str(THIS_DIR.parent / "dataset" / "netflix_titles.csv")

try:
    with st.spinner("Loading Netflix data…"):
        df_raw = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"❌ Dataset not found at `{DATA_PATH}`")
    st.info(
        "**Setup:**\n"
        "1. Download from [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)\n"
        "2. Place `netflix_titles.csv` in the `dataset/` folder at the repo root\n"
        "3. Redeploy / refresh"
    )
    st.stop()

df, data_path = render_sidebar(df_raw, DATA_PATH)

# If user manually changed path in sidebar, reload with new path
if data_path != DATA_PATH:
    try:
        df_raw = load_data(data_path)
        from src.utils.data_loader import apply_filters
    except FileNotFoundError:
        st.error(f"❌ File not found: `{data_path}`")
        st.stop()

page_header(len(df))

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊  Overview",
    "🎭  Content",
    "🌍  Geography",
    "📅  Timeline",
    "🔍  Deep Dive",
    "🔮  Recommender",
])

with tab1: tab_overview.render(df)
with tab2: tab_content.render(df)
with tab3: tab_geography.render(df)
with tab4: tab_timeline.render(df)
with tab5: tab_deepdive.render(df, df_raw)
with tab6: tab_recommender.render(df_raw)
