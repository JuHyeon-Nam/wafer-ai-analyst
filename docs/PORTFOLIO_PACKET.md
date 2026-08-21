# Wafer AI Analyst Portfolio Packet

- Generated at: `2026-08-21 10:23:13`
- Purpose: portfolio review, interview preparation, and demo rehearsal

---

<!-- Source: docs/PORTFOLIO_BRIEF.md -->

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

---

<!-- Source: docs/INTERVIEW_PLAYBOOK.md -->

# Interview Playbook

## 30-Second Answer

```text
Wafer AI Analyst는 반도체 wafer 전기 측정 데이터를 자동 분석하는 프로젝트입니다.
CSV/Excel raw data에서 diode, resistor, capacitor, NMOS별 전기 feature를 추출하고, rule-based anomaly review와 RandomForest ML prediction을 결합했습니다.
최종적으로 dashboard에서 rule 결과, ML 예측, feature importance, raw curve, 자동 report를 확인할 수 있게 만들었습니다.
```

## 1-Minute Answer

```text
이 프로젝트는 wafer 전기 측정 raw data를 분석 가능한 구조로 바꾸는 것에서 시작했습니다.
측정 파일마다 column과 sheet 구조가 달라서 먼저 parser를 만들고, measurement table, curve table, feature table로 나눴습니다.
그다음 diode는 특정 전압에서의 전류와 fitting error, resistor는 resistance와 I-V linearity, capacitor는 capacitance range와 invalid point, NMOS는 drain current span과 gate leakage를 feature로 만들었습니다.

실제 불량 label이 부족했기 때문에 rule-based anomaly review를 baseline으로 만들었고, 실제 feature 분포를 참고해 synthetic defect scenario dataset을 만들어 RandomForest 모델을 학습했습니다.
튜닝 후 test accuracy 0.9722, macro F1 0.9718을 얻었고, feature importance와 curve detail을 dashboard에 연결해 모델 판단 근거까지 확인할 수 있게 했습니다.
```

## 3-Minute Answer

```text
프로젝트 목표는 반도체 wafer 전기 측정 데이터를 사람이 빠르게 리뷰할 수 있는 AI-assisted 분석 workflow로 만드는 것이었습니다.

처음 raw data를 봤을 때 CSV와 Excel 안에 측정 curve, metadata, shot 정보가 섞여 있었습니다.
그래서 첫 단계로 parser를 만들고, 소자별 측정값을 normalized curve table로 정리했습니다.
그 후 diode, resistor, capacitor, NMOS마다 의미 있는 feature를 추출했습니다.

예를 들어 diode는 0V, 0.7V, 1V, 2V에서의 current와 IFIT 오차를 봤습니다.
resistor는 I-V slope로 resistance와 conductance를 계산하고, linearity와 compliance hit를 봤습니다.
capacitor는 C-V curve에서 capacitance range, raw outlier, invalid point를 봤습니다.
NMOS는 drain current span과 gate leakage를 봤습니다.

그 다음 rule-based anomaly detection을 만들었습니다.
실제 공정 불량 label이 충분하지 않았기 때문에 처음부터 deep learning을 쓰기보다, 사람이 이해할 수 있는 기준으로 normal/review/priority를 나누는 baseline을 만들었습니다.

AI 경험을 보여주기 위해 synthetic defect scenario dataset도 만들었습니다.
실제 feature 분포를 기반으로 diode leakage, resistor nonlinearity, capacitance variation, NMOS gate leakage 같은 scenario를 생성했고, RandomForest classifier를 학습했습니다.
72개 parameter 조합을 비교해 tuned model을 골랐고, test accuracy 0.9722와 macro F1 0.9718을 기록했습니다.

마지막으로 Streamlit dashboard에 Overview, ML Prediction, Feature Importance, Curve Detail, Report 탭을 만들었습니다.
이렇게 해서 단순히 모델을 학습시키는 데서 끝나지 않고, rule 결과와 ML 결과를 비교하고, feature importance와 raw curve로 판단 근거를 확인하고, Markdown/HTML report까지 자동 생성하는 workflow로 완성했습니다.

다만 이 프로젝트는 실제 root cause를 확정하는 시스템이라고 말하지 않습니다.
공정 recipe, 온도, 두께, 장비 log, SEM 이미지가 없기 때문에 원인 확정은 어렵고, 대신 먼저 확인할 shot/device 후보를 좁혀주는 decision support workflow로 설계했습니다.
```

## Team Talking Points

### 남주현

강조할 경험:

- end-to-end Python pipeline 설계
- parser, feature table, ML inference, dashboard, report workflow 연결
- GitHub commit 기반 개발 이력 관리

말하기 좋은 문장:

```text
저는 전체 workflow를 하나로 연결하는 역할을 맡았습니다. Raw data parsing부터 feature engineering, model inference, dashboard, report generation까지 끊기지 않게 구성하는 데 집중했습니다.
```

### 임유경

