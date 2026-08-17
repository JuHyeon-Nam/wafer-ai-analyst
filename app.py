from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.wafer_ai_analyst.explanations import add_explanations
from src.wafer_ai_analyst.features import extract_features
from src.wafer_ai_analyst.importance import summarize_feature_importance
from src.wafer_ai_analyst.ml_inference import add_ml_predictions, load_model_artifact
from src.wafer_ai_analyst.parsers import load_measurements, measurements_to_curve_frame
from src.wafer_ai_analyst.process_reasoning import infer_process_candidates
from src.wafer_ai_analyst.rules import apply_anomaly_rules


DEFAULT_INPUT_PATH = "data/raw"
DEFAULT_FEATURE_PATH = "data/processed/features_preview.csv"
DEFAULT_CURVE_PATH = "data/processed/curves_preview.csv"
DEFAULT_MODEL_PATH = "models/random_forest_tuned.joblib"
DEFAULT_IMPORTANCE_PATH = "data/processed/rf_tuned_feature_importance_preview.csv"


st.set_page_config(page_title="Wafer AI Analyst", layout="wide")


def run_rule_pipeline(input_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    measurements = load_measurements(Path(input_path))
    features = extract_features(measurements)
    result = apply_anomaly_rules(features)
    result["process_issue_candidates"] = result["anomaly_flags"].map(infer_process_candidates)
    result = add_explanations(result)
    curves = measurements_to_curve_frame(measurements)
    return result, curves


def attach_model_result(result: pd.DataFrame, model_path: str) -> pd.DataFrame:
    path = Path(model_path)
    if not path.exists() or result.empty:
        return result
    artifact = load_model_artifact(path)
    return add_ml_predictions(result, artifact)


def load_demo_tables(feature_path: str, curve_path: str, model_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    result = pd.read_csv(feature_path)
    result = attach_model_result(result, model_path)
    curves = pd.read_csv(curve_path) if Path(curve_path).exists() else pd.DataFrame()
    return result, curves


def render_metrics(result: pd.DataFrame) -> None:
    total, normal, review, priority, ml_defect = st.columns(5)
    total.metric("Measurements", len(result))
    normal.metric("Rule Normal", int(result["review_status"].eq("normal").sum()) if "review_status" in result else 0)
    review.metric("Rule Review", int(result["review_status"].eq("review").sum()) if "review_status" in result else 0)
    priority.metric("Rule Priority", int(result["review_status"].eq("priority").sum()) if "review_status" in result else 0)
    if "ml_review_level" in result:
        ml_defect.metric("ML Defect Review", int(result["ml_review_level"].eq("defect_candidate_review").sum()))
    else:
        ml_defect.metric("ML Defect Review", 0)


def render_overview(result: pd.DataFrame) -> None:
    render_metrics(result)

    if {"device", "shot"}.issubset(result.columns):
        left, right = st.columns(2)
        with left:
            st.subheader("Shot Count by Device")
            chart_data = result.groupby(["device", "shot"], dropna=False).size().reset_index(name="count")
            fig = px.bar(chart_data, x="shot", y="count", color="device", barmode="group")
            st.plotly_chart(fig, width="stretch")
        with right:
            st.subheader("Rule Review Status")
            if "review_status" in result.columns:
                status_data = result.groupby(["device", "review_status"], dropna=False).size().reset_index(name="count")
                fig = px.bar(status_data, x="device", y="count", color="review_status", barmode="stack")
                st.plotly_chart(fig, width="stretch")

    st.subheader("Feature Table")
    st.dataframe(result, width="stretch")


def render_ml_prediction(result: pd.DataFrame) -> None:
    required = {"device", "ml_predicted_label", "ml_confidence", "ml_review_level"}
    if not required.issubset(result.columns):
        st.info("학습된 model artifact가 없어서 ML prediction view를 표시하지 못했습니다.")
        return

    left, right = st.columns(2)
    with left:
        st.subheader("ML Predicted Defect Label")
        chart_data = result.groupby(["device", "ml_predicted_label"], dropna=False).size().reset_index(name="count")
        fig = px.bar(chart_data, x="device", y="count", color="ml_predicted_label", barmode="stack")
        st.plotly_chart(fig, width="stretch")
    with right:
        st.subheader("Rule vs ML Review Level")
        compare = result.groupby(["review_status", "ml_review_level"], dropna=False).size().reset_index(name="count")
        fig = px.bar(compare, x="review_status", y="count", color="ml_review_level", barmode="group")
        st.plotly_chart(fig, width="stretch")

    columns = [
        "measurement_id",
        "device",
        "shot",
        "review_status",
        "anomaly_flags",
        "ml_predicted_label",
        "ml_confidence",
        "ml_second_label",
        "ml_second_confidence",
        "ml_top3_labels",
        "process_issue_candidates",
    ]
    available = [column for column in columns if column in result.columns]
    st.subheader("ML Review Table")
    st.dataframe(result[available].sort_values("ml_confidence", ascending=False), width="stretch")


def render_feature_importance(importance_path: str) -> None:
    path = Path(importance_path)
    if not path.exists():
        st.info("feature importance CSV가 아직 없습니다.")
        return

    importance = pd.read_csv(path)
    top, group_summary = summarize_feature_importance(importance)

    left, right = st.columns(2)
    with left:
        st.subheader("Top Feature Importance")
        fig = px.bar(
            top.sort_values("importance"),
            x="importance",
            y="feature",
            color="feature_group",
            orientation="h",
        )
        st.plotly_chart(fig, width="stretch")
    with right:
        st.subheader("Importance by Feature Group")
        fig = px.pie(group_summary, names="feature_group", values="importance")
        st.plotly_chart(fig, width="stretch")

    st.subheader("Plain Explanation")
    st.dataframe(top[["feature", "feature_group", "importance", "plain_explanation"]], width="stretch")


def render_curve_detail(result: pd.DataFrame, curves: pd.DataFrame) -> None:
    if result.empty:
        st.info("표시할 measurement가 없습니다.")
        return

    label_source = result["measurement_id"] if "measurement_id" in result.columns else result.index.to_series().astype(str)
    selected_label = st.selectbox("Measurement", label_source.tolist())
    selected = result[label_source.eq(selected_label)].iloc[0]

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Selected Measurement")
        summary_columns = [
            "measurement_id",
            "device",
            "shot",
            "review_status",
            "anomaly_flags",
            "ml_predicted_label",
            "ml_confidence",
            "process_issue_candidates",
        ]
        available = [column for column in summary_columns if column in result.columns]
        st.dataframe(pd.DataFrame([selected[available]]), width="stretch")

        if "engineer_explanation" in selected:
            st.markdown("**Engineer Explanation**")
            st.write(selected["engineer_explanation"])

    with right:
        st.subheader("Raw Curve")
        if curves.empty or "measurement_id" not in curves.columns:
            st.info("curve table이 없습니다.")
            return
        curve = curves[curves["measurement_id"].eq(selected["measurement_id"])].copy()
        if curve.empty:
            st.info("선택한 measurement의 curve row가 없습니다.")
            return
        _plot_curve(curve, str(selected.get("device", "")))


def _plot_curve(curve: pd.DataFrame, device: str) -> None:
    if device == "Cap" and {"V", "C"}.issubset(curve.columns):
        fig = px.line(curve, x="V", y="C", markers=True, title="Capacitor C-V Curve")
        st.plotly_chart(fig, width="stretch")
        return
    if device == "diode" and {"AnodeV", "AnodeI"}.issubset(curve.columns):
        fig = px.line(curve, x="AnodeV", y="AnodeI", markers=True, title="Diode I-V Curve")
        st.plotly_chart(fig, width="stretch")
        return
    if device == "resistor" and {"AV", "AI"}.issubset(curve.columns):
        fig = px.line(curve, x="AV", y="AI", markers=True, title="Resistor I-V Curve")
        st.plotly_chart(fig, width="stretch")
        return
    if device == "NMOS" and {"GateV", "DrainI"}.issubset(curve.columns):
        fig = px.line(curve, x="GateV", y="DrainI", markers=True, title="NMOS Id-Vg Curve")
        st.plotly_chart(fig, width="stretch")
        if "GateI" in curve.columns:
            leak_fig = px.line(curve, x="GateV", y="GateI", markers=True, title="NMOS Gate Leakage Curve")
            st.plotly_chart(leak_fig, width="stretch")
        return
    st.dataframe(curve, width="stretch")


def render_explanation(result: pd.DataFrame) -> None:
    if not {"beginner_explanation", "engineer_explanation", "llm_prompt"}.issubset(result.columns):
        st.info("explanation columns are not available yet.")
        return

    label_source = result["measurement_id"] if "measurement_id" in result.columns else result.index.to_series().astype(str)
    selected_label = st.selectbox("Explanation Measurement", label_source.tolist())
    selected = result[label_source.eq(selected_label)].iloc[0]
    beginner_tab, engineer_tab, prompt_tab = st.tabs(["Beginner", "Engineer", "LLM Prompt"])
    with beginner_tab:
        st.write(selected["beginner_explanation"])
    with engineer_tab:
        st.write(selected["engineer_explanation"])
    with prompt_tab:
        st.code(selected["llm_prompt"], language="text")


st.title("Wafer AI Analyst")
st.caption("반도체 웨이퍼 전기 측정 데이터 AI 품질 분석 에이전트")

with st.sidebar:
    st.header("Inputs")
    input_path = st.text_input("Raw data path", DEFAULT_INPUT_PATH)
    feature_path = st.text_input("Demo feature CSV", DEFAULT_FEATURE_PATH)
    curve_path = st.text_input("Demo curve CSV", DEFAULT_CURVE_PATH)
    model_path = st.text_input("Model artifact", DEFAULT_MODEL_PATH)
    importance_path = st.text_input("Feature importance CSV", DEFAULT_IMPORTANCE_PATH)

    if st.button("Raw Data 분석 실행"):
        result, curves = run_rule_pipeline(input_path)
        result = attach_model_result(result, model_path)
        st.session_state["result"] = result
        st.session_state["curves"] = curves

    if st.button("Demo 결과 불러오기"):
        result, curves = load_demo_tables(feature_path, curve_path, model_path)
        st.session_state["result"] = result
        st.session_state["curves"] = curves

if "result" not in st.session_state and Path(DEFAULT_FEATURE_PATH).exists():
    result, curves = load_demo_tables(DEFAULT_FEATURE_PATH, DEFAULT_CURVE_PATH, DEFAULT_MODEL_PATH)
    st.session_state["result"] = result
    st.session_state["curves"] = curves

if "result" in st.session_state:
    result = st.session_state["result"]
    curves = st.session_state.get("curves", pd.DataFrame())
    overview_tab, ml_tab, importance_tab, detail_tab, explanation_tab = st.tabs(
        ["Overview", "ML Prediction", "Feature Importance", "Curve Detail", "Explanation"]
    )
    with overview_tab:
        render_overview(result)
    with ml_tab:
        render_ml_prediction(result)
    with importance_tab:
        render_feature_importance(importance_path)
    with detail_tab:
        render_curve_detail(result, curves)
    with explanation_tab:
        render_explanation(result)
else:
    st.info("Raw data path를 분석하거나 Demo 결과를 불러오세요.")
