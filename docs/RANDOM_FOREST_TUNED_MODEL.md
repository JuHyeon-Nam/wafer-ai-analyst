# RandomForest Training Report

## Summary

- Train rows: `576`
- Test rows: `144`
- Feature columns: `70`
- Train accuracy: `0.9896`
- Test accuracy: `0.9722`
- Test macro F1-score: `0.9718`

## Model Parameters

| Parameter | Value |
|---|---:|
| `n_estimators` | `100` |
| `max_depth` | `None` |
| `min_samples_leaf` | `3` |
| `class_weight` | `None` |
| `random_state` | `42` |

## Confusion Matrix

| label | capacitance_outlier | capacitance_variation | diode_contact_issue | diode_leakage | nmos_compliance_limit | nmos_gate_leakage | normal | resistance_shift | resistor_nonlinearity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capacitance_outlier | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| capacitance_variation | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| diode_contact_issue | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| diode_leakage | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 |
| nmos_compliance_limit | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 |
| nmos_gate_leakage | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 |
| normal | 0 | 0 | 0 | 0 | 0 | 4 | 12 | 0 | 0 |
| resistance_shift | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 0 |
| resistor_nonlinearity | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |

## Top Feature Importance

| feature | importance |
| --- | --- |
| drain_i_span_a | 0.07842490577332496 |
| invalid_c_points | 0.050328716690130136 |
| i_at_0v_a | 0.04624634634162186 |
| c_abs_max_raw_f | 0.044199747921172754 |
| ifit_max_abs_error_a_missing | 0.04308235304100844 |
| ifit_mae_a_missing | 0.04058405108967647 |
| compliance_hits | 0.03322851847068584 |
| gate_leak_abs_max_a | 0.03262895983311282 |
| i_at_0_7v_a | 0.02633089310630291 |
| i_at_3v_a | 0.02538324548027181 |
| iv_linearity_r2 | 0.02439840794904577 |
| i_at_minus_3v_a | 0.02246793210749682 |
| conductance_s | 0.019265012083454377 |
| i_at_minus_3v_a_missing | 0.01837568998340694 |
| resistance_ohm | 0.018008208443472774 |
| c_range_f | 0.01775122580897735 |
| drain_i_at_gate_0v_a_missing | 0.017354440567880196 |
| c_abs_max_raw_f_missing | 0.017325352760533232 |
| c_at_0v_f | 0.017202180584049025 |
| c_max_f | 0.01702807073447896 |

## Per-Class Test Metrics

| Label | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| `capacitance_outlier` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `capacitance_variation` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `diode_contact_issue` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `diode_leakage` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `nmos_compliance_limit` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `nmos_gate_leakage` | 0.8000 | 1.0000 | 0.8889 | 16 |
| `normal` | 1.0000 | 0.7500 | 0.8571 | 16 |
| `resistance_shift` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `resistor_nonlinearity` | 1.0000 | 1.0000 | 1.0000 | 16 |

## Interpretation

This model is a classifier trained on synthetic defect scenario features.
The goal is not to claim production-level defect prediction, but to verify that the feature table can support a supervised ML workflow.
The confusion matrix and per-class metrics should be reviewed before using the model result as an engineering decision aid.
