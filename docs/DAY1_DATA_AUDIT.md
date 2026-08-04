# Day 1 Data Audit

## Goal

Day 1의 목표는 GitHub repository를 정리하고, 실제 wafer electrical test 데이터가 어떤 구조로 되어 있는지 확인하는 것입니다.

## Dataset Inventory

### Primary Measurement Folder

원본 폴더 기준 파일 수는 총 159개입니다.

| File Type | Count |
|---|---:|
| CSV | 72 |
| PNG | 71 |
| PPTX | 5 |
| XLSX | 3 |
| OPJU | 4 |
| No extension | 4 |

상위 폴더 구조는 다음과 같습니다.

| Folder | Count |
|---|---:|
| CKS | 46 |
| CKS-2 | 56 |
| CKS-3 | 49 |
| Si test pattern 관련자료 | 8 |

### Device Types

CSV 측정 데이터는 다음 4개 소자로 구성됩니다.

| Device | Measurement Type | Notes |
|---|---|---|
| Diode | I-V curve | Anode current/voltage 기반 분석 |
| Resistor | I-V curve | 저항값과 선형성 계산 가능 |
| Capacitor | C-V curve | capacitance와 비정상 측정점 확인 가능 |
| NMOS | Id-Vg curve | drain current, gate leakage, compliance 가능성 확인 |

### Additional Diode Excel File

`7-2-2_Diode.xlsx`는 6개 diode shot을 포함합니다.

| Sheet | Voltage Range | Points | Max Current |
|---|---:|---:|---:|
| 7-2-2_Diode_#7-3-3 | 0V to 2V | 201 | 8.42e-08 A |
| 7-2-2_Diode_#7-2-3 | 0V to 2V | 201 | 1.52e-07 A |
| 7-2-2_Diode_#5-3-3 | 0V to 2V | 201 | 1.08e-07 A |
| 7-2-2_Diode_#5-2-3 | 0V to 2V | 201 | 8.22e-08 A |
| 7-2-2_Diode_#3-3-3 | 0V to 2V | 201 | 6.00e-08 A |
| 7-2-2_Diode_#3-2-3 | 0V to 2V | 201 | 2.08e-08 A |

## Initial Findings

- CSV 파일은 단순한 표가 아니라, 측정값 block과 장비 metadata block이 함께 들어 있는 구조입니다.
- `CKS`, `CKS-2`, `CKS-3` 폴더에는 중복 또는 반복 측정으로 보이는 파일이 포함되어 있습니다.
- Capacitor 데이터 일부에는 물리적으로 비정상적인 큰 값이 있어 measurement error 후보로 분류할 수 있습니다.
- NMOS 데이터 일부는 drain current가 장비 current limit 근처에 고정되어 compliance limit 후보로 볼 수 있습니다.
- 추가 diode Excel 파일은 shot별 current 차이가 뚜렷해 shot-level variation 분석에 적합합니다.

## Day 1 Output

- GitHub repository 생성 및 collaborator 초대
- README를 팀 프로젝트 형식으로 정리
- 프로젝트 기술스택과 10일 sprint 계획 정리
- Baseline parser, feature extraction, anomaly rule 구조 확인
- Raw data는 GitHub에 올리지 않고 로컬 분석 대상으로 유지

## Next Step

Day 2에서는 CSV parser를 더 안정화하고, measurement metadata를 별도 table로 저장할 수 있도록 구조를 확장합니다.

