"""
theme.py — Netflix colour palette, Plotly layout defaults, and CSS injection.
"""

import plotly.graph_objects as go
import streamlit as st

# ── Palette ──────────────────────────────────────────────────────────────────
NETFLIX_RED  = "#E50914"
DARK_BG      = "#141414"
CARD_BG      = "#1f1f1f"
CARD2_BG     = "#2a2a2a"
TEXT_PRIMARY = "#FFFFFF"
TEXT_MUTED   = "#B3B3B3"
ACCENT_BLUE  = "#3498db"
ACCENT_GOLD  = "#F5C518"


# ── Plotly helper ─────────────────────────────────────────────────────────────
def apply_netflix_theme(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply the Netflix dark theme to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_PRIMARY, family="'Helvetica Neue', Arial"),
        title=dict(text=title, font=dict(size=14, color=TEXT_PRIMARY)),
        margin=dict(t=50, l=10, r=10, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#2d2d2d", linecolor="#3d3d3d", tickcolor="#666"),
        yaxis=dict(gridcolor="#2d2d2d", linecolor="#3d3d3d", tickcolor="#666"),
    )
    return fig


# ── CSS injection ─────────────────────────────────────────────────────────────
def inject_css() -> None:
    """Inject global Netflix-dark CSS into the Streamlit page."""
    st.markdown(f"""
    <style>
      html, body, [class*="css"] {{
          background-color: {DARK_BG} !important;
          color: {TEXT_PRIMARY} !important;
          font-family: 'Helvetica Neue', Arial, sans-serif;
      }}
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
      hr {{
          border: none;
          border-top: 1px solid #2a2a2a !important;
          margin: 20px 0 !important;
      }}
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
      .stPlotlyChart {{ border-radius: 10px; overflow: hidden; }}
      ::-webkit-scrollbar {{ width: 6px; }}
      ::-webkit-scrollbar-track {{ background: {DARK_BG}; }}
      ::-webkit-scrollbar-thumb {{ background: #444; border-radius: 3px; }}
      .stDataFrame {{ border: 1px solid #2a2a2a !important; }}
      [data-testid="metric-container"] {{
          background: {CARD_BG};
          border: 1px solid #2d2d2d;
          border-radius: 10px;
          padding: 16px !important;
      }}
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
