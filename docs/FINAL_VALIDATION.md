# Final Validation Summary

- Generated at: `2026-08-21 09:09:54`
- Validation scope: `current working tree at runtime`
- Checks: `65`
- Passed: `65`
- Failed: `0`

## Project Snapshot

- Measurements: `74`
- Curve points: `10294`
- Devices: `Cap, NMOS, diode, resistor`
- Shots: `1-1, 1-4, 5-1, 5-4, 9-1, 9-4`
- Tuned model test accuracy: `0.9722`
- Tuned model macro F1-score: `0.9718`

## Validation Checks

| Check | Status | Detail |
|---|---|---|
| `file:README.md` | `PASS` | exists |
| `file:app.py` | `PASS` | exists |
| `file:requirements.txt` | `PASS` | exists |
| `file:docs/DEMO_GUIDE.md` | `PASS` | exists |
| `file:docs/DEMO_RUN_SUMMARY.md` | `PASS` | exists |
| `file:docs/ANALYSIS_REPORT_DEMO.md` | `PASS` | exists |
| `file:scripts/run_demo_check.py` | `PASS` | exists |
| `file:scripts/generate_analysis_report.py` | `PASS` | exists |
| `file:data/processed/features_preview.csv` | `PASS` | exists |
| `file:data/processed/curves_preview.csv` | `PASS` | exists |
| `file:models/random_forest_tuned.joblib` | `PASS` | exists |
| `file:data/processed/rf_tuned_feature_importance_preview.csv` | `PASS` | exists |
| `file:data/processed/rf_tuned_metrics_preview.json` | `PASS` | exists |
| `compile:src/wafer_ai_analyst/synthetic.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/process_reasoning.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/explanations.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/importance.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/__init__.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/rules.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/features.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/parsers.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/ml_dataset.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/cli.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/ml_inference.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/tuning.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/modeling.py` | `PASS` | compiled |
| `compile:src/wafer_ai_analyst/reporting.py` | `PASS` | compiled |
| `compile:scripts/generate_analysis_report.py` | `PASS` | compiled |
| `compile:scripts/generate_readme_assets.py` | `PASS` | compiled |
| `compile:scripts/prepare_ml_dataset.py` | `PASS` | compiled |
| `compile:scripts/run_final_validation.py` | `PASS` | compiled |
| `compile:scripts/analyze_feature_importance.py` | `PASS` | compiled |
| `compile:scripts/tune_random_forest.py` | `PASS` | compiled |
| `compile:scripts/train_random_forest.py` | `PASS` | compiled |
| `compile:scripts/run_demo_check.py` | `PASS` | compiled |
| `compile:scripts/generate_synthetic_dataset.py` | `PASS` | compiled |
| `compile:scripts/generate_portfolio_packet.py` | `PASS` | compiled |
| `compile:app.py` | `PASS` | compiled |
| `import:src.wafer_ai_analyst.parsers` | `PASS` | imported |
| `import:src.wafer_ai_analyst.features` | `PASS` | imported |
| `import:src.wafer_ai_analyst.rules` | `PASS` | imported |
| `import:src.wafer_ai_analyst.synthetic` | `PASS` | imported |
| `import:src.wafer_ai_analyst.ml_dataset` | `PASS` | imported |
| `import:src.wafer_ai_analyst.modeling` | `PASS` | imported |
| `import:src.wafer_ai_analyst.tuning` | `PASS` | imported |
| `import:src.wafer_ai_analyst.ml_inference` | `PASS` | imported |
| `import:src.wafer_ai_analyst.reporting` | `PASS` | imported |
| `dataset:measurements` | `PASS` | 74 |
| `dataset:curve_points` | `PASS` | 10294 |
| `dataset:column:measurement_id` | `PASS` | available |
| `dataset:column:device` | `PASS` | available |
| `dataset:column:shot` | `PASS` | available |
| `dataset:column:review_status` | `PASS` | available |
| `dataset:column:ml_predicted_label` | `PASS` | available |
| `dataset:column:ml_confidence` | `PASS` | available |
| `model:test_accuracy` | `PASS` | 0.9722 |
| `model:test_macro_f1` | `PASS` | 0.9718 |
| `model:feature_count` | `PASS` | 70 |
| `report:section:Executive Summary` | `PASS` | markdown |
| `report:section:Review Count` | `PASS` | markdown |
| `report:section:ML Prediction Count` | `PASS` | markdown |
| `report:section:Feature Importance Summary` | `PASS` | markdown |
| `report:section:Model Metrics` | `PASS` | markdown |
| `report:html_title` | `PASS` | html |
| `report:html_table` | `PASS` | html |

## Final Status

The project is ready for a reproducible local demo when all checks pass.
Generated data/model artifacts remain local outputs and are intentionally excluded from GitHub.
