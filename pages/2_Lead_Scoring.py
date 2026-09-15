"""
Page 2 — Lead Scoring Engine
=============================
ML-powered lead scoring with conversion probability, priority tiers,
feature importance, and downloadable action lists.
"""

import streamlit as st

st.set_page_config(page_title="Lead Scoring", page_icon="🎯", layout="wide")

from utils.styles import (
    inject_custom_css, render_metric_card, render_hero, render_divider,
    render_section_header, render_info_box, CHART_COLORS, get_plotly_layout,
)
from utils.data_loader import load_data
from utils.lead_scorer import train_and_score, get_tier_summary, get_actionable_leads
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

inject_custom_css()

# ── Load & score ──────────────────────────────────────────────────────────
df = load_data()
scored_df, feature_imp, model_info = train_and_score(df)

# ── Header ───────────────────────────────────────────────────────────────
render_hero("🎯 Lead Scoring Engine", "ML-powered conversion probability for every lead")

# ── Model info cards ─────────────────────────────────────────────────────
render_section_header("🤖 Model Performance")

m1, m2, m3, m4 = st.columns(4)
with m1:
    render_metric_card("Model AUC", f"{model_info['cv_auc_mean']:.3f}", "5-fold cross-validated", "gradient")
with m2:
    render_metric_card("Features Used", str(model_info["n_features"]), "Logistic regression", "blue")
with m3:
    render_metric_card("Hot Threshold", f"≥ {model_info['hot_threshold']:.0f}%", "Top 25% of scores", "red")
with m4:
    render_metric_card("Base Conv. Rate", f"{model_info['conversion_rate']:.1f}%", f"{model_info['n_samples']:,} leads", "amber")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 1: Tier Summary
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🏷️ Priority Tier Breakdown")

tier_df = get_tier_summary(scored_df)

tier_cols = st.columns(3)
tier_colors = {"🔴 Hot": "red", "🟡 Warm": "amber", "🔵 Cold": "blue"}

for col, (_, row) in zip(tier_cols, tier_df.iterrows()):
    with col:
        render_metric_card(
            row["priority_tier"],
            f"{row['count']:,} leads",
            f"Actual conv: {row['actual_conversion_rate']:.1f}% · Avg score: {row['avg_score']:.0f}",
            tier_colors.get(row["priority_tier"], "white"),
        )

# Tier conversion comparison chart
fig_tier = go.Figure()
fig_tier.add_trace(go.Bar(
    x=tier_df["priority_tier"],
    y=tier_df["actual_conversion_rate"],
    marker_color=["#FC8181", "#ECC94B", "#63B3ED"],
    text=[f"{v:.1f}%" for v in tier_df["actual_conversion_rate"]],
    textposition="outside",
    textfont=dict(color="#FAFAFA", size=14),
))
fig_tier.update_layout(**get_plotly_layout(
    title=dict(text="Actual Conversion Rate by Priority Tier"),
    height=350,
    yaxis=dict(title="Conversion Rate (%)", range=[0, tier_df["actual_conversion_rate"].max() * 1.3]),
))
st.plotly_chart(fig_tier, width="stretch")

render_info_box(
    "💡 <b>Hot leads</b> convert at a significantly higher rate than cold leads. "
    "Focusing rep effort on Hot leads first can dramatically improve ROI."
)

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 2: Feature Importance
# ══════════════════════════════════════════════════════════════════════════
render_section_header("🔑 What Drives Conversion?")

top_n = 15
top_features = feature_imp.head(top_n).copy()

fig_imp = go.Figure()
fig_imp.add_trace(go.Bar(
    y=top_features["feature_display"][::-1],
    x=top_features["coefficient"][::-1],
    orientation="h",
    marker_color=[
        "#48BB78" if c > 0 else "#FC8181"
        for c in top_features["coefficient"][::-1]
    ],
    text=[f"{c:+.2f}" for c in top_features["coefficient"][::-1]],
    textposition="outside",
    textfont=dict(color="#FAFAFA", size=11),
))
fig_imp.update_layout(**get_plotly_layout(
    title=dict(text=f"Top {top_n} Features by Impact on Conversion"),
    height=500,
    xaxis=dict(title="Coefficient (+ = increases conversion, − = decreases)"),
    margin=dict(l=180),
))
st.plotly_chart(fig_imp, width="stretch")

imp_col1, imp_col2 = st.columns(2)
with imp_col1:
    st.markdown("**🟢 Top Positive Drivers**")
    pos = feature_imp[feature_imp["coefficient"] > 0].head(5)
    for _, row in pos.iterrows():
        st.markdown(f"- **{row['feature_display']}** (+{row['coefficient']:.2f})")
with imp_col2:
    st.markdown("**🔴 Top Negative Drivers**")
    neg = feature_imp[feature_imp["coefficient"] < 0].head(5)
    for _, row in neg.iterrows():
        st.markdown(f"- **{row['feature_display']}** ({row['coefficient']:.2f})")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 3: Score Distribution
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📊 Score Distribution")

fig_dist = go.Figure()
fig_dist.add_trace(go.Histogram(
    x=scored_df[scored_df["converted_flag"] == 0]["conversion_score"],
    name="Not Converted",
    marker_color="rgba(99,179,237,0.5)",
    nbinsx=50,
))
fig_dist.add_trace(go.Histogram(
    x=scored_df[scored_df["converted_flag"] == 1]["conversion_score"],
    name="Converted",
    marker_color="rgba(72,187,120,0.7)",
    nbinsx=50,
))
fig_dist.update_layout(**get_plotly_layout(
    title=dict(text="Score Distribution: Converted vs Not Converted"),
    height=380,
    barmode="overlay",
    xaxis=dict(title="Conversion Score (%)"),
    yaxis=dict(title="Number of Leads"),
))
st.plotly_chart(fig_dist, width="stretch")

render_divider()

# ══════════════════════════════════════════════════════════════════════════
# SECTION 4: Searchable Lead Table
# ══════════════════════════════════════════════════════════════════════════
render_section_header("📋 Scored Lead Table")

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

st.markdown(f"*Showing top {min(200, len(filtered)):,} of {len(filtered):,} filtered leads*")

# Download button
csv_data = filtered[available_cols].to_csv(index=False)
st.download_button(
    "⬇️ Download Scored Leads as CSV",
    csv_data,
    "brightchamps_scored_leads.csv",
    "text/csv",
    width="stretch",
)
