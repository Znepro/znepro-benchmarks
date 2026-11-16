# rigetti-cepheus-v1

This is the ZNEPro team's evaluation on Rigetti Cepheus-1-108Q, engine 0.1.3.

The hardware plan is 30 cases, three rounds, 162 tasks, and 162,000 shots. The scored arm is `single_run_zero_telemetry`. Of the 25 pre-registered cases, 20 of 25 have lower absolute error than raw in all three rounds, and 21 of 25 have a lower three-round mean absolute error. Two cases are worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. Both are zero-reference observables whose three-round mean shifts (-1.31e-4 and -1.30e-3) are smaller than 0.08 three-round shot standard errors (SE <= 0.0183 at 3,000 pooled shots).

No-card receipts cover all 30 cases: 148 in each round and 444 in total. All scored and appendix receipts are verified against engine_version: "0.1.3". The exploratory historical partial card covers 4 circuits, 10 case-rounds, and 84 receipts. The card is better than the no-card replay in 5 comparisons and worse in 5. The partial card supplied only one-qubit `error_1q`, `t1_us`, and `t2_us` without readout assignment error, so readout-dominated single-qubit product circuits (`diag_product_6q`, `diag_asymmetric_3q`) favored `single_run_zero_telemetry`, whereas `h2_sto3g_trial_00` achieved lower error with the partial card (0.0248 Ha in round 2 and 0.00136 Ha in round 3). At the zero-angle Hartree-Fock point (`h2_sto3g_trial_00`), the uploaded logical OpenQASM ansatz contains cnot phase gadgets with zero rotation angles, which the Rigetti compiler simplifies to single-qubit native gates in the compiled Quil programs. This study evaluates standalone ZNEPro mitigation against raw QPU measurements; third-party error-mitigation packages were not run on this dataset.

The PDF attached to this release is `rigetti-cepheus-v1.pdf`.

From the study directory:

```bash
python reproduce.py
```
