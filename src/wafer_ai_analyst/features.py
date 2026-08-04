from __future__ import annotations

import numpy as np
import pandas as pd

from .parsers import Measurement


def _interp(x: np.ndarray, y: np.ndarray, value: float) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if not mask.any():
        return float("nan")
    x_valid = x[mask]
    y_valid = y[mask]
    if value < np.nanmin(x_valid) or value > np.nanmax(x_valid):
        return float("nan")
    order = np.argsort(x_valid)
    return float(np.interp(value, x_valid[order], y_valid[order]))


def diode_features(m: Measurement) -> dict[str, float | str | None]:
    df = m.table
    v = df["AnodeV"].to_numpy(float)
    i = df["AnodeI"].to_numpy(float)
    result = {
        "i_at_1v_a": _interp(v, i, 1.0),
        "i_at_2v_a": _interp(v, i, 2.0),
        "i_max_a": float(np.nanmax(i)),
        "i_min_a": float(np.nanmin(i)),
    }
    if "IFIT" in df.columns:
        fit = df["IFIT"].to_numpy(float)
        mask = np.isfinite(i) & np.isfinite(fit)
        result["ifit_mae_a"] = float(np.nanmean(np.abs(i[mask] - fit[mask]))) if mask.any() else float("nan")
    return result


def resistor_features(m: Measurement) -> dict[str, float | str | None]:
    df = m.table
    v = df["AV"].to_numpy(float)
    i = df["AI"].to_numpy(float)
    mask = np.isfinite(v) & np.isfinite(i) & (np.abs(i) < 0.09)
    if mask.sum() < 10:
        mask = np.isfinite(v) & np.isfinite(i)
    slope, intercept = np.polyfit(v[mask], i[mask], 1)
    pred = slope * v[mask] + intercept
    denom = np.sum((i[mask] - np.mean(i[mask])) ** 2)
    r2 = 1 - np.sum((i[mask] - pred) ** 2) / denom if denom else float("nan")
    return {
        "resistance_ohm": float(1 / slope),
        "iv_linearity_r2": float(r2),
        "compliance_hits": int(np.sum(np.abs(i) > 0.099)),
    }


def capacitor_features(m: Measurement) -> dict[str, float | str | None]:
    df = m.table
    v = df["V"].to_numpy(float)
    c = df["C"].to_numpy(float)
    valid = np.isfinite(c) & (np.abs(c) < 1e-6)
    return {
        "c_at_0v_f": _interp(v[valid], c[valid], 0.0) if valid.any() else float("nan"),
        "c_max_f": float(np.nanmax(c[valid])) if valid.any() else float("nan"),
        "c_min_f": float(np.nanmin(c[valid])) if valid.any() else float("nan"),
        "invalid_c_points": int(np.sum(np.isfinite(c) & ~valid)),
    }


def nmos_features(m: Measurement) -> dict[str, float | str | None]:
    df = m.table
    drain_i = df["DrainI"].to_numpy(float)
    gate_i = df["GateI"].to_numpy(float)
    return {
        "drain_i_mean_a": float(np.nanmean(drain_i)),
        "drain_i_span_a": float(np.nanmax(drain_i) - np.nanmin(drain_i)),
        "gate_leak_abs_max_a": float(np.nanmax(np.abs(gate_i))),
        "compliance_suspect": bool(np.nanmin(drain_i) > 0.095),
    }


def extract_features(measurements: list[Measurement]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for m in measurements:
        base: dict[str, object] = {
            "source": str(m.source_path),
            "device": m.device,
            "shot": m.shot,
            "rows": len(m.table),
        }
        try:
            if m.device == "diode" and {"AnodeI", "AnodeV"}.issubset(m.table.columns):
                base.update(diode_features(m))
            elif m.device == "resistor" and {"AI", "AV"}.issubset(m.table.columns):
                base.update(resistor_features(m))
            elif m.device == "Cap" and {"C", "V"}.issubset(m.table.columns):
                base.update(capacitor_features(m))
            elif m.device == "NMOS" and {"DrainI", "GateI"}.issubset(m.table.columns):
                base.update(nmos_features(m))
            else:
                base["parse_warning"] = "unsupported schema"
        except Exception as exc:
            base["parse_warning"] = repr(exc)
        rows.append(base)
    return pd.DataFrame(rows)

