from __future__ import annotations

import pandas as pd


FEATURE_GROUPS = {
    "capacitance": (
        "c_at_0v_f",
        "c_max_f",
        "c_min_f",
        "c_range_f",
        "c_abs_max_raw_f",
        "invalid_c_points",
        "g_or_r_median",
    ),
    "diode_iv": (
        "i_at_0v_a",
        "i_at_0_7v_a",
        "i_at_1v_a",
        "i_at_2v_a",
        "i_max_a",
        "i_min_a",
        "v_at_10na_v",
        "v_at_100na_v",
        "v_at_1ua_v",
        "ifit_mae_a",
        "ifit_max_abs_error_a",
    ),
    "resistor_iv": (
        "resistance_ohm",
        "conductance_s",
        "fit_intercept_a",
        "iv_linearity_r2",
        "fit_points",
        "i_at_3v_a",
        "i_at_minus_3v_a",
        "compliance_hits",
    ),
    "nmos_idvg": (
        "drain_v_mean_v",
        "gate_v_min_v",
        "gate_v_max_v",
        "drain_i_mean_a",
        "drain_i_span_a",
        "drain_i_at_gate_0v_a",
        "gate_leak_abs_max_a",
    ),
    "device_indicator": ("device_",),
    "missing_indicator": ("_missing",),
}

FEATURE_EXPLANATIONS = {
    "drain_i_span_a": "NMOS Id-Vg curve에서 drain current가 얼마나 변했는지 보는 값입니다. channel 동작 변화나 compliance 후보와 연결됩니다.",
    "invalid_c_points": "Capacitor C-V 측정에서 물리적으로 이상한 capacitance point가 얼마나 나왔는지 보는 값입니다.",
    "i_at_0v_a": "Diode 0V 근처 전류입니다. 역방향/저전압 leakage 후보를 볼 때 사용됩니다.",
    "ifit_mae_a_missing": "Diode fitting error column의 결측 여부입니다. 특정 소자에서만 생기는 column 구조 차이를 모델이 구분에 사용한 신호입니다.",
    "gate_leak_abs_max_a": "NMOS gate에 새는 전류의 최대값입니다. gate oxide 또는 surface leakage 후보를 볼 때 중요합니다.",
    "ifit_max_abs_error_a_missing": "Diode fitting 최대 오차 column의 결측 여부입니다. 실제 물리량이라기보다 소자/측정 schema 구분 신호에 가깝습니다.",
    "c_abs_max_raw_f": "Capacitor raw C 값의 절대 최대값입니다. range 오류, probe contact, 저장 artifact 후보와 연결됩니다.",
    "compliance_hits": "전류가 장비 제한값 근처에 걸린 point 수입니다. compliance limit 또는 contact 영향 후보와 연결됩니다.",
    "i_at_3v_a": "Resistor 또는 diode curve에서 3V 지점 전류입니다. 저항 변화나 slope 변화를 볼 때 사용됩니다.",
    "i_at_0_7v_a": "Diode forward 동작을 보는 대표 전류 지점입니다.",
    "device_diode": "입력 row가 diode 측정인지 알려주는 one-hot feature입니다.",
    "resistance_ohm": "Resistor I-V curve slope로 계산한 저항값입니다.",
    "iv_linearity_r2": "Resistor I-V curve가 얼마나 직선에 가까운지 보는 값입니다. 낮으면 contact, self-heating, compliance 후보를 확인합니다.",
    "i_at_minus_3v_a": "음전압 -3V 지점 전류입니다. resistor slope 대칭성과 leakage 성향을 볼 때 사용됩니다.",
    "conductance_s": "저항의 반대 개념인 conductance입니다. 전류가 얼마나 쉽게 흐르는지 나타냅니다.",
    "c_range_f": "Capacitor C-V sweep 동안 capacitance가 얼마나 변했는지 보는 값입니다.",
    "c_at_0v_f": "Capacitor 0V 지점 capacitance입니다. 박막 두께나 유전 특성 변화 후보를 볼 때 사용됩니다.",
    "c_max_f": "Capacitor sweep에서 가장 큰 유효 capacitance 값입니다.",
}


