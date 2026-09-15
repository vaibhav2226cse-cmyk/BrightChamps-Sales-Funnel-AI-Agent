"""
BrightChamps Lead Funnel AI Agent
==================================
Home page — high-level KPIs, funnel snapshot, and navigation guide.
Official BrightChamps Brand Theme: Curious. Confident. Unstoppable.

Run with:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="BrightChamps Sales Funnel AI Agent",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import (
    inject_custom_css, render_brand_logo_sidebar,
    render_metric_card, render_hero, render_divider, render_section_header,
    render_info_box, format_inr, CHART_COLORS, FUNNEL_COLORS, get_plotly_layout,
)
from utils.data_loader import load_data, get_months_span
from utils.funnel_analyzer import (
    get_funnel_counts, get_funnel_rates, calculate_leak_values,
    get_biggest_leak, get_total_leak_monthly,
)
import plotly.graph_objects as go

# ── Inject styles ─────────────────────────────────────────────────────────
inject_custom_css()

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    render_brand_logo_sidebar()
    st.markdown("---")
    st.markdown("""
    **🧭 Navigation**
    - 🔍 **Funnel Leak Analysis** — Where is revenue leaking?
    - 🎯 **Lead Scoring Engine** — ML conversion probability
    - 📞 **Follow-Up Engine** — No-show recovery & nudges
    - 👥 **Rep Performance** — Leaderboard & coaching
    """)
    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.75rem; color:#64748B; text-align:center; padding: 0.5rem;">'
        '<b>BrightChamps Founder\'s Office</b><br>AI Forward Deployed Associate Case'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Load data ─────────────────────────────────────────────────────────────
df = load_data()
months = get_months_span(df)

# ── Funnel calculations ──────────────────────────────────────────────────
counts = get_funnel_counts(df)
rates = get_funnel_rates(counts)
leaks = calculate_leak_values(df, months=months)
biggest = get_biggest_leak(leaks)
total_leak = get_total_leak_monthly(leaks)

# ── Hero header ──────────────────────────────────────────────────────────
render_hero(
    'Curious<span class="dot-yellow">.</span> Confident<span class="dot-green">.</span> Unstoppable<span class="dot-blue">.</span>',
    "Sales Funnel AI Agent — Identify Leaks · Score Leads · Recover No-Shows · Track Reps"
)

# ── KPI row ──────────────────────────────────────────────────────────────
render_section_header("📊 Key Funnel Metrics at a Glance")
k1, k2, k3, k4 = st.columns(4)
with k1:
    render_metric_card("Total Leads Ingested", f"{counts['Lead Created']:,}", f"{months:.0f}-month dataset", "purple")
with k2:
    conv_rate = rates["Converted"]["cumulative_rate"] * 100
    render_metric_card("Overall Conversion", f"{conv_rate:.1f}%", f"{counts['Converted']:,} total enrolled students", "green")
with k3:
    render_metric_card("₹ Leaked / Month", format_inr(total_leak), "Gross opportunity cost", "red")
with k4:
    render_metric_card(
        "Largest Revenue Leak",
        f"{biggest['stage_from'].replace('Lead Created','Lead')} → {biggest['stage_to'].replace('Demo Scheduled','Sched.')}",
        f"{biggest['leads_lost']:,} leads lost · {format_inr(biggest['revenue_leaked_monthly'])}/mo",
        "red",
    )

render_divider()

# ── Funnel visualization ────────────────────────────────────────────────
render_section_header("🔽 Funnel Drop-off Architecture")

col_funnel, col_table = st.columns([3, 2])

with col_funnel:
    stage_names = list(counts.keys())
    stage_values = list(counts.values())

    fig = go.Figure(go.Funnel(
        y=stage_names,
        x=stage_values,
        textinfo="value+percent initial",
        textfont=dict(size=14, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif"),
        marker=dict(
            color=FUNNEL_COLORS,
            line=dict(width=1.5, color="#FFFFFF"),
        ),
        connector=dict(line=dict(color="#DDD6FE", width=1.5)),
    ))
    fig.update_layout(
        **get_plotly_layout(
            title=dict(text="Funnel Drop-off by Stage", font=dict(size=16, color="#0F172A")),
            height=420,
            margin=dict(l=20, r=20, t=50, b=20),
        )
    )
    st.plotly_chart(fig, width="stretch")

with col_table:
    st.markdown("<h4 style='color:#0F172A; margin-bottom:0.6rem;'>Stage-by-Stage Breakdown</h4>", unsafe_allow_html=True)
    table_data = []
    for stage, info in rates.items():
        table_data.append({
            "Stage": stage,
            "Count": f"{info['count']:,}",
            "Stage Retention": f"{info['stage_rate']:.0%}",
            "Overall Conversion": f"{info['cumulative_rate']:.1%}",
        })
    st.dataframe(
        table_data,
        width="stretch",
        hide_index=True,
    )

    st.markdown("")
    render_info_box(
        f"💡 Out of <b>{counts['Lead Created']:,}</b> leads, <b>{counts['Lead Created'] - counts['Converted']:,}</b> "
        f"({(1 - rates['Converted']['cumulative_rate']):.1%}) drop out before buying, "
        f"draining an estimated <b>{format_inr(total_leak)} / month</b> in gross revenue."
    )

render_divider()

# ── Quick leak summary ──────────────────────────────────────────────────
render_section_header("💸 Revenue Leaks Quantified in ₹ / Month")

leak_cols = st.columns(len(leaks))
for i, leak in enumerate(leaks):
    with leak_cols[i]:
        arrow = f"{leak['stage_from'].split()[-1]} → {leak['stage_to'].split()[-1]}"
        is_biggest = leak == biggest
        render_metric_card(
            f"{'⚠️ ' if is_biggest else ''}{arrow}",
            format_inr(leak["revenue_leaked_monthly"]) + " / mo",
            f"{leak['leads_lost']:,} lost · {leak['downstream_conversion_rate']:.0%} downstream conv.",
            "red" if is_biggest else "amber",
        )

render_divider()

# ── Navigation guide ─────────────────────────────────────────────────────
render_section_header("🗺️ Quick Navigation Guide")

guide_cols = st.columns(4)
guides = [
    ("🔍", "Funnel Leak Analysis", "Deep-dive into drop-offs, scheduling latency, and ₹ leak quantification.", "#6929CA"),
    ("🎯", "Lead Scoring Engine", "ML-based conversion probabilities, Hot/Warm/Cold tiers, and CSV exports.", "#E11D48"),
    ("📞", "Follow-Up Engine", "Target no-shows, timezone mismatches, and fatigue filters for instant SDR action.", "#059669"),
    ("👥", "Rep Performance", "Compare all 12 reps on scheduling, demo joins, and conversion coaching.", "#2563EB"),
]

for col, (icon, title, desc, border_c) in zip(guide_cols, guides):
    with col:
        st.markdown(
            f"""
            <div class="styled-container" style="text-align:center; min-height:190px; border-top: 3px solid {border_c};">
                <div style="font-size:2.2rem; margin-bottom:0.4rem;">{icon}</div>
                <div style="font-weight:800; font-size:1.02rem; color:#0F172A; margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.83rem; color:#64748B; line-height:1.4;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
render_info_box(
    "👈 <b>How to start:</b> Select any page from the sidebar to analyze leaks, score leads, or review reps."
)
