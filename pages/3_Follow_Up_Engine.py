"""
Page 3 — Smart Follow-Up Engine
================================
Identifies no-show leads, timezone mismatches, over-contacted leads,
and generates actionable follow-up recommendations per lead.
"""

import streamlit as st

st.set_page_config(page_title="Follow-Up Engine", page_icon="📞", layout="wide")

from utils.styles import (
    inject_custom_css, render_metric_card, render_hero, render_divider,
    render_section_header, render_info_box, CHART_COLORS, get_plotly_layout,
)
from utils.data_loader import load_data
import plotly.graph_objects as go
import pandas as pd
import numpy as np

inject_custom_css()

# ── Load data ─────────────────────────────────────────────────────────────
df = load_data()

# ── Header ───────────────────────────────────────────────────────────────
render_hero("📞 Smart Follow-Up Engine", "Identify who needs attention, why, and what action to take")


# ══════════════════════════════════════════════════════════════════════════
# Classify leads into action categories
# ══════════════════════════════════════════════════════════════════════════
def classify_leads(df: pd.DataFrame) -> pd.DataFrame:
    """Assign each lead a follow-up action category and recommendation."""
    out = df.copy()

    conditions = [
        # 1. Converted — no action needed
        out["converted_flag"] == 1,
        # 2. Never scheduled — needs immediate scheduling outreach
        out["has_demo_scheduled"] == 0,
        # 3. Scheduled but no-show — needs re-engagement
        (out["has_demo_scheduled"] == 1) & (out["demo_joined_flag"] == 0),
        # 4. Joined but dropped mid-demo — needs re-demo offer
        (out["demo_joined_flag"] == 1) & (out["demo_completed_flag"] == 0),
        # 5. Completed demo but didn't convert — needs closing follow-up
        (out["demo_completed_flag"] == 1) & (out["converted_flag"] == 0),
    ]
    categories = [
        "✅ Converted",
        "🔴 Never Scheduled",
        "🟠 No-Show",
        "🟡 Dropped Mid-Demo",
        "🔵 Needs Closing",
    ]
    out["action_category"] = np.select(conditions, categories, default="Unknown")

    # Recommendations
    rec_conditions = [
        out["action_category"] == "✅ Converted",
        out["action_category"] == "🔴 Never Scheduled",
        out["action_category"] == "🟠 No-Show",
        out["action_category"] == "🟡 Dropped Mid-Demo",
        out["action_category"] == "🔵 Needs Closing",
    ]
    recommendations = [
        "No action — already converted.",
        "Schedule demo ASAP. Prioritise within 24h of lead creation. Send WhatsApp/SMS with booking link.",
        "Re-engage with a reschedule message. Match timing to parent timezone. Offer flexible slot.",
        "Offer a shorter re-demo or personalised summary. Ask what went wrong.",
        "Send personalised follow-up with pricing/offer. Assign to a senior closer if possible.",
    ]
    out["recommendation"] = np.select(rec_conditions, recommendations, default="Review manually.")

    # Flag issues
    out["is_over_contacted"] = out["follow_up_attempts"] > 4
    out["is_tz_misaligned"] = out["timezone_aligned"] == 0

    # Urgency score (simple heuristic)
    urgency = np.zeros(len(out))
    urgency += np.where(out["action_category"] == "🔴 Never Scheduled", 3, 0)
    urgency += np.where(out["action_category"] == "🟠 No-Show", 2, 0)
    urgency += np.where(out["action_category"] == "🔵 Needs Closing", 2, 0)
    urgency += np.where(out["action_category"] == "🟡 Dropped Mid-Demo", 1, 0)
    urgency += np.where(out["is_tz_misaligned"], 1, 0)
    urgency += np.where(out["follow_up_attempts"] < 2, 1, 0)
    urgency -= np.where(out["is_over_contacted"], 2, 0)
    urgency = np.clip(urgency, 0, 5)
    out["urgency"] = urgency.astype(int)

    return out


