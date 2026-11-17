# Fez three-round summary

Device: IBM Fez (156Q Heron r2). Engine 0.1.3. Three rounds. 30 cases (25 pre-registered, 5 examined). 162 benchmark tasks and 6 readout calibration tasks at 4,096 shots. Benchmark shots 663,552. Total shots 688,128. Active register: 22 physical qubits.

All 1,332 receipts are COMPLETED on engine_version 0.1.3. 444 receipts belong to each arm.

## Preregistered 25

Mean absolute error, each case-round weighted equally.

| family | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `control_diagnostics` | 0.105976 | 0.0568953 | 0.108119 | 0.0443351 | 0.0451908 |
| `vqe_molecular` | 0.0590805 | 0.0428005 | 0.056069 | 0.0228104 | 0.01934 |
| `qaoa_maxcut` | 0.0795912 | 0.0485778 | 0.0459166 | 0.0339785 | 0.0260004 |
| `ising_dynamics` | 0.0771301 | 0.0780851 | 0.0872858 | 0.078083 | 0.0844625 |
| `parametric_circuits` | 0.0144851 | 0.0100233 | 0.0110456 | 0.0168846 | 0.00800908 |

Rounds better than raw, counted as 3, 2, 1, 0, then cases whose three-round mean is lower than raw:

| arm | 3 | 2 | 1 | 0 | mean lower |
| --- | ---: | ---: | ---: | ---: | ---: |
| `m3_in_session` | 20 | 1 | 1 | 3 | 20 of 25 |
| `single_run_zero_telemetry` | 19 | 0 | 3 | 3 | 20 of 25 |
| `provider_target_card` | 16 | 1 | 6 | 2 | 18 of 25 |
| `in_session_card` | 19 | 4 | 0 | 2 | 22 of 25 |

Against `m3_in_session`, counting case-rounds that are strictly lower, strictly higher, and cases whose three-round mean is lower:

| arm | lower | higher | mean lower |
| --- | ---: | ---: | ---: |
| `provider_target_card` | 50 | 25 | 17 of 25 |
| `in_session_card` | 55 | 20 | 17 of 25 |

## All 30 cases

| family | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `control_diagnostics` | 0.0899996 | 0.0497782 | 0.0960277 | 0.0449622 | 0.0431305 |
| `vqe_molecular` | 0.0521241 | 0.0360766 | 0.0495921 | 0.0197086 | 0.0163276 |
| `qaoa_maxcut` | 0.0708292 | 0.0435122 | 0.0426158 | 0.0317467 | 0.0243611 |
| `ising_dynamics` | 0.102645 | 0.0865742 | 0.109184 | 0.0854079 | 0.0901401 |
| `parametric_circuits` | 0.0142413 | 0.00885704 | 0.0103938 | 0.015942 | 0.00703244 |

| arm | 3 | 2 | 1 | 0 | mean lower |
| --- | ---: | ---: | ---: | ---: | ---: |
| `m3_in_session` | 24 | 1 | 1 | 4 | 24 of 30 |
| `single_run_zero_telemetry` | 23 | 0 | 3 | 4 | 24 of 30 |
| `provider_target_card` | 19 | 2 | 6 | 3 | 22 of 30 |
| `in_session_card` | 23 | 4 | 0 | 3 | 26 of 30 |

| arm | lower | higher | mean lower |
| --- | ---: | ---: | ---: |
| `provider_target_card` | 53 | 37 | 18 of 30 |
| `in_session_card` | 64 | 26 | 21 of 30 |

H2 STO-3G energies, six trials and three rounds, are rebuilt by `reproduce.py` and written to `reproduced/TABLES.md`. `reproduce.py` checks those 18 rows against the published six-significant-digit values.