def classify_feature_group(feature: str) -> str:
    if feature.endswith("_missing"):
        return "missing_indicator"
    for group, patterns in FEATURE_GROUPS.items():
        if group == "missing_indicator":
            continue
        for pattern in patterns:
            if pattern.endswith("_"):
                if feature.startswith(pattern):
                    return group
            elif feature == pattern or feature.startswith(f"{pattern}_"):
                return group
    return "other"


def summarize_feature_importance(importance: pd.DataFrame, top_n: int = 20) -> tuple[pd.DataFrame, pd.DataFrame]:
    ranked = importance.copy()
    ranked["feature_group"] = ranked["feature"].map(classify_feature_group)
    ranked["plain_explanation"] = ranked["feature"].map(
        lambda feature: FEATURE_EXPLANATIONS.get(feature, "모델이 defect label을 나눌 때 사용한 electrical/statistical feature입니다.")
    )
    ranked = ranked.sort_values("importance", ascending=False).reset_index(drop=True)

    group_summary = (
        ranked.groupby("feature_group", as_index=False)["importance"]
        .sum()
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    group_summary["importance_share"] = group_summary["importance"] / group_summary["importance"].sum()

    return ranked.head(top_n), group_summary


def feature_importance_report_markdown(importance: pd.DataFrame) -> str:
    top, group_summary = summarize_feature_importance(importance, top_n=20)
    top_display = top.copy()
    top_display["importance"] = top_display["importance"].map(lambda value: f"{float(value):.4f}")
    group_display = group_summary.copy()
    group_display["importance"] = group_display["importance"].map(lambda value: f"{float(value):.4f}")
    group_display["importance_share"] = group_display["importance_share"].map(lambda value: f"{float(value) * 100:.1f}%")

    lines = [
        "# Feature Importance Analysis",
        "",
        "## Summary",
        "",
        "RandomForest tuned model이 defect scenario를 분류할 때 어떤 feature를 많이 봤는지 정리했습니다.",
        "이 결과는 실제 공정 원인을 확정하는 근거가 아니라, 어떤 전기 측정 항목을 먼저 리뷰할지 정하는 우선순위 근거입니다.",
        "",
        "## Importance by Feature Group",
        "",
        _markdown_table(group_display),
        "",
        "## Top Features",
        "",
        _markdown_table(top_display[["feature", "feature_group", "importance", "plain_explanation"]]),
        "",
        "## Engineering Interpretation",
        "",
        "- `invalid_c_points`, `c_abs_max_raw_f`가 높게 나오면 capacitor C-V 측정에서 range/probe/data artifact 후보를 먼저 확인합니다.",
        "- `gate_leak_abs_max_a`가 높게 나오면 NMOS gate leakage 또는 gate oxide 관련 후보를 먼저 확인합니다.",
        "- `compliance_hits`가 높게 나오면 장비 compliance limit, contact resistance, high-current saturation 후보를 확인합니다.",
        "- `_missing` feature가 높게 나오면 물리 현상 자체보다 device별 column 구조 차이를 모델이 사용했을 수 있으므로 해석에 주의합니다.",
        "",
        "## Interview Story",
        "",
        "단순히 정확도만 확인하지 않고, feature importance를 통해 모델이 어떤 전기적 지표를 근거로 판단했는지 검토했습니다.",
        "특히 missing indicator가 상위에 등장하는 경우 label leakage는 아니지만 device schema 구분 신호가 될 수 있어, 해석 가능한 feature와 schema feature를 분리해서 보았습니다.",
    ]
    return "\n".join(lines) + "\n"


def _markdown_table(frame: pd.DataFrame) -> str:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)
