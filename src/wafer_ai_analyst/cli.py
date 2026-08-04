from __future__ import annotations

import argparse
from pathlib import Path

from .features import extract_features
from .parsers import load_measurements
from .process_reasoning import infer_process_candidates
from .rules import apply_anomaly_rules


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze wafer electrical test files.")
    parser.add_argument("--input", required=True, help="Input file or folder path.")
    parser.add_argument("--output", required=True, help="Output CSV path for feature table.")
    args = parser.parse_args()

    measurements = load_measurements(Path(args.input))
    features = extract_features(measurements)
    result = apply_anomaly_rules(features)
    result["process_issue_candidates"] = result["anomaly_flags"].map(infer_process_candidates)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"saved {len(result)} rows to {output}")


if __name__ == "__main__":
    main()

