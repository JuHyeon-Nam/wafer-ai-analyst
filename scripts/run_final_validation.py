from __future__ import annotations

import argparse
import importlib
import json
import py_compile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))

from src.wafer_ai_analyst.ml_inference import add_ml_predictions, load_model_artifact
from src.wafer_ai_analyst.reporting import generate_analysis_report


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str


def main() -> None:
    parser = argparse.ArgumentParser(description="Run final project validation and write a Markdown summary.")
    parser.add_argument("--features-input", default="data/processed/features_preview.csv")
    parser.add_argument("--curves-input", default="data/processed/curves_preview.csv")
    parser.add_argument("--model-input", default="models/random_forest_tuned.joblib")
    parser.add_argument("--importance-input", default="data/processed/rf_tuned_feature_importance_preview.csv")
    parser.add_argument("--metrics-input", default="data/processed/rf_tuned_metrics_preview.json")
    parser.add_argument("--summary-output", default="docs/FINAL_VALIDATION.md")
    args = parser.parse_args()

    checks: list[CheckResult] = []
    checks.extend(_check_required_files(args))
    checks.extend(_check_python_compile())
    checks.extend(_check_module_imports())

    features = pd.read_csv(ROOT / args.features_input)
    curves = pd.read_csv(ROOT / args.curves_input)
    metrics = json.loads((ROOT / args.metrics_input).read_text())
    importance = pd.read_csv(ROOT / args.importance_input)
    model_artifact = load_model_artifact(ROOT / args.model_input)
    result = add_ml_predictions(features, model_artifact)
    report = generate_analysis_report(result, importance=importance, model_metrics=metrics)

    checks.extend(_check_dataset(result, curves))
    checks.extend(_check_model_metrics(metrics))
    checks.extend(_check_report(report.markdown, report.html))

    summary = _summary_markdown(checks, result, curves, metrics)
    output = ROOT / args.summary_output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(summary)

    failed = [check for check in checks if check.status != "PASS"]
    print(f"checks={len(checks)} pass={len(checks) - len(failed)} fail={len(failed)}")
    print(f"measurements={len(result)} curve_points={len(curves)}")
    print(f"test_accuracy={metrics.get('test_accuracy'):.4f} test_macro_f1={metrics.get('test_macro_f1'):.4f}")
    print(f"summary={output.relative_to(ROOT)}")
    if failed:
        raise SystemExit(1)


def _check_required_files(args: argparse.Namespace) -> list[CheckResult]:
    required = [
        "README.md",
        "app.py",
        "requirements.txt",
        "docs/DEMO_GUIDE.md",
        "docs/DEMO_RUN_SUMMARY.md",
        "docs/ANALYSIS_REPORT_DEMO.md",
        "scripts/run_demo_check.py",
        "scripts/generate_analysis_report.py",
        args.features_input,
        args.curves_input,
        args.model_input,
        args.importance_input,
        args.metrics_input,
    ]
    checks = []
    for path in required:
        target = ROOT / path
        status = "PASS" if target.exists() else "FAIL"
        detail = "exists" if target.exists() else "missing"
        checks.append(CheckResult(f"file:{path}", status, detail))
    return checks


def _check_python_compile() -> list[CheckResult]:
    paths = list((ROOT / "src").rglob("*.py")) + list((ROOT / "scripts").rglob("*.py")) + [ROOT / "app.py"]
    checks = []
    for path in paths:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            checks.append(CheckResult(f"compile:{path.relative_to(ROOT)}", "FAIL", str(exc)))
        else:
            checks.append(CheckResult(f"compile:{path.relative_to(ROOT)}", "PASS", "compiled"))
    return checks


def _check_module_imports() -> list[CheckResult]:
    modules = [
        "src.wafer_ai_analyst.parsers",
        "src.wafer_ai_analyst.features",
        "src.wafer_ai_analyst.rules",
        "src.wafer_ai_analyst.synthetic",
        "src.wafer_ai_analyst.ml_dataset",
        "src.wafer_ai_analyst.modeling",
        "src.wafer_ai_analyst.tuning",
        "src.wafer_ai_analyst.ml_inference",
        "src.wafer_ai_analyst.reporting",
    ]
    checks = []
    for module in modules:
        try:
            importlib.import_module(module)
        except Exception as exc:
            checks.append(CheckResult(f"import:{module}", "FAIL", repr(exc)))
        else:
            checks.append(CheckResult(f"import:{module}", "PASS", "imported"))
    return checks


