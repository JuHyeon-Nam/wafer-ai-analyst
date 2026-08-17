# RandomForest Training Report

## Summary

- Train rows: `576`
- Test rows: `144`
- Feature columns: `70`
- Train accuracy: `0.9774`
- Test accuracy: `0.9583`
- Test macro F1-score: `0.9560`

## Model Parameters

| Parameter | Value |
|---|---:|
| `n_estimators` | `100` |
| `max_depth` | `8` |
| `min_samples_leaf` | `3` |
| `class_weight` | `balanced` |
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
| normal | 0 | 0 | 0 | 0 | 0 | 5 | 10 | 0 | 1 |
| resistance_shift | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 0 |
| resistor_nonlinearity | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |

## Top Feature Importance

| feature | importance |
| --- | --- |
| drain_i_span_a | 0.07328345043788889 |
| invalid_c_points | 0.05482680379513095 |
| i_at_0v_a | 0.043985465509799024 |
| ifit_mae_a_missing | 0.04284822969253363 |
| ifit_max_abs_error_a_missing | 0.042323057986973965 |
| c_abs_max_raw_f | 0.04088697212828602 |
| gate_leak_abs_max_a | 0.031707067491897556 |
| compliance_hits | 0.030723161773075006 |
| i_at_0_7v_a | 0.027607676692401936 |
| i_at_3v_a | 0.025348482758235397 |
| i_at_minus_3v_a | 0.02370461713461467 |
| i_at_minus_3v_a_missing | 0.02127038046769877 |
| iv_linearity_r2 | 0.021068899123634775 |
| conductance_s | 0.020954890789417605 |
| resistance_ohm | 0.01938380504974151 |
| drain_i_at_gate_0v_a_missing | 0.017882365410197734 |
| fit_points_missing | 0.01690667799725349 |
| device_diode | 0.016844716956653256 |
| gate_v_max_v_missing | 0.016136298231748454 |
| gate_v_min_v_missing | 0.014916593703086357 |

## Per-Class Test Metrics

| Label | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| `capacitance_outlier` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `capacitance_variation` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `diode_contact_issue` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `diode_leakage` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `nmos_compliance_limit` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `nmos_gate_leakage` | 0.7619 | 1.0000 | 0.8649 | 16 |
| `normal` | 1.0000 | 0.6250 | 0.7692 | 16 |
| `resistance_shift` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `resistor_nonlinearity` | 0.9412 | 1.0000 | 0.9697 | 16 |

## Interpretation

This model is a classifier trained on synthetic defect scenario features.
The goal is not to claim production-level defect prediction, but to verify that the feature table can support a supervised ML workflow.
The confusion matrix and per-class metrics should be reviewed before using the model result as an engineering decision aid.
