# Utility-scale three-round summary

Device: IBM Fez (156Q Heron r2). Engine 0.1.4. Three rounds. Nine circuits at 50, 80, and 100 qubits. 27 stabilizer observables. 27 benchmark tasks and 6 readout calibration tasks at 4,096 shots. Benchmark shots 110,592. Total shots 135,168. Active register: 103 physical qubits. Largest circuit: 732 `cz` gates.

All 243 receipts are COMPLETED on engine_version 0.1.4. 81 receipts belong to each arm.

Mean absolute error pools every case-round in the group. Each group below has 27 case-rounds.

## By width

| width | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `50` | 0.216833 | 0.115087 | 0.0891778 | 0.0463885 | 0.0442466 |
| `80` | 0.198532 | 0.137404 | 0.0632484 | 0.0300838 | 0.0451668 |
| `100` | 0.171007 | 0.114083 | 0.0562958 | 0.0428317 | 0.0401012 |

## By circuit

| circuit | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `mirror_brickwork_d8` | 0.278935 | 0.222392 | 9.8587e-06 | 1e-06 | 1e-06 |
| `clifford_ising_trotter_d6` | 0.202962 | 0.125667 | 0.179798 | 0.110476 | 0.120282 |
| `ghz_ladder_local_zz` | 0.104474 | 0.018515 | 0.0289138 | 0.00882671 | 0.00923194 |

## By observable weight

| weight | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Z` | 0.0542354 | 0.0340117 | 0.00683859 | 0.00451599 | 0.00213397 |
| `ZZ` | 0.233706 | 0.148894 | 0.0757422 | 0.0437228 | 0.0443089 |
| `ZZZZ` | 0.29843 | 0.183669 | 0.126141 | 0.0710652 | 0.0830717 |

Every arm is better than raw in all three rounds for 27 of 27 observables.

Against `m3_in_session`, counting case-rounds that are strictly lower, strictly higher, or tied:

| arm | lower | higher | tied |
| --- | ---: | ---: | ---: |
| `provider_target_card` | 65 | 16 | 0 |
| `in_session_card` | 76 | 5 | 0 |
