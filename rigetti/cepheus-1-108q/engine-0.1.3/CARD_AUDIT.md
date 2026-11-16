# Full-card audit

The audit covered the same 162 Cepheus tasks before any with-card score was used. A card was eligible only when every field the SDK card would send had a measurement time from before the task and a documented maximum age accepted that gap. The manifest records `card_max_age` as null.

Eligible tasks: 0. Ineligible tasks: 153. Unresolved tasks: 9. Complete paired case-rounds: 0.

The published benchmark therefore uses `single_run_zero_telemetry`. The historical partial card in the appendix is a separate exploratory replay. The partial card supplied only one-qubit `error_1q`, `t1_us`, and `t2_us` without readout assignment error, so readout-dominated single-qubit product circuits (`diag_product_6q`, `diag_asymmetric_3q`) favored `single_run_zero_telemetry`, whereas `h2_sto3g_trial_00` achieved lower error with the partial card (0.0248 Ha in round 2 and 0.00136 Ha in round 3). At the zero-angle Hartree-Fock point (`h2_sto3g_trial_00`), the uploaded logical OpenQASM ansatz contains cnot phase gadgets with zero rotation angles, which the Rigetti compiler simplifies to single-qubit native gates in the compiled Quil programs. Its official temporal validity remains undetermined. All scored and appendix receipts are verified against engine_version: "0.1.3".