강조할 경험:

- wafer shot 구조와 측정 흐름 이해
- 공정/장비 이슈 후보 해석
- 비전공자도 이해할 수 있는 설명 정리

말하기 좋은 문장:

```text
저는 전기 측정 결과가 실제 공정/장비 이슈 후보와 어떻게 연결될 수 있는지 정리했습니다. 특히 probe contact, measurement range, compliance 같은 후보를 단정이 아니라 review candidate로 표현하는 데 집중했습니다.
```

### 임채진

강조할 경험:

- dashboard result table 구성
- rule result와 ML prediction 비교 화면 이해
- report artifact와 시연 흐름 정리

말하기 좋은 문장:

```text
저는 분석 결과가 사용자가 보기 쉬운 형태로 전달되는 흐름을 맡았습니다. feature table, ML prediction, curve detail, report가 dashboard에서 어떻게 이어지는지 정리했습니다.
```

### 최규상

강조할 경험:

- diode/resistor/capacitor/NMOS별 electrical feature 이해
- IV/CV curve 기반 anomaly signal 정리
- feature importance 해석

말하기 좋은 문장:

```text
저는 소자별 전기적 feature와 anomaly 기준을 정리했습니다. diode leakage, resistor linearity, capacitance outlier, NMOS gate leakage처럼 feature가 어떤 이상 후보와 연결되는지 설명할 수 있게 준비했습니다.
```

## Technical Q&A

### Q. 왜 RandomForest를 사용했나요?

현재 데이터는 이미지가 아니라 feature table입니다. RandomForest는 tabular data에서 baseline으로 강하고, 소량 데이터에서도 빠르게 학습되며, feature importance로 판단 근거를 설명할 수 있습니다.

### Q. 왜 deep learning을 쓰지 않았나요?

deep learning은 데이터가 많고 label이 충분할 때 강합니다. 이 프로젝트는 실제 confirmed defect label이 부족했기 때문에, deep learning보다 RandomForest가 더 현실적인 선택이었습니다.

### Q. synthetic data를 쓴 이유는 뭔가요?

실제 불량 label이 부족했기 때문입니다. 대신 원본 wafer feature distribution을 참고해 defect scenario를 만들고, supervised learning workflow가 가능한지 검증했습니다.

### Q. synthetic data라면 성능이 과장된 것 아닌가요?

그 가능성을 인정해야 합니다. 그래서 이 모델을 production-grade defect classifier라고 말하지 않습니다. 목적은 실제 양산 판정이 아니라, feature engineering부터 model training, tuning, inference, explanation까지 AI workflow를 구현한 것입니다.

### Q. label leakage는 어떻게 막았나요?

model feature에서 `measurement_id`, `scenario_description`, `modified_features`, `anomaly_flags`, `review_status`, explanation text 같은 column을 제외했습니다. 즉 정답이나 rule 결과를 그대로 모델에 넣지 않았습니다.

### Q. rule-based와 ML을 같이 쓴 이유는 뭔가요?

실제 label이 부족한 초기 상황에서는 rule-based baseline이 필요합니다. ML prediction은 그 위에 추가적인 후보 판단을 제공하고, 둘이 다르게 판단하면 curve detail에서 다시 확인하도록 했습니다.

### Q. feature importance에서 missing indicator가 높은 이유는 뭔가요?

소자마다 측정 column 구조가 다르기 때문입니다. 예를 들어 diode에만 있는 fitting error column은 다른 소자에서는 missing입니다. 그래서 missing indicator가 물리 현상 자체보다 schema 차이를 반영할 수 있어 해석에 주의해야 합니다.

### Q. 공정 원인을 확정할 수 있나요?

아닙니다. 전기 측정 데이터만으로 root cause를 확정할 수는 없습니다. 공정 recipe, 박막 두께, 온도/압력/시간 조건, 장비 log, SEM 이미지, 반복 측정 데이터가 추가로 필요합니다.

### Q. 그럼 프로젝트의 의미는 뭔가요?

원인 확정이 아니라 review 우선순위를 정하는 데 의미가 있습니다. 어떤 shot/device를 먼저 볼지, 어떤 전기 feature를 확인할지 좁혀주는 decision support workflow입니다.

## Trouble Shooting Story

### 1. 파일마다 column 구조가 달랐음

문제:

- CSV와 Excel sheet 구조가 달랐습니다.
- metadata와 curve data가 섞여 있었습니다.

해결:

- parser에서 measurement table, metadata table, curve table을 분리했습니다.
- 소자별 feature extractor를 따로 만들었습니다.

### 2. 실제 불량 label이 부족했음

문제:

- supervised ML을 바로 하기 어려웠습니다.

해결:

- rule-based baseline을 먼저 만들었습니다.
- 실제 feature 분포를 참고해 synthetic defect scenario dataset을 만들었습니다.

### 3. 모델 입력 column이 실제 feature table과 달랐음

문제:

