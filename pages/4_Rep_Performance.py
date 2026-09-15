"""
Page 4 — Rep Performance Tracker
==================================
Compare all 12 sales reps on scheduling, demo joins, conversion,
and timezone alignment. Identify coaching opportunities.
Official BrightChamps Brand Theme.
"""

import streamlit as st

st.set_page_config(page_title="Rep Performance — BrightChamps", page_icon="👥", layout="wide")

from utils.styles import (
    inject_custom_css, render_brand_logo_sidebar,
    render_metric_card, render_hero, render_divider,
    render_section_header, render_info_box, CHART_COLORS, FUNNEL_COLORS, get_plotly_layout,
)
from utils.data_loader import load_data
from utils.funnel_analyzer import get_segmented_funnel
import plotly.graph_objects as go
import pandas as pd
import numpy as np

inject_custom_css()

with st.sidebar:
    render_brand_logo_sidebar()
    st.markdown("---")
    st.markdown("""
    **👥 Rep Diagnostics**
    - 🏆 Leaderboard & Top Closers
    - 📉 Scheduling vs Demo Join gap
    - 🕐 Shift & Timezone alignment
    """)

# ── Load data ─────────────────────────────────────────────────────────────
df = load_data()

# ── Header ───────────────────────────────────────────────────────────────
render_hero("👥 Sales Rep Performance", "Compare rep conversion, full-funnel velocity, and automated coaching alerts")

# ══════════════════════════════════════════════════════════════════════════
# Build rep stats
# ══════════════════════════════════════════════════════════════════════════
rep_stats = (
    df.groupby("rep_assigned")
    .agg(
        total_leads=("lead_id", "count"),
        scheduled=("has_demo_scheduled", "sum"),
        joined=("demo_joined_flag", "sum"),
        completed=("demo_completed_flag", "sum"),
        converted=("converted_flag", "sum"),
        avg_follow_ups=("follow_up_attempts", "mean"),
        tz_aligned_pct=("timezone_aligned", "mean"),
        shift=("rep_shift", "first"),
    )
    .reset_index()
)

rep_stats["schedule_rate"] = rep_stats["scheduled"] / rep_stats["total_leads"]
rep_stats["join_rate"] = rep_stats["joined"] / rep_stats["total_leads"]
rep_stats["completion_rate"] = rep_stats["completed"] / rep_stats["total_leads"]
rep_stats["conversion_rate"] = rep_stats["converted"] / rep_stats["total_leads"]
rep_stats["close_rate"] = np.where(
    rep_stats["completed"] > 0,
    rep_stats["converted"] / rep_stats["completed"],
    0,
)

rep_stats = rep_stats.sort_values("conversion_rate", ascending=False)

# ══════════════════════════════════════════════════════════════════════════
# SECTION 1: Top-level KPIs
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🏆 Sales Rep Leaderboard")

top_rep = rep_stats.iloc[0]
bottom_rep = rep_stats.iloc[-1]
avg_conv = rep_stats["conversion_rate"].mean()

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_metric_card(
        "Top Performer",
        top_rep["rep_assigned"],
        f"Conv: {top_rep['conversion_rate']:.1%} · {int(top_rep['converted'])} enrollments",
        "green",
    )
with k2:
    render_metric_card(
        "Needs Support",
        bottom_rep["rep_assigned"],
        f"Conv: {bottom_rep['conversion_rate']:.1%} · {int(bottom_rep['converted'])} enrollments",
        "red",
    )
with k3:
    render_metric_card("Team Average Conversion", f"{avg_conv:.1%}", f"Across {len(rep_stats)} sales reps", "purple")
with k4:
    spread = top_rep["conversion_rate"] - bottom_rep["conversion_rate"]
    render_metric_card("Performance Gap", f"{spread:.1%}", "Top vs bottom rep delta", "amber")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 2: Multi-metric comparison
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📊 Multi-Metric Rep Comparison")

metric_tab1, metric_tab2, metric_tab3 = st.tabs([
    "📈 Lead-to-Conversion Rate", "🔽 Full Funnel Conversion", "🎯 Closing Efficiency (Demo → Sale)"
])

