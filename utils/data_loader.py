"""
Data loading and preprocessing for the BrightChamps Lead Funnel dataset.
Handles CSV parsing, date conversion, and derived feature engineering.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st


# Timezone-to-shift alignment mapping
# Defines which rep shift is "natural" for each parent timezone
TIMEZONE_SHIFT_MAP = {
    "America/New_York": "US_SHIFT",
    "America/Chicago": "US_SHIFT",
    "America/Denver": "US_SHIFT",
    "America/Los_Angeles": "US_SHIFT",
    "Europe/London": "IST_SHIFT",     # UK business hours overlap with IST evening
    "Asia/Kolkata": "IST_SHIFT",
    "Asia/Dubai": "IST_SHIFT",
    "Asia/Riyadh": "IST_SHIFT",
    "Asia/Ho_Chi_Minh": "SEA_SHIFT",
    "Asia/Singapore": "SEA_SHIFT",
    "Australia/Sydney": "SEA_SHIFT",
}


@st.cache_data(show_spinner="Loading dataset…")
def load_data(filepath: str | None = None) -> pd.DataFrame:
    """Load and preprocess the BrightChamps FDA case dataset.

    Parameters
    ----------
    filepath : str, optional
        Absolute or relative path to the CSV. Defaults to the CSV alongside app.py.

    Returns
    -------
    pd.DataFrame
        Preprocessed DataFrame with derived columns.
    """
    if filepath is None:
        # Try common locations
        candidates = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "BrightChamps_FDA_Case_Dataset.csv"),
            "BrightChamps_FDA_Case_Dataset.csv",
        ]
        for c in candidates:
            if os.path.exists(c):
                filepath = c
                break
        if filepath is None:
            st.error("❌ Could not find `BrightChamps_FDA_Case_Dataset.csv`. Please place it in the project root.")
            st.stop()

    df = pd.read_csv(filepath)

    # ── Parse timestamps ─────────────────────────────────────────────────
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["demo_scheduled_at"] = pd.to_datetime(df["demo_scheduled_at"], errors="coerce")

    # ── Binary flags (1/0) ───────────────────────────────────────────────
    df["has_demo_scheduled"] = df["demo_scheduled_at"].notna().astype(int)
    df["demo_joined_flag"] = (df["demo_joined"] == "Y").astype(int)
    df["demo_completed_flag"] = (df["demo_completed"] == "Y").astype(int)
    df["converted_flag"] = (df["converted"] == "Y").astype(int)

    # ── Scheduling delay (hours) ─────────────────────────────────────────
    df["schedule_delay_hours"] = np.where(
        df["demo_scheduled_at"].notna(),
        (df["demo_scheduled_at"] - df["created_at"]).dt.total_seconds() / 3600,
        np.nan,
    )

    # ── Delay bucket ─────────────────────────────────────────────────────
    conditions = [
        df["schedule_delay_hours"].isna(),
        df["schedule_delay_hours"] < 24,
        df["schedule_delay_hours"] < 48,
        df["schedule_delay_hours"] < 72,
        df["schedule_delay_hours"] >= 72,
    ]
    choices = ["Not Scheduled", "<24 h", "24–48 h", "48–72 h", "72 h+"]
    df["delay_bucket"] = np.select(conditions, choices, default="Unknown")

    # ── Funnel stage (furthest stage reached) ────────────────────────────
    df["funnel_stage"] = np.select(
        [
            df["converted_flag"] == 1,
            df["demo_completed_flag"] == 1,
            df["demo_joined_flag"] == 1,
            df["has_demo_scheduled"] == 1,
        ],
        ["Converted", "Demo Completed", "Demo Joined", "Demo Scheduled"],
        default="Lead Only",
    )

    # ── Time features ────────────────────────────────────────────────────
    df["created_hour"] = df["created_at"].dt.hour
    df["created_dow"] = df["created_at"].dt.day_name()
    df["created_date"] = df["created_at"].dt.date

    # ── Timezone alignment ───────────────────────────────────────────────
    df["ideal_shift"] = df["parent_timezone"].map(TIMEZONE_SHIFT_MAP)
    df["timezone_aligned"] = (df["rep_shift"] == df["ideal_shift"]).astype(int)

    return df


def get_date_range(df: pd.DataFrame) -> tuple:
    """Return (min_date, max_date) from the created_at column."""
    return df["created_at"].min(), df["created_at"].max()


def get_months_span(df: pd.DataFrame) -> float:
    """Return the number of months the dataset covers (used for monthly projections)."""
    min_dt, max_dt = get_date_range(df)
    days = (max_dt - min_dt).days
    return max(days / 30.0, 1.0)  # at least 1 month
