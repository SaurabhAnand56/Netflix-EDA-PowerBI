"""
tab_recommender.py — Tab 6: TF-IDF content recommender.
"""

import streamlit as st
import pandas as pd

from src.utils.theme import NETFLIX_RED, CARD_BG, CARD2_BG, TEXT_PRIMARY, TEXT_MUTED
from src.components.ui_components import rec_card


@st.cache_resource(show_spinner=False)
def _build_model(n_rows: int):
    """Build (and cache) TF-IDF matrix + cosine similarity. Re-built only when row count changes."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    return None, None   # placeholder — populated in render()


def render(df_raw: pd.DataFrame) -> None:
    """Render the Recommender tab."""

    st.markdown("#### 🔮 Content Recommender Engine")
    st.markdown(
        f'<span style="color:{TEXT_MUTED}; font-size:0.85rem;">'
        "TF-IDF + Cosine Similarity on genre, description, rating, and type"
        "</span>",
        unsafe_allow_html=True,
    )

    # ── Build model ───────────────────────────────────────────────────────────
    @st.cache_resource(show_spinner=False)
    def build_recommender(_key: int):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        df = df_raw.copy()
        df["soup"] = (
            df["listed_in"].fillna("") + " " +
            df["description"].fillna("") + " " +
            df["rating"].fillna("") + " " +
            df["type"].fillna("")
        )
        tfidf  = TfidfVectorizer(stop_words="english", max_features=5000)
        matrix = tfidf.fit_transform(df["soup"])
        sim    = cosine_similarity(matrix, matrix)
        return df, sim

    with st.spinner("Building recommendation engine..."):
        df_rec, cosine_sim = build_recommender(len(df_raw))

    # ── UI ────────────────────────────────────────────────────────────────────
    all_titles = sorted(df_rec["title"].dropna().unique().tolist())
    default_idx = (
        all_titles.index("Stranger Things")
        if "Stranger Things" in all_titles else 0
    )

    sel_title = st.selectbox("Search for a title:", options=all_titles,
                              index=default_idx)
    n_recs    = st.slider("Number of recommendations", 3, 10, 5)

    if st.button("🎬 Get Recommendations", type="primary"):
        idx_list = df_rec[df_rec["title"].str.lower() == sel_title.lower()].index

        if len(idx_list) == 0:
            st.warning("Title not found in dataset.")
            return

        idx        = idx_list[0]
        sim_scores = sorted(
            enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True
        )[1 : n_recs + 1]

        rec_indices = [i for i, _ in sim_scores]
        rec_df      = df_rec[["title", "type", "listed_in", "rating", "release_year"]].iloc[
            rec_indices
        ].reset_index(drop=True)

        # Selected title card
        sel_row = df_rec[df_rec["title"] == sel_title].iloc[0]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{CARD_BG},{CARD2_BG});
                    border:1px solid {NETFLIX_RED}; border-radius:12px;
                    padding:18px; margin:16px 0;">
          <div style="font-size:0.7rem; color:{NETFLIX_RED}; text-transform:uppercase;
                      letter-spacing:0.15em; margin-bottom:4px;">Selected Title</div>
          <div style="font-size:1.4rem; font-weight:800; color:{TEXT_PRIMARY};">
            {sel_row['title']}
          </div>
          <div style="color:{TEXT_MUTED}; font-size:0.85rem; margin-top:6px;">
            {sel_row.get('type','—')} · {sel_row.get('listed_in','—')} ·
            {sel_row.get('rating','—')} · {int(sel_row.get('release_year', 0))}
          </div>
          <div style="color:{TEXT_MUTED}; font-size:0.8rem; margin-top:8px;">
            {str(sel_row.get('description',''))[:260]}…
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**Top {n_recs} Recommendations:**")
        for rank, (_, row) in enumerate(rec_df.iterrows(), start=1):
            score = sim_scores[rank - 1][1]
            st.markdown(
                rec_card(
                    rank,
                    row["title"],
                    row["type"],
                    row["listed_in"],
                    row["rating"],
                    int(row["release_year"]),
                    score,
                ),
                unsafe_allow_html=True,
            )
