# RandomForest Training Report

## Summary

- Train rows: `576`
- Test rows: `144`
- Feature columns: `70`
- Train accuracy: `0.9618`
- Test accuracy: `0.9028`
- Test macro F1-score: `0.8960`

## Model Parameters

| Parameter | Value |
|---|---:|
| `n_estimators` | `100` |
| `max_depth` | `None` |
| `min_samples_leaf` | `1` |
| `class_weight` | `None` |
| `random_state` | `42` |

## Confusion Matrix

| label | capacitance_outlier | capacitance_variation | diode_contact_issue | diode_leakage | nmos_compliance_limit | nmos_gate_leakage | normal | resistance_shift | resistor_nonlinearity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capacitance_outlier | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| capacitance_variation | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| diode_contact_issue | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| diode_leakage | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 |
| nmos_compliance_limit | 0 | 0 | 0 | 0 | 14 | 2 | 0 | 0 | 0 |
| nmos_gate_leakage | 0 | 0 | 0 | 0 | 3 | 13 | 0 | 0 | 0 |
| normal | 0 | 2 | 0 | 1 | 4 | 2 | 7 | 0 | 0 |
| resistance_shift | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 0 |
| resistor_nonlinearity | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |

## Top Feature Importance

| feature | importance |
| --- | --- |
| invalid_c_points | 0.08424392927070357 |
| ifit_mae_a_missing | 0.0610703682802654 |
| gate_leak_abs_max_a | 0.04573037499794516 |
| ifit_max_abs_error_a_missing | 0.044263320126281015 |
| c_abs_max_raw_f | 0.04125170648600106 |
| compliance_hits | 0.04120664044585882 |
| i_at_3v_a | 0.03306500476854698 |
| i_at_0_7v_a | 0.027486773229845926 |
| device_diode | 0.026777488463673074 |
| resistance_ohm | 0.025784160485788393 |
| i_at_minus_3v_a | 0.024449164870179674 |
| iv_linearity_r2 | 0.0224024768289282 |
| conductance_s | 0.021359157190599092 |
| drain_i_mean_a | 0.021157667199999758 |
| gate_v_max_v_missing | 0.019421056832313398 |
| drain_v_mean_v | 0.01918014396529997 |
| drain_i_at_gate_0v_a | 0.018561361450904392 |
| gate_v_max_v | 0.01841399907148358 |
| fit_intercept_a_missing | 0.01772478210705822 |
| c_abs_max_raw_f_missing | 0.016423741192439605 |

## Per-Class Test Metrics

| Label | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| `capacitance_outlier` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `capacitance_variation` | 0.8889 | 1.0000 | 0.9412 | 16 |
| `diode_contact_issue` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `diode_leakage` | 0.9412 | 1.0000 | 0.9697 | 16 |
| `nmos_compliance_limit` | 0.6667 | 0.8750 | 0.7568 | 16 |
| `nmos_gate_leakage` | 0.7647 | 0.8125 | 0.7879 | 16 |
| `normal` | 1.0000 | 0.4375 | 0.6087 | 16 |
| `resistance_shift` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `resistor_nonlinearity` | 1.0000 | 1.0000 | 1.0000 | 16 |

## Interpretation

This model is a classifier trained on synthetic defect scenario features.
The goal is not to claim production-level defect prediction, but to verify that the feature table can support a supervised ML workflow.
The confusion matrix and per-class metrics should be reviewed before using the model result as an engineering decision aid.
