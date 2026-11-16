# Slide 1. Three-round no-card result

ZNEPro team evaluation on Rigetti Cepheus-1-108Q. Arm: `single_run_zero_telemetry`. Engine 0.1.3.

Hardware plan: 30 cases, three rounds, 162 tasks, 162,000 shots.

Denominator: 25 pre-registered cases. 20 of 25 are better than raw in all three rounds. 21 of 25 have a lower three-round mean absolute error.

Two cases are worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. Both are zero-reference observables whose three-round mean shifts (-1.31e-4 and -1.30e-3) are smaller than 0.08 three-round shot standard errors (SE <= 0.0183 at 3,000 pooled shots).

In the `vqe_molecular` family (H2 STO-3G), all 5 pre-registered cases (and all 6 H2 circuits including `trial_00`) reduced error in all three rounds (18 of 18 circuit-rounds).

This study evaluates standalone ZNEPro mitigation against raw QPU measurements; third-party error-mitigation packages were not run on this dataset.

All scored and appendix receipts are verified against engine_version: "0.1.3".

---

# Slide 2. Families inside the 25

Each case has equal weight. Units stay inside the family.

| family | 3, 2, 1, 0 rounds better | mean lower | family mean |
| --- | --- | ---: | ---: |
| `control_diagnostics` | 4, 0, 0, 1 | 4 | 0.03328591424663367 dimensionless |
| `vqe_molecular` | 5, 0, 0, 0 | 5 | 0.025372676023568408 Hartree |
| `qaoa_maxcut` | 4, 0, 1, 0 | 4 | 0.043746796042507335 cut_weight |
| `ising_dynamics` | 3, 1, 0, 1 | 4 | 0.016534358967124886 dimensionless |
| `parametric_circuits` | 4, 0, 1, 0 | 4 | 0.023908453390230976 dimensionless |

---

# Slide 3. Why 20 of 25 and 21 of 25 differ

A round is better when raw absolute error minus ZNEPro absolute error is positive.

`ising_2_corr_step2` is better in 2 of 3 rounds and has a positive mean, so it is inside the 21 and outside the 20.

Worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. `maxcut_path6_angles_a` and `param_hea_2_b` are better in 1 of 3 rounds and have a negative mean.

No case in the 25 is equal to raw, and none is incomplete for engine 0.1.3.

---

# Slide 4. Historical partial card

Separate denominator: 4 circuits, 10 case-rounds, 84 receipts.

The card is better than the no-card replay in 5 comparisons and worse in 5. None are equal.

Main rows: `diag_near_zero_2q` and `diag_product_6q`, rounds 1-3. Examined rows: `diag_asymmetric_3q` and `h2_sto3g_trial_00`, rounds 2-3.

The partial card supplied only one-qubit `error_1q`, `t1_us`, and `t2_us` without readout assignment error, so readout-dominated single-qubit product circuits (`diag_product_6q`, `diag_asymmetric_3q`) favored `single_run_zero_telemetry`, whereas `h2_sto3g_trial_00` achieved lower error with the partial card (0.0248 Ha in round 2 and 0.00136 Ha in round 3).

Official temporal validity is undetermined. All scored and appendix receipts are verified against engine_version: "0.1.3". This appendix does not change the 20 of 25 or 21 of 25 counts.

---

# Slide 5. H2 trial 00 and reproduction

The energy uses the registered constant and all 14 non-identity terms. At the zero-angle Hartree-Fock point (`h2_sto3g_trial_00`), the uploaded logical OpenQASM ansatz contains cnot phase gadgets with zero rotation angles, which the Rigetti compiler simplifies to single-qubit native gates in the compiled Quil programs.

Field ages span 14.544762 to 14.580604 hours in round 2 and 2.019235 to 2.062868 hours in round 3. Each with-card receipt records `calibration_applied: true` and a `calibration_sha256`.

From this directory, offline:

```bash
python reproduce.py
```
