from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wafer_ai_analyst.modeling import train_random_forest, training_report_markdown


def _parse_max_depth(value: str) -> int | None:
    if value.lower() in {"none", "null"}:
        return None
    return int(value)


def _parse_class_weight(value: str) -> str | None:
    if value.lower() in {"none", "null"}:
        return None
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Train RandomForest baseline on prepared ML dataset.")
    parser.add_argument("--input", required=True, help="Prepared ML dataset CSV path.")
    parser.add_argument("--model-output", required=True, help="Model artifact output path.")
    parser.add_argument("--report-output", required=True, help="Markdown training report output path.")
    parser.add_argument("--predictions-output", help="Optional test prediction CSV output path.")
    parser.add_argument("--importance-output", help="Optional feature importance CSV output path.")
    parser.add_argument("--metrics-output", help="Optional metrics JSON output path.")
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--max-depth", type=_parse_max_depth, default=8)
    parser.add_argument("--min-samples-leaf", type=int, default=3)
    parser.add_argument("--class-weight", type=_parse_class_weight, default="balanced")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    dataset = pd.read_csv(args.input)
    result = train_random_forest(
        dataset,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        min_samples_leaf=args.min_samples_leaf,
        class_weight=args.class_weight,
        random_state=args.random_state,
    )

    model_output = Path(args.model_output)
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": result.model,
            "feature_columns": result.feature_columns,
            "labels": result.labels,
            "metrics": result.metrics,
        },
        model_output,
    )
    print(f"saved model to {model_output}")

    report_output = Path(args.report_output)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(training_report_markdown(result))
    print(f"saved training report to {report_output}")

    if args.predictions_output:
        predictions_output = Path(args.predictions_output)
        predictions_output.parent.mkdir(parents=True, exist_ok=True)
        result.predictions.to_csv(predictions_output, index=False)
        print(f"saved predictions to {predictions_output}")

    if args.importance_output:
        importance_output = Path(args.importance_output)
        importance_output.parent.mkdir(parents=True, exist_ok=True)
        result.feature_importance.to_csv(importance_output, index=False)
        print(f"saved feature importance to {importance_output}")

    if args.metrics_output:
        metrics_output = Path(args.metrics_output)
        metrics_output.parent.mkdir(parents=True, exist_ok=True)
        metrics_output.write_text(json.dumps(result.metrics, indent=2))
        print(f"saved metrics to {metrics_output}")

    print(
        "metrics "
        f"train_accuracy={result.metrics['train_accuracy']:.4f} "
        f"test_accuracy={result.metrics['test_accuracy']:.4f} "
        f"test_macro_f1={result.metrics['test_macro_f1']:.4f}"
    )


if __name__ == "__main__":
    main()
