# Feature Importance Analysis

## Summary

RandomForest tuned model이 defect scenario를 분류할 때 어떤 feature를 많이 봤는지 정리했습니다.
이 결과는 실제 공정 원인을 확정하는 근거가 아니라, 어떤 전기 측정 항목을 먼저 리뷰할지 정하는 우선순위 근거입니다.

## Importance by Feature Group

| feature_group | importance | importance_share |
| --- | --- | --- |
| missing_indicator | 0.3821 | 38.2% |
| capacitance | 0.1699 | 17.0% |
| resistor_iv | 0.1557 | 15.6% |
| nmos_idvg | 0.1554 | 15.5% |
| diode_iv | 0.0959 | 9.6% |
| device_indicator | 0.0410 | 4.1% |

## Top Features

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
| conductance_s | resistor_iv | 0.0193 | 저항의 반대 개념인 conductance입니다. 전류가 얼마나 쉽게 흐르는지 나타냅니다. |
| i_at_minus_3v_a_missing | missing_indicator | 0.0184 | 모델이 defect label을 나눌 때 사용한 electrical/statistical feature입니다. |
| resistance_ohm | resistor_iv | 0.0180 | Resistor I-V curve slope로 계산한 저항값입니다. |
| c_range_f | capacitance | 0.0178 | Capacitor C-V sweep 동안 capacitance가 얼마나 변했는지 보는 값입니다. |
| drain_i_at_gate_0v_a_missing | missing_indicator | 0.0174 | 모델이 defect label을 나눌 때 사용한 electrical/statistical feature입니다. |
| c_abs_max_raw_f_missing | missing_indicator | 0.0173 | 모델이 defect label을 나눌 때 사용한 electrical/statistical feature입니다. |
| c_at_0v_f | capacitance | 0.0172 | Capacitor 0V 지점 capacitance입니다. 박막 두께나 유전 특성 변화 후보를 볼 때 사용됩니다. |
| c_max_f | capacitance | 0.0170 | Capacitor sweep에서 가장 큰 유효 capacitance 값입니다. |

## Engineering Interpretation

- `invalid_c_points`, `c_abs_max_raw_f`가 높게 나오면 capacitor C-V 측정에서 range/probe/data artifact 후보를 먼저 확인합니다.
- `gate_leak_abs_max_a`가 높게 나오면 NMOS gate leakage 또는 gate oxide 관련 후보를 먼저 확인합니다.
- `compliance_hits`가 높게 나오면 장비 compliance limit, contact resistance, high-current saturation 후보를 확인합니다.
- `_missing` feature가 높게 나오면 물리 현상 자체보다 device별 column 구조 차이를 모델이 사용했을 수 있으므로 해석에 주의합니다.

## Interview Story

단순히 정확도만 확인하지 않고, feature importance를 통해 모델이 어떤 전기적 지표를 근거로 판단했는지 검토했습니다.
특히 missing indicator가 상위에 등장하는 경우 label leakage는 아니지만 device schema 구분 신호가 될 수 있어, 해석 가능한 feature와 schema feature를 분리해서 보았습니다.
