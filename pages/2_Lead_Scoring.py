"""
Page 2 — Lead Scoring Engine
==============================
Machine-learning lead prioritization model for sales reps.
Predicts conversion probability for each lead and buckets into Hot / Warm / Cold.
Official BrightChamps Brand Theme.
"""

import streamlit as st

st.set_page_config(page_title="Lead Scoring — BrightChamps", page_icon="🎯", layout="wide")

from utils.styles import (
    inject_custom_css, render_top_banner, render_brand_logo_sidebar,
    render_metric_card, render_hero, render_divider,
    render_section_header, render_info_box, get_plotly_layout,
    COLORS, CHART_COLORS,
)
from utils.data_loader import load_data
from utils.lead_scorer import train_and_score, get_tier_summary, get_feature_importance
import plotly.graph_objects as go
import pandas as pd

inject_custom_css()
render_top_banner()

with st.sidebar:
    render_brand_logo_sidebar()
    st.markdown("---")
    st.markdown("""
    **🎯 Lead Prioritization**
    - 🔴 **Hot (>20% score)** — Call within 15 min
    - 🟡 **Warm (10–20% score)** — Same-day reachout
    - 🔵 **Cold (<10% score)** — Automated drip
    """)

# ── Header ───────────────────────────────────────────────────────────────
render_hero("🎯 AI Lead Scoring Engine", "Predict conversion probability and prioritize reps' daily outreach")

# ── Train model & score ──────────────────────────────────────────────────
with st.spinner("Training predictive model & scoring 5,000 leads..."):
    scored_df, model, preprocessor = train_and_score()
    feature_imp = get_feature_importance(model, preprocessor)

# ══════════════════════════════════════════════════════════════════════════
# SECTION 1: Priority Tier Summary
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🎯 Leads by Priority Tier")

tier_df = get_tier_summary(scored_df)

tier_cols = st.columns(3)
tier_colors = {"🔴 Hot": "red", "🟡 Warm": "amber", "🔵 Cold": "purple"}

for col, (_, row) in zip(tier_cols, tier_df.iterrows()):
    with col:
        render_metric_card(
            row["priority_tier"],
            f"{row['count']:,} leads",
            f"Actual conv: {row['actual_conversion_rate']:.1f}% · Avg score: {row['avg_score']:.0f}%",
            tier_colors.get(row["priority_tier"], "white"),
        )

# Tier conversion comparison chart
fig_tier = go.Figure()
fig_tier.add_trace(go.Bar(
    x=tier_df["priority_tier"],
    y=tier_df["actual_conversion_rate"],
    marker_color=["#DC2626", "#F59E0B", "#6929CA"],
    text=[f"{v:.1f}%" for v in tier_df["actual_conversion_rate"]],
    textposition="outside",
    textfont=dict(color="#0F172A", size=14, family="Plus Jakarta Sans, sans-serif"),
))
fig_tier.update_layout(**get_plotly_layout(
    title=dict(text="Actual Conversion Rate by Priority Tier", font=dict(color="#0F172A")),
    height=350,
    yaxis=dict(title="Conversion Rate (%)", range=[0, tier_df["actual_conversion_rate"].max() * 1.35]),
))
st.plotly_chart(fig_tier, width="stretch")

render_info_box(
    "💡 <b>Hot leads</b> convert at nearly <b>4× the baseline</b> of cold leads. "
    "Routing Hot leads to available reps within 15 minutes captures parent momentum when intent is peak."
)

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 2: Feature Importance
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🔑 Key Drivers of Conversion")

top_n = 15
top_features = feature_imp.head(top_n).copy()

fig_imp = go.Figure()
fig_imp.add_trace(go.Bar(
    y=top_features["feature_display"][::-1],
    x=top_features["coefficient"][::-1],
    orientation="h",
    marker_color=[
        "#10B981" if c > 0 else "#E11D48"
        for c in top_features["coefficient"][::-1]
    ],
    text=[f"{c:+.2f}" for c in top_features["coefficient"][::-1]],
    textposition="outside",
    textfont=dict(color="#0F172A", size=11),
))
fig_imp.update_layout(**get_plotly_layout(
    title=dict(text=f"Top {top_n} Factors Influencing Conversion Probability", font=dict(color="#0F172A")),
    height=500,
    xaxis=dict(title="Model Coefficient (+ = Increases Likelihood, − = Decreases)"),
    margin=dict(l=180),
))
st.plotly_chart(fig_imp, width="stretch")

