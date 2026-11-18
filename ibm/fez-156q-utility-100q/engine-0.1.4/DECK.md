# Slide 1. Three-round utility-scale result

ZNEPro team evaluation on IBM Fez (156Q Heron r2). Engine 0.1.4.

Nine native circuits at 50, 80, and 100 qubits. Basis `rz`, `sx`, `x`, `cz`. Largest program: 732 `cz` gates. 27 stabilizer observables. Three rounds. 27 benchmark tasks plus 6 readout calibration tasks. 4,096 shots per task. Benchmark shots 110,592. Total shots 135,168. Active register: 103 physical qubits.

Every arm is better than raw in all three rounds for 27 of 27 observables: `m3_in_session`, `single_run_zero_telemetry`, `provider_target_card`, and `in_session_card`.

All 243 receipts are COMPLETED on engine_version 0.1.4. 81 receipts belong to each arm.

---

# Slide 2. Mean absolute error by width

Each case-round has equal weight. Each row has 27 case-rounds.

| width | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `50` | 0.216833 | 0.115087 | 0.0891778 | 0.0463885 | 0.0442466 |
| `80` | 0.198532 | 0.137404 | 0.0632484 | 0.0300838 | 0.0451668 |
| `100` | 0.171007 | 0.114083 | 0.0562958 | 0.0428317 | 0.0401012 |

---

# Slide 3. Mean absolute error by circuit

| circuit | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `mirror_brickwork_d8` | 0.278935 | 0.222392 | 9.8587e-06 | 1e-06 | 1e-06 |
| `clifford_ising_trotter_d6` | 0.202962 | 0.125667 | 0.179798 | 0.110476 | 0.120282 |
| `ghz_ladder_local_zz` | 0.104474 | 0.018515 | 0.0289138 | 0.00882671 | 0.00923194 |

---

# Slide 4. Head to head with m3_in_session

On 81 case-rounds, `in_session_card` is strictly lower than `m3_in_session` on 76 and strictly higher on 5.

`provider_target_card` is strictly lower on 65 and strictly higher on 16.

Neither comparison has a tie.

`provider_target_card` keeps `error_1q`, `error_2q`, `t1_us`, `t2_us`, `prob_meas1_prep0`, and `prob_meas0_prep1` for the 103 active qubits. Its witness is `249cf82cd9b2137980b920afac9009873081c5b49577656275e2045710fc08f0`. `in_session_card` replaces the two assignment probabilities with that round's all-zero and all-one pubs. `single_run_zero_telemetry` sends no card.

---

# Slide 5. Bit order and how to rebuild

Counts are stored `q0_left`. `source_bit_order` is `qiskit`: the source string had qubit 0 on the right, and the published keys were reversed before storage. Do not reverse them again.

A round is better when the arm absolute error is lower than raw. Width, circuit, and weight means pool every case-round with equal weight.

From this directory, `python3 reproduce.py` checks 243 receipts, 135,168 shots, both card witnesses, the three mean tables, the 27 of 27 win counts, and the 76 of 81 and 65 of 81 head-to-head counts.