- 학습 dataset에는 missing indicator와 device one-hot column이 있었고, 실제 feature table에는 없었습니다.

해결:

- inference adapter를 만들어 실제 feature table을 모델 입력 column과 같은 형태로 변환했습니다.

### 4. 모델 결과를 설명하기 어려웠음

문제:

- predicted label만 보여주면 왜 그렇게 판단했는지 설명하기 어려웠습니다.

해결:

- feature importance와 curve detail view를 dashboard에 추가했습니다.
- 자동 report에도 feature group summary와 candidate table을 넣었습니다.

## Closing Sentence

```text
이 프로젝트는 모델 하나를 만든 프로젝트라기보다, 반도체 전기 측정 데이터를 실제 분석 workflow로 바꾼 프로젝트입니다.
데이터 구조화, feature engineering, rule baseline, ML training, model interpretation, dashboard, report generation까지 연결했다는 점이 핵심입니다.
```

---

<!-- Source: docs/SELF_INTRO_AI_EXPERIENCE.md -->

# Self-Introduction AI Experience Guide

이 문서는 Wafer AI Analyst 프로젝트를 자기소개서와 면접에서 설명할 때 사용할 수 있는 경험 정리 가이드입니다.

핵심은 "AI 모델을 무작정 만들었다"가 아니라, 반도체 전기 측정 데이터를 분석 가능한 형태로 바꾸고, rule-based review와 RandomForest model을 함께 사용해 이상 후보를 좁히는 workflow를 만들었다는 점입니다.

## 한 줄 요약

반도체 wafer 전기 측정 raw data를 Python으로 정리하고, electrical feature를 추출한 뒤, RandomForest 기반 defect classification model과 dashboard를 구축해 측정 이상 후보를 빠르게 검토할 수 있는 AI-assisted 분석 시스템을 구현했습니다.

## 자소서에 쓰기 좋은 핵심 경험

| 경험 | 쉽게 말하면 | 자소서에서 강조할 점 |
|---|---|---|
| 데이터 전처리 | 엑셀/CSV에 흩어진 측정값을 표로 정리 | AI 모델보다 먼저 데이터 구조를 이해하고 정리했다 |
| Feature engineering | 전류, 전압, 저항, 누설전류 같은 의미 있는 숫자를 뽑음 | 반도체 전기 특성을 AI 입력값으로 바꿨다 |
| Rule-based review | 사람이 정한 기준으로 이상 후보를 먼저 걸러냄 | 현업식 baseline을 만들고 모델 결과와 비교했다 |
| Synthetic defect scenario | 실제 불량 label 부족을 보완하기 위해 가상 불량 패턴을 설계 | 데이터 부족 상황에서 학습 가능한 형태를 만들었다 |
| RandomForest model | 여러 decision tree를 묶어 표 데이터 분류를 수행 | tabular data에 적합하고 설명 가능한 모델을 선택했다 |
| Hyperparameter tuning | 모델 옵션을 바꿔가며 성능 비교 | 단순 실행이 아니라 성능 개선 과정을 경험했다 |
| Feature importance | 모델이 어떤 변수에 영향을 받았는지 확인 | AI 결과를 설명 가능한 형태로 해석했다 |
| Dashboard | 분석 결과를 Streamlit 화면으로 보여줌 | 결과를 팀원과 비전공자도 이해할 수 있게 시각화했다 |
| Report automation | 분석 결과를 Markdown/HTML 보고서로 생성 | 분석 결과를 재사용 가능한 산출물로 만들었다 |

## 자소서 문장 기본형

아래 문장은 그대로 복사하기보다, 본인 지원 직무와 말투에 맞게 줄이는 것이 좋습니다.

```text
반도체 wafer 전기 측정 데이터를 활용해 AI-assisted 분석 시스템을 구축한 경험이 있습니다. CSV와 Excel 형태의 raw data에는 소자별 측정 curve와 metadata가 섞여 있어 바로 모델에 넣기 어려웠기 때문에, 먼저 Python과 pandas를 사용해 measurement table, curve table, feature table로 구조화했습니다. 이후 diode, resistor, capacitor, NMOS의 전기적 특성을 반영해 leakage current, resistance, capacitance range, compliance suspect 등 분석 feature를 추출했습니다.

초기에는 실제 불량 label이 부족했기 때문에 rule-based anomaly review를 baseline으로 만들고, 이후 실제 feature 분포를 참고한 synthetic defect scenario dataset을 생성해 RandomForest classifier를 학습했습니다. 모델은 accuracy 0.9722, macro F1-score 0.9718을 기록했으며, feature importance를 통해 모델 판단에 영향을 준 전기 feature를 해석했습니다. 최종적으로 Streamlit dashboard와 자동 report를 구성해 rule 결과, ML prediction, curve detail, process issue candidate를 한 화면에서 검토할 수 있도록 만들었습니다.
```

## 더 쉬운 버전

