from __future__ import annotations

import pandas as pd


FLAG_SCORE = {
    "measurement_error_suspect": 3,
    "raw_capacitance_outlier": 3,
    "compliance_limit_suspect": 3,
    "current_saturation_suspect": 2,
    "curve_fit_mismatch": 2,
    "diode_current_variation": 2,
    "leakage_current_suspect": 2,
    "gate_leakage_suspect": 2,
    "capacitance_variation": 2,
    "resistor_linearity_drop": 2,
    "nmos_current_span_suspect": 1,
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
        raw_capacitance = row.get("c_abs_max_raw_f")
        compliance_suspect = row.get("compliance_suspect")
        compliance_hits = row.get("compliance_hits")
        if _has_value(invalid_c_points) and invalid_c_points > 0:
            flags.append("measurement_error_suspect")
        if _has_value(raw_capacitance) and abs(raw_capacitance) > 1e-6:
            flags.append("raw_capacitance_outlier")
        if _has_value(compliance_suspect) and bool(compliance_suspect):
            flags.append("compliance_limit_suspect")
        if _has_value(compliance_hits) and compliance_hits > 0:
            flags.append("current_saturation_suspect")
        if _has_value(row.get("ifit_mae_a")) and row.get("ifit_mae_a", 0) > 1e-8:
            flags.append("curve_fit_mismatch")
        if _has_value(row.get("i_at_0v_a")) and abs(row.get("i_at_0v_a", 0)) > 2e-8:
            flags.append("leakage_current_suspect")
        if _has_value(row.get("gate_leak_abs_max_a")) and row.get("gate_leak_abs_max_a", 0) > 1e-6:
            flags.append("gate_leakage_suspect")
        if _has_value(row.get("iv_linearity_r2")) and row.get("iv_linearity_r2", 1) < 0.98:
            flags.append("resistor_linearity_drop")
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
        if "drain_i_span_a" in result.columns and _has_value(row.get("drain_i_span_a")):
            group = result[result["device"].eq(row.get("device"))]["drain_i_span_a"].dropna()
            if len(group) >= 4:
                median = group.median()
                if median and row["drain_i_span_a"] > median * 3.0:
                    flags.append("nmos_current_span_suspect")
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
