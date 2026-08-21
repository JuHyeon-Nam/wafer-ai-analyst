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