classified = classify_leads(df)

# ══════════════════════════════════════════════════════════════════════════
# SECTION 1: Overview KPIs
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📊 Follow-Up Overview")

cat_counts = classified["action_category"].value_counts()
not_converted = classified[classified["converted_flag"] == 0]

k1, k2, k3, k4 = st.columns(4)
with k1:
    never_sched = cat_counts.get("🔴 Never Scheduled", 0)
    render_metric_card("Never Scheduled", f"{never_sched:,}", "Need demo scheduling outreach", "red")
with k2:
    no_show = cat_counts.get("🟠 No-Show", 0)
    render_metric_card("No-Shows", f"{no_show:,}", "Scheduled but didn't join", "amber")
with k3:
    needs_closing = cat_counts.get("🔵 Needs Closing", 0)
    render_metric_card("Needs Closing", f"{needs_closing:,}", "Completed demo, didn't buy", "blue")
with k4:
    over_contacted = int(not_converted["is_over_contacted"].sum())
    render_metric_card("Over-Contacted", f"{over_contacted:,}", ">4 attempts, diminishing returns", "red")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 2: Action Category Breakdown
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🎯 Action Categories")

cat_summary = (
    classified.groupby("action_category")
    .agg(
        count=("lead_id", "count"),
        avg_follow_ups=("follow_up_attempts", "mean"),
        tz_misaligned=("is_tz_misaligned", "sum"),
        over_contacted=("is_over_contacted", "sum"),
    )
    .reset_index()
    .sort_values("count", ascending=False)
)

fig_cat = go.Figure()
fig_cat.add_trace(go.Bar(
    x=cat_summary["action_category"],
    y=cat_summary["count"],
    marker_color=["#48BB78", "#FC8181", "#ED8936", "#ECC94B", "#63B3ED"][:len(cat_summary)],
    text=[f"{v:,}" for v in cat_summary["count"]],
    textposition="outside",
    textfont=dict(color="#FAFAFA", size=13),
))
fig_cat.update_layout(**get_plotly_layout(
    title=dict(text="Leads by Action Category"),
    height=400,
    yaxis=dict(title="Number of Leads"),
))
st.plotly_chart(fig_cat, width="stretch")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 3: Issue Flags
# ══════════════════════════════════════════════════════════════════════════
render_section_header("⚠️ Issue Flags")

flag_tab1, flag_tab2, flag_tab3 = st.tabs(["🕐 Timezone Mismatches", "📱 Over-Contacted Leads", "⏰ Stale Leads (Long Delay)"])

with flag_tab1:
    tz_mismatch = not_converted[not_converted["is_tz_misaligned"] == True]
    st.markdown(f"**{len(tz_mismatch):,} active leads** have a rep whose shift doesn't match the parent's timezone.")

    if len(tz_mismatch) > 0:
        tz_by_shift = tz_mismatch.groupby(["rep_shift", "parent_timezone"]).size().reset_index(name="count")
        fig_tz = go.Figure(go.Treemap(
            labels=[f"{row['rep_shift']} → {row['parent_timezone']}" for _, row in tz_by_shift.iterrows()],
            parents=["" for _ in range(len(tz_by_shift))],
            values=tz_by_shift["count"],
            textinfo="label+value",
            marker=dict(colors=CHART_COLORS[:len(tz_by_shift)]),
        ))
        fig_tz.update_layout(**get_plotly_layout(title=dict(text="Misaligned Shift–Timezone Combinations"), height=400))
        st.plotly_chart(fig_tz, width="stretch")

        render_info_box(
            "💡 <b>Fix:</b> Re-route these leads to reps on the matching shift, or adjust follow-up timing to "
            "the parent's local business hours."
        )

