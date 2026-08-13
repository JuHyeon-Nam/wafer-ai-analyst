# RandomForest Baseline Training Report

## Summary

- Train rows: `576`
- Test rows: `144`
- Feature columns: `70`
- Train accuracy: `0.9097`
- Test accuracy: `0.8819`
- Test macro F1-score: `0.8736`

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
| nmos_compliance_limit | 0 | 0 | 0 | 0 | 13 | 3 | 0 | 0 | 0 |
| nmos_gate_leakage | 0 | 0 | 0 | 0 | 4 | 12 | 0 | 0 | 0 |
| normal | 0 | 2 | 0 | 2 | 5 | 1 | 6 | 0 | 0 |
| resistance_shift | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 0 |
| resistor_nonlinearity | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |

## Top Feature Importance

| feature | importance |
| --- | --- |
| invalid_c_points | 0.0825855477883794 |
| ifit_mae_a_missing | 0.0549986086611583 |
| c_abs_max_raw_f | 0.05191315924901507 |
| compliance_hits | 0.04830302515409428 |
| ifit_max_abs_error_a_missing | 0.0410418588203036 |
| i_at_0_7v_a | 0.04013115370708943 |
| gate_leak_abs_max_a | 0.03847063026390242 |
| i_at_3v_a | 0.027400575380117507 |
| iv_linearity_r2 | 0.027148067515135665 |
| i_at_minus_3v_a | 0.027145312719608575 |
| g_or_r_median_missing | 0.023230126228527857 |
| conductance_s | 0.022369535978871497 |
| gate_leak_abs_max_a_missing | 0.021593385233463613 |
| resistance_ohm | 0.020159129316082363 |
| device_diode | 0.019369682385833906 |
| conductance_s_missing | 0.019015168578482622 |
| iv_linearity_r2_missing | 0.018358731947281787 |
| gate_v_max_v_missing | 0.017935803743968658 |
| device_NMOS | 0.01695465491710097 |
| c_range_f_missing | 0.016631187753801645 |

## Per-Class Test Metrics

| Label | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| `capacitance_outlier` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `capacitance_variation` | 0.8889 | 1.0000 | 0.9412 | 16 |
| `diode_contact_issue` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `diode_leakage` | 0.8889 | 1.0000 | 0.9412 | 16 |
| `nmos_compliance_limit` | 0.5909 | 0.8125 | 0.6842 | 16 |
| `nmos_gate_leakage` | 0.7500 | 0.7500 | 0.7500 | 16 |
| `normal` | 1.0000 | 0.3750 | 0.5455 | 16 |
| `resistance_shift` | 1.0000 | 1.0000 | 1.0000 | 16 |
| `resistor_nonlinearity` | 1.0000 | 1.0000 | 1.0000 | 16 |

## Interpretation

This model is a baseline classifier trained on synthetic defect scenario features.
The goal is not to claim production-level defect prediction, but to verify that the feature table can support a supervised ML workflow.
The next step is hyperparameter tuning and robustness checks against overfitting.
