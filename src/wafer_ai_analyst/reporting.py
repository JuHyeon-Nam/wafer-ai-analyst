from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape

import pandas as pd

from .importance import summarize_feature_importance


@dataclass(frozen=True)
class AnalysisReport:
    markdown: str
    html: str


def generate_analysis_report(
    result: pd.DataFrame,
    importance: pd.DataFrame | None = None,
    model_metrics: dict[str, object] | None = None,
    generated_at: datetime | None = None,
) -> AnalysisReport:
    generated_at = generated_at or datetime.now()
    markdown = _markdown_report(result, importance, model_metrics, generated_at)
    html = _html_report(result, importance, model_metrics, generated_at)
    return AnalysisReport(markdown=markdown, html=html)


def _markdown_report(
    result: pd.DataFrame,
    importance: pd.DataFrame | None,
    model_metrics: dict[str, object] | None,
    generated_at: datetime,
) -> str:
    lines = [
        "# Wafer Electrical Test Analysis Report",
        "",
        f"- Generated at: `{generated_at.strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- Measurements: `{len(result)}`",
        f"- Devices: `{_joined_unique(result, 'device')}`",
        f"- Shots: `{_joined_unique(result, 'shot')}`",
        "",
        "## Executive Summary",
        "",
        _executive_summary(result),
        "",
        "## Review Count",
        "",
        _count_table(result, "review_status"),
        "",
        "## ML Prediction Count",
        "",
        _count_table(result, "ml_predicted_label"),
        "",
        "## Device and Shot Coverage",
        "",
        _group_table(result, ["device", "shot"]),
        "",
        "## High Priority Review Candidates",
        "",
        _candidate_table_markdown(result),
        "",
        "## Feature Importance Summary",
        "",
        _importance_markdown(importance),
        "",
        "## Model Metrics",
        "",
        _model_metrics_markdown(model_metrics),
        "",
        "## Engineering Notes",
        "",
        "- Rule-based result는 사람이 정의한 전기적 기준입니다.",
        "- ML prediction은 synthetic defect scenario dataset으로 학습한 RandomForest 모델의 후보 판단입니다.",
        "- Root cause를 확정하려면 공정 recipe, 박막 두께, 온도/압력/시간 조건, 장비 log, 반복 측정 데이터가 추가로 필요합니다.",
        "- 이 리포트는 이상 후보를 빠르게 좁히는 review workflow 산출물로 사용합니다.",
    ]
    return "\n".join(lines) + "\n"


