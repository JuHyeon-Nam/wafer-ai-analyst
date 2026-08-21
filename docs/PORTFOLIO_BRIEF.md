# Portfolio Brief

## One-Line Summary

Wafer AI Analyst는 반도체 wafer 전기 측정 raw data를 소자/shot 단위로 정리하고, rule-based review와 RandomForest ML prediction을 결합해 이상 후보를 좁히는 AI-assisted semiconductor test analysis workflow입니다.

## Problem

Wafer 전기 측정 데이터는 CSV/Excel 파일 안에 측정 curve, 장비 조건, sheet 정보, shot 정보가 섞여 있습니다.

이 상태에서는 다음 문제가 있습니다.

- 파일마다 column 구조가 달라 바로 비교하기 어렵습니다.
- diode, resistor, capacitor, NMOS가 서로 다른 전기적 의미를 가집니다.
- 실제 불량 label이 충분하지 않아 처음부터 production-grade AI 모델을 만들기 어렵습니다.
- 숫자만 보면 비전공자나 다른 팀원이 결과를 이해하기 어렵습니다.

## Solution

이 프로젝트는 raw data를 분석 가능한 구조로 바꾼 뒤, rule과 ML을 함께 사용합니다.

```text
Raw CSV / Excel
-> parser
-> curve table
-> feature table
-> rule-based anomaly review
-> synthetic defect scenario
-> RandomForest training / tuning
-> ML prediction
-> feature importance
-> dashboard / report
```

## Main Results

| Item | Result |
|---|---:|
| Measurements | 74 |
| Curve points | 10,294 |
| Devices | Cap, NMOS, diode, resistor |
| Shots | 1-1, 1-4, 5-1, 5-4, 9-1, 9-4 |
| Tuned model test accuracy | 0.9722 |
| Tuned model macro F1-score | 0.9718 |
| Final validation | 65 PASS / 0 FAIL |

## What Was Built

| Area | Implementation |
|---|---|
| Data parsing | Clarius-style CSV parser, multi-sheet diode Excel parser |
| Feature engineering | IV/CV curve에서 전류, 저항, capacitance, leakage, compliance feature 추출 |
| Rule review | `normal`, `review`, `priority` status와 anomaly flag 생성 |
| Process reasoning | anomaly flag를 가능한 공정/측정 이슈 후보와 연결 |
| ML dataset | 실제 feature 분포 기반 synthetic defect scenario dataset 생성 |
| Model | RandomForest baseline 학습, 72개 parameter 조합 tuning |
| Evaluation | accuracy, macro F1, confusion matrix, per-class metric |
| Interpretability | feature importance를 전기 feature group별로 분석 |
| Dashboard | Overview, ML Prediction, Feature Importance, Curve Detail, Report 탭 |
| Report | Markdown/HTML analysis report 자동 생성 |
| Validation | demo check와 final validation script 구성 |

## Why RandomForest

RandomForest를 선택한 이유는 데이터 형태와 프로젝트 상황에 맞기 때문입니다.

- 데이터가 이미지가 아니라 tabular feature data입니다.
- 실제 label이 많지 않아 deep learning보다 현실적입니다.
- local 환경에서 학습과 튜닝이 빠릅니다.
- feature importance로 모델 판단 근거를 설명할 수 있습니다.
- baseline model로 현업/프로젝트에서 설명하기 쉽습니다.

## Technical Differentiators

- Raw file을 바로 모델에 넣지 않고, 소자별 curve feature를 먼저 설계했습니다.
- rule-based baseline을 먼저 만들어 데이터 구조와 이상 기준을 명확히 했습니다.
- synthetic defect scenario를 사용하되, 실제 feature distribution을 기반으로 만들었습니다.
- label leakage를 줄이기 위해 ID, 설명문, rule 결과 column은 model feature에서 제외했습니다.
- 모델 결과를 dashboard에 붙일 때 missing indicator와 device one-hot column을 맞추는 inference adapter를 만들었습니다.
- feature importance와 curve detail을 함께 보여줘 모델 결과를 설명 가능하게 만들었습니다.

## Engineering Boundary

이 프로젝트는 실제 양산 공정의 root cause를 확정하는 시스템이 아닙니다.

현재 데이터만으로 원인을 확정하려면 부족합니다. 실제 root cause analysis에는 공정 recipe, 박막 두께, 온도/압력/시간 조건, 장비 log, SEM/광학 이미지, 반복 측정 데이터가 더 필요합니다.

따라서 이 프로젝트는 다음처럼 설명하는 것이 정확합니다.

```text
실제 wafer 측정 데이터 구조를 기반으로 feature engineering, rule review, ML training, dashboard inference, report generation까지 연결한 decision support workflow입니다.
```

## Best Interview Message

```text
이 프로젝트에서 가장 신경 쓴 부분은 모델 정확도 하나가 아니라, 반도체 전기 측정 데이터를 실제 분석 workflow로 연결하는 것이었습니다.
Raw data parsing부터 feature engineering, rule baseline, synthetic ML dataset, RandomForest tuning, feature importance, dashboard, 자동 report까지 end-to-end로 구성했습니다.
실제 불량 원인을 단정하지 않고, 엔지니어가 먼저 확인할 shot/device 후보를 좁히는 decision support system으로 설계했습니다.
```
