# Releases

## ibm-fez-utility-100q-v1

This is the ZNEPro team's utility-scale evaluation on IBM Fez (156Q Heron r2), engine 0.1.4.

The hardware plan is 9 native circuits at 50, 80, and 100 qubits, 27 stabilizer observables, three rounds, and 135,168 shots. The largest program has 732 `cz` gates. The scored arms are `single_run_zero_telemetry`, `provider_target_card`, and `in_session_card`. `m3_in_session` is rebuilt from the stored all-zero and all-one histograms. Every arm is better than raw in all three rounds for 27 of 27 observables. `in_session_card` is strictly lower than `m3_in_session` on 76 of 81 case-rounds. `provider_target_card` is strictly lower on 65 of 81.

Receipts cover all 27 observables: 81 for each arm and 243 in total. All scored receipts are verified against engine_version: "0.1.4". The provider card witness is `249cf82cd9b2137980b920afac9009873081c5b49577656275e2045710fc08f0`. The in-session card replaces assignment probabilities with that round's readout pubs.

The PDF attached to this release is `ibm-fez-utility-100q-v1.pdf`.

From the study directory:

```bash
python3 reproduce.py
```

## ibm-fez-v1

This is the ZNEPro team's evaluation on IBM Fez (156Q Heron r2), engine 0.1.3.

The hardware plan is 30 cases, three rounds, 162 benchmark tasks, 6 readout calibration tasks, and 688,128 shots. The scored arms are `single_run_zero_telemetry`, `provider_target_card`, and `in_session_card`. `m3_in_session` is rebuilt from the stored all-zero and all-one histograms. Of the 25 pre-registered cases, `in_session_card` has lower absolute error than raw in all three rounds for 19 of 25 and a lower three-round mean for 22 of 25. `single_run_zero_telemetry` is 19 of 25 and 20 of 25. `provider_target_card` is 16 of 25 and 18 of 25.

Receipts cover all 30 cases: 444 for each arm and 1,332 in total. All scored receipts are verified against engine_version: "0.1.3". The provider card witness is `c61ebc1290d2dba44fdbeb33cb559c6df443caf937c7792567fd0011e689a943`. The in-session card replaces assignment probabilities with that round's readout pubs. This study evaluates standalone ZNEPro mitigation against raw QPU measurements; third-party error-mitigation packages were not run on this dataset.

The PDF attached to this release is `ibm-fez-v1.pdf`.

From the study directory:

```bash
python3 reproduce.py
```

## rigetti-cepheus-v1

This is the ZNEPro team's evaluation on Rigetti Cepheus-1-108Q, engine 0.1.3.

The hardware plan is 30 cases, three rounds, 162 tasks, and 162,000 shots. The scored arm is `single_run_zero_telemetry`. Of the 25 pre-registered cases, 20 of 25 have lower absolute error than raw in all three rounds, and 21 of 25 have a lower three-round mean absolute error. Two cases are worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. Both are zero-reference observables whose three-round mean shifts (-1.31e-4 and -1.30e-3) are smaller than 0.08 three-round shot standard errors (SE <= 0.0183 at 3,000 pooled shots).

No-card receipts cover all 30 cases: 148 in each round and 444 in total. All scored and appendix receipts are verified against engine_version: "0.1.3". The exploratory historical partial card covers 4 circuits, 10 case-rounds, and 84 receipts. The card is better than the no-card replay in 5 comparisons and worse in 5. The partial card supplied only one-qubit `error_1q`, `t1_us`, and `t2_us` without readout assignment error, so readout-dominated single-qubit product circuits (`diag_product_6q`, `diag_asymmetric_3q`) favored `single_run_zero_telemetry`, whereas `h2_sto3g_trial_00` achieved lower error with the partial card (0.0248 Ha in round 2 and 0.00136 Ha in round 3). At the zero-angle Hartree-Fock point (`h2_sto3g_trial_00`), the uploaded logical OpenQASM ansatz contains cnot phase gadgets with zero rotation angles, which the Rigetti compiler simplifies to single-qubit native gates in the compiled Quil programs. This study evaluates standalone ZNEPro mitigation against raw QPU measurements; third-party error-mitigation packages were not run on this dataset.

The PDF attached to this release is `rigetti-cepheus-v1.pdf`.

From the study directory:

```bash
python reproduce.py
```

## cepheus engine 0.1.4 replay

This is not a new processor execution and it does not replace `rigetti-cepheus-v1`.

Engine 0.1.4 rescores the published Cepheus counts with `single_run_zero_telemetry`. The directory is `rigetti/cepheus-1-108q/engine-0.1.4/`. It holds 444 `COMPLETED` receipts, `calibration_applied` false, and `readout_telemetry` false. The recorded audit has no readout data on 162 groups and no coupling data on 93 two-qubit-gated groups. Expectations and the 20 of 25 and 21 of 25 headlines match engine 0.1.3, including the zero-reference cases `diag_near_zero_2q` and `ising_6_mag_step1`. The 0.1.3 receipts are left unchanged. The shot total of the archive stays 985,296.

From the study directory:

```bash
python3 reproduce.py
```