def _html_report(
    result: pd.DataFrame,
    importance: pd.DataFrame | None,
    model_metrics: dict[str, object] | None,
    generated_at: datetime,
) -> str:
    review_counts = _counts_frame(result, "review_status")
    ml_counts = _counts_frame(result, "ml_predicted_label")
    device_shot = _group_frame(result, ["device", "shot"])
    candidates = _candidate_frame(result)
    top_features, group_summary = _importance_frames(importance)

    body = f"""
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Wafer Electrical Test Analysis Report</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #172033;
      background: #f5f7fb;
    }}
    header {{
      padding: 32px 40px;
      background: #0b2545;
      color: white;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 28px;
    }}
    h1, h2 {{
      margin: 0 0 12px;
    }}
    section {{
      margin: 0 0 24px;
      padding: 22px;
      background: white;
      border: 1px solid #dfe6f1;
      border-radius: 8px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 12px;
      margin-top: 20px;
    }}
    .metric {{
      padding: 16px;
      background: #eef4fb;
      border-left: 4px solid #2e74b5;
      border-radius: 6px;
    }}
    .metric span {{
      display: block;
      color: #526070;
      font-size: 13px;
    }}
    .metric strong {{
      display: block;
      margin-top: 6px;
      font-size: 24px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid #dfe6f1;
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      color: #0b2545;
      background: #f0f4f8;
    }}
    .note {{
      line-height: 1.65;
    }}
    .tag {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 999px;
      background: #e8f0fe;
      color: #0b2545;
      font-size: 12px;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Wafer Electrical Test Analysis Report</h1>
    <p>Rule-based anomaly review + RandomForest ML prediction + feature importance summary</p>
    <div class="metrics">
      <div class="metric"><span>Generated</span><strong>{escape(generated_at.strftime('%Y-%m-%d %H:%M'))}</strong></div>
      <div class="metric"><span>Measurements</span><strong>{len(result)}</strong></div>
      <div class="metric"><span>Devices</span><strong>{escape(_joined_unique(result, 'device'))}</strong></div>
      <div class="metric"><span>Shots</span><strong>{escape(_joined_unique(result, 'shot'))}</strong></div>
    </div>
  </header>
  <main>
    <section>
      <h2>Executive Summary</h2>
      <p class="note">{escape(_executive_summary(result))}</p>
    </section>
    <section>
      <h2>Review Count</h2>
      {_html_table(review_counts)}
    </section>
    <section>
      <h2>ML Prediction Count</h2>
      {_html_table(ml_counts)}
    </section>
    <section>
      <h2>Device and Shot Coverage</h2>
      {_html_table(device_shot)}
    </section>
    <section>
      <h2>High Priority Review Candidates</h2>
      {_html_table(candidates)}
    </section>
    <section>
      <h2>Feature Importance by Group</h2>
      {_html_table(group_summary)}
    </section>
    <section>
      <h2>Top Feature Importance</h2>
      {_html_table(top_features)}
    </section>
    <section>
      <h2>Model Metrics</h2>
      {_html_table(_model_metrics_frame(model_metrics))}
    </section>
    <section>
      <h2>Engineering Notes</h2>
      <p class="note">
        Rule result는 사람이 정한 전기적 기준이고, ML prediction은 synthetic defect scenario dataset으로 학습한 모델의 후보 판단입니다.
        이 리포트는 root cause를 확정하는 문서가 아니라, 먼저 확인할 shot/device 후보와 전기 feature를 좁히는 review workflow 산출물입니다.
      </p>
    </section>
  </main>
</body>
</html>
"""
    return body.strip() + "\n"


def _joined_unique(frame: pd.DataFrame, column: str) -> str:
    if column not in frame.columns:
        return "unknown"
    values = sorted(str(value) for value in frame[column].dropna().unique().tolist())
    return ", ".join(values) if values else "unknown"


def _executive_summary(result: pd.DataFrame) -> str:
    total = len(result)
    priority = _count_value(result, "review_status", "priority")
    review = _count_value(result, "review_status", "review")
    ml_defect = int(result["ml_predicted_label"].ne("normal").sum()) if "ml_predicted_label" in result else 0
    low_confidence = _count_value(result, "ml_review_level", "low_confidence_review")
    return (
        f"총 {total}개 measurement를 분석했습니다. Rule 기준 priority 후보는 {priority}개, review 후보는 {review}개입니다. "
        f"ML 모델은 {ml_defect}개 measurement를 normal이 아닌 defect scenario 후보로 분류했고, "
        f"그중 confidence가 낮아 추가 확인이 필요한 항목은 {low_confidence}개입니다."
    )


def _count_value(frame: pd.DataFrame, column: str, value: str) -> int:
    if column not in frame.columns:
        return 0
    return int(frame[column].fillna("unknown").eq(value).sum())


