from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DefectScenario:
    label: str
    device: str | None
    description: str
    modified_features: tuple[str, ...]


SCENARIOS = [
    DefectScenario(
        label="normal",
        device=None,
        description="Small measurement variation around the original feature distribution.",
        modified_features=(),
    ),
    DefectScenario(
        label="diode_leakage",
        device="diode",
        description="Low-bias diode current is increased to simulate leakage path behavior.",
        modified_features=("i_at_0v_a", "i_at_0_7v_a", "i_min_a"),
    ),
    DefectScenario(
        label="diode_contact_issue",
        device="diode",
        description="Diode fitting residual is increased to mimic unstable probe/contact behavior.",
        modified_features=("ifit_mae_a", "ifit_max_abs_error_a"),
    ),
    DefectScenario(
        label="resistance_shift",
        device="resistor",
        description="Resistance is shifted by changing the effective I-V slope.",
        modified_features=("resistance_ohm", "conductance_s", "i_at_3v_a", "i_at_minus_3v_a"),
    ),
    DefectScenario(
        label="resistor_nonlinearity",
        device="resistor",
        description="I-V linearity is reduced and high-current compliance hits are introduced.",
        modified_features=("iv_linearity_r2", "compliance_hits"),
    ),
    DefectScenario(
        label="capacitance_variation",
        device="Cap",
        description="Capacitance level is shifted to mimic oxide/deposition thickness variation.",
        modified_features=("c_at_0v_f", "c_max_f", "c_min_f", "c_range_f"),
    ),
    DefectScenario(
        label="capacitance_outlier",
        device="Cap",
        description="Raw CV value spike is injected to mimic range/probe/data artifact behavior.",
        modified_features=("c_abs_max_raw_f", "invalid_c_points"),
    ),
    DefectScenario(
        label="nmos_gate_leakage",
        device="NMOS",
        description="Gate leakage is increased to mimic gate oxide or surface leakage weakness.",
        modified_features=("gate_leak_abs_max_a",),
    ),
    DefectScenario(
        label="nmos_compliance_limit",
        device="NMOS",
        description="Drain current behavior is pushed toward compliance-limited operation.",
        modified_features=("drain_i_mean_a", "drain_i_span_a", "compliance_suspect"),
    ),
]

SCENARIO_BY_LABEL = {scenario.label: scenario for scenario in SCENARIOS}

EXPECTED_FLAGS = {
    "normal": "normal_or_review",
    "diode_leakage": "leakage_current_suspect",
    "diode_contact_issue": "curve_fit_mismatch",
    "resistance_shift": "resistance_shift",
    "resistor_nonlinearity": "resistor_linearity_drop, current_saturation_suspect",
    "capacitance_variation": "capacitance_variation",
    "capacitance_outlier": "measurement_error_suspect, raw_capacitance_outlier",
    "nmos_gate_leakage": "gate_leakage_suspect",
    "nmos_compliance_limit": "compliance_limit_suspect",
}

NON_FEATURE_COLUMNS = {
    "source",
    "source_file",
    "measurement_id",
    "measurement_name",
    "test_name",
    "site_coordinate",
    "last_executed",
    "sweep_mode",
    "current_range",
    "compliance",
    "parse_warning",
    "anomaly_flags",
    "anomaly_score",
    "review_status",
    "process_issue_candidates",
    "beginner_explanation",
    "engineer_explanation",
    "llm_prompt",
}


def scenario_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "scenario_label": scenario.label,
            "target_device": scenario.device or "all",
            "description": scenario.description,
            "modified_features": ", ".join(scenario.modified_features) or "light feature jitter",
            "expected_anomaly_flags": EXPECTED_FLAGS[scenario.label],
        }
        for scenario in SCENARIOS
    )


def _finite_number(value: object) -> bool:
    try:
        return pd.notna(value) and np.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _scale(row: pd.Series, column: str, factor: float) -> None:
    if column in row and _finite_number(row[column]):
        row[column] = float(row[column]) * factor


def _set_range(row: pd.Series, column: str, rng: np.random.Generator, low: float, high: float) -> None:
    row[column] = float(rng.uniform(low, high))


def _jitter_features(row: pd.Series, rng: np.random.Generator, noise: float = 0.035) -> None:
    for column, value in row.items():
        if column in NON_FEATURE_COLUMNS:
            continue
        if (
            pd.notna(value)
            and not isinstance(value, (bool, np.bool_))
            and isinstance(value, (int, float, np.integer, np.floating))
            and np.isfinite(value)
        ):
            if abs(float(value)) > 0:
                row[column] = float(value) * float(rng.normal(1.0, noise))


