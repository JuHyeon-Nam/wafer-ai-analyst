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
