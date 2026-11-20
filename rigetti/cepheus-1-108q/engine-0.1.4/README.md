# Rigetti Cepheus-1-108Q, engine 0.1.4

This directory is a zero-telemetry replay of the published Cepheus counts. The device is Cepheus-1-108Q and the arm is `single_run_zero_telemetry` on engine 0.1.4. The client pin is znepro 1.0.3. No new quantum-processor task was run. The 162,000 shots stay the shots already stored under `../engine-0.1.3/counts/`.

The hardware record remains 30 cases, three rounds, 162 tasks, and 162,000 shots. The historical baseline in `../engine-0.1.3/` is not rewritten. Its receipts stay on engine 0.1.3. This directory adds 444 receipts, 148 in each round, each `COMPLETED`, with `calibration_applied` false and `readout_telemetry` false.

On the 25 pre-registered cases the rebuilt scores match the baseline: 20 of 25 are better than raw in all three rounds, and 21 of 25 have a lower three-round mean absolute error. Family mean absolute errors and mean error reductions match the 0.1.3 figures. Two cases stay worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`. Both are zero-reference observables. Their absolute error is the size of the estimate, so a small change in a mitigated expectation does not establish a gain.

Execution-time cards for all 162 groups had no readout telemetry. 93 groups whose compiled program contains a two-qubit opcode also had no coupling telemetry. Those two counts are the recorded audit in `status.json`. The compiled programs for that audit are not republished here. The scored arm therefore sends no calibration card.

## Reproduce

From this directory:

```bash
python3 reproduce.py
```

The command uses no network and no credential. It reads this directory and, read-only, the sibling baseline. It checks that every 0.1.4 expectation equals the stored 0.1.3 expectation, rebuilds the 25-case and family tables, and checks that the baseline tree is unchanged. Files under `reproduced/` are outputs.

## Files

- `status.json` records the arm, the 20 of 25 and 21 of 25 headlines, and the telemetry gaps.
- `receipts/` holds the 444 public receipts. Local task identifiers are not included.
- `BIT_ORDER.md` states the `q0_left` convention.
- `SCORING.md` states how absolute error is reduced.
- `SUMMARY.md` is the one-page result.

A receipt id has the form `r{round}/{case_id}__{group_id}/{observable}`. These ids are local to this study. A replay on the same shots is the same execution, not another round.
