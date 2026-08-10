from __future__ import annotations


ISSUE_MAP = {
    "measurement_error_suspect": [
        "probe contact issue",
        "measurement range error",
        "data artifact",
    ],
    "raw_capacitance_outlier": [
        "measurement range error",
        "open/unstable probe contact",
        "instrument parsing artifact",
    ],
    "compliance_limit_suspect": [
        "measurement condition issue",
        "short suspect",
        "device over-current path",
    ],
    "current_saturation_suspect": [
        "contact resistance change",
        "series resistance effect",
        "instrument compliance",
    ],
    "curve_fit_mismatch": [
        "junction characteristic variation",
        "contact instability",
        "non-ideal diode behavior",
    ],
    "leakage_current_suspect": [
        "junction leakage path",
        "surface contamination",
        "oxide/interface defect",
    ],
    "gate_leakage_suspect": [
        "gate oxide weakness",
        "surface leakage",
        "probe contact instability",
    ],
    "diode_current_variation": [
        "junction variation",
        "series resistance shift",
        "probe contact variation",
        "pattern CD variation",
    ],
    "capacitance_variation": [
        "oxide thickness variation",
        "deposition non-uniformity",
        "etch variation",
    ],
    "resistance_shift": [
        "thin film thickness variation",
        "line width variation",
        "contact resistance variation",
    ],
    "resistor_linearity_drop": [
        "contact resistance variation",
        "self-heating effect",
        "instrument compliance",
    ],
    "nmos_current_span_suspect": [
        "threshold voltage shift",
        "channel process variation",
        "local short/leakage path",
    ],
}


def infer_process_candidates(flags: str) -> str:
    if not flags or flags == "normal_or_review":
        return "baseline review"
    candidates: list[str] = []
    for flag in [f.strip() for f in flags.split(",")]:
        candidates.extend(ISSUE_MAP.get(flag, []))
    deduped = list(dict.fromkeys(candidates))
    return ", ".join(deduped) if deduped else "engineering review required"
