from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wafer_ai_analyst.modeling import training_report_markdown
from src.wafer_ai_analyst.tuning import tune_random_forest, tuning_report_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Tune RandomForest hyperparameters.")
    parser.add_argument("--input", required=True, help="Prepared ML dataset CSV path.")
    parser.add_argument("--results-output", required=True, help="Tuning result CSV path.")
    parser.add_argument("--report-output", required=True, help="Tuning Markdown report path.")
    parser.add_argument("--best-model-output", required=True, help="Best model artifact path.")
    parser.add_argument("--best-report-output", help="Optional best model training report path.")
    parser.add_argument("--best-predictions-output", help="Optional best model test prediction CSV path.")
    parser.add_argument("--best-importance-output", help="Optional best model feature importance CSV path.")
    parser.add_argument("--metrics-output", help="Optional best metrics JSON path.")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    dataset = pd.read_csv(args.input)
    tuning = tune_random_forest(dataset, random_state=args.random_state)
    best = tuning.best_result

    results_output = Path(args.results_output)
    results_output.parent.mkdir(parents=True, exist_ok=True)
    tuning.results.to_csv(results_output, index=False)
    print(f"saved tuning results to {results_output}")

    report_output = Path(args.report_output)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(tuning_report_markdown(tuning))
    print(f"saved tuning report to {report_output}")

    best_model_output = Path(args.best_model_output)
    best_model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": best.model,
            "feature_columns": best.feature_columns,
            "labels": best.labels,
            "metrics": best.metrics,
            "tuning_results": tuning.results,
        },
        best_model_output,
    )
    print(f"saved best model to {best_model_output}")

    if args.best_report_output:
        best_report_output = Path(args.best_report_output)
        best_report_output.parent.mkdir(parents=True, exist_ok=True)
        best_report_output.write_text(training_report_markdown(best))
        print(f"saved best model report to {best_report_output}")

    if args.best_predictions_output:
        best_predictions_output = Path(args.best_predictions_output)
        best_predictions_output.parent.mkdir(parents=True, exist_ok=True)
        best.predictions.to_csv(best_predictions_output, index=False)
        print(f"saved best predictions to {best_predictions_output}")

    if args.best_importance_output:
        best_importance_output = Path(args.best_importance_output)
        best_importance_output.parent.mkdir(parents=True, exist_ok=True)
        best.feature_importance.to_csv(best_importance_output, index=False)
        print(f"saved best feature importance to {best_importance_output}")

    if args.metrics_output:
        metrics_output = Path(args.metrics_output)
        metrics_output.parent.mkdir(parents=True, exist_ok=True)
        metrics_output.write_text(json.dumps(best.metrics, indent=2))
        print(f"saved best metrics to {metrics_output}")

    print(
        "best "
        f"test_accuracy={best.metrics['test_accuracy']:.4f} "
        f"test_macro_f1={best.metrics['test_macro_f1']:.4f} "
        f"params={best.metrics['parameters']}"
    )


if __name__ == "__main__":
    main()
