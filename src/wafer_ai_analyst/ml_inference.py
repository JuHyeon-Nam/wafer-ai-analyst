from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


def load_model_artifact(path: str | Path) -> dict[str, object]:
    return joblib.load(Path(path))


def prepare_inference_features(features: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    prepared = pd.DataFrame(index=features.index)

    for column in feature_columns:
        if column.startswith("device_"):
            device_name = column.removeprefix("device_")
            prepared[column] = features.get("device", pd.Series(index=features.index)).fillna("unknown").eq(device_name).astype(int)
            continue

        if column.endswith("_missing"):
            source_column = column[: -len("_missing")]
            if source_column in features.columns:
                prepared[column] = features[source_column].isna().astype(int)
            else:
                prepared[column] = 1
            continue

        if column in features.columns:
            values = pd.to_numeric(features[column], errors="coerce")
            median = values.median()
            prepared[column] = values.fillna(0.0 if pd.isna(median) else median)
        else:
            prepared[column] = 0.0

    return prepared[feature_columns]


def predict_feature_table(features: pd.DataFrame, model_artifact: dict[str, object]) -> pd.DataFrame:
    model = model_artifact["model"]
    feature_columns = list(model_artifact["feature_columns"])
    labels = list(model_artifact["labels"])

    prepared = prepare_inference_features(features, feature_columns)
    predicted = model.predict(prepared)
    probabilities = model.predict_proba(prepared)

    rows: list[dict[str, object]] = []
    for idx, label in enumerate(predicted):
        proba = probabilities[idx]
        ranked = sorted(zip(labels, proba, strict=True), key=lambda item: item[1], reverse=True)
        top3 = ranked[:3]
        confidence = float(top3[0][1])
        rows.append(
            {
                "measurement_id": features.iloc[idx].get("measurement_id", f"row-{idx}"),
                "ml_predicted_label": label,
                "ml_confidence": confidence,
                "ml_second_label": top3[1][0] if len(top3) > 1 else None,
                "ml_second_confidence": float(top3[1][1]) if len(top3) > 1 else None,
                "ml_top3_labels": ", ".join(f"{name}:{score:.2f}" for name, score in top3),
                "ml_review_level": _review_level(label, confidence),
            }
        )

    return pd.DataFrame(rows)


def add_ml_predictions(features: pd.DataFrame, model_artifact: dict[str, object]) -> pd.DataFrame:
    predictions = predict_feature_table(features, model_artifact)
    result = features.reset_index(drop=True).copy()
    prediction_columns = [column for column in predictions.columns if column != "measurement_id"]
    return pd.concat([result, predictions[prediction_columns].reset_index(drop=True)], axis=1)


def _review_level(label: str, confidence: float) -> str:
    if label == "normal" and confidence >= 0.65:
        return "ml_normal"
    if confidence < 0.55:
        return "low_confidence_review"
    if label == "normal":
        return "normal_candidate_review"
    return "defect_candidate_review"
