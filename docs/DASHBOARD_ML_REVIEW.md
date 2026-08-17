# Dashboard ML Review Workflow

## Purpose

Streamlit dashboard는 rule-based anomaly result와 tuned RandomForest prediction을 한 화면에서 비교하기 위한 review tool입니다.

이 dashboard의 목적은 공정 불량 원인을 확정하는 것이 아니라, 전기 측정 데이터에서 먼저 확인할 shot/device 후보를 좁히는 것입니다.

## Dashboard Tabs

| Tab | What It Shows | Why It Matters |
|---|---|---|
| Overview | 전체 measurement 수, rule status, shot/device chart, feature table | wafer 측정 데이터가 어떤 소자와 shot에 분포하는지 빠르게 확인 |
| ML Prediction | RandomForest predicted label, confidence, rule result와 ML result 비교 | rule과 ML이 같은 방향을 보는지, 다른 판단을 하는지 확인 |
| Feature Importance | 모델이 많이 사용한 feature와 feature group | AI 모델이 어떤 전기적 지표를 근거로 판단했는지 설명 |
| Curve Detail | 선택한 measurement의 raw IV/CV curve와 rule/ML 판단 | 숫자 table만 보지 않고 실제 curve shape를 같이 확인 |
| Explanation | beginner/engineer explanation과 LLM prompt | 결과를 비전공자와 엔지니어 관점으로 각각 설명 |

## ML Prediction Logic

학습된 RandomForest model artifact는 `models/random_forest_tuned.joblib`에 저장됩니다.

Dashboard는 feature table을 model input 형태로 바꾼 뒤 prediction을 수행합니다.

```text
feature table
-> numeric feature alignment
-> missing indicator 생성
-> device one-hot column 생성
-> RandomForest prediction
-> predicted label / confidence / top3 label 표시
```

## Review Rule

| ML Output | Meaning |
|---|---|
| `ml_normal` | 모델이 정상 후보로 비교적 확신함 |
| `normal_candidate_review` | 정상 후보지만 confidence가 충분히 높지 않아 확인 필요 |
| `defect_candidate_review` | 모델이 불량 scenario 후보로 분류 |
| `low_confidence_review` | 모델 확신도가 낮아 rule result와 curve를 같이 봐야 함 |

## Engineering Interpretation

- Rule result는 사람이 정한 전기적 기준입니다.
- ML prediction은 synthetic defect scenario를 학습한 모델의 판단입니다.
- 두 결과가 같은 방향이면 review 우선순위가 높아집니다.
- 두 결과가 다르면 curve detail에서 실제 IV/CV shape를 확인합니다.
- Confidence가 낮으면 모델이 확신하지 못한 것이므로 단정하지 않습니다.

## Current Limitation

현재 모델은 synthetic defect scenario dataset으로 학습했습니다. 따라서 실제 양산 공정의 root cause를 직접 확정할 수 없습니다.

다만 실제 wafer measurement structure를 기반으로 feature extraction, model training, tuning, importance analysis, dashboard inference까지 연결했기 때문에 AI-assisted semiconductor test review workflow로 설명할 수 있습니다.