```text
저는 반도체 측정 데이터를 AI가 분석할 수 있는 형태로 바꾸는 프로젝트를 진행했습니다. 처음 데이터는 엑셀과 CSV에 측정값이 섞여 있어 사람이 보기에도 복잡했기 때문에, Python으로 데이터를 정리하고 소자별 특징값을 뽑았습니다. 예를 들어 diode는 누설전류, resistor는 저항 변화, capacitor는 capacitance 변화, NMOS는 gate leakage 같은 값을 계산했습니다.

그 다음 정상/이상 후보를 rule로 먼저 분류하고, 부족한 불량 데이터를 보완하기 위해 가상 불량 시나리오를 만들어 RandomForest 모델을 학습했습니다. 마지막으로 모델 결과와 그래프를 dashboard로 보여주어, 어떤 측정값이 이상 후보인지 쉽게 확인할 수 있게 만들었습니다.
```

## AI 경험으로 어필할 포인트

### 1. AI 모델만 돌린 것이 아니라 데이터 문제부터 해결했다

AI 프로젝트에서 가장 중요한 부분은 모델 자체보다 데이터 정리입니다.

이 프로젝트에서는 raw CSV/Excel을 바로 학습에 사용하지 않고, 다음 순서로 구조화했습니다.

```text
raw file
-> measurement table
-> curve table
-> feature table
-> rule review
-> ML dataset
-> model prediction
```

자소서에서는 "모델 학습 전 데이터 구조화와 feature engineering을 수행했다"고 쓰면 좋습니다.

### 2. 반도체 지식을 AI 입력값으로 바꿨다

모델은 전류와 전압의 의미를 스스로 알지 못합니다.

그래서 사람이 소자별로 의미 있는 값을 뽑아줘야 합니다.

| Device | AI 입력값으로 바꾼 예시 |
|---|---|
| Diode | low-bias current, fitting error, leakage suspect |
| Resistor | resistance, conductance, I-V linearity |
| Capacitor | C@0V, capacitance range, invalid point count |
| NMOS | drain current span, gate leakage, compliance suspect |

이 부분은 반도체 경험과 AI 경험을 동시에 보여주는 핵심입니다.

### 3. RandomForest를 선택한 이유를 설명할 수 있다

RandomForest는 여러 개의 decision tree를 묶어서 예측하는 모델입니다.

이 프로젝트에서 RandomForest를 사용한 이유는 다음과 같습니다.

- 데이터가 이미지가 아니라 표 형태의 tabular data였음
- local 환경에서도 빠르게 학습 가능했음
- 데이터 수가 많지 않아 deep learning보다 현실적이었음
- feature importance로 어떤 전기적 특성이 중요했는지 설명 가능했음
- baseline model로 성능 비교와 개선 과정을 보여주기 좋았음

자소서에서는 "데이터 특성과 프로젝트 제약을 고려해 설명 가능한 tabular model을 선택했다"고 표현하면 좋습니다.

### 4. 모델 성능 개선 과정을 경험했다

그냥 모델을 한 번 돌린 것이 아니라, parameter를 바꿔가며 성능을 비교했습니다.

| 항목 | 내용 |
|---|---|
| baseline model | 기본 RandomForest 학습 |
| tuning | `n_estimators`, `max_depth`, `min_samples_leaf`, `class_weight` 비교 |
| 비교 기준 | accuracy, macro F1-score |
| 결과 | test accuracy 0.9583 -> 0.9722, macro F1 0.9560 -> 0.9718 |

여기서 macro F1-score는 class별 성능을 고르게 보는 지표입니다.

정상 데이터만 잘 맞히는 모델이 아니라, 여러 불량 후보 class를 균형 있게 맞히는지 확인하기 위해 사용했습니다.

### 5. AI 결과를 설명 가능한 형태로 만들었다

AI 모델이 "이상입니다"라고만 말하면 현업에서 쓰기 어렵습니다.

그래서 이 프로젝트에서는 다음 내용을 같이 보여줍니다.

- rule-based review status
- ML predicted label
- prediction confidence
- feature importance
- raw curve detail
- process issue candidate

자소서에서는 "모델 결과를 dashboard와 report로 시각화해 팀원이 의사결정에 활용할 수 있게 했다"고 쓰면 좋습니다.

## 개인별 자소서 방향

### 남주현

강조 방향: AI pipeline, software architecture, end-to-end implementation

쓸 수 있는 문장:

```text
저는 프로젝트에서 raw data parsing부터 feature engineering, model inference, dashboard, report generation까지 이어지는 end-to-end AI 분석 pipeline을 설계했습니다. 특히 반도체 전기 측정 데이터처럼 파일 구조가 일정하지 않은 데이터를 measurement, curve, feature table로 나누어 처리하고, 모델 입력 column을 안정적으로 관리하는 구조를 구현했습니다. 이를 통해 단순 분석 script가 아니라 재실행 가능한 workflow 형태로 프로젝트를 구성했습니다.
```

