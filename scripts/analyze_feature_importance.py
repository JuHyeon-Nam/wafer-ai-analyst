from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wafer_ai_analyst.importance import feature_importance_report_markdown, summarize_feature_importance


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze RandomForest feature importance.")
    parser.add_argument("--input", required=True, help="Feature importance CSV path.")
    parser.add_argument("--report-output", required=True, help="Markdown report output path.")
    parser.add_argument("--top-output", help="Optional top feature CSV output path.")
    parser.add_argument("--group-output", help="Optional feature group summary CSV output path.")
    args = parser.parse_args()

    importance = pd.read_csv(args.input)
    top, group_summary = summarize_feature_importance(importance)

    report_output = Path(args.report_output)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(feature_importance_report_markdown(importance))
    print(f"saved feature importance report to {report_output}")

    if args.top_output:
        top_output = Path(args.top_output)
        top_output.parent.mkdir(parents=True, exist_ok=True)
        top.to_csv(top_output, index=False)
        print(f"saved top feature table to {top_output}")

    if args.group_output:
        group_output = Path(args.group_output)
        group_output.parent.mkdir(parents=True, exist_ok=True)
        group_summary.to_csv(group_output, index=False)
        print(f"saved group summary to {group_output}")


if __name__ == "__main__":
    main()
