from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wafer_ai_analyst.ml_dataset import prepare_ml_dataset, validation_report_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare model-ready ML dataset from synthetic features.")
    parser.add_argument("--input", required=True, help="Synthetic feature CSV path.")
    parser.add_argument("--output", required=True, help="Prepared ML dataset CSV output path.")
    parser.add_argument("--feature-columns-output", help="Optional feature column list output path.")
    parser.add_argument("--report-output", help="Optional Markdown validation report output path.")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--min-non-null", type=int, default=10)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    synthetic = pd.read_csv(args.input)
    prepared = prepare_ml_dataset(
        synthetic,
        min_non_null=args.min_non_null,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    prepared.frame.to_csv(output, index=False)
    print(f"saved {len(prepared.frame)} ML rows to {output}")
    print(f"feature columns: {len(prepared.feature_columns)}")
    print(prepared.frame.groupby(["scenario_label", "split"]).size().unstack(fill_value=0).to_string())

    if args.feature_columns_output:
        feature_columns_output = Path(args.feature_columns_output)
        feature_columns_output.parent.mkdir(parents=True, exist_ok=True)
        feature_columns_output.write_text("\n".join(prepared.feature_columns) + "\n")
        print(f"saved feature columns to {feature_columns_output}")

    if args.report_output:
        report_output = Path(args.report_output)
        report_output.parent.mkdir(parents=True, exist_ok=True)
        report_output.write_text(validation_report_markdown(prepared.report))
        print(f"saved validation report to {report_output}")


if __name__ == "__main__":
    main()