면접에서 말할 키워드:

- end-to-end pipeline
- parser, feature, rule, model, dashboard 연결
- GitHub commit 기반 개발 이력 관리
- Streamlit demo와 report 자동화

### 임유경

강조 방향: 반도체 공정 흐름 이해, wafer shot 구조, AI 결과 해석

쓸 수 있는 문장:

```text
저는 wafer shot 단위 측정 구조와 공정/장비 이슈 후보를 정리하는 역할을 맡았습니다. 측정값에서 이상 징후가 발견되더라도 원인을 바로 단정할 수 없기 때문에, probe contact, measurement range, compliance limit, leakage, capacitance variation처럼 가능한 후보를 분류하는 방식으로 접근했습니다. 이를 통해 AI 모델 결과를 공정 관점에서 해석하고, 다음 확인 방향을 좁히는 경험을 했습니다.
```

면접에서 말할 키워드:

- wafer shot 단위 분석
- 공정 이슈를 확정하지 않고 candidate로 표현
- probe contact, leakage, compliance, capacitance variation
- AI 결과를 현장 엔지니어가 이해할 수 있게 해석

### 임채진

강조 방향: 데이터 시각화, dashboard, 결과 전달력

쓸 수 있는 문장:

```text
저는 분석 결과를 사용자가 이해하기 쉬운 형태로 전달하는 부분에 집중했습니다. rule-based review와 ML prediction 결과를 표와 그래프로 정리하고, measurement별 curve detail을 확인할 수 있도록 dashboard 흐름을 구성했습니다. 단순히 모델 성능 수치만 제시하는 것이 아니라, 어떤 소자와 shot에서 review가 필요한지 빠르게 파악할 수 있도록 결과 전달 구조를 설계했습니다.
```

면접에서 말할 키워드:

- Streamlit dashboard
- Plotly chart
- rule result와 ML prediction 비교
- 분석 결과를 비전공자도 이해 가능한 화면으로 구성

### 최규상

강조 방향: 전기적 feature 이해, AI 활용 경험, 모델 해석

쓸 수 있는 문장:

```text
저는 diode, resistor, capacitor, NMOS 측정 curve에서 AI 모델에 사용할 전기적 feature를 정의하고 해석하는 부분에 참여했습니다. 예를 들어 diode는 leakage current와 fitting error, resistor는 I-V linearity와 resistance, capacitor는 capacitance range, NMOS는 gate leakage와 compliance suspect를 주요 feature로 보았습니다. 이후 RandomForest 모델의 feature importance를 확인하면서 어떤 전기적 특성이 defect prediction에 영향을 주는지 해석했습니다.
```

면접에서 말할 키워드:

- electrical feature engineering
- diode leakage, resistor linearity, capacitance variation, gate leakage
- RandomForest feature importance
- 전기공학 지식을 AI 입력값으로 변환

## 최규상 AI 경험용 상세 버전

규상이가 "AI 경험이 부족한데 이 프로젝트로 무엇을 말할 수 있나"에 대한 답은 아래처럼 잡으면 됩니다.

```text
저는 AI 모델을 직접 깊게 개발한 경험은 많지 않았지만, 이번 프로젝트를 통해 전기적 domain knowledge를 AI 모델이 사용할 수 있는 feature로 바꾸는 과정을 경험했습니다. 처음에는 전류-전압 curve를 단순 그래프로만 보았지만, 모델 학습을 위해서는 누설전류, 선형성, 저항 변화, compliance 의심 여부처럼 숫자로 정리된 입력값이 필요하다는 것을 이해했습니다.

프로젝트에서는 RandomForest 모델을 사용해 synthetic defect scenario를 분류했고, parameter tuning을 통해 성능 변화를 비교했습니다. 특히 feature importance를 확인하면서 모델이 어떤 feature를 중요하게 판단하는지 분석했고, AI 결과를 전기적 의미와 연결해 설명하는 방식에 익숙해졌습니다. 이 경험을 통해 AI를 단순한 도구가 아니라, 전공 지식을 데이터화하고 의사결정에 활용하는 방법으로 이해하게 되었습니다.
```

## 반도체 직무용 문장

```text
이 프로젝트를 통해 반도체 공정 데이터를 직접 다루지는 않았지만, wafer 전기 측정 결과를 기반으로 이상 징후를 분석하는 흐름을 경험했습니다. 전기 측정 데이터만으로 공정 원인을 확정할 수는 없기 때문에, 결과를 단정하지 않고 가능한 이슈 후보를 좁히는 방식으로 접근했습니다. 이는 실제 현업에서도 수율이나 불량 분석 시 단일 데이터만으로 결론을 내리기보다, 측정값을 기반으로 추가 확인 방향을 설정하는 과정과 유사하다고 생각합니다.
```

## AI 직무/디지털 역량용 문장

