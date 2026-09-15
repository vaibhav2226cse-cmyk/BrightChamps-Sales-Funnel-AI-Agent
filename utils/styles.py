"""
Custom CSS styles and UI helper functions for the BrightChamps Lead Funnel AI Agent.
Official BrightChamps Brand Design System — Clean Modern Light Theme with Signature Purple,
Multicolor Accents, Pill Buttons, and Crisp Card Elevators.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# BrightChamps Brand Color Palette
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#6929CA",         # BrightChamps Signature Electric Purple
    "primary_dark": "#4C1D95",    # Deep Royal Purple
    "primary_light": "#F5F3FF",   # Soft Lavender Tint
    "secondary": "#3B1F8C",       # Deep Brand Indigo
    "pink": "#E11D48",            # Champs Pink/Red
    "yellow": "#F59E0B",          # Star Gold / Amber
    "green": "#10B981",           # Emerald Green
    "teal": "#00D2A0",            # Confident Dot Teal
    "blue": "#2563EB",            # Unstoppable Dot Blue
    "orange": "#F97316",          # Sunset Orange
    "success": "#059669",         # Success Green
    "warning": "#D97706",         # Warning Amber
    "danger": "#DC2626",          # Danger Crimson
    "info": "#2563EB",            # Info Blue
    "dark_text": "#0F172A",       # Primary Headline Dark
    "sub_text": "#475569",        # Muted Slate
    "border": "#E2E8F0",          # Crisp Slate Border
    "card_bg": "#FFFFFF",         # Pure White Cards
    "page_bg": "#F8FAFC",         # Soft Cloud Canvas
}

CHART_COLORS = [
    "#6929CA",  # Signature Purple
    "#E11D48",  # Rose Pink
    "#F59E0B",  # Gold / Amber
    "#10B981",  # Emerald Green
    "#2563EB",  # Electric Blue
    "#F97316",  # Sunset Orange
    "#8B5CF6",  # Violet
    "#00D2A0",  # Mint / Teal
    "#0284C7",  # Sky Blue
    "#D946EF",  # Magenta
]

FUNNEL_COLORS = ["#6929CA", "#8B5CF6", "#F59E0B", "#F97316", "#10B981"]

# ---------------------------------------------------------------------------
# Plotly base layout (BrightChamps Clean Light Theme)
# ---------------------------------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#1E293B", family="Inter, system-ui, sans-serif", size=13),
    margin=dict(l=40, r=40, t=50, b=40),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E8F0",
        borderwidth=1,
        font=dict(color="#1E293B", size=12),
    ),
    xaxis=dict(
        gridcolor="#F1F5F9",
        zerolinecolor="#E2E8F0",
        tickfont=dict(color="#475569", size=11),
    ),
    yaxis=dict(
        gridcolor="#F1F5F9",
        zerolinecolor="#E2E8F0",
        tickfont=dict(color="#475569", size=11),
    ),
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
    """Inject BrightChamps branded custom CSS into the Streamlit app."""
    st.markdown(
        """
        <style>
        /* ── Google Fonts ────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        html, body {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
            color: #0F172A;
        }

        /* ── Protect Streamlit Material Icon ligatures ─────────────── */
        [data-testid*="Icon"],
        [data-testid*="Icon"] *,
        [class*="material-symbols"],
        [class*="material-icons"],
        [data-testid="stExpanderToggleIcon"],
        [data-testid="stExpanderToggleIcon"] * {
            font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons", sans-serif !important;
        }

        /* ── Clean Background ────────────────────────────────────── */
        .stApp {
            background-color: #F8FAFC !important;
        }

        /* ── Hide Streamlit chrome ───────────────────────────────── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* ── Page wrapper ────────────────────────────────────────── */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1240px;
        }

        /* ── Top Promo Banner ────────────────────────────────────── */
        .bc-promo-banner {
            background: linear-gradient(90deg, #6929CA 0%, #7C3AED 50%, #6320EE 100%);
            color: #FFFFFF;
            text-align: center;
            padding: 8px 16px;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 14px rgba(105, 41, 202, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        .bc-promo-banner .pill-code {
            background: rgba(255,255,255,0.2);
            padding: 2px 10px;
            border-radius: 20px;
            border: 1px dashed rgba(255,255,255,0.6);
            font-size: 0.8rem;
        }

        /* ── Hero Header ─────────────────────────────────────────── */
        .hero-header {
            text-align: center;
            padding: 1.8rem 1rem 1.4rem 1rem;
            margin-bottom: 1.8rem;
            background: #FFFFFF;
            border-radius: 20px;
            border: 1px solid #EDE9FE;
            box-shadow: 0 10px 30px -5px rgba(105, 41, 202, 0.08);
            position: relative;
            overflow: hidden;
        }
        .hero-header::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #6929CA 0%, #E11D48 30%, #F59E0B 60%, #10B981 100%);
        }
        .hero-eyebrow {
            font-size: 0.82rem;
            font-weight: 800;
            color: #6929CA;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0.5rem;
        }
        .hero-title {
            font-size: 2.3rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.2;
            margin-bottom: 0.6rem;
            letter-spacing: -0.5px;
        }
        .hero-title .dot-yellow { color: #F59E0B; }
        .hero-title .dot-green  { color: #00D2A0; }
        .hero-title .dot-blue   { color: #2563EB; }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #475569;
            font-weight: 500;
            max-width: 700px;
            margin: 0 auto;
        }

        /* ── Metric Cards ────────────────────────────────────────── */
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: 3.5px solid #6929CA;
            border-radius: 16px;
            padding: 22px 24px;
            margin: 8px 0;
            box-shadow: 0 4px 18px -2px rgba(105, 41, 202, 0.06);
            transition: all 0.25s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 28px -4px rgba(105, 41, 202, 0.16);
            border-top-color: #E11D48;
        }
        .metric-label {
            font-size: 0.78rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 1.1px;
            margin-bottom: 6px;
        }
        .metric-value {
            font-size: 2.05rem;
            font-weight: 800;
            line-height: 1.1;
            color: #0F172A;
        }
        .metric-value.gradient {
            background: linear-gradient(135deg, #6929CA 0%, #E11D48 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-value.purple { color: #6929CA; }
        .metric-value.green  { color: #059669; }
        .metric-value.red    { color: #DC2626; }
        .metric-value.amber  { color: #D97706; }
        .metric-value.blue   { color: #2563EB; }
        .metric-value.white  { color: #0F172A; }

        .metric-delta {
            font-size: 0.82rem;
            margin-top: 6px;
            color: #64748B;
            font-weight: 500;
        }

        /* ── Section Header ──────────────────────────────────────── */
        .section-header {
            font-size: 1.35rem;
            font-weight: 800;
            margin: 2.2rem 0 1rem 0;
            padding-bottom: 0.6rem;
            border-bottom: 2px solid #EDE9FE;
            color: #0F172A;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* ── Styled Container ────────────────────────────────────── */
        .styled-container {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 22px;
            margin: 14px 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.03);
        }

        /* ── Sidebar Styling ─────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        [data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }
        [data-testid="stSidebarNav"] {
            padding-top: 0.5rem;
        }
        [data-testid="stSidebarNav"] span {
            font-weight: 600;
            color: #1E293B;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #F5F3FF !important;
            border-left: 3px solid #6929CA !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] span {
            color: #6929CA !important;
            font-weight: 700;
        }

        /* ── BrightChamps Primary Buttons (Pill-shaped) ─────────── */
        .stButton > button, div[data-testid="stDownloadButton"] > button {
            background: #6929CA !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.55rem 1.6rem !important;
            box-shadow: 0 4px 14px rgba(105, 41, 202, 0.3) !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
            background: #5419B4 !important;
            color: #FFFFFF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 22px rgba(105, 41, 202, 0.4) !important;
        }
        .stButton > button:active, div[data-testid="stDownloadButton"] > button:active {
            transform: translateY(0) !important;
        }

        /* ── Badges ──────────────────────────────────────────────── */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.4px;
        }
        .badge-hot   { background: #FEF2F2; color: #DC2626; border: 1px solid #FECDD3; }
        .badge-warm  { background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; }
        .badge-cold  { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }
        .badge-green { background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; }
        .badge-purple{ background: #F5F3FF; color: #6929CA; border: 1px solid #DDD6FE; }

        /* ── Divider ─────────────────────────────────────────────── */
        .styled-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #E2E8F0 20%, #E2E8F0 80%, transparent);
            margin: 2rem 0;
        }

        /* ── Info Box ────────────────────────────────────────────── */
        .info-box {
            background: #F5F3FF;
            border-left: 4px solid #6929CA;
            border-radius: 0 12px 12px 0;
            padding: 16px 20px;
            margin: 12px 0;
            font-size: 0.92rem;
            color: #3730A3;
            box-shadow: 0 2px 8px rgba(105, 41, 202, 0.05);
        }

        /* ── Leak Callout ────────────────────────────────────────── */
        .leak-callout {
            background: linear-gradient(135deg, #FFF1F2 0%, #FFFBEB 100%);
            border: 2px solid #FECDD3;
            border-radius: 18px;
            padding: 26px;
            margin: 16px 0;
            text-align: center;
            box-shadow: 0 6px 20px rgba(225, 29, 72, 0.08);
        }
        .leak-callout .leak-amount {
            font-size: 3.0rem;
            font-weight: 900;
            color: #DC2626;
            letter-spacing: -1px;
        }
        .leak-callout .leak-label {
            font-size: 0.88rem;
            font-weight: 700;
            color: #991B1B;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 4px;
        }

        /* ── Streamlit Tabs ──────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 2px solid #E2E8F0;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            font-weight: 600;
            color: #64748B;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #6929CA !important;
            border-bottom: 3px solid #6929CA !important;
            background: #F5F3FF;
        }

        /* ── Inputs, Selectboxes, Multiselect ─────────────────────── */
        div[data-baseweb="select"] > div {
            border-radius: 10px !important;
            border-color: #CBD5E1 !important;
            background-color: #FFFFFF !important;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: #6929CA !important;
        }

        /* ── Tables & Dataframes ─────────────────────────────────── */
        [data-testid="stDataFrame"] {
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        }

        /* ── Custom Scrollbar ────────────────────────────────────── */
        ::-webkit-scrollbar { width: 7px; height: 7px; }
        ::-webkit-scrollbar-track { background: #F1F5F9; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #6929CA; }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Reusable UI components
# ---------------------------------------------------------------------------

def render_top_banner():
    """No-op: promotional coupon banner removed."""
    pass


def _get_logo_base64() -> str:
    """Load and base64-encode logo.png for embedding in sidebar HTML."""
    try:
        from pathlib import Path
        import base64
        logo_path = Path(__file__).resolve().parent.parent / "logo.png"
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        pass
    return ""


def render_brand_logo_sidebar():
    """Render the official BrightChamps logo in the sidebar."""
    b64 = _get_logo_base64()
    if b64:
        icon_html = f'<img src="data:image/png;base64,{b64}" style="width:34px; height:auto; max-height:38px; object-fit:contain; filter:drop-shadow(0 2px 5px rgba(0,0,0,0.06));" alt="BrightChamps Logo" />'
    else:
        icon_html = '<span style="font-size:1.4rem;">⭐</span>'

    st.markdown(
        f"""
        <div style="text-align:center; padding: 1.2rem 0 0.8rem 0;">
            <div style="display:flex; align-items:center; justify-content:center; gap:8px;">
                {icon_html}
                <span style="font-size:1.6rem; font-weight:800; letter-spacing:-0.5px;">
                    <span style="color:#1E1B4B;">Bright</span><span style="color:#E11D48;">C</span><span style="color:#F59E0B;">H</span><span style="color:#10B981;">A</span><span style="color:#2563EB;">M</span><span style="color:#8B5CF6;">P</span><span style="color:#F97316;">S</span>
                </span>
            </div>
            <div style="font-size:0.76rem; font-weight:700; color:#6929CA; letter-spacing:1px;
                        text-transform:uppercase; margin-top:0.4rem;">
                Sales Funnel AI Agent
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, delta: str = "", color: str = "gradient"):
    """Render a styled BrightChamps metric card."""
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
    """Render the official BrightChamps hero banner."""
    sub_html = f'<div class="hero-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="hero-header">
            <div class="hero-eyebrow">A NEW KIND OF EDUCATION</div>
            <div class="hero-title">
                {title}
            </div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_divider():
    """Render a subtle divider."""
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)


def render_info_box(text: str):
    """Render an info callout box."""
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)


def format_inr(amount: float) -> str:
    """Format a number in Indian Rupee lakhs / crores for readability."""
    if abs(amount) >= 1_00_00_000:
        return f"₹{amount / 1_00_00_000:,.2f} Cr"
    elif abs(amount) >= 1_00_000:
        return f"₹{amount / 1_00_000:,.1f}L"
    else:
        return f"₹{amount:,.0f}"


def format_inr_full(amount: float) -> str:
    """Format a number in Indian Rupee with commas (no abbreviation)."""
    return f"₹{amount:,.0f}"
