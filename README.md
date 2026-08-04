<h1 align="center">Wafer AI Analyst</h1>

<p align="center">
  <b>AI-assisted semiconductor wafer electrical test analysis system</b><br/>
  Shot-level quality review · Electrical feature extraction · Process issue reasoning
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-10_Day_Sprint-2E74B5?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Domain-Semiconductor-0B2545?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-LLM_Agent-6F42C1?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" />
</p>

## Overview

**Wafer AI Analyst**는 반도체 웨이퍼 전기 측정 데이터를 자동으로 정리하고, 소자별 IV/CV curve에서 핵심 feature를 추출한 뒤, shot 단위 이상 징후와 가능한 공정 이슈 후보를 제시하는 분석 시스템입니다.

측정 장비에서 나온 raw CSV/Excel 파일은 측정값, 장비 조건, shot 정보가 섞여 있어 사람이 바로 비교하기 어렵습니다. 이 프로젝트는 그 과정을 자동화해 엔지니어가 shot별 품질 상태를 빠르게 검토할 수 있도록 설계했습니다.

```text
Raw measurement files
-> Data parsing
-> Device/shot classification
-> Electrical feature extraction
-> Anomaly rule check
-> Process issue candidate reasoning
-> AI explanation-ready report
-> Dashboard visualization
```

## Team

### 남주현 | Team Lead

`인하대학교 소프트웨어공학과`

