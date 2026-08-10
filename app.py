from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.wafer_ai_analyst.explanations import add_explanations
from src.wafer_ai_analyst.features import extract_features
from src.wafer_ai_analyst.parsers import load_measurements
from src.wafer_ai_analyst.process_reasoning import infer_process_candidates
from src.wafer_ai_analyst.rules import apply_anomaly_rules


st.set_page_config(page_title="Wafer AI Analyst", layout="wide")

st.title("Wafer AI Analyst")
st.caption("반도체 웨이퍼 전기 측정 데이터 AI 품질 분석 에이전트")

input_path = st.text_input("분석할 로컬 데이터 경로", "data/raw")

if st.button("분석 실행"):
    measurements = load_measurements(Path(input_path))
    features = extract_features(measurements)
    result = apply_anomaly_rules(features)
    result["process_issue_candidates"] = result["anomaly_flags"].map(infer_process_candidates)
    result = add_explanations(result)
    st.session_state["result"] = result

if "result" in st.session_state:
    result = st.session_state["result"]
    total, normal, review, priority = st.columns(4)
    total.metric("Measurements", len(result))
    normal.metric("Normal", int(result["review_status"].eq("normal").sum()) if "review_status" in result else 0)
    review.metric("Review", int(result["review_status"].eq("review").sum()) if "review_status" in result else 0)
    priority.metric("Priority", int(result["review_status"].eq("priority").sum()) if "review_status" in result else 0)

    st.subheader("Feature Table")
    st.dataframe(result, use_container_width=True)

    if {"device", "shot"}.issubset(result.columns):
        left, right = st.columns(2)
        with left:
            st.subheader("Shot Count by Device")
            chart_data = result.groupby(["device", "shot"], dropna=False).size().reset_index(name="count")
            fig = px.bar(chart_data, x="shot", y="count", color="device", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        with right:
            st.subheader("Review Status")
            if "review_status" in result.columns:
                status_data = result.groupby(["device", "review_status"], dropna=False).size().reset_index(name="count")
                fig = px.bar(status_data, x="device", y="count", color="review_status", barmode="stack")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("review_status column is not available yet.")

    if {"beginner_explanation", "engineer_explanation", "llm_prompt"}.issubset(result.columns):
        st.subheader("AI Explanation")
        label_source = (
            result["measurement_id"]
            if "measurement_id" in result.columns
            else result.index.to_series().astype(str)
        )
        selected_label = st.selectbox("Measurement", label_source.tolist())
        selected = result[label_source.eq(selected_label)].iloc[0]
        beginner_tab, engineer_tab, prompt_tab = st.tabs(["Beginner", "Engineer", "LLM Prompt"])
        with beginner_tab:
            st.write(selected["beginner_explanation"])
        with engineer_tab:
            st.write(selected["engineer_explanation"])
        with prompt_tab:
            st.code(selected["llm_prompt"], language="text")
else:
    st.info("데이터 경로를 입력하고 분석 실행을 누르세요.")