```text
AI 모델을 적용하기 위해 raw data를 그대로 사용하는 것이 아니라, 분석 목적에 맞는 feature table을 설계하고 모델 입력값을 관리하는 과정이 중요하다는 것을 배웠습니다. 또한 모델 성능만 보는 것이 아니라, feature importance와 dashboard를 통해 결과를 설명 가능한 형태로 만드는 것이 실제 활용성에 중요하다는 점을 경험했습니다.
```

## 트러블슈팅 스토리

### 문제 1. 파일 구조가 일정하지 않았다

상황:

CSV와 Excel 파일 안에 측정값, metadata, sheet 정보가 섞여 있었습니다.

해결:

measurement table, curve table, metadata table로 나누어 저장했습니다.

자소서 표현:

```text
초기 데이터는 파일마다 column 구조가 달라 바로 분석하기 어려웠습니다. 이를 해결하기 위해 측정 단위와 curve point 단위를 분리하고, 공통 measurement_id를 기준으로 연결하는 구조를 설계했습니다.
```

### 문제 2. 실제 불량 label이 부족했다

상황:

AI 분류 모델을 학습하려면 정상/불량 label이 필요한데, 실제 데이터에는 충분한 label이 없었습니다.

해결:

실제 feature 분포를 참고해 synthetic defect scenario를 만들고, 이를 학습/평가용으로 사용했습니다.

자소서 표현:

```text
실제 불량 label이 부족한 상황에서 모델 학습을 바로 진행하기 어려웠기 때문에, 실제 feature 분포를 기준으로 synthetic defect scenario를 설계했습니다. 이를 통해 데이터 부족 상황에서도 baseline AI model을 구성하고 평가할 수 있었습니다.
```

### 문제 3. 모델 결과를 설명하기 어려웠다

상황:

모델이 예측 label만 출력하면 왜 그런 판단을 했는지 알기 어려웠습니다.

해결:

feature importance, rule flag, raw curve chart를 함께 보여줬습니다.

자소서 표현:

```text
모델 예측 결과가 단순 label로 끝나지 않도록 feature importance와 raw curve를 함께 제공했습니다. 이를 통해 사용자가 모델 판단 근거를 확인하고, 공정/측정 이슈 후보를 검토할 수 있도록 구성했습니다.
```

## 면접에서 조심해야 할 표현

아래 표현은 피하는 것이 좋습니다.

| 피할 표현 | 이유 | 대신 쓸 표현 |
|---|---|---|
| 실제 공정 불량 원인을 찾아냈다 | 공정 recipe나 SEM data가 없으면 단정 불가 | 이상 후보와 가능한 원인 범위를 좁혔다 |
| 완전한 AI 자동 판정 시스템이다 | 실제 검증 데이터가 부족함 | review candidate를 제시하는 보조 분석 workflow다 |
| 딥러닝 모델을 만들었다 | 사용한 모델은 RandomForest임 | tabular data에 적합한 ML model을 학습했다 |
| 실제 불량 데이터를 대량 학습했다 | synthetic scenario를 사용했음 | 실제 feature 분포 기반 synthetic defect scenario로 baseline을 만들었다 |

## 가장 좋은 최종 답변

면접에서 짧게 말해야 하면 아래처럼 말하면 됩니다.

```text
이 프로젝트는 반도체 wafer 전기 측정 데이터를 AI가 분석할 수 있는 구조로 바꾸고, 소자별 전기 feature를 추출해 이상 후보를 분류한 프로젝트입니다. 실제 불량 label이 부족했기 때문에 rule-based review를 baseline으로 만들고, synthetic defect scenario를 생성해 RandomForest 모델을 학습했습니다. 이후 feature importance와 dashboard를 통해 모델 판단 근거를 설명 가능한 형태로 정리했습니다. 그래서 단순히 모델을 돌린 경험이 아니라, 데이터 전처리, feature engineering, 모델 학습, 평가, 시각화까지 이어지는 AI 활용 workflow를 경험했습니다.
```

---

<!-- Source: docs/DEMO_GUIDE.md -->

# Demo Guide

## Demo Goal

이 데모는 wafer electrical test data를 분석 가능한 feature table로 바꾸고, rule-based anomaly review와 RandomForest ML prediction을 함께 보여주는 end-to-end workflow를 설명하기 위한 것입니다.

핵심 메시지는 다음 한 문장입니다.

```text
전기 측정 raw data를 소자/shot 단위로 정리하고, 이상 후보를 rule과 ML로 함께 좁힌 뒤, curve와 feature importance로 판단 근거를 확인하는 분석 시스템을 만들었다.
```

## Demo Order

### 1. README에서 프로젝트 구조 설명

먼저 README의 `Overview`, `Dataset`, `Current Implementation`을 보여줍니다.

설명 포인트:

- 데이터는 diode, resistor, capacitor, NMOS 전기 측정 결과입니다.
- shot은 wafer 위에서 측정 위치를 묶는 단위입니다.
- raw file을 바로 보는 것이 아니라 parser로 measurement/curve/feature table로 정리했습니다.
- 실제 불량 label이 부족해서 rule-based review를 먼저 만들고, synthetic defect scenario로 ML workflow를 추가했습니다.

