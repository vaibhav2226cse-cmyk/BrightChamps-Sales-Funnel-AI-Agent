"""
Page 1 — Funnel Leak Analysis
==============================
Deep-dive into where leads drop off and how much money each leak costs.
Segment by source, geography, rep, and scheduling delay.
"""

import streamlit as st

st.set_page_config(page_title="Funnel Leak Analysis", page_icon="🔍", layout="wide")

from utils.styles import (
    inject_custom_css, render_metric_card, render_hero, render_divider,
    render_section_header, render_info_box, format_inr, format_inr_full,
    CHART_COLORS, FUNNEL_COLORS, get_plotly_layout,
)
from utils.data_loader import load_data, get_months_span
from utils.funnel_analyzer import (
    get_funnel_counts, get_funnel_rates, calculate_leak_values,
    get_biggest_leak, get_total_leak_monthly, get_segmented_funnel,
    get_delay_analysis, get_timezone_alignment_analysis,
    REVENUE_PER_CONVERSION, COST_PER_LEAD,
)
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

inject_custom_css()

# ── Load data ─────────────────────────────────────────────────────────────
df = load_data()
months = get_months_span(df)

# ── Header ───────────────────────────────────────────────────────────────
render_hero("🔍 Funnel Leak Analysis", "Where is the funnel losing the most money — and how much?")

# ══════════════════════════════════════════════════════════════════════════
# SECTION 1: Overall Leak Quantification
# ══════════════════════════════════════════════════════════════════════════
render_section_header("💸 Revenue Leak by Stage (₹ per Month)")

counts = get_funnel_counts(df)
leaks = calculate_leak_values(df, months=months)
biggest = get_biggest_leak(leaks)
total_leak = get_total_leak_monthly(leaks)

