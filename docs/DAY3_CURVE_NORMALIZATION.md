# Day 3 Curve Normalization

## Goal

Day 3의 목표는 각 파일에 흩어진 IV/CV curve를 하나의 long-format table로 정리하는 것입니다.

## Implemented

- 모든 measurement table에 공통 identifier 추가
- `measurement_id`, `source_file`, `device`, `shot`, `measurement_name`, `point_index` 컬럼 생성
- CSV/Excel 측정 curve를 하나의 normalized curve table로 export
- Dashboard에서 device/shot별 curve viewer를 만들 수 있는 기반 구성

## CLI Output

```bash
python -m src.wafer_ai_analyst.cli \
  --input data/raw \
  --output data/processed/features.csv \
  --curves-output data/processed/curves.csv
```

## Why It Matters

Feature table은 shot별 요약값을 보여주고, curve table은 실제 IV/CV 그래프를 다시 그리는 데 사용됩니다. 두 table을 분리하면 분석 결과와 원본 curve를 함께 추적할 수 있습니다.

