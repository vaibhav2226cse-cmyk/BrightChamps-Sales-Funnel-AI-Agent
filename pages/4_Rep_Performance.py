"""
Page 4 — Rep Performance Tracker
==================================
Compare all 12 sales reps on scheduling, demo joins, conversion,
and timezone alignment. Identify coaching opportunities.
"""

import streamlit as st

st.set_page_config(page_title="Rep Performance", page_icon="👥", layout="wide")

from utils.styles import (
    inject_custom_css, render_metric_card, render_hero, render_divider,
    render_section_header, render_info_box, CHART_COLORS, get_plotly_layout,
)
from utils.data_loader import load_data
from utils.funnel_analyzer import get_segmented_funnel
import plotly.graph_objects as go
import pandas as pd
import numpy as np

inject_custom_css()

# ── Load data ─────────────────────────────────────────────────────────────
df = load_data()

# ── Header ───────────────────────────────────────────────────────────────
render_hero("👥 Rep Performance Tracker", "Compare all reps — spot top performers and coaching opportunities")

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
render_section_header("🏆 Leaderboard")

top_rep = rep_stats.iloc[0]
bottom_rep = rep_stats.iloc[-1]
avg_conv = rep_stats["conversion_rate"].mean()

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_metric_card(
        "Top Rep",
        top_rep["rep_assigned"],
        f"Conv: {top_rep['conversion_rate']:.1%} · {int(top_rep['converted'])} conversions",
        "green",
    )
with k2:
    render_metric_card(
        "Bottom Rep",
        bottom_rep["rep_assigned"],
        f"Conv: {bottom_rep['conversion_rate']:.1%} · {int(bottom_rep['converted'])} conversions",
        "red",
    )
with k3:
    render_metric_card("Avg Conversion", f"{avg_conv:.1%}", f"Across {len(rep_stats)} reps", "gradient")
with k4:
    spread = top_rep["conversion_rate"] - bottom_rep["conversion_rate"]
    render_metric_card("Performance Spread", f"{spread:.1%}", "Gap between best & worst", "amber")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 2: Multi-metric comparison
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📊 Rep Comparison — All Metrics")

metric_tab1, metric_tab2, metric_tab3 = st.tabs([
    "📈 Conversion Rate", "🔽 Full Funnel Rates", "📊 Close Rate (Demo→Sale)"
])

with metric_tab1:
    sorted_conv = rep_stats.sort_values("conversion_rate", ascending=True)
    fig_conv = go.Figure()
    fig_conv.add_trace(go.Bar(
        y=sorted_conv["rep_assigned"],
        x=sorted_conv["conversion_rate"],
        orientation="h",
        marker_color=[
            "#48BB78" if v >= avg_conv else "#FC8181"
            for v in sorted_conv["conversion_rate"]
        ],
        text=[f"{v:.1%}" for v in sorted_conv["conversion_rate"]],
        textposition="outside",
        textfont=dict(color="#FAFAFA", size=12),
    ))
    fig_conv.add_vline(x=avg_conv, line_dash="dash", line_color="#ECC94B",
                       annotation_text=f"Avg: {avg_conv:.1%}", annotation_font_color="#ECC94B")
    fig_conv.update_layout(**get_plotly_layout(
        title=dict(text="Conversion Rate by Rep (Lead → Converted)"),
        height=450,
        xaxis=dict(title="Conversion Rate", tickformat=".1%"),
    ))
    st.plotly_chart(fig_conv, width="stretch")

