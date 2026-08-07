from __future__ import annotations

import pandas as pd


FLAG_SCORE = {
    "measurement_error_suspect": 3,
    "compliance_limit_suspect": 3,
    "current_saturation_suspect": 2,
    "curve_fit_mismatch": 2,
    "diode_current_variation": 2,
    "capacitance_variation": 2,
    "resistance_shift": 1,
}


def _has_value(value: object) -> bool:
    return value is not None and pd.notna(value)


def apply_anomaly_rules(features: pd.DataFrame) -> pd.DataFrame:
    result = features.copy()
    labels: list[str] = []

    for _, row in result.iterrows():
        flags: list[str] = []
        invalid_c_points = row.get("invalid_c_points")
        compliance_suspect = row.get("compliance_suspect")
        compliance_hits = row.get("compliance_hits")
        if _has_value(invalid_c_points) and invalid_c_points > 0:
            flags.append("measurement_error_suspect")
        if _has_value(compliance_suspect) and bool(compliance_suspect):
            flags.append("compliance_limit_suspect")
        if _has_value(compliance_hits) and compliance_hits > 0:
            flags.append("current_saturation_suspect")
        if _has_value(row.get("ifit_mae_a")) and row.get("ifit_mae_a", 0) > 1e-8:
            flags.append("curve_fit_mismatch")
        if "i_at_2v_a" in result.columns and _has_value(row.get("i_at_2v_a")):
            group = result[result["device"].eq(row.get("device"))]["i_at_2v_a"].dropna()
            if len(group) >= 4:
                median = group.median()
                if median and (row["i_at_2v_a"] > median * 1.8 or row["i_at_2v_a"] < median / 1.8):
                    flags.append("diode_current_variation")
        if "c_at_0v_f" in result.columns and _has_value(row.get("c_at_0v_f")):
            group = result[result["device"].eq(row.get("device"))]["c_at_0v_f"].dropna().abs()
            current = abs(row["c_at_0v_f"])
            if len(group) >= 4:
                median = group.median()
                if median and (current > median * 2.0 or current < median / 2.0):
                    flags.append("capacitance_variation")
        if "resistance_ohm" in result.columns and _has_value(row.get("resistance_ohm")):
            group = result[result["device"].eq(row.get("device"))]["resistance_ohm"].dropna()
            if len(group) >= 4:
                median = group.median()
                if median and abs(row["resistance_ohm"] - median) / median > 0.08:
                    flags.append("resistance_shift")
        labels.append(", ".join(flags) if flags else "normal_or_review")

    result["anomaly_flags"] = labels
    result["anomaly_score"] = [
        sum(FLAG_SCORE.get(flag.strip(), 0) for flag in flags.split(",") if flags != "normal_or_review")
        for flags in labels
    ]
    result["review_status"] = pd.cut(
        result["anomaly_score"],
        bins=[-1, 0, 2, 99],
        labels=["normal", "review", "priority"],
    ).astype(str)
    return result
