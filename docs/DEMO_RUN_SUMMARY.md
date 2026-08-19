# Demo Run Summary

## Dataset Snapshot

- Measurements: `74`
- Curve points: `10294`
- Devices: `Cap, NMOS, diode, resistor`
- Shots: `1-1, 1-4, 5-1, 5-4, 9-1, 9-4`

## Model Snapshot

- Test accuracy: `0.9722`
- Test macro F1-score: `0.9718`
- Feature columns: `70`

## Rule Review Count

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

## Candidate Preview

| measurement_id | device | shot | review_status | ml_predicted_label | ml_confidence | anomaly_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Cap:1-4:cap1-4 | Cap | 1-4 | priority | normal | 0.385 | measurement_error_suspect, raw_capacitance_outlier, capacitance_variation |
| NMOS:1-4:nmos1-4 | NMOS | 1-4 | priority | nmos_gate_leakage | 0.519 | compliance_limit_suspect, gate_leakage_suspect, nmos_current_span_suspect |
| NMOS:1-1:nmos1-1 | NMOS | 1-1 | priority | nmos_gate_leakage | 0.608 | compliance_limit_suspect, gate_leakage_suspect |
| NMOS:5-1:nmos 5-1 | NMOS | 5-1 | priority | nmos_gate_leakage | 0.576 | compliance_limit_suspect, gate_leakage_suspect |
| resistor:9-1:R 9-1 | resistor | 9-1 | priority | resistor_nonlinearity | 0.448 | current_saturation_suspect, resistor_linearity_drop, resistance_shift |
| resistor:5-4:R5-4 | resistor | 5-4 | priority | resistance_shift | 0.405 | current_saturation_suspect, resistor_linearity_drop, resistance_shift |
| NMOS:5-4:nmos 5-4 | NMOS | 5-4 | priority | normal | 0.345 | compliance_limit_suspect, gate_leakage_suspect |
| NMOS:9-4:nmos9-4 | NMOS | 9-4 | priority | nmos_gate_leakage | 0.460 | compliance_limit_suspect |

## Demo Talking Points

1. Raw wafer electrical test files were normalized into measurement, curve, feature, and explanation tables.
2. Rule-based anomaly logic was used first because the real dataset has limited confirmed defect labels.
3. Synthetic defect scenarios were generated from real feature distributions to create a supervised ML workflow.
4. RandomForest was trained and tuned, then connected back to the real feature table for predicted label and confidence.
5. Feature importance and curve detail views keep the result explainable instead of treating the model as a black box.
6. The final report generator exports the analysis as Markdown/HTML for sharing outside the dashboard.

## Report Check

- Markdown report length: `7194` characters
- Contains executive summary: `True`
