# Synthetic ML Dataset Validation Report

## Summary

- Rows: `720`
- Scenario labels: `9`
- ML feature columns: `70`
- Train rows: `576`
- Test rows: `144`

## Class Balance

| Scenario Label | Rows | Train | Test |
|---|---:|---:|---:|
| `capacitance_outlier` | 80 | 64 | 16 |
| `capacitance_variation` | 80 | 64 | 16 |
| `diode_contact_issue` | 80 | 64 | 16 |
| `diode_leakage` | 80 | 64 | 16 |
| `nmos_compliance_limit` | 80 | 64 | 16 |
| `nmos_gate_leakage` | 80 | 64 | 16 |
| `normal` | 80 | 64 | 16 |
| `resistance_shift` | 80 | 64 | 16 |
| `resistor_nonlinearity` | 80 | 64 | 16 |

## Feature Columns

The model-ready dataset contains numeric electrical features, missing-value indicators, and one-hot device columns.

```text
c_at_0v_f
c_max_f
c_min_f
c_range_f
c_abs_max_raw_f
g_or_r_median
invalid_c_points
drain_v_mean_v
gate_v_min_v
gate_v_max_v
drain_i_mean_a
drain_i_span_a
drain_i_at_gate_0v_a
gate_leak_abs_max_a
i_at_0v_a
i_at_0_7v_a
i_at_1v_a
i_at_2v_a
i_max_a
i_min_a
v_at_10na_v
v_at_100na_v
v_at_1ua_v
resistance_ohm
conductance_s
fit_intercept_a
iv_linearity_r2
fit_points
i_at_3v_a
i_at_minus_3v_a
compliance_hits
ifit_mae_a
ifit_max_abs_error_a
c_at_0v_f_missing
c_max_f_missing
c_min_f_missing
c_range_f_missing
c_abs_max_raw_f_missing
g_or_r_median_missing
invalid_c_points_missing
drain_v_mean_v_missing
gate_v_min_v_missing
gate_v_max_v_missing
drain_i_mean_a_missing
drain_i_span_a_missing
drain_i_at_gate_0v_a_missing
gate_leak_abs_max_a_missing
i_at_0v_a_missing
i_at_0_7v_a_missing
i_at_1v_a_missing
i_at_2v_a_missing
i_max_a_missing
i_min_a_missing
v_at_10na_v_missing
v_at_100na_v_missing
v_at_1ua_v_missing
resistance_ohm_missing
conductance_s_missing
fit_intercept_a_missing
iv_linearity_r2_missing
fit_points_missing
i_at_3v_a_missing
i_at_minus_3v_a_missing
compliance_hits_missing
ifit_mae_a_missing
ifit_max_abs_error_a_missing
device_Cap
device_NMOS
device_diode
device_resistor
```

## Notes

- `scenario_label` is the supervised learning target.
- Metadata, generated explanations, anomaly flags, and process reasoning text are excluded from model features.
- Missing values are imputed with each feature median, and missing indicators are added.
- The split is stratified by scenario label to keep train/test label balance stable.
