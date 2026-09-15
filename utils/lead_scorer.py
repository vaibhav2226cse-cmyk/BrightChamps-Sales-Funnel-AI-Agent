"""
Lead scoring model for the BrightChamps funnel.

Trains a lightweight logistic-regression model on historical data and
scores each lead with a conversion probability + priority tier.
"""

import pandas as pd
import numpy as np
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score


# Feature columns used for scoring
CATEGORICAL_FEATURES = ["lead_source", "geography", "rep_shift"]
NUMERIC_FEATURES = ["follow_up_attempts", "schedule_delay_hours_filled", "has_demo_scheduled", "created_hour", "timezone_aligned"]


def _prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features for the scoring model.

    Parameters
    ----------
    df : pd.DataFrame
        The preprocessed dataset (output of data_loader.load_data).

    Returns
    -------
    pd.DataFrame
        Feature matrix ready for model training / scoring.
    """
    feat = pd.DataFrame(index=df.index)

    # Numeric features
    feat["follow_up_attempts"] = df["follow_up_attempts"]
    feat["has_demo_scheduled"] = df["has_demo_scheduled"]
    feat["created_hour"] = df["created_hour"]
    feat["timezone_aligned"] = df["timezone_aligned"]

    # Fill NaN schedule delay with a high sentinel value (lead never got scheduled)
    median_delay = df.loc[df["schedule_delay_hours"].notna(), "schedule_delay_hours"].median()
    feat["schedule_delay_hours_filled"] = df["schedule_delay_hours"].fillna(median_delay * 3)

    # One-hot encode categoricals
    for col in CATEGORICAL_FEATURES:
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
        feat = pd.concat([feat, dummies], axis=1)

    return feat


@st.cache_data(show_spinner="Training lead scoring model…")
def train_and_score(_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Train a logistic regression model and score all leads.

    Parameters
    ----------
    _df : pd.DataFrame
        The preprocessed dataset.

    Returns
    -------
    scored_df : pd.DataFrame
        Original df with added columns: conversion_score, priority_tier.
    feature_importance : pd.DataFrame
        Feature importance (coefficient magnitude), sorted descending.
    model_info : dict
        Model metadata (accuracy, cross-val score, etc.)
    """
    df = _df.copy()
    X = _prepare_features(df)
    y = df["converted_flag"].values

    # Standardize numeric features for stable logistic regression
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.values.astype(float))

    # Train logistic regression with class_weight to handle imbalance
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        C=1.0,
        random_state=42,
    )
    model.fit(X_scaled, y)

    # Cross-validation score
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring="roc_auc")

    # Score all leads
    probabilities = model.predict_proba(X_scaled)[:, 1]
    df["conversion_score"] = np.round(probabilities * 100, 1)

    # Assign priority tiers based on percentiles
    p75 = np.percentile(probabilities, 75)
    p40 = np.percentile(probabilities, 40)
    df["priority_tier"] = np.where(
        probabilities >= p75, "🔴 Hot",
        np.where(probabilities >= p40, "🟡 Warm", "🔵 Cold")
    )

    # Feature importance
    coef_df = pd.DataFrame({
        "feature": X.columns,
        "coefficient": model.coef_[0],
        "abs_coefficient": np.abs(model.coef_[0]),
    }).sort_values("abs_coefficient", ascending=False)

    # Clean up feature names for display
    coef_df["feature_display"] = (
        coef_df["feature"]
        .str.replace("lead_source_", "Source: ", regex=False)
        .str.replace("geography_", "Geo: ", regex=False)
        .str.replace("rep_shift_", "Shift: ", regex=False)
        .str.replace("_", " ", regex=False)
        .str.title()
    )

    model_info = {
        "cv_auc_mean": round(cv_scores.mean(), 3),
        "cv_auc_std": round(cv_scores.std(), 3),
        "n_features": X.shape[1],
        "n_samples": X.shape[0],
        "conversion_rate": round(y.mean() * 100, 1),
        "hot_threshold": round(p75 * 100, 1),
        "warm_threshold": round(p40 * 100, 1),
    }

    return df, coef_df, model_info


def get_tier_summary(scored_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize lead counts and conversion rates by priority tier.

    Returns
    -------
    pd.DataFrame
        Columns: priority_tier, count, actual_conversion_rate, avg_score
    """
    rows = []
    for tier in ["🔴 Hot", "🟡 Warm", "🔵 Cold"]:
        sub = scored_df[scored_df["priority_tier"] == tier]
        if len(sub) == 0:
            continue
        rows.append({
            "priority_tier": tier,
            "count": len(sub),
            "actual_conversion_rate": round(sub["converted_flag"].mean() * 100, 1),
            "avg_score": round(sub["conversion_score"].mean(), 1),
        })
    return pd.DataFrame(rows)


def get_actionable_leads(scored_df: pd.DataFrame, tier: str = "🔴 Hot", limit: int = 50) -> pd.DataFrame:
    """Return top leads for a given tier with actionable information.

    Returns
    -------
    pd.DataFrame
        Subset of scored_df with key columns, sorted by score descending.
    """
    cols = [
        "lead_id", "conversion_score", "priority_tier", "lead_source",
        "geography", "parent_timezone", "rep_assigned", "rep_shift",
        "follow_up_attempts", "funnel_stage", "timezone_aligned",
    ]
    available_cols = [c for c in cols if c in scored_df.columns]
    return (
        scored_df[scored_df["priority_tier"] == tier]
        .sort_values("conversion_score", ascending=False)
        .head(limit)[available_cols]
        .reset_index(drop=True)
    )
