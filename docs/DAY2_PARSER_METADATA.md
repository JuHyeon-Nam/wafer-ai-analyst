# Day 2 Parser and Metadata Export

## Goal

Day 2의 목표는 raw measurement file을 분석 가능한 구조로 안정적으로 분리하는 것입니다.

## Implemented

- Clarius-style CSV에서 measurement block과 metadata block 분리
- Excel diode file의 `Settings` sheet를 읽어 sheet별 metadata 연결
- `measurement_id`, `measurement_name`, `source_file`, `device`, `shot` 기준 추가
- Metadata를 별도 CSV로 export하는 CLI 옵션 추가

## CLI Output

```bash
python -m src.wafer_ai_analyst.cli \
  --input data/raw \
  --output data/processed/features.csv \
  --metadata-output data/processed/metadata.csv
```

## Why It Matters

반도체 측정 raw data는 단순한 숫자 표가 아니라 측정 조건과 장비 설정이 함께 들어 있습니다. Metadata를 분리하면 나중에 같은 이상 징후가 측정 조건 때문인지, 실제 소자 특성 때문인지 검토할 수 있습니다.