def _counts_frame(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in frame.columns:
        return pd.DataFrame({"item": ["not_available"], "count": [0]})
    return frame[column].fillna("unknown").value_counts().rename_axis("item").reset_index(name="count")


def _count_table(frame: pd.DataFrame, column: str) -> str:
    return _markdown_table(_counts_frame(frame, column))


def _group_frame(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    available = [column for column in columns if column in frame.columns]
    if not available:
        return pd.DataFrame({"item": ["not_available"], "count": [0]})
    return frame.groupby(available, dropna=False).size().reset_index(name="count")


def _group_table(frame: pd.DataFrame, columns: list[str]) -> str:
    return _markdown_table(_group_frame(frame, columns))


def _candidate_frame(frame: pd.DataFrame, limit: int = 15) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    result = frame.copy()
    if "ml_confidence" in result.columns:
        result["ml_confidence"] = pd.to_numeric(result["ml_confidence"], errors="coerce").fillna(0)
    else:
        result["ml_confidence"] = 0.0

    if "anomaly_score" in result.columns:
        result["anomaly_score"] = pd.to_numeric(result["anomaly_score"], errors="coerce").fillna(0)
    else:
        result["anomaly_score"] = 0.0

    if "ml_predicted_label" in result.columns:
        defect_mask = result["ml_predicted_label"].fillna("normal").ne("normal")
    else:
        defect_mask = pd.Series(False, index=result.index)
    if "review_status" in result.columns:
        rule_mask = result["review_status"].fillna("normal").isin(["review", "priority"])
    else:
        rule_mask = pd.Series(False, index=result.index)

    candidates = result[defect_mask | rule_mask].copy()
    if candidates.empty:
        candidates = result.copy()
    candidates = candidates.sort_values(["anomaly_score", "ml_confidence"], ascending=False)
    if "measurement_id" in candidates.columns:
        candidates = candidates.drop_duplicates(subset=["measurement_id"], keep="first")
    candidates = candidates.head(limit)
    columns = [
        "measurement_id",
        "device",
        "shot",
        "review_status",
        "anomaly_flags",
        "ml_predicted_label",
        "ml_confidence",
        "process_issue_candidates",
    ]
    available = [column for column in columns if column in candidates.columns]
    display = candidates[available].copy()
    if "ml_confidence" in display.columns:
        display["ml_confidence"] = display["ml_confidence"].map(lambda value: f"{float(value):.3f}")
    return display


def _candidate_table_markdown(frame: pd.DataFrame) -> str:
    candidates = _candidate_frame(frame)
    if candidates.empty:
        return "No candidate rows available."
    return _markdown_table(candidates)


def _importance_frames(importance: pd.DataFrame | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    if importance is None or importance.empty:
        empty = pd.DataFrame({"item": ["not_available"], "value": [0]})
        return empty, empty
    top, group_summary = summarize_feature_importance(importance)
    top_display = top[["feature", "feature_group", "importance", "plain_explanation"]].head(12).copy()
    top_display["importance"] = top_display["importance"].map(lambda value: f"{float(value):.4f}")
    group_display = group_summary.copy()
    group_display["importance"] = group_display["importance"].map(lambda value: f"{float(value):.4f}")
    group_display["importance_share"] = group_display["importance_share"].map(lambda value: f"{float(value) * 100:.1f}%")
    return top_display, group_display


def _importance_markdown(importance: pd.DataFrame | None) -> str:
    top, group_summary = _importance_frames(importance)
    return "\n".join(
        [
            "### By Feature Group",
            "",
            _markdown_table(group_summary),
            "",
            "### Top Features",
            "",
            _markdown_table(top),
        ]
    )


def _model_metrics_frame(model_metrics: dict[str, object] | None) -> pd.DataFrame:
    if not model_metrics:
        return pd.DataFrame({"metric": ["not_available"], "value": ["not_available"]})
    rows = []
    for key in ["train_accuracy", "test_accuracy", "test_macro_f1", "train_rows", "test_rows", "feature_count"]:
        if key in model_metrics:
            value = model_metrics[key]
            if isinstance(value, float):
                value = f"{value:.4f}"
            rows.append({"metric": key, "value": value})
    parameters = model_metrics.get("parameters")
    if isinstance(parameters, dict):
        for key, value in parameters.items():
            if value is None:
                value = "None"
            rows.append({"metric": f"parameter.{key}", "value": value})
    return pd.DataFrame(rows) if rows else pd.DataFrame({"metric": ["not_available"], "value": ["not_available"]})


def _model_metrics_markdown(model_metrics: dict[str, object] | None) -> str:
    return _markdown_table(_model_metrics_frame(model_metrics))


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "No rows available."
    table = frame.fillna("")
    headers = [str(column) for column in table.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in table.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(_clean_cell(value) for value in row) + " |")
    return "\n".join(lines)


def _html_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "<p>No rows available.</p>"
    table = frame.fillna("")
    headers = "".join(f"<th>{escape(str(column))}</th>" for column in table.columns)
    rows = []
    for row in table.itertuples(index=False, name=None):
        cells = "".join(f"<td>{escape(str(value))}</td>" for value in row)
        rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{headers}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def _clean_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "/")
