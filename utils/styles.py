"""
Custom CSS styles and UI helper functions for the BrightChamps Lead Funnel AI Agent.
Provides consistent dark-themed styling across all pages.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#667EEA",
    "secondary": "#764BA2",
    "success": "#48BB78",
    "warning": "#ECC94B",
    "danger": "#FC8181",
    "info": "#63B3ED",
    "purple": "#9F7AEA",
    "pink": "#F687B3",
    "teal": "#4FD1C5",
    "orange": "#ED8936",
}

CHART_COLORS = [
    "#667EEA", "#764BA2", "#48BB78", "#ECC94B", "#FC8181",
    "#63B3ED", "#F687B3", "#68D391", "#9F7AEA", "#ED8936",
    "#4FD1C5", "#FBD38D",
]

FUNNEL_COLORS = ["#667EEA", "#9F7AEA", "#ECC94B", "#ED8936", "#48BB78"]

# ---------------------------------------------------------------------------
# Plotly base layout (dark theme)
# ---------------------------------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA", family="Inter, sans-serif", size=13),
    margin=dict(l=40, r=40, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#FAFAFA")),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
)


def get_plotly_layout(**overrides):
    """Return a copy of the base Plotly layout merged with *overrides*."""
    layout = {**PLOTLY_LAYOUT}
    layout.update(overrides)
    return layout


# ---------------------------------------------------------------------------
# Custom CSS injection
# ---------------------------------------------------------------------------
def inject_custom_css():
    """Inject premium custom CSS into the Streamlit app."""
    st.markdown(
        """
        <style>
        /* ── Google Font ────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* ── Hide Streamlit chrome ──────────────────────────── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* ── Page wrapper ───────────────────────────────────── */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px;
        }

        /* ── Metric cards ───────────────────────────────────── */
        .metric-card {
            background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
            border: 1px solid rgba(102,126,234,0.2);
            border-radius: 16px;
            padding: 24px 28px;
            margin: 8px 0;
            transition: transform 0.25s cubic-bezier(.4,0,.2,1),
                        box-shadow 0.25s cubic-bezier(.4,0,.2,1);
        }
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(102,126,234,0.18);
        }

        .metric-label {
            font-size: 0.78rem;
            font-weight: 600;
            color: #A0AEC0;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 6px;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.1;
        }

        .metric-value.gradient {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-value.green  { color: #48BB78; }
        .metric-value.red    { color: #FC8181; }
        .metric-value.amber  { color: #ECC94B; }
        .metric-value.blue   { color: #63B3ED; }
        .metric-value.white  { color: #FAFAFA; }

        .metric-delta {
            font-size: 0.8rem;
            margin-top: 6px;
            color: #A0AEC0;
        }

        /* ── Section header ─────────────────────────────────── */
        .section-header {
            font-size: 1.35rem;
            font-weight: 700;
            margin: 2.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(102,126,234,0.3);
            color: #FAFAFA;
        }

        /* ── Styled container ───────────────────────────────── */
        .styled-container {
            background: rgba(26,31,46,0.5);
            border: 1px solid rgba(102,126,234,0.12);
            border-radius: 14px;
            padding: 22px;
            margin: 14px 0;
        }

        /* ── Hero header ────────────────────────────────────── */
        .hero-header {
            text-align: center;
            padding: 2rem 1rem 1.5rem 1rem;
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 50%, #FC8181 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #A0AEC0;
            font-weight: 400;
        }

        /* ── Sidebar styling ────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0E1117 0%, #161B26 100%);
            border-right: 1px solid rgba(102,126,234,0.15);
        }
        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem;
        }

        /* ── Badge / tag ────────────────────────────────────── */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .badge-hot   { background: rgba(252,129,129,0.18); color: #FC8181; }
        .badge-warm  { background: rgba(236,201,75,0.18);  color: #ECC94B; }
        .badge-cold  { background: rgba(99,179,237,0.18);  color: #63B3ED; }
        .badge-green { background: rgba(72,187,120,0.18);  color: #48BB78; }

        /* ── Divider ────────────────────────────────────────── */
        .styled-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(102,126,234,0.3), transparent);
            margin: 2rem 0;
        }

        /* ── Custom scrollbar ───────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0E1117; }
        ::-webkit-scrollbar-thumb { background: #667EEA; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #764BA2; }

        /* ── Tabs ───────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
        }

        /* ── Expander ───────────────────────────────────────── */
        .streamlit-expanderHeader {
            font-weight: 600;
            font-size: 0.95rem;
        }

        /* ── Info box ───────────────────────────────────────── */
        .info-box {
            background: rgba(102,126,234,0.08);
            border-left: 4px solid #667EEA;
            border-radius: 0 10px 10px 0;
            padding: 16px 20px;
            margin: 12px 0;
            font-size: 0.9rem;
            color: #CBD5E0;
        }

        /* ── Leak callout ───────────────────────────────────── */
        .leak-callout {
            background: linear-gradient(135deg, rgba(252,129,129,0.08) 0%, rgba(237,137,54,0.08) 100%);
            border: 1px solid rgba(252,129,129,0.25);
            border-radius: 14px;
            padding: 24px;
            margin: 16px 0;
            text-align: center;
        }
        .leak-callout .leak-amount {
            font-size: 2.8rem;
            font-weight: 800;
            color: #FC8181;
        }
        .leak-callout .leak-label {
            font-size: 0.9rem;
            color: #A0AEC0;
            margin-top: 4px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Reusable UI components
# ---------------------------------------------------------------------------

def render_metric_card(label: str, value: str, delta: str = "", color: str = "gradient"):
    """Render a styled metric card.

    Parameters
    ----------
    label : str
        Small uppercase label above the value.
    value : str
        Main number / text to display.
    delta : str, optional
        Subtitle below the value.
    color : str
        CSS class for the value: "gradient", "green", "red", "amber", "blue", "white".
    """
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {color}">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(text: str):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def render_hero(title: str, subtitle: str = ""):
    """Render a gradient hero header."""
    sub_html = f'<div class="hero-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="hero-header">
            <div class="hero-title">{title}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_divider():
    """Render a subtle gradient divider."""
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)


def render_info_box(text: str):
    """Render an info callout box."""
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)


def format_inr(amount: float) -> str:
    """Format a number in Indian Rupee lakhs / crores for readability."""
    if abs(amount) >= 1_00_00_000:
        return f"₹{amount / 1_00_00_000:,.1f} Cr"
    elif abs(amount) >= 1_00_000:
        return f"₹{amount / 1_00_000:,.1f}L"
    else:
        return f"₹{amount:,.0f}"


def format_inr_full(amount: float) -> str:
    """Format a number in Indian Rupee with commas (no abbreviation)."""
    return f"₹{amount:,.0f}"
