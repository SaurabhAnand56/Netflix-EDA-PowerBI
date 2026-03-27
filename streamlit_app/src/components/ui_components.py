"""
ui_components.py — Reusable HTML/Streamlit UI building blocks.
"""

import streamlit as st
from src.utils.theme import NETFLIX_RED, CARD_BG, CARD2_BG, TEXT_PRIMARY, TEXT_MUTED


def kpi_card(value: str, label: str, delta: str = None) -> str:
    """Return an HTML string for a KPI card."""
    delta_html = f'<div class="kpi-delta">▲ {delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
      {delta_html}
    </div>"""


def section_header(text: str) -> None:
    """Render a styled section header in the sidebar or main area."""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def insight_card(key: str, value: str) -> str:
    """Return an HTML string for a key-insight card."""
    return f"""
    <div style="background:{CARD_BG}; border:1px solid #2d2d2d;
                border-left:3px solid {NETFLIX_RED}; border-radius:8px;
                padding:12px 16px; margin-bottom:10px;">
      <div style="font-size:0.75rem; color:{TEXT_MUTED}; text-transform:uppercase;
                  letter-spacing:0.1em;">{key}</div>
      <div style="font-size:0.95rem; font-weight:600; color:{TEXT_PRIMARY};
                  margin-top:4px;">{value}</div>
    </div>"""


def rec_card(rank: int, title: str, content_type: str, genres: str,
             rating: str, year: int, score: float) -> str:
    """Return an HTML string for a recommendation result card."""
    bar_w = int(score * 200)
    return f"""
    <div style="background:{CARD_BG}; border:1px solid #2d2d2d; border-radius:10px;
                padding:14px 18px; margin-bottom:8px;
                display:flex; align-items:center; gap:16px;">
      <div style="min-width:28px; width:28px; height:28px; background:{NETFLIX_RED};
                  border-radius:50%; display:flex; align-items:center;
                  justify-content:center; font-weight:800; font-size:0.85rem;
                  color:white;">{rank}</div>
      <div style="flex:1;">
        <div style="font-weight:700; color:{TEXT_PRIMARY}; font-size:1rem;">{title}</div>
        <div style="font-size:0.78rem; color:{TEXT_MUTED}; margin-top:2px;">
          {content_type} · {genres} · {rating} · {year}
        </div>
        <div style="background:#2a2a2a; height:4px; border-radius:2px;
                    margin-top:8px; width:200px;">
          <div style="background:linear-gradient(90deg,{NETFLIX_RED},#F5C518);
                      height:100%; width:{bar_w}px; border-radius:2px;"></div>
        </div>
        <div style="font-size:0.7rem; color:{TEXT_MUTED}; margin-top:2px;">
          Similarity: {score:.3f}
        </div>
      </div>
    </div>"""


def page_header(filtered_count: int) -> None:
    """Render the top Netflix dashboard header."""
    st.markdown(f"""
    <div class="netflix-header">
      <span class="netflix-logo">NETFLIX</span>
      <div>
        <div style="font-size:1.4rem; font-weight:700; color:{TEXT_PRIMARY};">
          Content Analytics Dashboard
        </div>
        <div class="netflix-subtitle">
          Exploratory Data Analysis • {filtered_count:,} Titles Shown
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
