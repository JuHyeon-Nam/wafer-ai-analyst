# RandomForest Baseline Training

## Purpose

8월 13일 작업의 목표는 synthetic ML dataset을 이용해 실제 baseline classifier를 학습시키는 것입니다.

이 단계부터 프로젝트는 단순 rule-based 분석을 넘어, `scenario_label`을 target으로 하는 supervised ML workflow를 갖게 됩니다.

## Model

Baseline model은 `RandomForestClassifier`입니다.

선택 이유:

- 현재 데이터가 image가 아니라 feature table 형태입니다.
- RandomForest는 tabular data에서 baseline으로 자주 쓰입니다.
- 학습 속도가 빠르고 local 환경에서 실행하기 쉽습니다.
- feature importance를 통해 모델이 어떤 전기적 feature를 중요하게 봤는지 설명할 수 있습니다.
- deep learning보다 데이터가 적은 상황에서 더 현실적인 baseline입니다.

## Input

```text
data/processed/ml_dataset.csv
```

이 dataset에는 다음이 포함됩니다.

- `scenario_label`: 정답 label
- `split`: train/test 구분
- numeric electrical features
- missing indicator columns
- device one-hot columns

## Parameters

현재 baseline parameter:

| Parameter | Value | Meaning |
|---|---:|---|
| `n_estimators` | `100` | decision tree 개수 |
| `max_depth` | `8` | tree가 너무 깊게 외우지 않도록 제한 |
| `min_samples_leaf` | `3` | 너무 작은 예외만 보고 판단하지 않도록 제한 |
| `class_weight` | `balanced` | label별 중요도를 균형 있게 반영 |
| `random_state` | `42` | 재현 가능한 결과를 위한 seed |

## Output

```text
models/random_forest_baseline.joblib
docs/RANDOM_FOREST_BASELINE.md
data/processed/rf_predictions.csv
data/processed/rf_feature_importance.csv
data/processed/rf_metrics.json
```

Model artifact와 processed CSV/JSON은 local generated output으로 관리합니다. GitHub에는 재현 가능한 script와 Markdown report를 남깁니다.

## Baseline Result

현재 검증 결과:

| Metric | Value |
|---|---:|
| Train accuracy | 0.9774 |
| Test accuracy | 0.9583 |
| Test macro F1-score | 0.9560 |

## Interpretation

모델은 `capacitance_outlier`, `diode_contact_issue`, `resistance_shift`, `resistor_nonlinearity` 같은 명확한 synthetic scenario는 잘 구분했습니다.

반면 `normal` class는 일부 `nmos_gate_leakage`, `resistor_nonlinearity` 후보와 혼동이 있었습니다. 이는 정상 scenario가 모든 device에서 생성되고, 정상 variation과 약한 defect scenario가 일부 feature 영역을 공유하기 때문입니다.

이 결과는 실패가 아니라 다음 tuning 포인트입니다.

다음 단계에서는:

- `max_depth`
- `min_samples_leaf`
- `n_estimators`
- `class_weight`

를 조정하면서 normal recall과 NMOS class confusion을 개선합니다.

## Command

```bash
python scripts/train_random_forest.py \
  --input data/processed/ml_dataset.csv \
  --model-output models/random_forest_baseline.joblib \
  --report-output docs/RANDOM_FOREST_BASELINE.md \
  --predictions-output data/processed/rf_predictions.csv \
  --importance-output data/processed/rf_feature_importance.csv \
  --metrics-output data/processed/rf_metrics.json \
  --n-estimators 100 \
  --max-depth 8 \
  --min-samples-leaf 3 \
  --class-weight balanced
```
