# ZNEPro benchmarks

Public hardware studies from the ZNEPro team. Each study is self-contained and can be rebuilt offline.

## Studies

- [IBM Fez 156Q Heron r2, engine 0.1.3](ibm/fez-156q/engine-0.1.3/README.md). Three rounds on Fez, 162 benchmark tasks plus 6 readout calibration tasks, 688,128 shots. The main denominator is 25 pre-registered cases. `in_session_card` is better than raw in all three rounds for 19 of 25 and has a lower three-round mean for 22 of 25. `single_run_zero_telemetry` is 19 of 25 and 20 of 25. `provider_target_card` is 16 of 25 and 18 of 25.
- [Rigetti Cepheus-1-108Q, engine 0.1.3](rigetti/cepheus-1-108q/engine-0.1.3/README.md). Three rounds on Cepheus, scored without a calibration card. The main denominator is 25 pre-registered cases: 20 of 25 are better than raw in all three rounds, and 21 of 25 have a lower three-round mean absolute error. Two cases are worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. Both are zero-reference observables whose three-round mean shifts (-1.31e-4 and -1.30e-3) are smaller than 0.08 three-round shot standard errors (SE <= 0.0183 at 3,000 pooled shots). In the `vqe_molecular` family (H2 STO-3G), all 5 pre-registered cases (and all 6 H2 circuits including `trial_00`) reduced error in all three rounds (18 of 18 circuit-rounds).
