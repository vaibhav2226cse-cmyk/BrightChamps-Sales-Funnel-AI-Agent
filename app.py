"""
BrightChamps Lead Funnel AI Agent
==================================
Home page — high-level KPIs, funnel snapshot, and navigation guide.

Run with:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="BrightChamps Lead Funnel AI Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_custom_css, render_metric_card, render_hero, render_divider, render_section_header, render_info_box, format_inr, CHART_COLORS, FUNNEL_COLORS, get_plotly_layout
from utils.data_loader import load_data, get_months_span
from utils.funnel_analyzer import get_funnel_counts, get_funnel_rates, calculate_leak_values, get_biggest_leak, get_total_leak_monthly
import plotly.graph_objects as go

# ── Inject styles ─────────────────────────────────────────────────────────
inject_custom_css()

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0;">
        <div style="font-size:2.2rem;">🚀</div>
        <div style="font-size:1.1rem; font-weight:700; margin-top:0.3rem;
                    background: linear-gradient(135deg, #667EEA, #764BA2);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            BrightChamps
        </div>
        <div style="font-size:0.75rem; color:#A0AEC0; margin-top:0.2rem;">
            Lead Funnel AI Agent
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    **📌 Pages**
    - 🔍 **Funnel Leak Analysis** — Where is money leaking?
    - 🎯 **Lead Scoring** — Which leads to prioritize?
    - 📞 **Follow-Up Engine** — Who needs attention?
    - 👥 **Rep Performance** — How are reps doing?
    """)
    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.72rem; color:#4A5568; text-align:center;">'
        'Built for BrightChamps Founder\'s Office<br>AI Forward Deployed Associate Case'
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
    "Lead Funnel AI Agent",
    "Identify leaks · Score leads · Optimise follow-ups · Track rep performance"
)

# ── KPI row ──────────────────────────────────────────────────────────────
render_section_header("📊 Key Metrics at a Glance")
k1, k2, k3, k4 = st.columns(4)
with k1:
    render_metric_card("Total Leads", f"{counts['Lead Created']:,}", f"{months:.0f}-month dataset", "white")
with k2:
    conv_rate = rates["Converted"]["cumulative_rate"] * 100
    render_metric_card("Conversion Rate", f"{conv_rate:.1f}%", f"{counts['Converted']:,} conversions", "amber")
with k3:
    render_metric_card("₹ Leaked / Month", format_inr(total_leak), "Potential revenue lost", "red")
with k4:
    render_metric_card(
        "Biggest Leak",
        f"{biggest['stage_from'].replace('Lead Created','Lead')} → {biggest['stage_to'].replace('Demo Scheduled','Sched.')}",
        f"{biggest['leads_lost']:,} leads lost · {format_inr(biggest['revenue_leaked_monthly'])}/mo",
        "red",
    )

render_divider()

# ── Funnel visualization ────────────────────────────────────────────────
render_section_header("🔽 The Funnel — From Lead to Conversion")

col_funnel, col_table = st.columns([3, 2])

with col_funnel:
    stage_names = list(counts.keys())
    stage_values = list(counts.values())

    fig = go.Figure(go.Funnel(
        y=stage_names,
        x=stage_values,
        textinfo="value+percent initial",
        textfont=dict(size=14, color="#FAFAFA"),
        marker=dict(
            color=FUNNEL_COLORS,
            line=dict(width=1, color="rgba(255,255,255,0.1)"),
        ),
        connector=dict(line=dict(color="rgba(102,126,234,0.3)", width=1)),
    ))
    fig.update_layout(
        **get_plotly_layout(
            title=dict(text="Funnel Drop-off", font=dict(size=16)),
            height=420,
            margin=dict(l=20, r=20, t=50, b=20),
        )
    )
    st.plotly_chart(fig, width="stretch")

with col_table:
    st.markdown("**Stage-by-Stage Breakdown**")
    table_data = []
    for stage, info in rates.items():
        table_data.append({
            "Stage": stage,
            "Count": f"{info['count']:,}",
            "Stage Rate": f"{info['stage_rate']:.0%}",
            "Overall": f"{info['cumulative_rate']:.1%}",
        })
    st.dataframe(
        table_data,
        width="stretch",
        hide_index=True,
    )

    st.markdown("")
    render_info_box(
        f"💡 The funnel loses <b>{counts['Lead Created'] - counts['Converted']:,}</b> leads "
        f"({(1 - rates['Converted']['cumulative_rate']):.0%}) before conversion, "
        f"leaking an estimated <b>{format_inr(total_leak)}/month</b> in potential revenue."
    )

render_divider()

# ── Quick leak summary ──────────────────────────────────────────────────
render_section_header("💸 Where Is the Money Leaking?")

leak_cols = st.columns(len(leaks))
for i, leak in enumerate(leaks):
    with leak_cols[i]:
        arrow = f"{leak['stage_from'].split()[-1]} → {leak['stage_to'].split()[-1]}"
        render_metric_card(
            arrow,
            format_inr(leak["revenue_leaked_monthly"]),
            f"{leak['leads_lost']:,} leads lost · {leak['downstream_conversion_rate']:.0%} downstream rate",
            "red" if leak == biggest else "amber",
        )

render_divider()

# ── Navigation guide ─────────────────────────────────────────────────────
render_section_header("🗺️ How to Use This Tool")

guide_cols = st.columns(4)
guides = [
    ("🔍", "Funnel Leak Analysis", "Deep-dive into where and why leads drop off. Segment by source, geography, rep, and timing."),
    ("🎯", "Lead Scoring", "ML-powered conversion probability for every lead. Prioritise hot leads, deprioritise cold ones."),
    ("📞", "Follow-Up Engine", "Identifies no-shows, timezone mismatches, and over-contacted leads. Generates action lists."),
    ("👥", "Rep Performance", "Compare all 12 reps on scheduling, join rates, and conversion. Spot coaching opportunities."),
]

for col, (icon, title, desc) in zip(guide_cols, guides):
    with col:
        st.markdown(
            f"""
            <div class="styled-container" style="text-align:center; min-height:200px;">
                <div style="font-size:2.2rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:700; font-size:1rem; margin-bottom:0.5rem;">{title}</div>
                <div style="font-size:0.82rem; color:#A0AEC0;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
render_info_box(
    "👈 Use the <b>sidebar</b> to navigate between pages. "
    "Each page is self-contained — explore them in any order."
)
