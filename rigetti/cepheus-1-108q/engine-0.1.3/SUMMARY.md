# Cepheus three-round summary

This is the ZNEPro team's evaluation on Rigetti Cepheus-1-108Q. The hardware plan is 30 cases, three rounds, 162 tasks, and 162,000 shots. The scored arm is `single_run_zero_telemetry`. This study evaluates standalone ZNEPro mitigation against raw QPU measurements; third-party error-mitigation packages were not run on this dataset.

The main denominator is 25 pre-registered cases. 20 of 25 cases have lower absolute error than raw in all three rounds. 21 of 25 cases have a lower three-round mean absolute error. Two cases are worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. Both are zero-reference observables whose three-round mean shifts (-1.31e-4 and -1.30e-3) are smaller than 0.08 three-round shot standard errors (SE <= 0.0183 at 3,000 pooled shots). In the `vqe_molecular` family (H2 STO-3G), all 5 pre-registered cases (and all 6 H2 circuits including `trial_00`) reduced error in all three rounds (18 of 18 circuit-rounds). `ising_2_corr_step2` is better in 2 of 3 rounds and is the case that makes the mean count 21. `maxcut_path6_angles_a` and `param_hea_2_b` are better in 1 of 3 rounds and still have a higher three-round mean.

No-card receipt coverage for all 30 cases is 148 receipts in each round and 444 in total.

## Families inside the 25

| family | better in 3, 2, 1, 0 rounds | mean lower | family mean | unit |
| --- | --- | ---: | ---: | --- |
| `control_diagnostics` | 4, 0, 0, 1 | 4 | 0.03328591424663367 | dimensionless |
| `vqe_molecular` | 5, 0, 0, 0 | 5 | 0.025372676023568408 | Hartree |
| `qaoa_maxcut` | 4, 0, 1, 0 | 4 | 0.043746796042507335 | cut_weight |
| `ising_dynamics` | 3, 1, 0, 1 | 4 | 0.016534358967124886 | dimensionless |
| `parametric_circuits` | 4, 0, 1, 0 | 4 | 0.023908453390230976 | dimensionless |

## Historical partial card

The appendix covers 4 circuits, 10 case-rounds, and 84 receipts. The card is better than the no-card replay in 5 comparisons and worse in 5. The six main rows are `diag_near_zero_2q` and `diag_product_6q`, rounds 1-3. The four examined rows are `diag_asymmetric_3q` and `h2_sto3g_trial_00`, rounds 2-3. The partial card supplied only one-qubit `error_1q`, `t1_us`, and `t2_us` without readout assignment error, so readout-dominated single-qubit product circuits (`diag_product_6q`, `diag_asymmetric_3q`) favored `single_run_zero_telemetry`, whereas `h2_sto3g_trial_00` achieved lower error with the partial card (0.0248 Ha in round 2 and 0.00136 Ha in round 3). Official temporal validity is undetermined. All scored and appendix receipts are verified against engine_version: "0.1.3".

H2 trial 00 uses the registered constant and all 14 non-identity terms. At the zero-angle Hartree-Fock point (`h2_sto3g_trial_00`), the uploaded logical OpenQASM ansatz contains cnot phase gadgets with zero rotation angles, which the Rigetti compiler simplifies to single-qubit native gates in the compiled Quil programs. Field ages at task start span 14.544762 to 14.580604 hours in round 2 and 2.019235 to 2.062868 hours in round 3.

Rebuild the full 25-case table, the examined-five table, and this appendix with `python reproduce.py`.
