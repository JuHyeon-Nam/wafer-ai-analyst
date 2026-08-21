# Release Notes

## 2026-08-20

Wafer AI Analyst is organized as a reproducible local demo for semiconductor electrical test analysis.

## 2026-08-21

Portfolio and interview preparation documents were added after release validation.

| Area | Result |
|---|---|
| Portfolio brief | One-page project summary with problem, solution, result, and boundary |
| Interview playbook | 30-second, 1-minute, 3-minute answers and technical Q&A |
| Team talking points | Role-based explanation points for each team member |
| Portfolio packet | Combined Markdown packet for review and rehearsal |

## What Is Included

| Area | Result |
|---|---|
| Raw data parsing | Clarius-style CSV and multi-sheet diode Excel parsing |
| Feature engineering | Diode, resistor, capacitor, and NMOS electrical feature extraction |
| Rule-based review | `normal`, `review`, `priority` status and anomaly flags |
| Process reasoning | Candidate process/measurement issues mapped from anomaly flags |
| Explanation workflow | Beginner/engineer explanation text and LLM prompt |
| Synthetic ML data | Defect scenario dataset generated from real feature distributions |
| Model training | RandomForest baseline and tuned classifier |
| Model evaluation | Accuracy, macro F1-score, confusion matrix, per-class metrics |
| Interpretability | Feature importance by feature and feature group |
| Dashboard | Overview, ML prediction, feature importance, curve detail, explanation, report tabs |
| Reporting | Markdown/HTML analysis report generation |
| Demo validation | Local artifact check and final validation summary |

## Final Metrics

| Model | Train Accuracy | Test Accuracy | Test Macro F1 |
|---|---:|---:|---:|
| Baseline RandomForest | 0.9774 | 0.9583 | 0.9560 |
| Tuned RandomForest | 0.9896 | 0.9722 | 0.9718 |

Selected tuned model:

| Parameter | Value |
|---|---:|
| `n_estimators` | `100` |
| `max_depth` | `None` |
| `min_samples_leaf` | `3` |
| `class_weight` | `None` |

## Demo Dataset Snapshot

| Item | Value |
|---|---:|
| Measurements | 74 |
| Curve points | 10,294 |
| Devices | Cap, NMOS, diode, resistor |
| Shots | 1-1, 1-4, 5-1, 5-4, 9-1, 9-4 |

## How To Validate

```bash
python scripts/run_demo_check.py
python scripts/run_final_validation.py
streamlit run app.py
```

## Engineering Boundary

This project does not claim confirmed semiconductor root cause analysis.

The real dataset has limited confirmed defect labels, so the supervised ML workflow uses synthetic defect scenarios generated from real electrical feature distributions. The output should be explained as a decision support workflow that narrows review candidates, not as a production-grade defect disposition system.

## Recommended Demo Path

```text
README overview
-> Dashboard Overview
-> ML Prediction
-> Feature Importance
-> Curve Detail
-> Report download
-> DEMO_GUIDE Q&A
```
