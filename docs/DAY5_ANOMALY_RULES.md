# Day 5 Anomaly Rule Expansion

## Goal

Day 5의 목표는 feature table에서 확인 가능한 전기적 이상 징후를 rule-based 방식으로 더 구체적으로 분류하는 것입니다.

## Implemented Rules

| Rule | Signal | Review Meaning |
|---|---|---|
| `measurement_error_suspect` | invalid capacitance point 존재 | 측정 오류 또는 probe contact 불안정 가능성 |
| `raw_capacitance_outlier` | raw capacitance가 물리적으로 큰 값으로 튐 | CV 측정 range 오류 또는 parsing artifact 가능성 |
| `compliance_limit_suspect` | NMOS drain current가 장비 제한에 가까움 | 장비 compliance 또는 short path 가능성 |
| `current_saturation_suspect` | resistor current가 high-current 구간에서 포화 | contact resistance 또는 compliance 영향 가능성 |
| `curve_fit_mismatch` | diode 측정 curve와 IFIT 차이가 큼 | 비이상적인 diode 동작 또는 contact 불안정 가능성 |
| `leakage_current_suspect` | diode low-bias current가 상대적으로 큼 | junction leakage 또는 surface contamination 가능성 |
| `gate_leakage_suspect` | NMOS gate leakage가 큼 | gate oxide 또는 probe contact 이슈 가능성 |
| `resistor_linearity_drop` | resistor I-V linearity가 낮음 | 저항 소자의 선형성 저하 또는 self-heating 가능성 |
| `diode_current_variation` | 같은 diode의 shot별 current 차이가 큼 | junction/contact/CD variation 가능성 |
| `capacitance_variation` | 같은 capacitor의 shot별 capacitance 차이가 큼 | oxide/deposition/etch variation 가능성 |
| `resistance_shift` | 같은 resistor의 shot별 resistance 차이가 큼 | film thickness, line width, contact resistance 변화 가능성 |
| `nmos_current_span_suspect` | NMOS current span이 다른 shot보다 큼 | Vth shift, channel variation, local leakage 가능성 |

## Scoring

각 flag는 severity에 따라 `anomaly_score`에 반영됩니다.

| Status | Score | Meaning |
|---|---:|---|
| `normal` | 0 | 우선순위 높은 이상 flag 없음 |
| `review` | 1-2 | 확인이 필요한 이상 후보 |
| `priority` | 3 이상 | 먼저 확인해야 할 이상 후보 |

## Why It Matters

반도체 측정 데이터에서 이상값은 공정 불량일 수도 있고, 측정 조건 문제일 수도 있습니다. Day 5에서는 둘을 바로 단정하지 않고, 전기적 패턴을 기준으로 review priority를 나누는 기준을 만들었습니다.
