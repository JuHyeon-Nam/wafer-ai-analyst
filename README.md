# Wafer AI Analyst

**Wafer AI Analyst**는 반도체 웨이퍼 전기 측정 데이터를 자동으로 정리하고, shot 단위 이상 징후와 가능한 공정 이슈 후보를 설명하는 AI 품질 분석 에이전트 프로젝트입니다.

## 프로젝트 목적

반도체 측정 장비에서 나온 CSV/Excel 데이터를 사람이 하나씩 열어보지 않아도, 시스템이 자동으로 다음 작업을 수행하도록 만드는 것이 목표입니다.

1. 원본 측정 파일을 읽는다.
2. 소자 종류와 shot 정보를 자동 분류한다.
3. IV/CV curve에서 전기적 feature를 계산한다.
4. rule-based anomaly detection으로 이상 후보를 찾는다.
5. 가능한 공정 이슈 후보를 제시한다.
6. LLM 기반 AI Agent가 분석 결과를 자연어 리포트로 설명한다.

## 핵심 키워드

- Wafer electrical test
- Shot-level quality analysis
- IV/CV curve parsing
- Electrical feature extraction
- Rule-based anomaly detection
- Process issue reasoning
- LLM explanation agent
- Streamlit dashboard

## 데이터

현재 분석 대상 데이터는 다음 소자 측정값입니다.

- `diode`: 다이오드 I-V curve
- `resistor`: 저항 I-V curve
- `Cap`: 커패시터 C-V curve
- `NMOS`: 트랜지스터 Id-Vg curve

원본 측정 데이터는 개인정보/실험 데이터 보호를 위해 기본적으로 Git에 올리지 않습니다. 로컬에서는 `data/raw/`에 넣고 실행합니다.

## 폴더 구조

```text
wafer-ai-analyst/
  data/
    raw/                 # 원본 측정 데이터, Git 제외
    processed/           # 정제 데이터, Git 제외
  docs/                  # 기획서, 팀원 가이드, 설명 문서
  notebooks/             # 실험용 노트북
  reports/
    figures/             # 생성 그래프, Git 제외
  src/
    wafer_ai_analyst/
      parsers.py         # CSV/Excel parser
      features.py        # 소자별 feature extraction
      rules.py           # anomaly detection rule
      process_reasoning.py
      cli.py             # command-line 실행 진입점
  app.py                 # Streamlit dashboard
```

## 빠른 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.wafer_ai_analyst.cli --input data/raw --output data/processed/features.csv
streamlit run app.py
```

## 포트폴리오 설명

```text
반도체 wafer electrical test data를 기반으로 parsing, feature extraction, anomaly detection, process issue reasoning, LLM explanation, dashboard까지 이어지는 AI-assisted analysis workflow를 설계했습니다.
```

## 한계점

이 프로젝트는 공정 불량 원인을 확정하는 시스템이 아닙니다. 전기적 측정 패턴을 바탕으로 가능한 원인 후보를 좁히고, 추가 확인 방향을 제시하는 분석 보조 시스템입니다.

