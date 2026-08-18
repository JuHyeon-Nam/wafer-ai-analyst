# Wafer Electrical Test Analysis Report

- Generated at: `2026-08-18 13:43:42`
- Measurements: `74`
- Devices: `Cap, NMOS, diode, resistor`
- Shots: `1-1, 1-4, 5-1, 5-4, 9-1, 9-4`

## Executive Summary

총 74개 measurement를 분석했습니다. Rule 기준 priority 후보는 23개, review 후보는 10개입니다. ML 모델은 21개 measurement를 normal이 아닌 defect scenario 후보로 분류했고, 그중 confidence가 낮아 추가 확인이 필요한 항목은 34개입니다.

## Review Count

| item | count |
| --- | --- |
| normal | 41 |
| priority | 23 |
| review | 10 |

## ML Prediction Count

| item | count |
| --- | --- |
| normal | 53 |
| nmos_gate_leakage | 15 |
| capacitance_variation | 3 |
| diode_leakage | 1 |
| resistor_nonlinearity | 1 |
| resistance_shift | 1 |

## Device and Shot Coverage

| device | shot | count |
| --- | --- | --- |
| Cap | 1-1 | 3 |
| Cap | 1-4 | 3 |
| Cap | 5-1 | 3 |
| Cap | 5-4 | 3 |
| Cap | 9-1 | 3 |
| Cap | 9-4 | 3 |
| NMOS | 1-1 | 3 |
| NMOS | 1-4 | 3 |
| NMOS | 5-1 | 3 |
| NMOS | 5-4 | 3 |
| NMOS | 9-1 | 3 |
| NMOS | 9-4 | 3 |
| diode | 1-4 | 3 |
| diode | 5-1 | 3 |
| diode | 5-4 | 3 |
| diode | 9-1 | 3 |
| diode | 9-4 | 3 |
| diode |  | 5 |
| resistor | 1-1 | 3 |
| resistor | 1-4 | 3 |
| resistor | 5-1 | 3 |
| resistor | 5-4 | 3 |
| resistor | 9-1 | 3 |
| resistor | 9-4 | 3 |

## High Priority Review Candidates

| measurement_id | device | shot | review_status | anomaly_flags | ml_predicted_label | ml_confidence | process_issue_candidates |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cap:1-4:cap1-4 | Cap | 1-4 | priority | measurement_error_suspect, raw_capacitance_outlier, capacitance_variation | normal | 0.385 | probe contact issue, measurement range error, data artifact, open/unstable probe contact, instrument parsing artifact, oxide thickness variation, deposition non-uniformity, etch variation |
| NMOS:1-4:nmos1-4 | NMOS | 1-4 | priority | compliance_limit_suspect, gate_leakage_suspect, nmos_current_span_suspect | nmos_gate_leakage | 0.519 | measurement condition issue, short suspect, device over-current path, gate oxide weakness, surface leakage, probe contact instability, threshold voltage shift, channel process variation, local short/leakage path |
| NMOS:1-1:nmos1-1 | NMOS | 1-1 | priority | compliance_limit_suspect, gate_leakage_suspect | nmos_gate_leakage | 0.608 | measurement condition issue, short suspect, device over-current path, gate oxide weakness, surface leakage, probe contact instability |
| NMOS:5-1:nmos 5-1 | NMOS | 5-1 | priority | compliance_limit_suspect, gate_leakage_suspect | nmos_gate_leakage | 0.576 | measurement condition issue, short suspect, device over-current path, gate oxide weakness, surface leakage, probe contact instability |
| resistor:9-1:R 9-1 | resistor | 9-1 | priority | current_saturation_suspect, resistor_linearity_drop, resistance_shift | resistor_nonlinearity | 0.448 | contact resistance change, series resistance effect, instrument compliance, contact resistance variation, self-heating effect, thin film thickness variation, line width variation |
| resistor:5-4:R5-4 | resistor | 5-4 | priority | current_saturation_suspect, resistor_linearity_drop, resistance_shift | resistance_shift | 0.405 | contact resistance change, series resistance effect, instrument compliance, contact resistance variation, self-heating effect, thin film thickness variation, line width variation |
| NMOS:5-4:nmos 5-4 | NMOS | 5-4 | priority | compliance_limit_suspect, gate_leakage_suspect | normal | 0.345 | measurement condition issue, short suspect, device over-current path, gate oxide weakness, surface leakage, probe contact instability |
| NMOS:9-4:nmos9-4 | NMOS | 9-4 | priority | compliance_limit_suspect | nmos_gate_leakage | 0.460 | measurement condition issue, short suspect, device over-current path |
| NMOS:9-1:nmos9-1 | NMOS | 9-1 | priority | compliance_limit_suspect | nmos_gate_leakage | 0.432 | measurement condition issue, short suspect, device over-current path |
| diode:5-1:Custom 5-1 | diode | 5-1 | review | leakage_current_suspect | normal | 0.694 | junction leakage path, surface contamination, oxide/interface defect |
| diode:9-4:Custom 9-4 | diode | 9-4 | review | leakage_current_suspect | normal | 0.644 | junction leakage path, surface contamination, oxide/interface defect |
| diode:9-1:Custom 9-1 | diode | 9-1 | review | diode_current_variation | normal | 0.465 | junction variation, series resistance shift, probe contact variation, pattern CD variation |
| diode:unknown-shot:Custom Test_1#1 | diode |  | review | diode_current_variation | diode_leakage | 0.440 | junction variation, series resistance shift, probe contact variation, pattern CD variation |
| Cap:5-1:cap5-1 | Cap | 5-1 | normal | normal_or_review | capacitance_variation | 0.518 | baseline review |

