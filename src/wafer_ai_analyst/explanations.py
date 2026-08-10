from __future__ import annotations

from typing import Any

import pandas as pd

from .process_reasoning import infer_process_candidates


FLAG_LABELS = {
    "measurement_error_suspect": "measurement error suspect",
    "raw_capacitance_outlier": "raw capacitance outlier",
    "compliance_limit_suspect": "compliance limit suspect",
    "current_saturation_suspect": "current saturation suspect",
    "curve_fit_mismatch": "curve fit mismatch",
    "diode_current_variation": "diode current variation",
    "leakage_current_suspect": "leakage current suspect",
    "gate_leakage_suspect": "gate leakage suspect",
    "capacitance_variation": "capacitance variation",
    "resistance_shift": "resistance shift",
    "resistor_linearity_drop": "resistor linearity drop",
    "nmos_current_span_suspect": "NMOS current span suspect",
}


BEGINNER_MEANINGS = {
    "measurement_error_suspect": "측정값 자체가 비정상적으로 튄 흔적이 있습니다.",
    "raw_capacitance_outlier": "커패시터 값이 물리적으로 보기 어려울 만큼 크게 튄 지점이 있습니다.",
    "compliance_limit_suspect": "장비가 허용 전류 한계에 걸려 실제 곡선이 눌렸을 가능성이 있습니다.",
    "current_saturation_suspect": "전류가 어느 지점부터 더 자연스럽게 증가하지 않고 막힌 모습입니다.",
    "curve_fit_mismatch": "실제 측정 곡선과 기준 fitting 곡선의 차이가 큽니다.",
    "diode_current_variation": "같은 diode인데 shot 위치에 따라 전류 흐름이 다릅니다.",
    "leakage_current_suspect": "원래 작아야 하는 누설 전류가 상대적으로 커 보입니다.",
    "gate_leakage_suspect": "NMOS gate 쪽으로 새는 전류가 커 보입니다.",
    "capacitance_variation": "같은 capacitor인데 shot 위치에 따라 capacitance가 다릅니다.",
    "resistance_shift": "같은 resistor인데 shot 위치에 따라 저항값이 달라졌습니다.",
    "resistor_linearity_drop": "저항 소자의 I-V 곡선이 직선에서 벗어났습니다.",
    "nmos_current_span_suspect": "NMOS 전류 변화폭이 다른 shot보다 크게 보입니다.",
}


ENGINEER_ACTIONS = {
    "measurement_error_suspect": "raw curve와 측정 range, probe contact 로그를 우선 확인",
    "raw_capacitance_outlier": "CV raw point, open/short correction, parsing artifact 여부 확인",
    "compliance_limit_suspect": "SMU compliance setting과 short/open 재측정 필요",
    "current_saturation_suspect": "I-V curve의 high-current 구간과 contact resistance 확인",
    "curve_fit_mismatch": "diode fitting residual과 forward bias 구간 재검토",
    "diode_current_variation": "shot 위치별 junction/contact/CD 조건 비교",
    "leakage_current_suspect": "zero/low-bias leakage와 surface contamination 가능성 확인",
    "gate_leakage_suspect": "gate oxide leakage, probe mark, Vg sweep 조건 확인",
    "capacitance_variation": "oxide thickness, deposition uniformity, etch loading 조건 비교",
    "resistance_shift": "film thickness, line width, contact resistance split 비교",
    "resistor_linearity_drop": "fit exclusion 구간과 thermal/compliance 영향 확인",
    "nmos_current_span_suspect": "Vth shift, channel variation, local leakage path 확인",
}


def _flags(value: Any) -> list[str]:
    if not value or pd.isna(value) or value == "normal_or_review":
        return []
    return [flag.strip() for flag in str(value).split(",") if flag.strip()]


def _fmt_number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    if isinstance(value, (int, float)):
        return f"{value:.3e}" if abs(value) < 0.01 or abs(value) > 1000 else f"{value:.4g}"
    return str(value)


def _field(row: pd.Series, name: str) -> Any:
    return row[name] if name in row and pd.notna(row[name]) else None


def evidence_items(row: pd.Series) -> list[str]:
    device = _field(row, "device")
    items = [
        f"device={device or 'unknown'}",
        f"shot={_field(row, 'shot') or 'unknown'}",
        f"status={_field(row, 'review_status') or 'unknown'}",
        f"score={_fmt_number(_field(row, 'anomaly_score'))}",
    ]
    for name in [
        "i_at_0v_a",
        "i_at_2v_a",
        "ifit_mae_a",
        "gate_leak_abs_max_a",
        "drain_i_span_a",
        "c_at_0v_f",
        "c_abs_max_raw_f",
        "resistance_ohm",
        "iv_linearity_r2",
    ]:
        value = _field(row, name)
        if value is not None:
            items.append(f"{name}={_fmt_number(value)}")
    return items


def beginner_explanation(row: pd.Series) -> str:
    flags = _flags(_field(row, "anomaly_flags"))
    device = _field(row, "device") or "unknown device"
    shot = _field(row, "shot") or "unknown shot"
    status = _field(row, "review_status") or "unknown"

    if not flags:
        return f"{shot} shot의 {device} 측정은 현재 기준에서 큰 이상 신호가 보이지 않습니다."

    meanings = [BEGINNER_MEANINGS.get(flag, FLAG_LABELS.get(flag, flag)) for flag in flags]
    candidates = _field(row, "process_issue_candidates") or infer_process_candidates(", ".join(flags))
    return (
        f"{shot} shot의 {device} 측정은 '{status}' 상태입니다. "
        f"주요 이유는 {' '.join(meanings)} "
        f"따라서 바로 원인을 단정하기보다는 {candidates} 쪽으로 확인 범위를 좁힐 수 있습니다."
    )


def engineer_explanation(row: pd.Series) -> str:
    flags = _flags(_field(row, "anomaly_flags"))
    evidence = "; ".join(evidence_items(row))
    candidates = _field(row, "process_issue_candidates") or infer_process_candidates(", ".join(flags))

    if not flags:
        return f"Baseline review. Evidence: {evidence}. No priority anomaly flag was triggered."

    actions = [ENGINEER_ACTIONS.get(flag, "engineering review required") for flag in flags]
    return (
        f"Triggered flags: {', '.join(flags)}. "
        f"Evidence: {evidence}. "
        f"Candidate causes: {candidates}. "
        f"Recommended checks: {'; '.join(dict.fromkeys(actions))}."
    )


def llm_prompt(row: pd.Series) -> str:
    return (
        "You are a semiconductor electrical test analysis assistant. "
        "Explain the wafer shot result in two versions: first for a non-major student, "
        "then for a semiconductor test engineer. Do not claim a confirmed root cause. "
        "Use the measured evidence, anomaly flags, and candidate process issues only.\n\n"
        f"Evidence: {'; '.join(evidence_items(row))}\n"
        f"Anomaly flags: {_field(row, 'anomaly_flags') or 'normal_or_review'}\n"
        f"Candidate process issues: {_field(row, 'process_issue_candidates') or 'baseline review'}"
    )


def add_explanations(features: pd.DataFrame) -> pd.DataFrame:
    result = features.copy()
    result["beginner_explanation"] = [beginner_explanation(row) for _, row in result.iterrows()]
    result["engineer_explanation"] = [engineer_explanation(row) for _, row in result.iterrows()]
    result["llm_prompt"] = [llm_prompt(row) for _, row in result.iterrows()]
    return result