def _apply_scenario(row: pd.Series, scenario: DefectScenario, rng: np.random.Generator) -> None:
    _jitter_features(row, rng)

    if scenario.label == "normal":
        return

    if scenario.label == "diode_leakage":
        _set_range(row, "i_at_0v_a", rng, 2.1e-8, 8.0e-8)
        _scale(row, "i_at_0v_a", float(rng.uniform(2.5, 6.0)))
        _scale(row, "i_at_0_7v_a", float(rng.uniform(1.8, 4.0)))
        _scale(row, "i_min_a", float(rng.uniform(1.5, 3.0)))
        return

    if scenario.label == "diode_contact_issue":
        if "ifit_mae_a" not in row or not _finite_number(row.get("ifit_mae_a")):
            row["ifit_mae_a"] = float(rng.uniform(1.2e-8, 6.0e-8))
        if "ifit_max_abs_error_a" not in row or not _finite_number(row.get("ifit_max_abs_error_a")):
            row["ifit_max_abs_error_a"] = float(rng.uniform(2.0e-8, 1.2e-7))
        _scale(row, "ifit_mae_a", float(rng.uniform(2.5, 8.0)))
        _scale(row, "ifit_max_abs_error_a", float(rng.uniform(2.0, 6.0)))
        _scale(row, "i_at_2v_a", float(rng.uniform(0.65, 1.45)))
        return

    if scenario.label == "resistance_shift":
        factor = float(rng.choice([rng.uniform(0.65, 0.85), rng.uniform(1.18, 1.55)]))
        _scale(row, "resistance_ohm", factor)
        if "conductance_s" in row and _finite_number(row.get("resistance_ohm")) and row["resistance_ohm"] != 0:
            row["conductance_s"] = 1.0 / float(row["resistance_ohm"])
        _scale(row, "i_at_3v_a", 1.0 / factor)
        _scale(row, "i_at_minus_3v_a", 1.0 / factor)
        return

    if scenario.label == "resistor_nonlinearity":
        _set_range(row, "iv_linearity_r2", rng, 0.84, 0.975)
        if "compliance_hits" in row:
            row["compliance_hits"] = int(rng.integers(4, 35))
        return

    if scenario.label == "capacitance_variation":
        factor = float(rng.choice([rng.uniform(0.45, 0.75), rng.uniform(1.35, 2.2)]))
        for column in ("c_at_0v_f", "c_max_f", "c_min_f", "c_range_f"):
            _scale(row, column, factor)
        return

    if scenario.label == "capacitance_outlier":
        if "c_abs_max_raw_f" in row:
            row["c_abs_max_raw_f"] = float(rng.choice([1e-3, 1e-1, 1e3, 1e12, 1e30]))
        if "invalid_c_points" in row:
            row["invalid_c_points"] = int(rng.integers(1, 12))
        return

    if scenario.label == "nmos_gate_leakage":
        _scale(row, "gate_leak_abs_max_a", float(rng.uniform(2.5, 7.5)))
        return

    if scenario.label == "nmos_compliance_limit":
        _set_range(row, "drain_i_mean_a", rng, 0.096, 0.105)
        _set_range(row, "drain_i_span_a", rng, 1e-8, 2.5e-7)
        if "compliance_suspect" in row:
            row["compliance_suspect"] = True


def generate_synthetic_features(
    real_features: pd.DataFrame,
    samples_per_scenario: int = 80,
    random_state: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    rows: list[pd.Series] = []

    for scenario in SCENARIOS:
        candidates = real_features
        if scenario.device:
            candidates = real_features[real_features["device"].eq(scenario.device)]
        if candidates.empty:
            continue

        for idx in range(samples_per_scenario):
            seed = candidates.sample(n=1, replace=True, random_state=int(rng.integers(0, 1_000_000))).iloc[0].copy()
            seed_measurement_id = seed.get("measurement_id", f"row-{idx}")
            _apply_scenario(seed, scenario, rng)
            synthetic_id = f"{scenario.label}-{idx + 1:04d}"
            seed["data_source"] = "synthetic"
            seed["seed_measurement_id"] = seed_measurement_id
            seed["synthetic_id"] = synthetic_id
            seed["measurement_id"] = synthetic_id
            seed["source"] = "synthetic"
            seed["source_file"] = "synthetic_features"
            seed["scenario_label"] = scenario.label
            seed["scenario_description"] = scenario.description
            seed["modified_features"] = ", ".join(scenario.modified_features) or "light feature jitter"
            seed["expected_anomaly_flags"] = EXPECTED_FLAGS[scenario.label]
            for column in [
                "anomaly_flags",
                "anomaly_score",
                "review_status",
                "process_issue_candidates",
                "beginner_explanation",
                "engineer_explanation",
                "llm_prompt",
            ]:
                if column in seed:
                    seed[column] = pd.NA
            rows.append(seed)

    return pd.DataFrame(rows).reset_index(drop=True)