### 2. Dashboard Overview 탭

```bash
streamlit run app.py
```

앱에서 `Overview` 탭을 보여줍니다.

설명 포인트:

- 전체 measurement 수, rule normal/review/priority 수를 보여줍니다.
- device별, shot별 데이터 분포를 확인합니다.
- feature table은 각 measurement를 숫자로 요약한 결과입니다.

쉽게 말하면, raw 곡선을 AI가 바로 보는 것이 아니라 곡선에서 중요한 숫자들을 뽑아 표로 만든 것입니다.

### 3. ML Prediction 탭

`ML Prediction` 탭에서는 RandomForest 모델의 predicted label과 confidence를 보여줍니다.

설명 포인트:

- `ml_predicted_label`은 모델이 가장 가능성이 높다고 본 defect scenario입니다.
- `ml_confidence`는 모델이 얼마나 확신하는지 나타냅니다.
- rule 결과와 ML 결과가 같으면 우선 확인 후보로 보기 좋습니다.
- rule과 ML이 다르면 `Curve Detail`에서 실제 곡선을 확인합니다.

면접 설명:

```text
단순 rule만 쓰면 사람이 정한 기준에만 의존하게 됩니다. 그래서 synthetic defect scenario로 RandomForest를 학습시키고, 실제 feature table에 다시 적용해 rule 판단과 ML 판단을 비교했습니다.
```

### 4. Feature Importance 탭

`Feature Importance` 탭에서는 모델이 어떤 feature를 많이 봤는지 보여줍니다.

설명 포인트:

- `drain_i_span_a`: NMOS drain current 변화 폭입니다.
- `invalid_c_points`: capacitor C-V에서 비정상 capacitance point 개수입니다.
- `i_at_0v_a`: diode 0V 근처 leakage 후보를 볼 때 쓰는 전류입니다.
- `c_abs_max_raw_f`: capacitor raw C 값의 비정상 spike를 확인하는 값입니다.
- `compliance_hits`: 전류가 장비 제한 근처에 걸린 횟수입니다.

면접 설명:

```text
모델 성능만 확인하지 않고 feature importance를 분석해 모델이 어떤 전기적 지표를 근거로 판단했는지 검토했습니다. 특히 missing indicator가 높게 나온 부분은 물리 현상보다 측정 schema 차이를 반영할 수 있어 해석에 주의했습니다.
```

### 5. Curve Detail 탭

`Curve Detail` 탭에서 measurement 하나를 선택합니다.

추천 후보:

- `NMOS:1-4:nmos1-4`
- `Cap:1-4:cap1-4`
- `resistor:9-1:R 9-1`

설명 포인트:

- 표의 숫자만 보는 것이 아니라 실제 IV/CV curve를 같이 봅니다.
- rule anomaly flag와 ML predicted label을 함께 봅니다.
- 공정 원인을 확정하지 않고, 가능한 후보를 좁히는 방식으로 설명합니다.

### 6. Report 탭

`Report` 탭에서는 현재 분석 결과를 Markdown/HTML로 다운로드할 수 있습니다.

설명 포인트:

- dashboard를 열지 않아도 분석 결과를 문서로 공유할 수 있습니다.
- report에는 전체 요약, review count, ML prediction count, high-priority candidate, feature importance, model metric이 들어갑니다.

## Demo Check Command

시연 전에 아래 명령으로 필요한 local artifact가 있는지 확인합니다.

```bash
python scripts/run_demo_check.py
```

정상 실행되면 `docs/DEMO_RUN_SUMMARY.md`가 생성됩니다.

## Short Presentation Script

```text
이 프로젝트는 반도체 wafer 전기 측정 데이터를 자동 분석하는 시스템입니다.
처음에는 CSV와 Excel raw data를 parser로 읽어서 measurement table, curve table, feature table로 정리했습니다.
그다음 diode, resistor, capacitor, NMOS별로 전기적 feature를 추출했습니다.
예를 들어 diode는 특정 전압에서의 전류, resistor는 저항과 선형성, capacitor는 capacitance 범위, NMOS는 gate leakage와 drain current span을 봤습니다.

실제 공정 불량 label이 충분하지 않았기 때문에 먼저 rule-based anomaly detection을 만들었습니다.
이후 실제 feature 분포를 참고해 synthetic defect scenario를 생성했고, RandomForest 모델을 학습시켜 defect candidate를 예측하게 했습니다.
모델은 hyperparameter tuning을 통해 test macro F1-score 0.9718까지 개선했습니다.

마지막으로 Streamlit dashboard에서 rule 결과, ML prediction, feature importance, raw curve detail, 자동 report를 한 번에 확인할 수 있게 연결했습니다.
이 시스템은 root cause를 확정하는 모델이 아니라, 엔지니어가 먼저 확인할 shot/device 후보를 빠르게 좁혀주는 decision support workflow입니다.
```

