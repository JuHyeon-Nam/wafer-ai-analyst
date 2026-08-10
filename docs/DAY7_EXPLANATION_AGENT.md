# Day 7 Explanation Agent

## Goal

Day 7의 목표는 분석 결과를 사람이 이해할 수 있는 설명으로 바꾸는 explanation agent layer를 구현하는 것입니다.

## Implemented

- `beginner_explanation`: 비전공자도 이해할 수 있는 쉬운 설명
- `engineer_explanation`: 측정 feature, anomaly flag, 후보 원인, 후속 확인 항목을 포함한 엔지니어용 설명
- `llm_prompt`: LLM API에 연결할 수 있는 구조화 prompt
- CLI `--explanations-output` 옵션 추가
- Streamlit dashboard에서 measurement별 설명 확인 기능 추가

## Example Flow

```text
Feature table
-> anomaly_flags
-> process_issue_candidates
-> beginner explanation
-> engineer explanation
-> LLM prompt
```

## Explanation Policy

생성된 설명은 다음 원칙을 따릅니다.

- 공정 원인을 확정하지 않음
- 측정 evidence를 먼저 제시
- anomaly flag와 공정 후보를 연결
- 비전공자용 설명과 엔지니어용 설명을 분리
- 추가 확인 방향을 제안

## CLI Output

```bash
python -m src.wafer_ai_analyst.cli \
  --input data/raw \
  --output data/processed/features.csv \
  --explanations-output data/processed/explanations.csv
```

## Why It Matters

AI 활용 경험으로 설명하기 좋은 부분은 단순히 "AI를 썼다"가 아니라, 숫자 데이터를 사람이 이해할 수 있는 의사결정 문장으로 바꾸는 workflow를 만들었다는 점입니다. Day 7은 이 프로젝트를 반도체 데이터 분석 프로젝트이면서 동시에 AI agent 프로젝트로 보이게 만드는 핵심 단계입니다.
