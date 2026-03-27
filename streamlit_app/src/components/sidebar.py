"""
src/components/sidebar.py
Sidebar: author profile card (GitHub photo), dataset path, all filters.
"""

import streamlit as st
from src.utils.theme import NETFLIX_RED, TEXT_PRIMARY, TEXT_MUTED
from src.utils.data_loader import apply_filters
from src.components.ui_components import section_header as section_label

AUTHOR = {
    "name":     "Saurabh Anand",
    "linkedin": "https://www.linkedin.com/in/saurabhanand56/",
    "github":   "https://github.com/SaurabhAnand56",
    "avatar":   "https://github.com/SaurabhAnand56.png",
}


def _author_card() -> None:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a0004,#2a0009);
                border:1px solid {NETFLIX_RED}44;border-radius:12px;
                padding:16px;margin-bottom:16px;text-align:center;">
      <img src="{AUTHOR['avatar']}"
           style="width:58px;height:58px;border-radius:50%;object-fit:cover;
                  display:block;margin:0 auto 10px;
                  border:2px solid {NETFLIX_RED};
                  box-shadow:0 0 18px rgba(229,9,20,0.45);"
           onerror="this.style.display='none'" />
      <div style="font-size:0.95rem;font-weight:700;color:{TEXT_PRIMARY};">
        {AUTHOR['name']}
      </div>
      <div style="font-size:0.65rem;color:{TEXT_MUTED};text-transform:uppercase;
                  letter-spacing:0.18em;margin-bottom:12px;">Data Analyst</div>
      <div style="display:flex;justify-content:center;gap:8px;">
        <a href="{AUTHOR['linkedin']}" target="_blank"
           style="background:#0A66C2;color:white;text-decoration:none;
                  padding:5px 11px;border-radius:6px;font-size:0.68rem;font-weight:600;">
          in  LinkedIn
        </a>
        <a href="{AUTHOR["github"]}" target="_blank"
           style="display:inline-flex; align-items:center; gap:5px;
                  background:#24292e; color:white; text-decoration:none;
                  padding:5px 10px; border-radius:6px; font-size:0.7rem;
                  font-weight:600; letter-spacing:0.05em;">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="white">
            <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0
                     0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0
                     0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38
                     13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5
                     4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37
                     3.37 0 0 0 9 18.13V22"/>
          </svg>
          GitHub
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(df_raw, DATA_PATH: str = "../dataset/netflix_titles.csv"):
    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div style="text-align:center;padding:6px 0 14px;">
          <span style="font-size:1.9rem;font-weight:900;color:{NETFLIX_RED};
                       letter-spacing:-1px;text-shadow:0 0 18px rgba(229,9,20,0.5);">
            NETFLIX
          </span><br>
          <span style="font-size:0.6rem;color:{TEXT_MUTED};letter-spacing:0.28em;
                       text-transform:uppercase;">EDA Dashboard</span>
        </div>
        """, unsafe_allow_html=True)

        _author_card()

        # Dataset path
        section_label("📂 Dataset")
        data_path = st.text_input(
            "path", value=DATA_PATH,
            label_visibility="collapsed",
            help="Path to netflix_titles.csv",
        )

        st.markdown("---")
        section_label("🎛️ Filters")

        content_type = st.multiselect(
            "Content Type", ["Movie", "TV Show"], default=["Movie", "TV Show"],
        )
        all_ratings = sorted(df_raw["rating"].dropna().unique().tolist())
        sel_ratings = st.multiselect("Ratings", all_ratings, default=all_ratings)

        y_min = int(df_raw["release_year"].min())
        y_max = int(df_raw["release_year"].max())
        year_range = st.slider("Release Year", y_min, y_max, (2000, y_max))

        top_countries = (
            df_raw[df_raw["country"] != "Unknown"]["country"]
            .value_counts().head(20).index.tolist()
        )
        sel_countries = st.multiselect(
            "Countries (top 20)", top_countries, default=[], placeholder="All",
        )

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:0.6rem;color:{TEXT_MUTED};text-align:center;line-height:1.8;">
          Netflix EDA Dashboard · v3.0<br>
          Streamlit + Plotly + scikit-learn<br>
          <a href="{AUTHOR['github']}/netflix-eda-dashboard"
             target="_blank" style="color:{NETFLIX_RED};text-decoration:none;">
            ⭐ Star on GitHub
          </a>
        </div>
        """, unsafe_allow_html=True)

    filtered = apply_filters(df_raw, content_type, sel_ratings, year_range, sel_countries)
    return filtered, data_path
