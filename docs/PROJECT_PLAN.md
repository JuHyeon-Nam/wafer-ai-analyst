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
- Feature importance analysis
- Dashboard ML prediction view
- Shot-level curve detail review
- Automated Markdown/HTML analysis report generation
- Demo guide and local artifact validation script
- Final validation summary and release notes

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
-> shot-level curve review
-> Markdown/HTML report artifact
-> demo check summary
-> final validation summary
```

## Schedule

| Date | Goal | Output |
|---|---|---|
| 2026-08-10 | README/project evidence 정리, dashboard preview asset 생성 | README refresh, graph/table preview images |
| 2026-08-11 | Synthetic defect scenario 설계 | defect label schema, scenario rules, generator script |
| 2026-08-12 | Synthetic feature dataset 생성 | ML-ready dataset, feature columns, validation report |
| 2026-08-13 | RandomForest baseline 학습 | training script, saved model artifact, baseline report |
| 2026-08-14 | Hyperparameter tuning | tuning result table, tuned model report |
| 2026-08-15 | Feature importance 분석 | important feature report, feature group summary |
| 2026-08-16 | Dashboard ML prediction view 추가 | rule result와 ML prediction 비교 화면 |
| 2026-08-17 | Curve viewer/detail review 개선 | device/shot별 상세 분석 화면 |
| 2026-08-18 | 자동 report 생성 | report generator, Markdown/HTML analysis report |
| 2026-08-19 | Documentation and demo scenario 정리 | demo guide, demo check summary |
| 2026-08-20 | End-to-end 검증 및 최종 정리 | final validation summary, release notes |

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
| Baseline RandomForest | 0.9774 | 0.9583 | 0.9560 |
| Tuned RandomForest | 0.9896 | 0.9722 | 0.9718 |

선택된 parameter 조합은 `n_estimators=100`, `max_depth=None`, `min_samples_leaf=3`, `class_weight=None`입니다.

튜닝 결과 전체 정확도와 macro F1-score는 개선되었지만, `normal` class 일부는 여전히 defect 후보와 혼동될 수 있습니다. 따라서 이 모델은 실제 불량 원인을 확정하는 모델이 아니라, review 우선순위를 정하는 decision support model로 사용합니다.

## Dashboard Integration

Dashboard는 다음 흐름으로 구성합니다.

```text
feature table
-> rule-based anomaly status
-> tuned RandomForest prediction
-> feature importance chart
-> selected measurement raw curve
-> beginner/engineer explanation
```

현재 dashboard는 `Overview`, `ML Prediction`, `Feature Importance`, `Curve Detail`, `Explanation` tab으로 구성되어 있습니다.

특히 `Curve Detail` tab은 ML prediction만 보여주는 것이 아니라, 선택한 measurement의 raw IV/CV curve를 같이 보여줍니다. 이 때문에 모델 결과를 숫자로만 받아들이지 않고 실제 전기 curve shape와 함께 리뷰할 수 있습니다.

## Report Generation

분석 결과는 `scripts/generate_analysis_report.py`로 Markdown과 HTML report artifact를 생성합니다.

Report에는 다음 항목이 포함됩니다.

- 전체 measurement/device/shot summary
- rule-based review count
- ML predicted label count
- high-priority review candidate table
- feature importance group summary
- tuned model metrics
- engineering boundary note

이 기능은 dashboard 화면을 직접 보여주기 어려운 상황에서도 분석 결과를 문서로 제출하거나 공유할 수 있게 하기 위한 단계입니다.

## Demo Validation

시연 전에는 `scripts/run_demo_check.py`를 실행해 local artifact가 준비되어 있는지 확인합니다.

검증 항목은 다음과 같습니다.

- `features_preview.csv` 존재 여부
- `curves_preview.csv` 존재 여부
- tuned RandomForest model artifact 존재 여부
- feature importance CSV 존재 여부
- tuned model metrics JSON 존재 여부
- measurement 수와 curve point 수
- rule review count와 ML prediction count
- 주요 review candidate preview

발표 흐름과 예상 질문 답변은 `docs/DEMO_GUIDE.md`에 정리했습니다.

## Final Validation

최종 검증은 `scripts/run_final_validation.py`로 실행합니다.

검증 항목은 다음과 같습니다.

- 필수 source/document/local artifact 존재 여부
- Python compile 가능 여부
- 핵심 분석 module import 가능 여부
- demo feature/curve/model artifact 연결 여부
- tuned model metric 기준 통과 여부
- Markdown/HTML report 생성 가능 여부

현재 최종 검증 결과는 `65 PASS / 0 FAIL`입니다.

최종 정리 문서는 다음 두 파일입니다.

- `docs/FINAL_VALIDATION.md`
- `docs/RELEASE_NOTES.md`

## Engineering Boundary

Synthetic dataset은 실제 불량 wafer data가 아닙니다. 실제 측정 데이터의 column structure와 electrical feature distribution을 참고해 만든 defect scenario dataset입니다.

따라서 최종 설명은 다음 표현을 기준으로 합니다.

```text
실제 wafer 측정 데이터가 제한적이었기 때문에,
원본 데이터의 curve 구조와 feature 분포를 참고해
synthetic defect scenario dataset을 생성하고,
ML 기반 defect classification 가능성을 검증했다.
```
