# Day 6 Process Issue Reasoning

## Goal

Day 6의 목표는 anomaly flag를 가능한 공정/측정 이슈 후보와 연결하는 것입니다.

## Reasoning Structure

```text
Electrical feature
-> anomaly flag
-> candidate process or measurement issue
-> next engineering review direction
```

## Candidate Mapping

| Anomaly Flag | Candidate Issues |
|---|---|
| `measurement_error_suspect` | probe contact issue, measurement range error, data artifact |
| `raw_capacitance_outlier` | measurement range error, open/unstable probe contact, instrument parsing artifact |
| `compliance_limit_suspect` | measurement condition issue, short suspect, device over-current path |
| `current_saturation_suspect` | contact resistance change, series resistance effect, instrument compliance |
| `curve_fit_mismatch` | junction characteristic variation, contact instability, non-ideal diode behavior |
| `leakage_current_suspect` | junction leakage path, surface contamination, oxide/interface defect |
| `gate_leakage_suspect` | gate oxide weakness, surface leakage, probe contact instability |
| `diode_current_variation` | junction variation, series resistance shift, probe contact variation, pattern CD variation |
| `capacitance_variation` | oxide thickness variation, deposition non-uniformity, etch variation |
| `resistance_shift` | thin film thickness variation, line width variation, contact resistance variation |
| `resistor_linearity_drop` | contact resistance variation, self-heating effect, instrument compliance |
| `nmos_current_span_suspect` | threshold voltage shift, channel process variation, local short/leakage path |

## Boundary

이 모듈은 root cause를 확정하지 않습니다. 전기 측정 데이터만으로 가능한 원인 후보를 좁히고, 추가 확인해야 할 공정/장비 항목을 제시합니다.

## Why It Matters

면접이나 리뷰에서 중요한 지점은 "AI가 원인을 맞혔다"가 아니라, 측정 데이터에서 어떤 증거를 보고 어떤 확인 방향을 제안했는지 설명하는 것입니다. Day 6은 이 연결 구조를 코드로 구현한 단계입니다.
