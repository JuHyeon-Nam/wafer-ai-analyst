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


def _read_json(path: str | None) -> dict[str, object] | None:
    if not path:
        return None
    target = Path(path)
    if not target.exists():
        return None
    return json.loads(target.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate wafer analysis Markdown and HTML reports.")
    parser.add_argument("--features-input", required=True, help="Feature table CSV path.")
    parser.add_argument("--model-input", help="Optional trained model artifact path.")
    parser.add_argument("--importance-input", help="Optional feature importance CSV path.")
    parser.add_argument("--metrics-input", help="Optional model metrics JSON path.")
    parser.add_argument("--markdown-output", required=True, help="Markdown report output path.")
    parser.add_argument("--html-output", required=True, help="HTML report output path.")
    args = parser.parse_args()

    result = pd.read_csv(args.features_input)
    if args.model_input and Path(args.model_input).exists():
        result = add_ml_predictions(result, load_model_artifact(args.model_input))

    importance = pd.read_csv(args.importance_input) if args.importance_input and Path(args.importance_input).exists() else None
    model_metrics = _read_json(args.metrics_input)
    report = generate_analysis_report(result, importance=importance, model_metrics=model_metrics)

    markdown_output = Path(args.markdown_output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(report.markdown)
    print(f"saved Markdown report to {markdown_output}")

    html_output = Path(args.html_output)
    html_output.parent.mkdir(parents=True, exist_ok=True)
    html_output.write_text(report.html)
    print(f"saved HTML report to {html_output}")


if __name__ == "__main__":
    main()