![Semiconductor](https://img.shields.io/badge/Semiconductor-Data_Analysis-0B2545?style=flat-square)
![AI](https://img.shields.io/badge/AI-Agent_Workflow-6F42C1?style=flat-square)
![Software](https://img.shields.io/badge/Software-Pipeline_Design-3776AB?style=flat-square)

- Wafer electrical test data 분석 구조 설계
- Python 기반 parser, feature extraction, anomaly rule workflow 구성
- LLM Agent 설명 생성 구조와 GitHub 개발 흐름 관리

### 임유경

`한국기술교육대학교 메카트로닉스공학부`

![Semiconductor](https://img.shields.io/badge/Semiconductor-Process_Flow-0B2545?style=flat-square)
![AI](https://img.shields.io/badge/AI-Result_Interpretation-6F42C1?style=flat-square)

- Wafer shot 구조와 측정 공정 흐름 정리
- 공정/장비 관점의 이상 원인 후보 정의
- AI 설명 결과가 비전공자도 이해 가능한지 검토

### 임채진

`한국기술교육대학교 정보통신공학과`

![Semiconductor](https://img.shields.io/badge/Semiconductor-Test_Data-0B2545?style=flat-square)
![AI](https://img.shields.io/badge/AI-Dashboard_Report-6F42C1?style=flat-square)

- Raw measurement data 처리 흐름 정리
- Dashboard 화면 구성과 분석 결과 시각화 설계
- AI report에 들어갈 shot별 요약 항목 정리

### 최규상

`한국기술교육대학교 전기공학과`

![Semiconductor](https://img.shields.io/badge/Semiconductor-Device_Feature-0B2545?style=flat-square)
![AI](https://img.shields.io/badge/AI-Anomaly_Rule-6F42C1?style=flat-square)

- Diode, NMOS, resistor, capacitor의 전기적 feature 정의
- IV/CV curve 기반 이상 징후 기준 정리
- AI Agent가 해석할 anomaly flag와 공정 이슈 후보 연결

## Problem Definition

반도체 제조와 테스트 과정에서는 wafer, shot, device 단위로 많은 전기 측정 데이터가 생성됩니다. 엔지니어는 다음 문제를 자주 마주합니다.

- 측정 파일이 많아 수작업 확인 시간이 오래 걸림
- CSV/Excel 안에 측정값과 장비 조건이 섞여 있음
- 같은 소자라도 shot 위치에 따라 전기적 특성이 달라짐
- 이상값이 실제 공정 문제인지, 측정 오류인지 빠르게 구분해야 함
- 분석 결과를 팀원이 이해할 수 있는 형태로 설명해야 함

Wafer AI Analyst는 전기 측정 데이터를 자동 정제하고, shot 단위 품질 상태를 빠르게 검토하는 분석 workflow를 제공합니다.

## System Architecture

```mermaid
flowchart LR
    A["Raw CSV / Excel<br/>Clarius measurement data"] --> B["Parser<br/>measurement block + metadata"]
    B --> C["Classifier<br/>device / shot inference"]
    C --> D["Feature Extractor<br/>IV/CV metrics"]
    D --> E["Anomaly Rules<br/>quality flags"]
    E --> F["Process Reasoning<br/>issue candidates"]
    F --> G["AI Explanation Layer<br/>engineer-readable summary"]
    G --> H["Streamlit Dashboard<br/>interactive review"]
```

## Dataset

분석 대상은 wafer shot 단위 전기 측정 데이터입니다.

| Device | Measurement | Main Columns | Extracted Features |
|---|---|---|---|
| Diode | I-V curve | `AnodeI`, `AnodeV`, `IFIT` | `I@1V`, `I@2V`, max current, fitting error |
| Resistor | I-V curve | `AI`, `AV` | resistance, linearity, current saturation count |
| Capacitor | C-V curve | `C`, `V`, `G_or_R` | `C@0V`, max/min capacitance, invalid point count |
| NMOS | Id-Vg curve | `DrainI`, `DrainV`, `GateI`, `GateV` | drain current span, gate leakage, compliance suspect |

Raw data는 실험 데이터 보호를 위해 GitHub에 포함하지 않습니다. 로컬 환경에서는 `data/raw/` 폴더에 측정 파일을 넣고 분석합니다.

## Core Features

### Raw Data Parsing

Clarius 계측 장비에서 export된 CSV 파일은 위쪽에 실제 측정값이 있고, 아래쪽에 측정 조건 metadata가 붙어 있습니다. Parser는 이 둘을 분리합니다.

```text
CSV file
-> measurement table
-> measurement metadata
-> device name
-> shot label
```

### Feature Extraction

소자별 품질 판단에 필요한 feature를 계산합니다.

| Device | Feature Meaning |
|---|---|
| Diode | 같은 전압에서 전류가 얼마나 흐르는지, fitting curve와 얼마나 다른지 확인 |
| Resistor | I-V curve가 직선에 가까운지, 계산된 저항값이 shot별로 다른지 확인 |
| Capacitor | capacitance 값이 물리적으로 정상 범위인지, 이상 측정점이 있는지 확인 |
| NMOS | drain current가 장비 전류 제한에 걸렸는지, gate leakage가 큰지 확인 |

### Anomaly Detection

초기 버전은 소량의 실제 측정 데이터에서도 안정적으로 동작하도록 rule-based 방식으로 이상 후보를 탐지합니다.

| Anomaly Flag | Trigger Example | Meaning |
|---|---|---|
| `measurement_error_suspect` | capacitor 값이 비정상적으로 큼 | 장비 오류값, probe contact 문제, 저장 오류 가능성 |
| `compliance_limit_suspect` | NMOS drain current가 제한값 근처에 고정 | 장비 compliance limit 또는 short 가능성 |
| `current_saturation_suspect` | resistor 전류가 특정 값 이상에서 포화 | 접촉 저항 변화 또는 측정 조건 영향 가능성 |
| `curve_fit_mismatch` | diode 측정 curve와 fitting curve 차이가 큼 | 비이상적인 diode 동작 또는 접촉 불안정 가능성 |

### Process Issue Reasoning

전기적 이상 징후를 가능한 공정/측정 이슈 후보와 연결합니다.

| Electrical Pattern | Candidate Issue | Interpretation |
|---|---|---|
| Diode current differs by shot | Junction variation, contact issue, CD variation | 같은 diode 구조가 shot 위치에 따라 다르게 동작 |
| Diode curve differs from fitting curve | Non-ideal diode behavior, contact instability | 이상적인 diode 모델과 실제 측정값 사이의 차이 |
| Resistor linearity decreases | Contact resistance, current saturation | 저항 소자가 정상적인 직선 응답을 보이지 않음 |
| Capacitor has unrealistic value | Measurement error, probe issue, data artifact | 물리값보다 장비/저장 오류 가능성 |
| NMOS current sticks near limit | Compliance limit, short suspect | 장비 전류 제한으로 실제 curve가 왜곡될 가능성 |

이 시스템은 공정 원인을 단정하지 않습니다. 전기적 증거를 바탕으로 가능한 원인 후보를 좁히고, 추가 확인 방향을 제시하는 engineering review tool입니다.

## Tech Stack

| Category | Stack | Usage |
|---|---|---|
| Language | Python | 분석 파이프라인과 dashboard 구현 |
| Data Processing | pandas, numpy | CSV/Excel 정제, 수치 계산, feature extraction |
| Excel Handling | openpyxl | multi-sheet diode Excel 파일 처리 |
| Visualization | plotly | IV/CV curve와 shot별 feature 시각화 |
| Dashboard | Streamlit | 사용자 입력과 분석 결과 화면 구성 |
| AI Layer | LLM prompt workflow | 분석 결과를 자연어 설명으로 변환 |
| Version Control | Git, GitHub | 팀 개발 이력 관리 |

## Project Structure

```text
wafer-ai-analyst/
  app.py
  requirements.txt
  README.md
  data/
    raw/
    processed/
  docs/
    DAY1_DATA_AUDIT.md
    GITHUB_SETUP.md
    PROJECT_PLAN.md
  reports/
    figures/
  src/
    wafer_ai_analyst/
      parsers.py
      features.py
      rules.py
      process_reasoning.py
      cli.py
```

## Quick Start

```bash
git clone https://github.com/JuHyeon-Nam/wafer-ai-analyst.git
cd wafer-ai-analyst

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

원본 측정 데이터를 `data/raw/`에 넣은 뒤 feature table을 생성합니다.

```bash
python -m src.wafer_ai_analyst.cli \
  --input data/raw \
  --output data/processed/features.csv
```

Dashboard를 실행합니다.

```bash
streamlit run app.py
```

## 10-Day Sprint Plan

| Day | Goal |
|---|---|
| Day 1 | Repository setup, README 정리, 데이터 구조 audit |
| Day 2 | CSV parser 고도화, metadata 분리 안정화 |
| Day 3 | Excel diode parser 고도화, shot별 curve 정리 |
| Day 4 | 소자별 feature extraction 확장 |
| Day 5 | anomaly rule 정리 및 threshold 조정 |
| Day 6 | process issue candidate mapping 고도화 |
| Day 7 | LLM explanation prompt module 구현 |
| Day 8 | Streamlit dashboard UI 개선 |
| Day 9 | 자동 분석 리포트 생성 |
| Day 10 | demo 결과 정리 및 최종 문서화 |

## Current Status

- [x] GitHub repository setup
- [x] Project directory structure
- [x] Team README rewrite
- [x] Day 1 dataset audit
- [x] CSV/Excel parser baseline
- [x] Device-level feature extraction baseline
- [x] Rule-based anomaly detection baseline
- [ ] Dashboard refinement
- [ ] AI explanation prompt module
- [ ] Automated report generation

## Engineering Notes

현재 데이터만으로 실제 공정 불량 원인을 확정할 수는 없습니다. 실제 root cause analysis에는 공정 recipe, 온도/압력/시간 조건, 증착 두께, 식각 조건, 도핑 조건, SEM/광학 이미지, 반복 측정 데이터가 추가로 필요합니다.

따라서 Wafer AI Analyst는 다음 목적에 초점을 둡니다.

```text
전기 측정 데이터에서 이상 징후를 찾고,
가능한 공정/측정 이슈 후보를 좁히고,
엔지니어가 다음 확인 방향을 빠르게 판단하도록 돕는다.!!!!!!!!!!!!!!!!!
```

## Documents

- [`docs/DAY1_DATA_AUDIT.md`](docs/DAY1_DATA_AUDIT.md)
- [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md)
- [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md)

