# Day 4 Feature Engineering and Review Status

## Goal

Day 4의 목표는 소자별 feature extraction을 확장하고, anomaly rule 결과를 dashboard에서 바로 사용할 수 있는 상태값으로 만드는 것입니다.

## Implemented Features

### Diode

- `I@0V`, `I@0.7V`, `I@1V`, `I@2V`
- max/min current
- `V@10nA`, `V@100nA`, `V@1uA`
- IFIT mean absolute error
- IFIT max absolute error

### Resistor

- resistance
- conductance
- fit intercept
- I-V linearity R2
- fit point count
- `I@3V`, `I@-3V`
- compliance hit count

### Capacitor

- `C@0V`
- max/min capacitance
- capacitance range
- raw absolute max capacitance
- median `G_or_R`
- invalid capacitance point count

### NMOS

- mean drain voltage
- gate voltage range
- mean drain current
- drain current span
- drain current at `Vg=0V`
- max gate leakage
- compliance suspect flag

## Review Status

Rule output now includes:

- `anomaly_flags`
- `anomaly_score`
- `review_status`

Review status categories:

| Status | Meaning |
|---|---|
| normal | 특이 flag 없음 |
| review | 확인이 필요한 이상 후보 |
| priority | 우선 검토가 필요한 이상 후보 |

## Why It Matters

소자별 feature가 충분히 정리되어야 AI Agent가 의미 있는 설명을 생성할 수 있습니다. Day 4에서는 단순 수치 추출을 넘어, dashboard와 report에서 바로 사용할 수 있는 품질 상태값까지 연결했습니다.