with metric_tab1:
    sorted_conv = rep_stats.sort_values("conversion_rate", ascending=True)
    fig_conv = go.Figure()
    fig_conv.add_trace(go.Bar(
        y=sorted_conv["rep_assigned"],
        x=sorted_conv["conversion_rate"],
        orientation="h",
        marker_color=[
            "#10B981" if v >= avg_conv else "#E11D48"
            for v in sorted_conv["conversion_rate"]
        ],
        text=[f"{v:.1%}" for v in sorted_conv["conversion_rate"]],
        textposition="outside",
        textfont=dict(color="#0F172A", size=12, family="Plus Jakarta Sans, sans-serif"),
    ))
    fig_conv.add_vline(x=avg_conv, line_dash="dash", line_color="#6929CA",
                       annotation_text=f"Team Mean: {avg_conv:.1%}", annotation_font_color="#6929CA")
    fig_conv.update_layout(**get_plotly_layout(
        title=dict(text="Overall Lead Conversion Rate by Rep", font=dict(color="#0F172A")),
        height=450,
        xaxis=dict(title="Conversion Rate", tickformat=".1%"),
    ))
    st.plotly_chart(fig_conv, width="stretch")

with metric_tab2:
    sorted_rep = rep_stats.sort_values("rep_assigned")
    fig_funnel = go.Figure()
    metrics = [
        ("schedule_rate", "Schedule Rate", "#6929CA"),
        ("join_rate", "Join Rate", "#8B5CF6"),
        ("completion_rate", "Completion Rate", "#F59E0B"),
        ("conversion_rate", "Conversion Rate", "#10B981"),
    ]
    for metric, label, color in metrics:
        fig_funnel.add_trace(go.Bar(
            name=label,
            x=sorted_rep["rep_assigned"],
            y=sorted_rep[metric],
            marker_color=color,
            text=[f"{v:.0%}" for v in sorted_rep[metric]],
            textposition="outside",
            textfont=dict(color="#0F172A", size=9),
        ))
    fig_funnel.update_layout(**get_plotly_layout(
        title=dict(text="Funnel Stage Retention by Rep", font=dict(color="#0F172A")),
        height=450,
        barmode="group",
        yaxis=dict(title="Retention Rate", tickformat=".0%"),
    ))
    st.plotly_chart(fig_funnel, width="stretch")

with metric_tab3:
    sorted_close = rep_stats.sort_values("close_rate", ascending=True)
    avg_close = rep_stats["close_rate"].mean()
    fig_close = go.Figure()
    fig_close.add_trace(go.Bar(
        y=sorted_close["rep_assigned"],
        x=sorted_close["close_rate"],
        orientation="h",
        marker_color=[
            "#10B981" if v >= avg_close else "#E11D48"
            for v in sorted_close["close_rate"]
        ],
        text=[f"{v:.1%}" for v in sorted_close["close_rate"]],
        textposition="outside",
        textfont=dict(color="#0F172A", size=12),
    ))
    fig_close.add_vline(x=avg_close, line_dash="dash", line_color="#6929CA",
                       annotation_text=f"Team Mean: {avg_close:.1%}", annotation_font_color="#6929CA")
    fig_close.update_layout(**get_plotly_layout(
        title=dict(text="Demo Close Rate by Rep (Completed Demo → Converted)", font=dict(color="#0F172A")),
        height=450,
        xaxis=dict(title="Close Rate", tickformat=".0%"),
    ))
    st.plotly_chart(fig_close, width="stretch")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 3: Timezone Alignment per Rep
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🕐 Timezone Alignment per Rep")

tz_col1, tz_col2 = st.columns([2, 1])

with tz_col1:
    sorted_tz = rep_stats.sort_values("tz_aligned_pct", ascending=True)
    fig_tz = go.Figure()
    fig_tz.add_trace(go.Bar(
        y=sorted_tz["rep_assigned"],
        x=sorted_tz["tz_aligned_pct"],
        orientation="h",
        marker_color=[
            "#10B981" if v >= 0.6 else "#F59E0B" if v >= 0.4 else "#DC2626"
            for v in sorted_tz["tz_aligned_pct"]
        ],
        text=[f"{v:.0%}" for v in sorted_tz["tz_aligned_pct"]],
        textposition="outside",
        textfont=dict(color="#0F172A", size=12),
    ))
    fig_tz.update_layout(**get_plotly_layout(
        title=dict(text="% of Assigned Leads Aligned with Rep Shift Timezone", font=dict(color="#0F172A")),
        height=450,
        xaxis=dict(title="TZ Alignment %", tickformat=".0%", range=[0, 1.1]),
    ))
    st.plotly_chart(fig_tz, width="stretch")

