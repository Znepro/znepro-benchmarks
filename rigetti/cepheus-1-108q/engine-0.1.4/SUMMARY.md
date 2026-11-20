# Cepheus engine 0.1.4

Zero-telemetry replay of the published Cepheus-1-108Q counts. Engine 0.1.4, client 1.0.3, arm `single_run_zero_telemetry`. No additional processor shots.

444 receipts, 148 per round, all `COMPLETED`. `calibration_applied` is false on every receipt. `readout_telemetry` is false on every receipt. The recorded audit has no readout data on 162 groups and no coupling data on 93 two-qubit-gated groups.

Main 25: 20 of 25 better than raw in all three rounds, 21 of 25 lower three-round mean absolute error. The same headlines as engine 0.1.3. Every mitigated expectation matches the stored 0.1.3 receipt.

Family mean absolute error and mean error reduction match the baseline:

| family | MAE | mean reduction | unit |
| --- | ---: | ---: | --- |
| `control_diagnostics` | 0.27178138 | 0.033285914 | dimensionless |
| `vqe_molecular` | 0.093121023 | 0.025372676 | Hartree |
| `qaoa_maxcut` | 0.57042544 | 0.043746796 | cut_weight |
| `ising_dynamics` | 0.20993661 | 0.016534359 | dimensionless |
| `parametric_circuits` | 0.036489691 | 0.023908453 | dimensionless |

Worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. Both are zero-reference observables. 162 tasks and 162,000 shots are the baseline execution, shared with engine 0.1.3.
