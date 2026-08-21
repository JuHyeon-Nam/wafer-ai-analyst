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