## Feature Importance Summary

### By Feature Group

| feature_group | importance | importance_share |
| --- | --- | --- |
| missing_indicator | 0.3821 | 38.2% |
| capacitance | 0.1699 | 17.0% |
| resistor_iv | 0.1557 | 15.6% |
| nmos_idvg | 0.1554 | 15.5% |
| diode_iv | 0.0959 | 9.6% |
| device_indicator | 0.0410 | 4.1% |

### Top Features

| feature | feature_group | importance | plain_explanation |
| --- | --- | --- | --- |
| drain_i_span_a | nmos_idvg | 0.0784 | NMOS Id-Vg curve에서 drain current가 얼마나 변했는지 보는 값입니다. channel 동작 변화나 compliance 후보와 연결됩니다. |
| invalid_c_points | capacitance | 0.0503 | Capacitor C-V 측정에서 물리적으로 이상한 capacitance point가 얼마나 나왔는지 보는 값입니다. |
| i_at_0v_a | diode_iv | 0.0462 | Diode 0V 근처 전류입니다. 역방향/저전압 leakage 후보를 볼 때 사용됩니다. |
| c_abs_max_raw_f | capacitance | 0.0442 | Capacitor raw C 값의 절대 최대값입니다. range 오류, probe contact, 저장 artifact 후보와 연결됩니다. |
| ifit_max_abs_error_a_missing | missing_indicator | 0.0431 | Diode fitting 최대 오차 column의 결측 여부입니다. 실제 물리량이라기보다 소자/측정 schema 구분 신호에 가깝습니다. |
| ifit_mae_a_missing | missing_indicator | 0.0406 | Diode fitting error column의 결측 여부입니다. 특정 소자에서만 생기는 column 구조 차이를 모델이 구분에 사용한 신호입니다. |
| compliance_hits | resistor_iv | 0.0332 | 전류가 장비 제한값 근처에 걸린 point 수입니다. compliance limit 또는 contact 영향 후보와 연결됩니다. |
| gate_leak_abs_max_a | nmos_idvg | 0.0326 | NMOS gate에 새는 전류의 최대값입니다. gate oxide 또는 surface leakage 후보를 볼 때 중요합니다. |
| i_at_0_7v_a | diode_iv | 0.0263 | Diode forward 동작을 보는 대표 전류 지점입니다. |
| i_at_3v_a | resistor_iv | 0.0254 | Resistor 또는 diode curve에서 3V 지점 전류입니다. 저항 변화나 slope 변화를 볼 때 사용됩니다. |
| iv_linearity_r2 | resistor_iv | 0.0244 | Resistor I-V curve가 얼마나 직선에 가까운지 보는 값입니다. 낮으면 contact, self-heating, compliance 후보를 확인합니다. |
| i_at_minus_3v_a | resistor_iv | 0.0225 | 음전압 -3V 지점 전류입니다. resistor slope 대칭성과 leakage 성향을 볼 때 사용됩니다. |

## Model Metrics

| metric | value |
| --- | --- |
| train_accuracy | 0.9896 |
| test_accuracy | 0.9722 |
| test_macro_f1 | 0.9718 |
| train_rows | 576 |
| test_rows | 144 |
| feature_count | 70 |
| parameter.n_estimators | 100 |
| parameter.max_depth | None |
| parameter.min_samples_leaf | 3 |
| parameter.class_weight | None |
| parameter.random_state | 42 |

## Engineering Notes

- Rule-based result는 사람이 정의한 전기적 기준입니다.
- ML prediction은 synthetic defect scenario dataset으로 학습한 RandomForest 모델의 후보 판단입니다.
- Root cause를 확정하려면 공정 recipe, 박막 두께, 온도/압력/시간 조건, 장비 log, 반복 측정 데이터가 추가로 필요합니다.
- 이 리포트는 이상 후보를 빠르게 좁히는 review workflow 산출물로 사용합니다.