with flag_tab2:
    over_contact = not_converted[not_converted["is_over_contacted"] == True]
    st.markdown(f"**{len(over_contact):,} unconverted leads** have received more than 4 follow-up attempts.")

    if len(over_contact) > 0:
        oc_by_attempts = over_contact["follow_up_attempts"].value_counts().sort_index()
        fig_oc = go.Figure(go.Bar(
            x=[str(v) for v in oc_by_attempts.index],
            y=oc_by_attempts.values,
            marker_color="#ECC94B",
            text=[f"{v:,}" for v in oc_by_attempts.values],
            textposition="outside",
            textfont=dict(color="#FAFAFA"),
        ))
        fig_oc.update_layout(**get_plotly_layout(
            title=dict(text="Over-Contacted Leads by Follow-Up Count"),
            height=350,
            xaxis=dict(title="Follow-Up Attempts"),
            yaxis=dict(title="Leads"),
        ))
        st.plotly_chart(fig_oc, width="stretch")

        render_info_box(
            "💡 <b>Fix:</b> After 4 attempts with no conversion, deprioritise and move to a "
            "nurture/drip campaign instead of manual follow-ups. Rep time is better spent on fresh leads."
        )

with flag_tab3:
    stale = df[(df["schedule_delay_hours"] > 72) & (df["converted_flag"] == 0)]
    st.markdown(f"**{len(stale):,} unconverted leads** had demos scheduled more than 72 hours after lead creation.")

    if len(stale) > 0:
        stale_by_source = stale["lead_source"].value_counts()
        fig_stale = go.Figure(go.Pie(
            labels=stale_by_source.index,
            values=stale_by_source.values,
            marker=dict(colors=CHART_COLORS[:len(stale_by_source)]),
            hole=0.45,
            textinfo="label+percent",
            textfont=dict(color="#FAFAFA"),
        ))
        fig_stale.update_layout(**get_plotly_layout(
            title=dict(text="Stale Leads by Source"),
            height=400,
        ))
        st.plotly_chart(fig_stale, width="stretch")

        render_info_box(
            "💡 <b>Fix:</b> Implement auto-scheduling within 24h of lead creation. Leads delayed beyond "
            "48h convert at less than half the rate of those scheduled within 24h."
        )

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 4: Actionable Follow-Up List
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📋 Actionable Follow-Up List")

# Filters
f1, f2, f3 = st.columns(3)
with f1:
    cat_filter = st.multiselect(
        "Action Category",
        [c for c in classified["action_category"].unique() if c != "✅ Converted"],
        default=["🔴 Never Scheduled", "🟠 No-Show"],
    )
with f2:
    urgency_min = st.slider("Minimum Urgency", 0, 5, 2)
with f3:
    max_rows = st.selectbox("Show top", [50, 100, 200, 500], index=1)

action_df = classified[
    (classified["action_category"].isin(cat_filter)) &
    (classified["urgency"] >= urgency_min)
].sort_values("urgency", ascending=False).head(max_rows)

display_cols = [
    "lead_id", "urgency", "action_category", "recommendation",
    "lead_source", "geography", "parent_timezone",
    "rep_assigned", "rep_shift", "follow_up_attempts",
    "is_tz_misaligned", "is_over_contacted",
]
available = [c for c in display_cols if c in action_df.columns]

st.dataframe(
    action_df[available].rename(columns={
        "lead_id": "Lead", "urgency": "Urgency", "action_category": "Category",
        "recommendation": "Recommended Action", "lead_source": "Source",
        "geography": "Geo", "parent_timezone": "TZ", "rep_assigned": "Rep",
        "rep_shift": "Shift", "follow_up_attempts": "Attempts",
        "is_tz_misaligned": "TZ Mismatch?", "is_over_contacted": "Over-Contacted?",
    }),
    width="stretch",
    hide_index=True,
    height=500,
)

st.markdown(f"*Showing {len(action_df):,} leads matching filters*")

csv_data = action_df[available].to_csv(index=False)
st.download_button(
    "⬇️ Download Action List as CSV",
    csv_data,
    "brightchamps_followup_actions.csv",
    "text/csv",
    width="stretch",
)
