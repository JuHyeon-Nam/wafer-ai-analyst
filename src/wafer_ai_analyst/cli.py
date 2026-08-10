from __future__ import annotations

import argparse
from pathlib import Path

from .explanations import add_explanations
from .features import extract_features
from .parsers import load_measurements, measurements_to_curve_frame, measurements_to_metadata_frame
from .process_reasoning import infer_process_candidates
from .rules import apply_anomaly_rules


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze wafer electrical test files.")
    parser.add_argument("--input", required=True, help="Input file or folder path.")
    parser.add_argument("--output", required=True, help="Output CSV path for feature table.")
    parser.add_argument("--metadata-output", help="Optional output CSV path for parsed metadata.")
    parser.add_argument("--curves-output", help="Optional output CSV path for normalized curve table.")
    parser.add_argument("--explanations-output", help="Optional output CSV path for explanation table.")
    args = parser.parse_args()

    measurements = load_measurements(Path(args.input))
    features = extract_features(measurements)
    result = apply_anomaly_rules(features)
    result["process_issue_candidates"] = result["anomaly_flags"].map(infer_process_candidates)
    result = add_explanations(result)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"saved {len(result)} rows to {output}")

    if args.metadata_output:
        metadata = measurements_to_metadata_frame(measurements)
        metadata_output = Path(args.metadata_output)
        metadata_output.parent.mkdir(parents=True, exist_ok=True)
        metadata.to_csv(metadata_output, index=False)
        print(f"saved {len(metadata)} metadata rows to {metadata_output}")

    if args.curves_output:
        curves = measurements_to_curve_frame(measurements)
        curves_output = Path(args.curves_output)
        curves_output.parent.mkdir(parents=True, exist_ok=True)
        curves.to_csv(curves_output, index=False)
        print(f"saved {len(curves)} curve rows to {curves_output}")

    if args.explanations_output:
        explanation_columns = [
            "measurement_id",
            "device",
            "shot",
            "review_status",
            "anomaly_flags",
            "process_issue_candidates",
            "beginner_explanation",
            "engineer_explanation",
            "llm_prompt",
        ]
        explanations = result[[col for col in explanation_columns if col in result.columns]]
        explanations_output = Path(args.explanations_output)
        explanations_output.parent.mkdir(parents=True, exist_ok=True)
        explanations.to_csv(explanations_output, index=False)
        print(f"saved {len(explanations)} explanation rows to {explanations_output}")


if __name__ == "__main__":
    main()
