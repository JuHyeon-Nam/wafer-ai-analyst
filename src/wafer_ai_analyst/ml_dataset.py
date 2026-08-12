from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


TARGET_COLUMN = "scenario_label"
SPLIT_COLUMN = "split"

EXCLUDED_COLUMNS = {
    "source",
    "source_file",
    "measurement_id",
    "measurement_name",
    "shot",
    "rows",
    "test_name",
    "site_coordinate",
    "last_executed",
    "sweep_mode",
    "current_range",
    "compliance",
    "parse_warning",
    "data_source",
    "seed_measurement_id",
    "synthetic_id",
    "scenario_label",
    "scenario_description",
    "modified_features",
    "expected_anomaly_flags",
    "anomaly_flags",
    "anomaly_score",
    "review_status",
    "process_issue_candidates",
    "beginner_explanation",
    "engineer_explanation",
    "llm_prompt",
}


@dataclass(frozen=True)
class PreparedDataset:
    frame: pd.DataFrame
    feature_columns: list[str]
    report: dict[str, object]


def _numeric_feature_columns(frame: pd.DataFrame, min_non_null: int) -> list[str]:
    columns: list[str] = []
    for column in frame.columns:
        if column in EXCLUDED_COLUMNS:
            continue
        series = frame[column]
        if pd.api.types.is_bool_dtype(series) or pd.api.types.is_numeric_dtype(series):
            if int(series.notna().sum()) >= min_non_null and series.nunique(dropna=True) > 1:
                columns.append(column)
    return columns


def _with_device_one_hot(frame: pd.DataFrame) -> pd.DataFrame:
    if "device" not in frame.columns:
        return pd.DataFrame(index=frame.index)
    encoded = pd.get_dummies(frame["device"].fillna("unknown"), prefix="device", dtype=int)
    return encoded


def _impute_numeric_features(features: pd.DataFrame) -> pd.DataFrame:
    result = features.copy()
    for column in result.columns:
        result[column] = pd.to_numeric(result[column], errors="coerce")
        median = result[column].median()
        result[f"{column}_missing"] = result[column].isna().astype(int)
        result[column] = result[column].fillna(0.0 if pd.isna(median) else median)
    return result


def add_stratified_split(
    frame: pd.DataFrame,
    label_column: str = TARGET_COLUMN,
    test_size: float = 0.2,
    random_state: int = 42,
) -> pd.Series:
    rng = np.random.default_rng(random_state)
    split = pd.Series("train", index=frame.index, dtype="object")

    for _, group in frame.groupby(label_column):
        indices = group.index.to_numpy()
        rng.shuffle(indices)
        test_count = max(1, int(round(len(indices) * test_size)))
        split.loc[indices[:test_count]] = "test"
    return split


def prepare_ml_dataset(
    synthetic_features: pd.DataFrame,
    min_non_null: int = 10,
    test_size: float = 0.2,
    random_state: int = 42,
) -> PreparedDataset:
    if TARGET_COLUMN not in synthetic_features.columns:
        raise ValueError(f"missing target column: {TARGET_COLUMN}")

    base = synthetic_features.copy()
    base[SPLIT_COLUMN] = add_stratified_split(base, test_size=test_size, random_state=random_state)

    numeric_columns = _numeric_feature_columns(base, min_non_null=min_non_null)
    numeric_features = _impute_numeric_features(base[numeric_columns])
    device_features = _with_device_one_hot(base)
    feature_frame = pd.concat([numeric_features, device_features], axis=1)
    feature_columns = feature_frame.columns.tolist()

    prepared = pd.concat(
        [
            base[["measurement_id", "seed_measurement_id", SPLIT_COLUMN, TARGET_COLUMN, "device"]].reset_index(drop=True),
            feature_frame.reset_index(drop=True),
        ],
        axis=1,
    )

    report = {
        "rows": len(prepared),
        "feature_count": len(feature_columns),
        "scenario_count": int(base[TARGET_COLUMN].nunique()),
        "train_rows": int(prepared[SPLIT_COLUMN].eq("train").sum()),
        "test_rows": int(prepared[SPLIT_COLUMN].eq("test").sum()),
        "feature_columns": feature_columns,
        "class_counts": base[TARGET_COLUMN].value_counts().sort_index().to_dict(),
        "split_counts": prepared.groupby([TARGET_COLUMN, SPLIT_COLUMN]).size().unstack(fill_value=0).to_dict("index"),
    }
    return PreparedDataset(frame=prepared, feature_columns=feature_columns, report=report)


def validation_report_markdown(report: dict[str, object]) -> str:
    class_counts = report["class_counts"]
    split_counts = report["split_counts"]
    feature_columns = report["feature_columns"]

    lines = [
        "# Synthetic ML Dataset Validation Report",
        "",
        "## Summary",
        "",
        f"- Rows: `{report['rows']}`",
        f"- Scenario labels: `{report['scenario_count']}`",
        f"- ML feature columns: `{report['feature_count']}`",
        f"- Train rows: `{report['train_rows']}`",
        f"- Test rows: `{report['test_rows']}`",
        "",
        "## Class Balance",
        "",
        "| Scenario Label | Rows | Train | Test |",
        "|---|---:|---:|---:|",
    ]

    for label, count in class_counts.items():
        split = split_counts.get(label, {})
        lines.append(f"| `{label}` | {count} | {split.get('train', 0)} | {split.get('test', 0)} |")

    lines.extend(
        [
            "",
            "## Feature Columns",
            "",
            "The model-ready dataset contains numeric electrical features, missing-value indicators, and one-hot device columns.",
            "",
            "```text",
            "\n".join(feature_columns),
            "```",
            "",
            "## Notes",
            "",
            "- `scenario_label` is the supervised learning target.",
            "- Metadata, generated explanations, anomaly flags, and process reasoning text are excluded from model features.",
            "- Missing values are imputed with each feature median, and missing indicators are added.",
            "- The split is stratified by scenario label to keep train/test label balance stable.",
        ]
    )
    return "\n".join(lines) + "\n"