## Questions and Answers

### Q. 이게 진짜 AI인가요?

네. rule-based logic만 있는 것이 아니라, synthetic defect scenario dataset으로 RandomForest classifier를 학습시키고 실제 feature table에 prediction을 붙였습니다.

### Q. 왜 deep learning을 안 썼나요?

현재 데이터는 이미지가 아니라 표 형태의 electrical feature data입니다. 데이터 수도 많지 않기 때문에 deep learning보다 RandomForest가 더 현실적이고 설명하기 쉽습니다.

### Q. synthetic data를 쓴 게 약점 아닌가요?

실제 불량 label이 부족한 상황에서는 약점이 맞습니다. 그래서 이 프로젝트는 양산용 확정 모델이 아니라, 실제 wafer data structure를 기반으로 ML workflow 가능성을 검증한 프로젝트라고 설명합니다.

### Q. 공정 원인까지 알 수 있나요?

전기 측정 데이터만으로 원인을 확정할 수는 없습니다. 대신 gate leakage, compliance, capacitance outlier, resistance shift 같은 전기적 증거를 바탕으로 확인해야 할 공정/측정 이슈 후보를 좁힙니다.

### Q. 가장 어필할 부분은 뭔가요?

단순 dashboard가 아니라 raw data parsing, feature engineering, anomaly rule, synthetic dataset, model training, tuning, feature importance, inference dashboard, report generation까지 end-to-end로 연결했다는 점입니다.

---

<!-- Source: docs/DEMO_RUN_SUMMARY.md -->

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

---

<!-- Source: docs/FINAL_VALIDATION.md -->

# Final Validation Summary

- Generated at: `2026-08-21 10:22:57`
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

---

<!-- Source: docs/RELEASE_NOTES.md -->

# Release Notes

## 2026-08-20

Wafer AI Analyst is organized as a reproducible local demo for semiconductor electrical test analysis.

## 2026-08-21

Portfolio, interview, and self-introduction preparation documents were added after release validation.

| Area | Result |
|---|---|
| README cleanup | Removed the date-based roadmap so the repository reads like a completed project |
| Portfolio brief | One-page project summary with problem, solution, result, and boundary |
| Interview playbook | 30-second, 1-minute, 3-minute answers and technical Q&A |
| Self-introduction guide | Resume-ready AI experience wording and personal talking points |
| Team talking points | Role-based explanation points for each team member |
| Portfolio packet | Combined Markdown packet for review and rehearsal |

## What Is Included

| Area | Result |
|---|---|
| Raw data parsing | Clarius-style CSV and multi-sheet diode Excel parsing |
| Feature engineering | Diode, resistor, capacitor, and NMOS electrical feature extraction |
| Rule-based review | `normal`, `review`, `priority` status and anomaly flags |
| Process reasoning | Candidate process/measurement issues mapped from anomaly flags |
| Explanation workflow | Beginner/engineer explanation text and LLM prompt |
| Synthetic ML data | Defect scenario dataset generated from real feature distributions |
| Model training | RandomForest baseline and tuned classifier |
| Model evaluation | Accuracy, macro F1-score, confusion matrix, per-class metrics |
| Interpretability | Feature importance by feature and feature group |
| Dashboard | Overview, ML prediction, feature importance, curve detail, explanation, report tabs |
| Reporting | Markdown/HTML analysis report generation |
| Demo validation | Local artifact check and final validation summary |

## Final Metrics

| Model | Train Accuracy | Test Accuracy | Test Macro F1 |
|---|---:|---:|---:|
| Baseline RandomForest | 0.9774 | 0.9583 | 0.9560 |
| Tuned RandomForest | 0.9896 | 0.9722 | 0.9718 |

Selected tuned model:

| Parameter | Value |
|---|---:|
| `n_estimators` | `100` |
| `max_depth` | `None` |
| `min_samples_leaf` | `3` |
| `class_weight` | `None` |

## Demo Dataset Snapshot

| Item | Value |
|---|---:|
| Measurements | 74 |
| Curve points | 10,294 |
| Devices | Cap, NMOS, diode, resistor |
| Shots | 1-1, 1-4, 5-1, 5-4, 9-1, 9-4 |

## How To Validate

```bash
python scripts/run_demo_check.py
python scripts/run_final_validation.py
streamlit run app.py
```

## Engineering Boundary

This project does not claim confirmed semiconductor root cause analysis.

The real dataset has limited confirmed defect labels, so the supervised ML workflow uses synthetic defect scenarios generated from real electrical feature distributions. The output should be explained as a decision support workflow that narrows review candidates, not as a production-grade defect disposition system.

## Recommended Demo Path

```text
README overview
-> Dashboard Overview
-> ML Prediction
-> Feature Importance
-> Curve Detail
-> Report download
-> DEMO_GUIDE Q&A
```
