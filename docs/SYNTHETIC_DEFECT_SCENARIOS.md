# Synthetic Defect Scenario Design

## Purpose

실제 wafer 측정 데이터는 sample 수와 defect label이 부족합니다. 따라서 현재 프로젝트에서는 실제 raw data를 그대로 복제하지 않고, 실제 feature 분포와 전기적 의미를 참고해 synthetic defect scenario dataset을 생성합니다.

이 synthetic dataset은 실제 공정 불량 데이터가 아니라, ML baseline 학습과 평가 workflow를 검증하기 위한 labeled training dataset입니다.

## Input and Output

Input:

```text
real feature table
```

Output:

```text
synthetic feature table
scenario label table
```

Synthetic feature table에는 다음 컬럼이 추가됩니다.

| Column | Meaning |
|---|---|
| `data_source` | `synthetic` |
| `seed_measurement_id` | 어떤 실제 measurement row를 기준으로 만들었는지 |
| `synthetic_id` | synthetic row id |
| `scenario_label` | 학습 target label |
| `scenario_description` | scenario 설명 |
| `modified_features` | 해당 scenario에서 주로 변형한 feature |
| `expected_anomaly_flags` | 해당 scenario에서 기대되는 anomaly pattern |

## Scenario Labels

| Scenario Label | Target Device | Main Feature Change | Expected Flag |
|---|---|---|---|
| `normal` | all | 작은 noise만 추가 | `normal_or_review` |
| `diode_leakage` | diode | `i_at_0v_a`, `i_at_0_7v_a` 증가 | `leakage_current_suspect` |
| `diode_contact_issue` | diode | `ifit_mae_a`, `ifit_max_abs_error_a` 증가 | `curve_fit_mismatch` |
| `resistance_shift` | resistor | `resistance_ohm`, `conductance_s` 변화 | `resistance_shift` |
| `resistor_nonlinearity` | resistor | `iv_linearity_r2` 감소, `compliance_hits` 증가 | `resistor_linearity_drop`, `current_saturation_suspect` |
| `capacitance_variation` | Cap | `c_at_0v_f`, `c_max_f`, `c_min_f` shift | `capacitance_variation` |
| `capacitance_outlier` | Cap | `c_abs_max_raw_f` spike, `invalid_c_points` 증가 | `measurement_error_suspect`, `raw_capacitance_outlier` |
| `nmos_gate_leakage` | NMOS | `gate_leak_abs_max_a` 증가 | `gate_leakage_suspect` |
| `nmos_compliance_limit` | NMOS | `drain_i_mean_a`를 compliance 근처로 이동 | `compliance_limit_suspect` |

## Generation Method

1. 실제 feature row를 seed로 선택합니다.
2. 모든 숫자 feature에 작은 random jitter를 적용합니다.
3. scenario별 핵심 feature를 전기적 의미에 맞게 변형합니다.
4. `scenario_label`을 붙여 ML training target으로 사용합니다.
5. 원본 row id를 `seed_measurement_id`로 남겨 추적 가능하게 합니다.

## Why Feature-Level Generation

Raw IV/CV curve를 직접 생성하는 방식도 가능하지만, 현재 프로젝트의 ML baseline은 feature table 기반 classification입니다. 따라서 먼저 feature-level synthetic dataset을 만들면 다음 단계인 RandomForest 학습, parameter tuning, confusion matrix, feature importance 분석으로 바로 연결할 수 있습니다.

## Troubleshooting Notes

- 단순 row duplication은 학습 의미가 없기 때문에 사용하지 않습니다.
- synthetic data와 real data는 `data_source`로 구분합니다.
- 실제 공정 불량이라고 표현하지 않고, defect scenario simulation이라고 표현합니다.
- 모델 성능은 실제 양산 성능이 아니라, feature-based defect classification 가능성 검증으로 해석합니다.

## Command

```bash
python scripts/generate_synthetic_dataset.py \
  --input data/processed/features.csv \
  --output data/processed/synthetic_features.csv \
  --scenario-output data/processed/synthetic_scenarios.csv \
  --samples-per-scenario 80
```
