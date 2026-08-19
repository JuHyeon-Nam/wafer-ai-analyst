from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wafer_ai_analyst.ml_inference import add_ml_predictions, load_model_artifact
from src.wafer_ai_analyst.reporting import generate_analysis_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate local demo artifacts and write a demo summary.")
    parser.add_argument("--features-input", default="data/processed/features_preview.csv")
    parser.add_argument("--curves-input", default="data/processed/curves_preview.csv")
    parser.add_argument("--model-input", default="models/random_forest_tuned.joblib")
    parser.add_argument("--importance-input", default="data/processed/rf_tuned_feature_importance_preview.csv")
    parser.add_argument("--metrics-input", default="data/processed/rf_tuned_metrics_preview.json")
    parser.add_argument("--summary-output", default="docs/DEMO_RUN_SUMMARY.md")
    args = parser.parse_args()

    paths = {
        "features": Path(args.features_input),
        "curves": Path(args.curves_input),
        "model": Path(args.model_input),
        "importance": Path(args.importance_input),
        "metrics": Path(args.metrics_input),
    }
    missing = [name for name, path in paths.items() if not path.exists()]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"missing demo artifact(s): {joined}")

    features = pd.read_csv(paths["features"])
    curves = pd.read_csv(paths["curves"])
    model_artifact = load_model_artifact(paths["model"])
    result = add_ml_predictions(features, model_artifact)
    importance = pd.read_csv(paths["importance"])
    metrics = json.loads(paths["metrics"].read_text())

    report = generate_analysis_report(result, importance=importance, model_metrics=metrics)
    summary = _demo_summary(result, curves, metrics, report.markdown)

    output = Path(args.summary_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(summary)

    print(f"measurements={len(result)}")
    print(f"curve_points={len(curves)}")
    print(f"devices={_joined_unique(result, 'device')}")
    print(f"shots={_joined_unique(result, 'shot')}")
    print(f"test_accuracy={metrics.get('test_accuracy'):.4f}")
    print(f"test_macro_f1={metrics.get('test_macro_f1'):.4f}")
    print(f"summary={output}")


def _demo_summary(result: pd.DataFrame, curves: pd.DataFrame, metrics: dict[str, object], report_markdown: str) -> str:
    rule_counts = _counts(result, "review_status")
    ml_counts = _counts(result, "ml_predicted_label")
    candidate_preview = _candidate_preview(result)

    lines = [
        "# Demo Run Summary",
        "",
        "## Dataset Snapshot",
        "",
        f"- Measurements: `{len(result)}`",
        f"- Curve points: `{len(curves)}`",
        f"- Devices: `{_joined_unique(result, 'device')}`",
        f"- Shots: `{_joined_unique(result, 'shot')}`",
        "",
        "## Model Snapshot",
        "",
        f"- Test accuracy: `{metrics.get('test_accuracy'):.4f}`",
        f"- Test macro F1-score: `{metrics.get('test_macro_f1'):.4f}`",
        f"- Feature columns: `{metrics.get('feature_count')}`",
        "",
        "## Rule Review Count",
        "",
        _markdown_table(rule_counts),
        "",
        "## ML Prediction Count",
        "",
        _markdown_table(ml_counts),
        "",
        "## Candidate Preview",
        "",
        _markdown_table(candidate_preview),
        "",
        "## Demo Talking Points",
        "",
        "1. Raw wafer electrical test files were normalized into measurement, curve, feature, and explanation tables.",
        "2. Rule-based anomaly logic was used first because the real dataset has limited confirmed defect labels.",
        "3. Synthetic defect scenarios were generated from real feature distributions to create a supervised ML workflow.",
        "4. RandomForest was trained and tuned, then connected back to the real feature table for predicted label and confidence.",
        "5. Feature importance and curve detail views keep the result explainable instead of treating the model as a black box.",
        "6. The final report generator exports the analysis as Markdown/HTML for sharing outside the dashboard.",
        "",
        "## Report Check",
        "",
        f"- Markdown report length: `{len(report_markdown)}` characters",
        f"- Contains executive summary: `{str('Executive Summary' in report_markdown)}`",
    ]
    return "\n".join(lines) + "\n"


def _candidate_preview(result: pd.DataFrame) -> pd.DataFrame:
    candidates = result.copy()
    if "ml_confidence" in candidates.columns:
        candidates["ml_confidence"] = pd.to_numeric(candidates["ml_confidence"], errors="coerce").fillna(0)
    else:
        candidates["ml_confidence"] = 0.0
    if "anomaly_score" in candidates.columns:
        candidates["anomaly_score"] = pd.to_numeric(candidates["anomaly_score"], errors="coerce").fillna(0)
    else:
        candidates["anomaly_score"] = 0.0

    if "review_status" in candidates.columns:
        rule_mask = candidates["review_status"].fillna("normal").isin(["review", "priority"])
    else:
        rule_mask = pd.Series(False, index=candidates.index)
    if "ml_predicted_label" in candidates.columns:
        ml_mask = candidates["ml_predicted_label"].fillna("normal").ne("normal")
    else:
        ml_mask = pd.Series(False, index=candidates.index)

    candidates = candidates[rule_mask | ml_mask].copy()
    if "measurement_id" in candidates.columns:
        candidates = candidates.drop_duplicates(subset=["measurement_id"], keep="first")
    candidates = candidates.sort_values(["anomaly_score", "ml_confidence"], ascending=False).head(8)
    columns = [
        "measurement_id",
        "device",
        "shot",
        "review_status",
        "ml_predicted_label",
        "ml_confidence",
        "anomaly_flags",
    ]
    available = [column for column in columns if column in candidates.columns]
    preview = candidates[available].copy()
    if "ml_confidence" in preview.columns:
        preview["ml_confidence"] = preview["ml_confidence"].map(lambda value: f"{float(value):.3f}")
    return preview


def _counts(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in frame.columns:
        return pd.DataFrame({"item": ["not_available"], "count": [0]})
    return frame[column].fillna("unknown").value_counts().rename_axis("item").reset_index(name="count")


def _joined_unique(frame: pd.DataFrame, column: str) -> str:
    values = sorted(str(value) for value in frame[column].dropna().unique().tolist()) if column in frame else []
    return ", ".join(values) if values else "unknown"


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "No rows available."
    table = frame.fillna("")
    headers = [str(column) for column in table.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in table.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value).replace("|", "/").replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
