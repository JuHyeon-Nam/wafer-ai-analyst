# Development Roadmap to 2026-08-20

## Objective

Wafer AI Analyst는 wafer electrical test raw data를 자동 분석하고, shot 단위 이상 후보를 분류하며, 가능한 공정/측정 이슈 후보와 설명 결과를 제공하는 분석 workflow입니다.

현재 구현된 rule-based baseline과 explanation agent를 유지하면서, synthetic defect scenario dataset과 RandomForest 기반 ML classifier를 추가합니다.

## Current Baseline

- Clarius-style CSV parser
- Multi-sheet diode Excel parser
- Measurement metadata export
- Normalized curve table export
- Device-level electrical feature extraction
- Rule-based anomaly detection
- Process issue candidate mapping
- Beginner/engineer explanation generation
- Streamlit dashboard
- Synthetic defect scenario schema
- Synthetic feature dataset generator
- ML-ready dataset preparation
- Stratified train/test split validation
- RandomForest baseline training
- Baseline classification report
- RandomForest hyperparameter tuning
- Tuned model report and tuning result table

## Target Architecture

```text
Real wafer measurement data
-> parser
-> feature extraction
-> rule-based anomaly baseline
-> process issue candidate mapping
-> explanation agent
-> dashboard

Synthetic defect scenario data
-> feature dataset
-> RandomForest model training
-> hyperparameter tuning
-> defect type prediction
-> model evaluation
-> dashboard comparison
```

## Schedule

| Date | Goal | Output |
|---|---|---|
| 2026-08-10 | README/project evidence 정리, dashboard preview asset 생성 | README refresh, graph/table preview images |
| 2026-08-11 | Synthetic defect scenario 설계 | defect label schema, scenario rules, generator script |
| 2026-08-12 | Synthetic feature dataset 생성 | ML-ready dataset, feature columns, validation report |
| 2026-08-13 | RandomForest baseline 학습 | training script, saved model artifact, baseline report |
| 2026-08-14 | Hyperparameter tuning | tuning result table, tuned model report |
| 2026-08-15 | Feature importance 분석 | important feature report |
| 2026-08-16 | Dashboard ML prediction view 추가 | rule result와 ML prediction 비교 화면 |
| 2026-08-17 | Curve viewer/detail review 개선 | device/shot별 상세 분석 화면 |
| 2026-08-18 | 자동 report 생성 | Markdown/HTML analysis report |
| 2026-08-19 | Documentation and demo scenario 정리 | README/docs/demo script |
| 2026-08-20 | End-to-end 검증 및 최종 정리 | reproducible release-ready workflow |

## Model Plan

### Model

`RandomForestClassifier`를 baseline model로 사용합니다.

선택 이유:

- Feature table 형태의 tabular data에 잘 맞음
- 소량 데이터에서도 baseline으로 안정적
- deep learning보다 설명하기 쉬움
- feature importance로 모델 판단 근거를 확인할 수 있음
- parameter tuning과 평가 흐름을 명확히 보여줄 수 있음

### Parameters to Tune

| Parameter | Meaning | Candidate Values |
|---|---|---|
| `n_estimators` | decision tree 개수 | `50`, `100`, `200` |
| `max_depth` | 각 tree가 데이터를 얼마나 깊게 나눌지 | `4`, `6`, `8`, `None` |
| `min_samples_leaf` | 마지막 leaf에 필요한 최소 sample 수 | `1`, `3`, `5` |
| `class_weight` | class imbalance 보정 | `None`, `balanced` |

### Evaluation

- Accuracy
- Macro F1-score
- Confusion matrix
- Feature importance

Accuracy만 보면 정상 class가 많은 경우 성능이 과대평가될 수 있으므로, defect class별 F1-score와 confusion matrix를 함께 확인합니다.

### Current Tuning Result

| Model | Train Accuracy | Test Accuracy | Test Macro F1 |
|---|---:|---:|---:|
| Baseline RandomForest | 0.9097 | 0.8819 | 0.8736 |
| Tuned RandomForest | 0.9618 | 0.9028 | 0.8960 |

선택된 parameter 조합은 `n_estimators=100`, `max_depth=None`, `min_samples_leaf=1`, `class_weight=None`입니다.

튜닝 결과 전체 정확도와 macro F1-score는 개선되었지만, `normal` class recall은 아직 낮습니다. 따라서 이 모델은 실제 불량 원인을 확정하는 모델이 아니라, review 우선순위를 정하는 decision support model로 사용합니다.

## Engineering Boundary

Synthetic dataset은 실제 불량 wafer data가 아닙니다. 실제 측정 데이터의 column structure와 electrical feature distribution을 참고해 만든 defect scenario dataset입니다.

따라서 최종 설명은 다음 표현을 기준으로 합니다.

```text
실제 wafer 측정 데이터가 제한적이었기 때문에,
원본 데이터의 curve 구조와 feature 분포를 참고해
synthetic defect scenario dataset을 생성하고,
ML 기반 defect classification 가능성을 검증했다.
```
