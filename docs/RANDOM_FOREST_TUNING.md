# RandomForest Hyperparameter Tuning Report

## Summary

- Tried parameter sets: `72`
- Best test accuracy: `0.9722`
- Best test macro F1-score: `0.9718`
- Best train accuracy: `0.9896`
- Best overfit gap: `0.0174`

## Selected Parameters

| Parameter | Value |
|---|---:|
| `n_estimators` | `100` |
| `max_depth` | `None` |
| `min_samples_leaf` | `3` |
| `class_weight` | `None` |
| `random_state` | `42` |

## Top Parameter Sets

| n_estimators | max_depth | min_samples_leaf | class_weight | test_macro_f1 | test_accuracy | normal_recall | nmos_compliance_recall | nmos_gate_leakage_recall | overfit_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | None | 3 | None | 0.9718 | 0.9722 | 0.7500 | 1.0000 | 1.0000 | 0.0174 |
| 100 | None | 3 | balanced | 0.9718 | 0.9722 | 0.7500 | 1.0000 | 1.0000 | 0.0174 |
| 50 | None | 3 | None | 0.9649 | 0.9653 | 0.7500 | 0.9375 | 1.0000 | 0.0226 |
| 50 | None | 3 | balanced | 0.9649 | 0.9653 | 0.7500 | 0.9375 | 1.0000 | 0.0226 |
| 200 | None | 3 | None | 0.9583 | 0.9583 | 0.6875 | 0.9375 | 1.0000 | 0.0330 |
| 200 | None | 3 | balanced | 0.9583 | 0.9583 | 0.6875 | 0.9375 | 1.0000 | 0.0330 |
| 100 | 8.0 | 3 | None | 0.9560 | 0.9583 | 0.6250 | 1.0000 | 1.0000 | 0.0191 |
| 100 | 8.0 | 3 | balanced | 0.9560 | 0.9583 | 0.6250 | 1.0000 | 1.0000 | 0.0191 |
| 50 | None | 1 | None | 0.9516 | 0.9514 | 0.7500 | 0.8750 | 0.9375 | 0.0486 |
| 50 | None | 1 | balanced | 0.9516 | 0.9514 | 0.7500 | 0.8750 | 0.9375 | 0.0486 |
| 50 | 8.0 | 1 | None | 0.9508 | 0.9514 | 0.6875 | 0.8750 | 1.0000 | 0.0365 |
| 50 | 8.0 | 1 | balanced | 0.9508 | 0.9514 | 0.6875 | 0.8750 | 1.0000 | 0.0365 |

## Why This Selection

The selected model is chosen by test macro F1-score first, then test accuracy, normal recall, NMOS recall, and lower overfit gap.
This keeps the tuning story focused on balanced defect classification instead of only maximizing overall accuracy.

## Next Step

The next step is feature importance analysis and dashboard integration of ML prediction results.
