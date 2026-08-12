# ML Dataset Preparation

## Purpose

Synthetic defect scenario dataset을 바로 모델에 넣을 수는 없습니다. 원본 synthetic table에는 설명 문장, anomaly flag, process issue candidate, seed id 같은 정보가 함께 들어 있기 때문입니다.

ML Dataset Preparation 단계에서는 모델이 봐야 할 feature와 보면 안 되는 metadata를 분리하고, train/test split을 만듭니다.

## Input

```text
data/processed/synthetic_features.csv
```

이 파일은 scenario별 synthetic feature row를 포함합니다.

## Output

```text
data/processed/ml_dataset.csv
data/processed/ml_feature_columns.txt
docs/SYNTHETIC_ML_DATASET_VALIDATION.md
```

## What Is Removed

다음 정보는 모델 feature에서 제외합니다.

| Removed Type | Reason |
|---|---|
| `measurement_id`, `seed_measurement_id`, `synthetic_id` | ID는 defect 판단 근거가 아니기 때문 |
| `scenario_description`, `modified_features` | 정답 label 설명이므로 모델이 보면 안 됨 |
| `anomaly_flags`, `review_status` | rule 결과가 target label과 연결되어 있어 label leakage 위험 |
| `process_issue_candidates` | 사람이 해석한 결과라서 모델 입력에서 제외 |
| `beginner_explanation`, `engineer_explanation`, `llm_prompt` | 자연어 설명은 이번 baseline classifier 입력이 아님 |
| `rows` | 측정 포인트 개수는 전기적 defect feature로 보기 어려움 |

## What Is Kept

모델에는 다음 정보만 남깁니다.

- 소자별 numeric electrical feature
- 결측 여부를 나타내는 missing indicator
- device one-hot column
- target label인 `scenario_label`
- 학습/평가 구분용 `split`

## Missing Value Handling

소자별 feature는 서로 다릅니다. 예를 들어 diode row에는 `resistance_ohm`이 없고, resistor row에는 `gate_leak_abs_max_a`가 없습니다.

이 문제를 처리하기 위해:

1. numeric feature는 median으로 채웁니다.
2. 원래 비어 있었는지를 나타내는 `_missing` column을 추가합니다.

이렇게 하면 모델은 값 자체와 함께 "이 feature가 원래 없는 소자였는지"도 볼 수 있습니다.

## Train/Test Split

각 scenario label마다 같은 비율로 train/test를 나눕니다.

현재 검증 결과:

| Item | Count |
|---|---:|
| Total rows | 720 |
| Scenario labels | 9 |
| Rows per label | 80 |
| Train rows per label | 64 |
| Test rows per label | 16 |
| Total train rows | 576 |
| Total test rows | 144 |
| ML feature columns | 70 |

## Why This Matters

이 단계가 없으면 모델이 실제 전기적 feature가 아니라 ID, 설명 문장, rule 결과 같은 쉬운 힌트를 보고 정답을 맞힐 수 있습니다. 이런 문제를 label leakage라고 합니다.

따라서 오늘 작업의 핵심은 "AI가 진짜 feature를 보고 학습하도록 데이터셋을 정리했다"는 점입니다.

## Command

```bash
python scripts/prepare_ml_dataset.py \
  --input data/processed/synthetic_features.csv \
  --output data/processed/ml_dataset.csv \
  --feature-columns-output data/processed/ml_feature_columns.txt \
  --report-output docs/SYNTHETIC_ML_DATASET_VALIDATION.md \
  --test-size 0.2
```
