from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from .ml_dataset import SPLIT_COLUMN, TARGET_COLUMN


METADATA_COLUMNS = {
    "measurement_id",
    "seed_measurement_id",
    SPLIT_COLUMN,
    TARGET_COLUMN,
    "device",
}


@dataclass(frozen=True)
class TrainingResult:
    model: RandomForestClassifier
    feature_columns: list[str]
    labels: list[str]
    metrics: dict[str, object]
    predictions: pd.DataFrame
    feature_importance: pd.DataFrame
    confusion_matrix: pd.DataFrame


def infer_feature_columns(dataset: pd.DataFrame) -> list[str]:
    return [column for column in dataset.columns if column not in METADATA_COLUMNS]


def train_random_forest(
    dataset: pd.DataFrame,
    n_estimators: int = 100,
    max_depth: int | None = 8,
    min_samples_leaf: int = 3,
    class_weight: str | None = "balanced",
    random_state: int = 42,
) -> TrainingResult:
    feature_columns = infer_feature_columns(dataset)
    train = dataset[dataset[SPLIT_COLUMN].eq("train")]
    test = dataset[dataset[SPLIT_COLUMN].eq("test")]

    if train.empty or test.empty:
        raise ValueError("dataset must contain both train and test split rows")

    labels = sorted(dataset[TARGET_COLUMN].dropna().unique().tolist())
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        class_weight=class_weight,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(train[feature_columns], train[TARGET_COLUMN])

    train_pred = model.predict(train[feature_columns])
    test_pred = model.predict(test[feature_columns])
    test_proba = model.predict_proba(test[feature_columns])
    confidence = test_proba.max(axis=1)

    predictions = test[["measurement_id", "seed_measurement_id", TARGET_COLUMN, "device"]].copy()
    predictions["predicted_label"] = test_pred
    predictions["confidence"] = confidence
    predictions["correct"] = predictions[TARGET_COLUMN].eq(predictions["predicted_label"])

    matrix = pd.DataFrame(
        confusion_matrix(test[TARGET_COLUMN], test_pred, labels=labels),
        index=labels,
        columns=labels,
    )
    importance = (
        pd.DataFrame(
            {
                "feature": feature_columns,
                "importance": model.feature_importances_,
            }
        )
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    metrics = {
        "train_accuracy": float(accuracy_score(train[TARGET_COLUMN], train_pred)),
        "test_accuracy": float(accuracy_score(test[TARGET_COLUMN], test_pred)),
        "test_macro_f1": float(f1_score(test[TARGET_COLUMN], test_pred, average="macro")),
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "feature_count": int(len(feature_columns)),
        "labels": labels,
        "parameters": {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_leaf": min_samples_leaf,
            "class_weight": class_weight,
            "random_state": random_state,
        },
        "classification_report": classification_report(test[TARGET_COLUMN], test_pred, labels=labels, output_dict=True),
    }

    return TrainingResult(
        model=model,
        feature_columns=feature_columns,
        labels=labels,
        metrics=metrics,
        predictions=predictions,
        feature_importance=importance,
        confusion_matrix=matrix,
    )


def _markdown_table(frame: pd.DataFrame, include_index: bool = True) -> str:
    table = frame.copy()
    if include_index:
        table = table.reset_index().rename(columns={"index": "label"})
    headers = [str(column) for column in table.columns]
    rows = [[str(value) for value in row] for row in table.itertuples(index=False, name=None)]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def training_report_markdown(result: TrainingResult) -> str:
    metrics = result.metrics
    params = metrics["parameters"]

    lines = [
        "# RandomForest Baseline Training Report",
        "",
        "## Summary",
        "",
        f"- Train rows: `{metrics['train_rows']}`",
        f"- Test rows: `{metrics['test_rows']}`",
        f"- Feature columns: `{metrics['feature_count']}`",
        f"- Train accuracy: `{metrics['train_accuracy']:.4f}`",
        f"- Test accuracy: `{metrics['test_accuracy']:.4f}`",
        f"- Test macro F1-score: `{metrics['test_macro_f1']:.4f}`",
        "",
        "## Model Parameters",
        "",
        "| Parameter | Value |",
        "|---|---:|",
    ]
    for key, value in params.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(
        [
            "",
            "## Confusion Matrix",
            "",
            _markdown_table(result.confusion_matrix),
            "",
            "## Top Feature Importance",
            "",
            _markdown_table(result.feature_importance.head(20), include_index=False),
            "",
            "## Per-Class Test Metrics",
            "",
            "| Label | Precision | Recall | F1-score | Support |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    report = metrics["classification_report"]
    for label in metrics["labels"]:
        item = report[label]
        lines.append(
            f"| `{label}` | {item['precision']:.4f} | {item['recall']:.4f} | "
            f"{item['f1-score']:.4f} | {int(item['support'])} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This model is a baseline classifier trained on synthetic defect scenario features.",
            "The goal is not to claim production-level defect prediction, but to verify that the feature table can support a supervised ML workflow.",
            "The next step is hyperparameter tuning and robustness checks against overfitting.",
        ]
    )
    return "\n".join(lines) + "\n"
