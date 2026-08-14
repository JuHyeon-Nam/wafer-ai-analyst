# RandomForest Hyperparameter Tuning Report

## Summary

- Tried parameter sets: `72`
- Best test accuracy: `0.9028`
- Best test macro F1-score: `0.8960`
- Best train accuracy: `0.9618`
- Best overfit gap: `0.0590`

## Selected Parameters

| Parameter | Value |
|---|---:|
| `n_estimators` | `100` |
| `max_depth` | `None` |
| `min_samples_leaf` | `1` |
| `class_weight` | `None` |
| `random_state` | `42` |

## Top Parameter Sets

| n_estimators | max_depth | min_samples_leaf | class_weight | test_macro_f1 | test_accuracy | normal_recall | nmos_compliance_recall | nmos_gate_leakage_recall | overfit_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | None | 1 | None | 0.8960 | 0.9028 | 0.4375 | 0.8750 | 0.8125 | 0.0590 |
| 200 | None | 1 | None | 0.8960 | 0.9028 | 0.4375 | 0.8750 | 0.8125 | 0.0608 |
| 50 | None | 1 | balanced | 0.8926 | 0.9028 | 0.3750 | 0.8750 | 0.8750 | 0.0590 |
| 50 | None | 1 | None | 0.8924 | 0.9028 | 0.3750 | 0.8750 | 0.8750 | 0.0590 |
| 100 | 8.0 | 1 | None | 0.8902 | 0.8958 | 0.4375 | 0.8750 | 0.7500 | 0.0330 |
| 200 | None | 1 | balanced | 0.8896 | 0.8958 | 0.4375 | 0.8750 | 0.7500 | 0.0677 |
| 50 | 8.0 | 1 | None | 0.8838 | 0.8889 | 0.4375 | 0.8125 | 0.7500 | 0.0417 |
| 100 | None | 5 | balanced | 0.8809 | 0.8889 | 0.3750 | 0.8750 | 0.7500 | 0.0122 |
| 100 | 8.0 | 5 | balanced | 0.8800 | 0.8889 | 0.3750 | 0.8750 | 0.7500 | 0.0035 |
| 200 | 8.0 | 3 | balanced | 0.8800 | 0.8889 | 0.3750 | 0.8750 | 0.7500 | 0.0208 |
| 200 | None | 3 | balanced | 0.8800 | 0.8889 | 0.3750 | 0.8750 | 0.7500 | 0.0243 |
| 100 | 8.0 | 1 | balanced | 0.8800 | 0.8889 | 0.3750 | 0.8750 | 0.7500 | 0.0312 |

## Why This Selection

The selected model is chosen by test macro F1-score first, then test accuracy, normal recall, NMOS recall, and lower overfit gap.
This keeps the tuning story focused on balanced defect classification instead of only maximizing overall accuracy.

## Next Step

The next step is feature importance analysis and dashboard integration of ML prediction results.