def _check_dataset(result: pd.DataFrame, curves: pd.DataFrame) -> list[CheckResult]:
    checks = [
        CheckResult("dataset:measurements", "PASS" if len(result) == 74 else "FAIL", str(len(result))),
        CheckResult("dataset:curve_points", "PASS" if len(curves) == 10294 else "FAIL", str(len(curves))),
    ]
    for column in ["measurement_id", "device", "shot", "review_status", "ml_predicted_label", "ml_confidence"]:
        status = "PASS" if column in result.columns else "FAIL"
        checks.append(CheckResult(f"dataset:column:{column}", status, "available" if status == "PASS" else "missing"))
    return checks


def _check_model_metrics(metrics: dict[str, object]) -> list[CheckResult]:
    accuracy = float(metrics.get("test_accuracy", 0))
    macro_f1 = float(metrics.get("test_macro_f1", 0))
    return [
        CheckResult("model:test_accuracy", "PASS" if accuracy >= 0.95 else "FAIL", f"{accuracy:.4f}"),
        CheckResult("model:test_macro_f1", "PASS" if macro_f1 >= 0.95 else "FAIL", f"{macro_f1:.4f}"),
        CheckResult("model:feature_count", "PASS" if metrics.get("feature_count") == 70 else "FAIL", str(metrics.get("feature_count"))),
    ]


def _check_report(markdown: str, html: str) -> list[CheckResult]:
    sections = ["Executive Summary", "Review Count", "ML Prediction Count", "Feature Importance Summary", "Model Metrics"]
    checks = []
    for section in sections:
        checks.append(CheckResult(f"report:section:{section}", "PASS" if section in markdown else "FAIL", "markdown"))
    checks.append(CheckResult("report:html_title", "PASS" if "Wafer Electrical Test Analysis Report" in html else "FAIL", "html"))
    checks.append(CheckResult("report:html_table", "PASS" if "<table>" in html else "FAIL", "html"))
    return checks


def _summary_markdown(
    checks: list[CheckResult],
    result: pd.DataFrame,
    curves: pd.DataFrame,
    metrics: dict[str, object],
) -> str:
    pass_count = sum(1 for check in checks if check.status == "PASS")
    fail_count = len(checks) - pass_count
    lines = [
        "# Final Validation Summary",
        "",
        f"- Generated at: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        "- Validation scope: `current working tree at runtime`",
        f"- Checks: `{len(checks)}`",
        f"- Passed: `{pass_count}`",
        f"- Failed: `{fail_count}`",
        "",
        "## Project Snapshot",
        "",
        f"- Measurements: `{len(result)}`",
        f"- Curve points: `{len(curves)}`",
        f"- Devices: `{_joined_unique(result, 'device')}`",
        f"- Shots: `{_joined_unique(result, 'shot')}`",
        f"- Tuned model test accuracy: `{float(metrics.get('test_accuracy', 0)):.4f}`",
        f"- Tuned model macro F1-score: `{float(metrics.get('test_macro_f1', 0)):.4f}`",
        "",
        "## Validation Checks",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| `{check.name}` | `{check.status}` | {str(check.detail).replace('|', '/')} |")

    lines.extend(
        [
            "",
            "## Final Status",
            "",
            "The project is ready for a reproducible local demo when all checks pass.",
            "Generated data/model artifacts remain local outputs and are intentionally excluded from GitHub.",
        ]
    )
    return "\n".join(lines) + "\n"


def _joined_unique(frame: pd.DataFrame, column: str) -> str:
    if column not in frame.columns:
        return "unknown"
    values = sorted(str(value) for value in frame[column].dropna().unique().tolist())
    return ", ".join(values) if values else "unknown"


if __name__ == "__main__":
    main()
