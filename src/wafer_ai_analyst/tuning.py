from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import pandas as pd

from .modeling import TrainingResult, train_random_forest


@dataclass(frozen=True)
class TuningResult:
    results: pd.DataFrame
    best_result: TrainingResult
    best_parameters: dict[str, object]


def _class_recall(result: TrainingResult, label: str) -> float:
    report = result.metrics["classification_report"]
    if label not in report:
        return 0.0
    return float(report[label]["recall"])


def _score_row(result: TrainingResult) -> dict[str, object]:
    metrics = result.metrics
    params = metrics["parameters"]
    train_accuracy = float(metrics["train_accuracy"])
    test_accuracy = float(metrics["test_accuracy"])
    overfit_gap = train_accuracy - test_accuracy
    return {
        **params,
        "train_accuracy": train_accuracy,
        "test_accuracy": test_accuracy,
        "test_macro_f1": float(metrics["test_macro_f1"]),
        "overfit_gap": overfit_gap,
        "normal_recall": _class_recall(result, "normal"),
        "nmos_compliance_recall": _class_recall(result, "nmos_compliance_limit"),
        "nmos_gate_leakage_recall": _class_recall(result, "nmos_gate_leakage"),
    }


def tune_random_forest(
    dataset: pd.DataFrame,
    n_estimators_values: list[int] | None = None,
    max_depth_values: list[int | None] | None = None,
    min_samples_leaf_values: list[int] | None = None,
    class_weight_values: list[str | None] | None = None,
    random_state: int = 42,
) -> TuningResult:
    n_estimators_values = n_estimators_values or [50, 100, 200]
    max_depth_values = max_depth_values or [4, 6, 8, None]
    min_samples_leaf_values = min_samples_leaf_values or [1, 3, 5]
    class_weight_values = class_weight_values or [None, "balanced"]

    rows: list[dict[str, object]] = []
    best_result: TrainingResult | None = None
    best_sort_key: tuple[float, float, float, float, float] | None = None

    for n_estimators, max_depth, min_samples_leaf, class_weight in product(
        n_estimators_values,
        max_depth_values,
        min_samples_leaf_values,
        class_weight_values,
    ):
        result = train_random_forest(
            dataset,
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            class_weight=class_weight,
            random_state=random_state,
        )
        row = _score_row(result)
        rows.append(row)

        sort_key = (
            float(row["test_macro_f1"]),
            float(row["test_accuracy"]),
            float(row["normal_recall"]),
            float(row["nmos_gate_leakage_recall"]),
            -abs(float(row["overfit_gap"])),
        )
        if best_sort_key is None or sort_key > best_sort_key:
            best_sort_key = sort_key
            best_result = result

    if best_result is None:
        raise ValueError("no tuning result was generated")

    results = pd.DataFrame(rows).sort_values(
        ["test_macro_f1", "test_accuracy", "normal_recall", "nmos_gate_leakage_recall", "overfit_gap"],
        ascending=[False, False, False, False, True],
    )
    return TuningResult(
        results=results.reset_index(drop=True),
        best_result=best_result,
        best_parameters=best_result.metrics["parameters"],
    )


def _markdown_table(frame: pd.DataFrame) -> str:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def tuning_report_markdown(result: TuningResult) -> str:
    best = result.best_result.metrics
    params = result.best_parameters
    display = result.results.head(12).copy()
    for column in [
        "train_accuracy",
        "test_accuracy",
        "test_macro_f1",
        "overfit_gap",
        "normal_recall",
        "nmos_compliance_recall",
        "nmos_gate_leakage_recall",
    ]:
        display[column] = display[column].map(lambda value: f"{float(value):.4f}")
    display["max_depth"] = display["max_depth"].fillna("None")
    display["class_weight"] = display["class_weight"].fillna("None")

    lines = [
        "# RandomForest Hyperparameter Tuning Report",
        "",
        "## Summary",
        "",
        f"- Tried parameter sets: `{len(result.results)}`",
        f"- Best test accuracy: `{best['test_accuracy']:.4f}`",
        f"- Best test macro F1-score: `{best['test_macro_f1']:.4f}`",
        f"- Best train accuracy: `{best['train_accuracy']:.4f}`",
        f"- Best overfit gap: `{best['train_accuracy'] - best['test_accuracy']:.4f}`",
        "",
        "## Selected Parameters",
        "",
        "| Parameter | Value |",
        "|---|---:|",
    ]
    for key, value in params.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(
        [
            "",
            "## Top Parameter Sets",
            "",
            _markdown_table(
                display[
                    [
                        "n_estimators",
                        "max_depth",
                        "min_samples_leaf",
                        "class_weight",
                        "test_macro_f1",
                        "test_accuracy",
                        "normal_recall",
                        "nmos_compliance_recall",
                        "nmos_gate_leakage_recall",
                        "overfit_gap",
                    ]
                ]
            ),
            "",
            "## Why This Selection",
            "",
            "The selected model is chosen by test macro F1-score first, then test accuracy, normal recall, NMOS recall, and lower overfit gap.",
            "This keeps the tuning story focused on balanced defect classification instead of only maximizing overall accuracy.",
            "",
            "## Next Step",
            "",
            "The next step is feature importance analysis and dashboard integration of ML prediction results.",
        ]
    )
    return "\n".join(lines) + "\n"
