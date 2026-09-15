"""
Funnel analysis and ₹ leak quantification engine.

Provides stage-by-stage conversion rates, monetary leak sizing,
and segmented funnel analysis for the BrightChamps dataset.
"""

import pandas as pd
import numpy as np

# ── Financial constants (from the case brief) ─────────────────────────────
REVENUE_PER_CONVERSION = 60_000   # ₹60,000 per converted customer
COST_PER_LEAD = 900               # ₹900 blended marketing cost per lead

# ── Funnel stage definitions (in order) ───────────────────────────────────
FUNNEL_STAGES = [
    "Lead Created",
    "Demo Scheduled",
    "Demo Joined",
    "Demo Completed",
    "Converted",
]


def get_funnel_counts(df: pd.DataFrame) -> dict:
    """Return absolute counts at each funnel stage.

    Returns
    -------
    dict
        {"Lead Created": N, "Demo Scheduled": N, ...}
    """
    return {
        "Lead Created": len(df),
        "Demo Scheduled": int(df["has_demo_scheduled"].sum()),
        "Demo Joined": int(df["demo_joined_flag"].sum()),
        "Demo Completed": int(df["demo_completed_flag"].sum()),
        "Converted": int(df["converted_flag"].sum()),
    }


def get_funnel_rates(counts: dict) -> dict:
    """Return stage-to-stage conversion rates and cumulative rates.

    Returns
    -------
    dict
        Keys: stage names.  Values: dict with "count", "stage_rate", "cumulative_rate".
    """
    stages = list(counts.keys())
    result = {}
    for i, stage in enumerate(stages):
        count = counts[stage]
        cumulative = count / counts[stages[0]] if counts[stages[0]] else 0
        if i == 0:
            stage_rate = 1.0
        else:
            prev_count = counts[stages[i - 1]]
            stage_rate = count / prev_count if prev_count else 0
        result[stage] = {
            "count": count,
            "stage_rate": stage_rate,
            "cumulative_rate": cumulative,
        }
    return result


def calculate_leak_values(df: pd.DataFrame, months: float = 2.0) -> list[dict]:
    """Quantify the ₹ leaked at each funnel transition.

    For each drop-off stage, estimates how much revenue would have been earned
    if those leads had continued at the downstream conversion rate.

    Parameters
    ----------
    df : pd.DataFrame
        The preprocessed dataset.
    months : float
        Number of months the data spans (for monthly projection).

    Returns
    -------
    list of dict
        Each dict: {stage_from, stage_to, leads_lost, downstream_conversion_rate,
                     potential_conversions, revenue_leaked_total, revenue_leaked_monthly,
                     marketing_waste_total, marketing_waste_monthly}
    """
    counts = get_funnel_counts(df)
    total_converted = counts["Converted"]

    # Downstream conversion rates:
    # If a lead reaches stage X, what % eventually convert?
    downstream_rates = {
        "Demo Scheduled": total_converted / counts["Demo Scheduled"] if counts["Demo Scheduled"] else 0,
        "Demo Joined": total_converted / counts["Demo Joined"] if counts["Demo Joined"] else 0,
        "Demo Completed": total_converted / counts["Demo Completed"] if counts["Demo Completed"] else 0,
    }

    transitions = [
        ("Lead Created", "Demo Scheduled", "Demo Scheduled"),
        ("Demo Scheduled", "Demo Joined", "Demo Joined"),
        ("Demo Joined", "Demo Completed", "Demo Completed"),
        ("Demo Completed", "Converted", None),  # final stage – use close rate
    ]

    leaks = []
    for stage_from, stage_to, downstream_key in transitions:
        leads_lost = counts[stage_from] - counts[stage_to]
        if downstream_key:
            dcr = downstream_rates[downstream_key]
        else:
            dcr = 1.0  # at the final stage, each lost lead IS a lost conversion

        potential_conversions = leads_lost * dcr
        revenue_leaked = potential_conversions * REVENUE_PER_CONVERSION
        marketing_waste = leads_lost * COST_PER_LEAD

        leaks.append({
            "stage_from": stage_from,
            "stage_to": stage_to,
            "leads_lost": leads_lost,
            "downstream_conversion_rate": dcr,
            "potential_conversions": round(potential_conversions, 1),
            "revenue_leaked_total": revenue_leaked,
            "revenue_leaked_monthly": revenue_leaked / months,
            "marketing_waste_total": marketing_waste,
            "marketing_waste_monthly": marketing_waste / months,
        })
    return leaks


def get_total_leak_monthly(leaks: list[dict]) -> float:
    """Sum all monthly revenue leaks."""
    return sum(l["revenue_leaked_monthly"] for l in leaks)


def get_biggest_leak(leaks: list[dict]) -> dict:
    """Return the single biggest leak by monthly revenue."""
    return max(leaks, key=lambda l: l["revenue_leaked_monthly"])


def get_segmented_funnel(df: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    """Return funnel counts and conversion rates segmented by a column.

    Parameters
    ----------
    df : pd.DataFrame
    segment_col : str
        Column to segment by (e.g., "lead_source", "geography").

    Returns
    -------
    pd.DataFrame
        Columns: segment, lead_count, demo_scheduled, demo_joined,
                 demo_completed, converted, conversion_rate
    """
    rows = []
    for seg_val, grp in df.groupby(segment_col):
        total = len(grp)
        rows.append({
            "segment": seg_val,
            "lead_count": total,
            "demo_scheduled": int(grp["has_demo_scheduled"].sum()),
            "demo_joined": int(grp["demo_joined_flag"].sum()),
            "demo_completed": int(grp["demo_completed_flag"].sum()),
            "converted": int(grp["converted_flag"].sum()),
            "conversion_rate": grp["converted_flag"].mean(),
            "schedule_rate": grp["has_demo_scheduled"].mean(),
            "join_rate": grp["demo_joined_flag"].mean(),
        })
    result = pd.DataFrame(rows).sort_values("conversion_rate", ascending=False)
    return result


def get_delay_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze conversion rates by scheduling delay bucket.

    Returns
    -------
    pd.DataFrame
        Columns: delay_bucket, lead_count, demo_joined, conversion_rate, join_rate
    """
    bucket_order = ["<24 h", "24–48 h", "48–72 h", "72 h+", "Not Scheduled"]
    rows = []
    for bucket in bucket_order:
        sub = df[df["delay_bucket"] == bucket]
        if len(sub) == 0:
            continue
        rows.append({
            "delay_bucket": bucket,
            "lead_count": len(sub),
            "demo_joined": int(sub["demo_joined_flag"].sum()),
            "converted": int(sub["converted_flag"].sum()),
            "join_rate": sub["demo_joined_flag"].mean(),
            "conversion_rate": sub["converted_flag"].mean(),
        })
    return pd.DataFrame(rows)


def get_timezone_alignment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Compare conversion rates for timezone-aligned vs misaligned lead–rep pairs.

    Returns
    -------
    pd.DataFrame
        Columns: alignment, lead_count, conversion_rate, join_rate, schedule_rate
    """
    rows = []
    for aligned, label in [(1, "Aligned"), (0, "Misaligned")]:
        sub = df[df["timezone_aligned"] == aligned]
        if len(sub) == 0:
            continue
        rows.append({
            "alignment": label,
            "lead_count": len(sub),
            "schedule_rate": sub["has_demo_scheduled"].mean(),
            "join_rate": sub["demo_joined_flag"].mean(),
            "conversion_rate": sub["converted_flag"].mean(),
        })
    return pd.DataFrame(rows)