with tz_col2:
    st.markdown("<h4 style='color:#0F172A; font-size:1.05rem;'>Rep Shift Roster</h4>", unsafe_allow_html=True)
    shift_info = rep_stats[["rep_assigned", "shift", "tz_aligned_pct"]].copy()
    shift_info["tz_aligned_pct"] = shift_info["tz_aligned_pct"].apply(lambda x: f"{x:.0%}")
    st.dataframe(
        shift_info.rename(columns={
            "rep_assigned": "Rep", "shift": "Shift", "tz_aligned_pct": "TZ Aligned",
        }),
        width="stretch",
        hide_index=True,
    )
    render_info_box(
        "💡 Reps with low timezone alignment (<40%) suffer reduced contact rates. "
        "Re-routing these leads to matching shifts immediately boosts conversion without training overhead."
    )

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 4: Detailed Rep Scorecard
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📋 Detailed Rep Scorecard")

scorecard = rep_stats[[
    "rep_assigned", "shift", "total_leads", "scheduled", "joined",
    "completed", "converted", "schedule_rate", "join_rate",
    "completion_rate", "conversion_rate", "close_rate",
    "avg_follow_ups", "tz_aligned_pct",
]].copy()

# Format percentages
for col in ["schedule_rate", "join_rate", "completion_rate", "conversion_rate", "close_rate", "tz_aligned_pct"]:
    scorecard[col] = scorecard[col].apply(lambda x: f"{x:.1%}")
scorecard["avg_follow_ups"] = scorecard["avg_follow_ups"].apply(lambda x: f"{x:.1f}")

st.dataframe(
    scorecard.rename(columns={
        "rep_assigned": "Rep", "shift": "Shift", "total_leads": "Leads",
        "scheduled": "Sched.", "joined": "Joined", "completed": "Completed",
        "converted": "Conv.", "schedule_rate": "Sched %",
        "join_rate": "Join %", "completion_rate": "Done %",
        "conversion_rate": "Conv %", "close_rate": "Close %",
        "avg_follow_ups": "Avg F/U", "tz_aligned_pct": "TZ Align",
    }),
    width="stretch",
    hide_index=True,
    height=500,
)

csv_data = scorecard.to_csv(index=False)
st.download_button(
    "⬇️ Download Rep Scorecard as CSV",
    csv_data,
    "brightchamps_rep_scorecard.csv",
    "text/csv",
    width="stretch",
)

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 5: Coaching Insights
# ══════════════════════════════════════════════════════════════════════════
render_section_header("💡 Auto-Generated Coaching Insights")

insights = []

# Find reps who schedule well but close poorly
high_sched_low_close = rep_stats[
    (rep_stats["schedule_rate"] > rep_stats["schedule_rate"].median()) &
    (rep_stats["close_rate"] < rep_stats["close_rate"].median())
]
if len(high_sched_low_close) > 0:
    reps_list = ", ".join(high_sched_low_close["rep_assigned"].tolist())
    insights.append(
        f"🔍 **High Scheduling, Low Closing:** {reps_list} — Excellent at getting parents into demos, but below average closing efficiency. "
        f"Recommended action: Demo pitch refresher and closing objection handling."
    )

# Find reps with low scheduling rates
low_sched = rep_stats[rep_stats["schedule_rate"] < rep_stats["schedule_rate"].quantile(0.25)]
if len(low_sched) > 0:
    reps_list = ", ".join(low_sched["rep_assigned"].tolist())
    insights.append(
        f"📅 **Low Scheduling Velocity:** {reps_list} — Sched rate is bottom quartile. "
        f"Recommended action: Review speed-to-call (<24h) and provide WhatsApp automated scheduling link templates."
    )

# Find reps with low TZ alignment
low_tz = rep_stats[rep_stats["tz_aligned_pct"] < 0.4]
if len(low_tz) > 0:
    reps_list = ", ".join(low_tz["rep_assigned"].tolist())
    insights.append(
        f"🕐 **Severe Timezone Mismatch:** {reps_list} — More than 60% of assigned leads fall outside their shift hours. "
        f"Recommended action: Re-allocate geographic queue in CRM."
    )

# Star performers
star = rep_stats[rep_stats["conversion_rate"] > rep_stats["conversion_rate"].quantile(0.75)]
if len(star) > 0:
    reps_list = ", ".join(star["rep_assigned"].tolist())
    insights.append(
        f"⭐ **Star Performers:** {reps_list} — Top quartile conversion rate across all metrics. "
        f"Action: Have these reps run peer workshops on parent demo engagement."
    )

for insight in insights:
    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #6929CA;
                    border-radius:10px; padding:14px 18px; margin:8px 0; font-size:0.92rem; color:#1E293B;
                    box-shadow:0 2px 8px rgba(105,41,202,0.04);">
            {insight}
        </div>
        """,
        unsafe_allow_html=True,
    )