# Big callout for total monthly leak
st.markdown(
    f"""
    <div class="leak-callout">
        <div class="leak-label">TOTAL ESTIMATED REVENUE LEAKED PER MONTH</div>
        <div class="leak-amount">{format_inr(total_leak)}</div>
        <div class="leak-label" style="margin-top:8px;">
            Based on ₹60,000 revenue per conversion · {counts['Lead Created']:,} leads over {months:.1f} months
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Leak cards
leak_cols = st.columns(len(leaks))
for i, leak in enumerate(leaks):
    with leak_cols[i]:
        is_biggest = leak == biggest
        render_metric_card(
            f"{'⚠️ ' if is_biggest else ''}{leak['stage_from']} → {leak['stage_to']}",
            format_inr(leak["revenue_leaked_monthly"]) + "/mo",
            (
                f"{leak['leads_lost']:,} leads lost<br>"
                f"~{leak['potential_conversions']:.0f} potential conversions<br>"
                f"Downstream conv. rate: {leak['downstream_conversion_rate']:.1%}"
            ),
            "red" if is_biggest else "amber",
        )

render_divider()

# ── Leak waterfall chart ─────────────────────────────────────────────────
render_section_header("📊 Leak Waterfall — Where ₹ Disappears")

waterfall_stages = [l["stage_from"] + " → " + l["stage_to"] for l in leaks]
waterfall_values = [l["revenue_leaked_monthly"] for l in leaks]

fig_wf = go.Figure(go.Bar(
    x=waterfall_stages,
    y=waterfall_values,
    marker_color=[FUNNEL_COLORS[i] for i in range(len(leaks))],
    text=[format_inr(v) for v in waterfall_values],
    textposition="outside",
    textfont=dict(color="#FAFAFA", size=13, family="Inter"),
))
fig_wf.update_layout(**get_plotly_layout(
    title=dict(text="Monthly Revenue Leaked at Each Stage", font=dict(size=15)),
    height=400,
    yaxis=dict(title="₹ Leaked / Month", gridcolor="rgba(255,255,255,0.06)"),
    xaxis=dict(title=""),
))
st.plotly_chart(fig_wf, width="stretch")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 2: Segmented Analysis
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🔬 Segmented Funnel Analysis")

seg_tab1, seg_tab2, seg_tab3 = st.tabs(["📣 By Lead Source", "🌍 By Geography", "⏰ By Scheduling Delay"])

# ── By Lead Source ───────────────────────────────────────────────────────
with seg_tab1:
    seg_source = get_segmented_funnel(df, "lead_source")

    fig_src = go.Figure()
    fig_src.add_trace(go.Bar(
        name="Conversion Rate",
        x=seg_source["segment"],
        y=seg_source["conversion_rate"],
        marker_color="#48BB78",
        text=[f"{v:.1%}" for v in seg_source["conversion_rate"]],
        textposition="outside",
        textfont=dict(color="#FAFAFA"),
    ))
    fig_src.update_layout(**get_plotly_layout(
        title=dict(text="Conversion Rate by Lead Source"),
        height=400,
        yaxis=dict(title="Conversion Rate", tickformat=".0%"),
    ))
    st.plotly_chart(fig_src, width="stretch")

    # Detailed table
    display_df = seg_source.copy()
    display_df["conversion_rate"] = display_df["conversion_rate"].apply(lambda x: f"{x:.1%}")
    display_df["schedule_rate"] = display_df["schedule_rate"].apply(lambda x: f"{x:.1%}")
    display_df["join_rate"] = display_df["join_rate"].apply(lambda x: f"{x:.1%}")
    st.dataframe(display_df.rename(columns={
        "segment": "Source", "lead_count": "Leads", "demo_scheduled": "Scheduled",
        "demo_joined": "Joined", "demo_completed": "Completed", "converted": "Converted",
        "conversion_rate": "Conv %", "schedule_rate": "Sched %", "join_rate": "Join %",
    }), width="stretch", hide_index=True)

    render_info_box(
        "💡 <b>Referral</b> and <b>Organic</b> leads convert at 10–11% — nearly 2× the rate of "
        "<b>Meta</b> and <b>Google</b> paid leads. <b>DSA</b> is the weakest source at ~4%."
    )

# ── By Geography ─────────────────────────────────────────────────────────
with seg_tab2:
    seg_geo = get_segmented_funnel(df, "geography")

    fig_geo = go.Figure()
    fig_geo.add_trace(go.Bar(
        name="Conversion Rate",
        x=seg_geo["segment"],
        y=seg_geo["conversion_rate"],
        marker_color=CHART_COLORS[:len(seg_geo)],
        text=[f"{v:.1%}" for v in seg_geo["conversion_rate"]],
        textposition="outside",
        textfont=dict(color="#FAFAFA"),
    ))
    fig_geo.update_layout(**get_plotly_layout(
        title=dict(text="Conversion Rate by Geography"),
        height=400,
        yaxis=dict(title="Conversion Rate", tickformat=".0%"),
    ))
    st.plotly_chart(fig_geo, width="stretch")

    display_geo = seg_geo.copy()
    display_geo["conversion_rate"] = display_geo["conversion_rate"].apply(lambda x: f"{x:.1%}")
    display_geo["schedule_rate"] = display_geo["schedule_rate"].apply(lambda x: f"{x:.1%}")
    st.dataframe(display_geo.rename(columns={
        "segment": "Geography", "lead_count": "Leads", "demo_scheduled": "Scheduled",
        "demo_joined": "Joined", "demo_completed": "Completed", "converted": "Converted",
        "conversion_rate": "Conv %", "schedule_rate": "Sched %",
    }), width="stretch", hide_index=True)

    render_info_box(
        "💡 <b>USA</b> (10%) and <b>Australia</b> (9%) are the top-converting geos. "
        "<b>India</b> (3.5%) and <b>Vietnam</b> (4.3%) convert poorly despite high lead volumes."
    )

# ── By Scheduling Delay ─────────────────────────────────────────────────
with seg_tab3:
    delay_df = get_delay_analysis(df)

    fig_delay = go.Figure()
    colors_delay = ["#48BB78", "#667EEA", "#ECC94B", "#FC8181", "#A0AEC0"]
    fig_delay.add_trace(go.Bar(
        x=delay_df["delay_bucket"],
        y=delay_df["conversion_rate"],
        marker_color=colors_delay[:len(delay_df)],
        text=[f"{v:.1%}" for v in delay_df["conversion_rate"]],
        textposition="outside",
        textfont=dict(color="#FAFAFA"),
    ))
    fig_delay.update_layout(**get_plotly_layout(
        title=dict(text="Conversion Rate by Scheduling Delay"),
        height=400,
        yaxis=dict(title="Conversion Rate", tickformat=".0%"),
        xaxis=dict(title="Time from Lead Creation to Demo Scheduled"),
    ))
    st.plotly_chart(fig_delay, width="stretch")

    st.dataframe(delay_df.rename(columns={
        "delay_bucket": "Delay", "lead_count": "Leads", "demo_joined": "Joined",
        "converted": "Converted", "join_rate": "Join %", "conversion_rate": "Conv %",
    }).assign(**{
        "Join %": delay_df["join_rate"].apply(lambda x: f"{x:.0%}"),
        "Conv %": delay_df["conversion_rate"].apply(lambda x: f"{x:.1%}"),
    }), width="stretch", hide_index=True)

    render_info_box(
        "💡 Leads scheduled within <b>48 hours</b> convert at <b>12.3%</b> — "
        "more than <b>2× the rate</b> of leads delayed beyond 48h (5.4%). "
        "Speed-to-schedule is a critical lever."
    )

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 3: Timezone Alignment
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🕐 Timezone Alignment Impact")

tz_df = get_timezone_alignment_analysis(df)

tz_col1, tz_col2 = st.columns([1, 2])

with tz_col1:
    for _, row in tz_df.iterrows():
        color = "green" if row["alignment"] == "Aligned" else "red"
        render_metric_card(
            f"TZ {row['alignment']}",
            f"{row['conversion_rate']:.1%}",
            f"{row['lead_count']:,} leads",
            color,
        )

with tz_col2:
    fig_tz = go.Figure()
    for metric, label, color in [
        ("schedule_rate", "Schedule Rate", "#667EEA"),
        ("join_rate", "Join Rate", "#9F7AEA"),
        ("conversion_rate", "Conversion Rate", "#48BB78"),
    ]:
        fig_tz.add_trace(go.Bar(
            name=label,
            x=tz_df["alignment"],
            y=tz_df[metric],
            marker_color=color,
            text=[f"{v:.1%}" for v in tz_df[metric]],
            textposition="outside",
            textfont=dict(color="#FAFAFA"),
        ))
    fig_tz.update_layout(**get_plotly_layout(
        title=dict(text="Aligned vs Misaligned Rep–Parent Timezone"),
        height=380,
        barmode="group",
        yaxis=dict(tickformat=".0%"),
    ))
    st.plotly_chart(fig_tz, width="stretch")

render_info_box(
    "💡 Timezone-aligned rep–parent pairs convert <b>better</b> across every metric. "
    "Re-routing leads to timezone-matched reps is a low-effort, high-impact intervention."
)

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 4: Detailed Working / Methodology
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📐 How We Sized the Leak")

with st.expander("Show detailed methodology & assumptions", expanded=False):
    st.markdown(f"""
    ### Assumptions
    - **Revenue per converted customer**: ₹{REVENUE_PER_CONVERSION:,}
    - **Blended marketing cost per lead**: ₹{COST_PER_LEAD:,}
    - **Dataset span**: {months:.1f} months (used to annualise figures)

    ### Methodology
    For each funnel stage transition, we calculate:

    1. **Leads lost** = Count at Stage A − Count at Stage B
    2. **Downstream conversion rate** = (Total conversions) ÷ (Count at Stage B)
       — i.e., "if this lead *had* progressed to Stage B, what fraction would have eventually converted?"
    3. **Potential conversions lost** = Leads lost × Downstream conversion rate
    4. **Revenue leaked** = Potential conversions lost × ₹{REVENUE_PER_CONVERSION:,}
    5. **Monthly figure** = Revenue leaked ÷ {months:.1f} months

    ### Stage-by-Stage Detail
    """)

    detail_rows = []
    for leak in leaks:
        detail_rows.append({
            "Transition": f"{leak['stage_from']} → {leak['stage_to']}",
            "Leads Lost": f"{leak['leads_lost']:,}",
            "Downstream Conv. Rate": f"{leak['downstream_conversion_rate']:.1%}",
            "Potential Conversions": f"{leak['potential_conversions']:.0f}",
            "₹ Leaked (Total)": format_inr_full(leak["revenue_leaked_total"]),
            "₹ Leaked (Monthly)": format_inr_full(leak["revenue_leaked_monthly"]),
        })
    st.dataframe(detail_rows, width="stretch", hide_index=True)

    st.markdown(f"""
    ### Key Caveat
    The leak sizing assumes that recovered leads would convert at the same rate as
    leads that *did* pass each gate. In practice, recovered leads may convert at a
    somewhat lower rate, so these figures represent an **upper-bound estimate**.
    """)
