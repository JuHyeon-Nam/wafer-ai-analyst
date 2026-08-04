from __future__ import annotations

import pandas as pd


def apply_anomaly_rules(features: pd.DataFrame) -> pd.DataFrame:
    result = features.copy()
    labels: list[str] = []

    for _, row in result.iterrows():
        flags: list[str] = []
        invalid_c_points = row.get("invalid_c_points")
        compliance_suspect = row.get("compliance_suspect")
        compliance_hits = row.get("compliance_hits")
        if pd.notna(invalid_c_points) and invalid_c_points > 0:
            flags.append("measurement_error_suspect")
        if pd.notna(compliance_suspect) and bool(compliance_suspect):
            flags.append("compliance_limit_suspect")
        if pd.notna(compliance_hits) and compliance_hits > 0:
            flags.append("current_saturation_suspect")
        if pd.notna(row.get("ifit_mae_a")) and row.get("ifit_mae_a", 0) > 1e-8:
            flags.append("curve_fit_mismatch")
        labels.append(", ".join(flags) if flags else "normal_or_review")

    result["anomaly_flags"] = labels
    return result
