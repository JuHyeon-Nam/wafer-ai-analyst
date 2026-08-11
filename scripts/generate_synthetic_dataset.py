from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wafer_ai_analyst.synthetic import generate_synthetic_features, scenario_frame


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic defect scenario features.")
    parser.add_argument("--input", required=True, help="Real feature CSV path.")
    parser.add_argument("--output", required=True, help="Synthetic feature CSV output path.")
    parser.add_argument("--scenario-output", help="Optional scenario schema CSV output path.")
    parser.add_argument("--samples-per-scenario", type=int, default=80)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    real_features = pd.read_csv(args.input)
    synthetic = generate_synthetic_features(
        real_features,
        samples_per_scenario=args.samples_per_scenario,
        random_state=args.random_state,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    synthetic.to_csv(output, index=False)
    print(f"saved {len(synthetic)} synthetic rows to {output}")
    print(synthetic["scenario_label"].value_counts().sort_index().to_string())

    if args.scenario_output:
        scenario_output = Path(args.scenario_output)
        scenario_output.parent.mkdir(parents=True, exist_ok=True)
        scenarios = scenario_frame()
        scenarios.to_csv(scenario_output, index=False)
        print(f"saved {len(scenarios)} scenario rows to {scenario_output}")


if __name__ == "__main__":
    main()
