# Slide 1. Three-round Fez result

ZNEPro team evaluation on IBM Fez (156Q Heron r2). Engine 0.1.3.

Hardware plan: 30 cases, three rounds, 162 benchmark tasks, 6 readout calibration tasks, 4,096 shots per task. Benchmark shots 663,552. Total shots 688,128.

Denominator: 25 pre-registered cases. `in_session_card` is better than raw in all three rounds for 19 of 25 and has a lower three-round mean for 22 of 25. `single_run_zero_telemetry` is 19 of 25 and 20 of 25. `provider_target_card` is 16 of 25 and 18 of 25. `m3_in_session`, rebuilt from the stored all-zero and all-one histograms, is 20 of 25 and 20 of 25.

This study evaluates standalone ZNEPro mitigation against raw QPU measurements; third-party error-mitigation packages were not run on this dataset.

All 1,332 receipts are COMPLETED on engine_version 0.1.3. 444 receipts belong to each arm.

---

# Slide 2. Families inside the 25

Each case-round has equal weight. Values are mean absolute error.

| family | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |
| --- | ---: | ---: | ---: | ---: | ---: |
| `control_diagnostics` | 0.105976 | 0.0568953 | 0.108119 | 0.0443351 | 0.0451908 |
| `vqe_molecular` | 0.0590805 | 0.0428005 | 0.056069 | 0.0228104 | 0.01934 |
| `qaoa_maxcut` | 0.0795912 | 0.0485778 | 0.0459166 | 0.0339785 | 0.0260004 |
| `ising_dynamics` | 0.0771301 | 0.0780851 | 0.0872858 | 0.078083 | 0.0844625 |
| `parametric_circuits` | 0.0144851 | 0.0100233 | 0.0110456 | 0.0168846 | 0.00800908 |

---

# Slide 3. Head to head with m3_in_session

On the 25, `provider_target_card` is strictly lower than `m3_in_session` on 50 case-rounds and strictly higher on 25. Its three-round mean is lower for 17 of 25.

`in_session_card` is strictly lower on 55 case-rounds and strictly higher on 20. Its three-round mean is lower for 17 of 25.

Across all 30 cases, `in_session_card` has a lower three-round mean than raw for 26 of 30, and a lower three-round mean than `m3_in_session` for 21 of 30.

---

# Slide 4. What the cards contain

`provider_target_card` is the active 22-qubit extract: `error_1q`, `error_2q`, `t1_us`, `t2_us`, `prob_meas1_prep0`, and `prob_meas0_prep1`. Its witness is `c61ebc1290d2dba44fdbeb33cb559c6df443caf937c7792567fd0011e689a943`, the published preflight properties digest. The sanitized JSON is not that digest.

`in_session_card` keeps the gate and coherence fields and replaces the two assignment probabilities with that round's all-zero and all-one pubs. `single_run_zero_telemetry` sends no card.

No card in this directory carries an account, an instance, or a job identifier.

---

# Slide 5. Bit order and how to rebuild

Counts are stored `q0_left`. `source_bit_order` is `qiskit`: the source string had qubit 0 on the right, and the published keys were reversed before storage. Do not reverse them again.

A round is better when the arm absolute error is lower than raw. A family mean pools every case-round with equal weight. H2 energy is the registered constant plus all 14 non-identity terms.

From this directory, `python3 reproduce.py` checks 1,332 receipts, 688,128 shots, both card witnesses, the family tables, the win counts, and the 18 H2 rows.