with metric_tab2:
    sorted_rep = rep_stats.sort_values("rep_assigned")
    fig_funnel = go.Figure()
    metrics = [
        ("schedule_rate", "Schedule Rate", "#667EEA"),
        ("join_rate", "Join Rate", "#9F7AEA"),
        ("completion_rate", "Completion Rate", "#ECC94B"),
        ("conversion_rate", "Conversion Rate", "#48BB78"),
    ]
    for metric, label, color in metrics:
        fig_funnel.add_trace(go.Bar(
            name=label,
            x=sorted_rep["rep_assigned"],
            y=sorted_rep[metric],
            marker_color=color,
            text=[f"{v:.0%}" for v in sorted_rep[metric]],
            textposition="outside",
            textfont=dict(color="#FAFAFA", size=9),
        ))
    fig_funnel.update_layout(**get_plotly_layout(
        title=dict(text="Full Funnel Rates by Rep"),
        height=450,
        barmode="group",
        yaxis=dict(title="Rate", tickformat=".0%"),
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
            "#48BB78" if v >= avg_close else "#FC8181"
            for v in sorted_close["close_rate"]
        ],
        text=[f"{v:.1%}" for v in sorted_close["close_rate"]],
        textposition="outside",
        textfont=dict(color="#FAFAFA", size=12),
    ))
    fig_close.add_vline(x=avg_close, line_dash="dash", line_color="#ECC94B",
                        annotation_text=f"Avg: {avg_close:.1%}", annotation_font_color="#ECC94B")
    fig_close.update_layout(**get_plotly_layout(
        title=dict(text="Close Rate by Rep (Completed Demo → Converted)"),
        height=450,
        xaxis=dict(title="Close Rate", tickformat=".0%"),
    ))
    st.plotly_chart(fig_close, width="stretch")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 3: Timezone Alignment per Rep
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🕐 Timezone Alignment by Rep")

tz_col1, tz_col2 = st.columns([2, 1])

with tz_col1:
    sorted_tz = rep_stats.sort_values("tz_aligned_pct", ascending=True)
    fig_tz = go.Figure()
    fig_tz.add_trace(go.Bar(
        y=sorted_tz["rep_assigned"],
        x=sorted_tz["tz_aligned_pct"],
        orientation="h",
        marker_color=[
            "#48BB78" if v >= 0.6 else "#ECC94B" if v >= 0.4 else "#FC8181"
            for v in sorted_tz["tz_aligned_pct"]
        ],
        text=[f"{v:.0%}" for v in sorted_tz["tz_aligned_pct"]],
        textposition="outside",
        textfont=dict(color="#FAFAFA", size=12),
    ))
    fig_tz.update_layout(**get_plotly_layout(
        title=dict(text="% of Leads that are Timezone-Aligned per Rep"),
        height=450,
        xaxis=dict(title="TZ Alignment %", tickformat=".0%", range=[0, 1.1]),
    ))
    st.plotly_chart(fig_tz, width="stretch")

with tz_col2:
    st.markdown("**Rep Shifts**")
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
        "💡 Reps with low TZ alignment are handling leads outside their natural timezone. "
        "Re-routing these leads can improve contact rates and conversions."
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
render_section_header("💡 Coaching Insights")

insights = []

# Find reps who schedule well but close poorly
high_sched_low_close = rep_stats[
    (rep_stats["schedule_rate"] > rep_stats["schedule_rate"].median()) &
    (rep_stats["close_rate"] < rep_stats["close_rate"].median())
]
if len(high_sched_low_close) > 0:
    reps_list = ", ".join(high_sched_low_close["rep_assigned"].tolist())
    insights.append(
        f"🔍 **High Schedule, Low Close:** {reps_list} — Schedule demos well but struggle to convert. "
        f"May need closing skill coaching or better demo scripts."
    )

# Find reps with low scheduling rates
low_sched = rep_stats[rep_stats["schedule_rate"] < rep_stats["schedule_rate"].quantile(0.25)]
if len(low_sched) > 0:
    reps_list = ", ".join(low_sched["rep_assigned"].tolist())
    insights.append(
        f"📅 **Low Scheduling:** {reps_list} — Below-average scheduling rates. "
        f"May need faster lead response processes or scheduling tool support."
    )

# Find reps with low TZ alignment
low_tz = rep_stats[rep_stats["tz_aligned_pct"] < 0.4]
if len(low_tz) > 0:
    reps_list = ", ".join(low_tz["rep_assigned"].tolist())
    insights.append(
        f"🕐 **Timezone Mismatch:** {reps_list} — Less than 40% of their leads match their shift timezone. "
        f"Lead routing rules should be reviewed."
    )

# Star performers
star = rep_stats[rep_stats["conversion_rate"] > rep_stats["conversion_rate"].quantile(0.75)]
if len(star) > 0:
    reps_list = ", ".join(star["rep_assigned"].tolist())
    insights.append(
        f"⭐ **Star Performers:** {reps_list} — Top quartile conversion rate. "
        f"Study their approach and share best practices with the team."
    )

for insight in insights:
    st.markdown(insight)

if not insights:
    st.info("No specific coaching insights identified — rep performance is relatively uniform.")