imp_col1, imp_col2 = st.columns(2)
with imp_col1:
    st.markdown("<h4 style='color:#059669; font-size:1.05rem;'>🟢 Top Positive Drivers</h4>", unsafe_allow_html=True)
    pos = feature_imp[feature_imp["coefficient"] > 0].head(5)
    for _, row in pos.iterrows():
        st.markdown(f"- **{row['feature_display']}** (+{row['coefficient']:.2f})")
with imp_col2:
    st.markdown("<h4 style='color:#DC2626; font-size:1.05rem;'>🔴 Top Friction Factors</h4>", unsafe_allow_html=True)
    neg = feature_imp[feature_imp["coefficient"] < 0].head(5)
    for _, row in neg.iterrows():
        st.markdown(f"- **{row['feature_display']}** ({row['coefficient']:.2f})")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 3: Score Distribution
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📊 Lead Score Distribution")

fig_dist = go.Figure()
fig_dist.add_trace(go.Histogram(
    x=scored_df[scored_df["converted_flag"] == 0]["conversion_score"],
    name="Did Not Convert",
    marker_color="rgba(105, 41, 202, 0.45)",
    nbinsx=50,
))
fig_dist.add_trace(go.Histogram(
    x=scored_df[scored_df["converted_flag"] == 1]["conversion_score"],
    name="Converted Students",
    marker_color="#10B981",
    nbinsx=50,
))
fig_dist.update_layout(**get_plotly_layout(
    title=dict(text="Score Distribution: Enrolled vs Unconverted Leads", font=dict(color="#0F172A")),
    height=380,
    barmode="overlay",
    xaxis=dict(title="Predicted Conversion Probability (%)"),
    yaxis=dict(title="Number of Leads"),
))
st.plotly_chart(fig_dist, width="stretch")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 4: Searchable Lead Table
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📋 Prioritized Lead Queue")

# Filters
f1, f2, f3 = st.columns(3)
with f1:
    tier_filter = st.multiselect("Priority Tier", ["🔴 Hot", "🟡 Warm", "🔵 Cold"], default=["🔴 Hot", "🟡 Warm", "🔵 Cold"])
with f2:
    source_filter = st.multiselect("Lead Source", sorted(scored_df["lead_source"].unique()), default=sorted(scored_df["lead_source"].unique()))
with f3:
    geo_filter = st.multiselect("Geography", sorted(scored_df["geography"].unique()), default=sorted(scored_df["geography"].unique()))

filtered = scored_df[
    (scored_df["priority_tier"].isin(tier_filter)) &
    (scored_df["lead_source"].isin(source_filter)) &
    (scored_df["geography"].isin(geo_filter))
].sort_values("conversion_score", ascending=False)

display_cols = [
    "lead_id", "conversion_score", "priority_tier", "lead_source",
    "geography", "rep_assigned", "follow_up_attempts", "funnel_stage",
]
available_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(
    filtered[available_cols].head(200).rename(columns={
        "lead_id": "Lead ID", "conversion_score": "Score (%)",
        "priority_tier": "Tier", "lead_source": "Source",
        "geography": "Geography", "rep_assigned": "Rep",
        "follow_up_attempts": "Follow-ups", "funnel_stage": "Stage",
    }),
    width="stretch",
    hide_index=True,
    height=500,
)

st.markdown(f"*Showing top {min(200, len(filtered)):,} of {len(filtered):,} matching leads*")

# Download button
csv_data = filtered[available_cols].to_csv(index=False)
st.download_button(
    "⬇️ Download Prioritized Leads CSV",
    csv_data,
    "brightchamps_prioritized_leads.csv",
    "text/csv",
    width="stretch",
)
