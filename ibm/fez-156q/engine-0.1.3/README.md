# IBM Fez (156Q Heron r2), engine 0.1.3

This directory is the ZNEPro team's evaluation on IBM Fez. The device is a 156-qubit Heron r2 processor. The scored arms are `single_run_zero_telemetry`, `provider_target_card`, and `in_session_card` on engine 0.1.3. `m3_in_session` is rebuilt in `reproduce.py` from the stored all-zero and all-one histograms. This study evaluates standalone ZNEPro mitigation against raw QPU measurements; third-party error-mitigation packages were not run on this dataset.

The hardware plan is 30 cases, three rounds, 162 benchmark tasks, and 6 readout calibration tasks. Each task is 4,096 shots. Benchmark shots are 663,552. Total shots are 688,128.

The main result uses 25 pre-registered cases. Five previously examined cases stay outside that denominator. On those 25, `in_session_card` has lower absolute error than raw in all three rounds for 19 of 25 cases and a lower three-round mean absolute error for 22 of 25. `single_run_zero_telemetry` is 19 of 25 and 20 of 25 on the same two counts. `provider_target_card` is 16 of 25 and 18 of 25.

Receipts cover all 30 cases: 148 observables in each round and 444 receipts for each of the three arms, 1,332 receipts in total. A receipt is accepted only when its own `status` is COMPLETED and its own `engine_version` is 0.1.3, and when its observable, arm, and shot count match the stored counts. All 1,332 receipts meet that check.

## Reproduce

From this directory:

```bash
python3 reproduce.py
```

The command uses no network and no credential. It reads `manifest.json`, `counts/`, `cards/`, and `receipts/`. Raw values come from the counts. `m3_in_session` comes from those counts and the in-session readout histograms. The three ZNEPro arms come from the COMPLETED 0.1.3 receipts. H2 energy is the registered constant plus all 14 non-identity terms. The files under `reproduced/` are outputs of this command, not its inputs.

## Files

- `SUMMARY.md` is the one-page result.
- `DECK.md` is the five-slide briefing.
- `ibm-fez-v1.pdf` is that briefing for Fez.
- `manifest.json` defines the circuits, terms, references, and active 22-qubit maps.
- `BIT_ORDER.md` states the `q0_left` convention.
- `SCORING.md` states how absolute error is reduced.
- `CARD_AUDIT.md` records the two sanitized cards.
- `counts/` holds one histogram per benchmark task and the readout calibration histograms.
- `cards/` holds one provider card and one in-session card per round.
- `receipts/zero_telemetry/`, `receipts/provider_target_card/`, and `receipts/in_session_card/` hold the public receipts.

A task id has the form `r{round}/{case_id}/{group_id}`. A receipt id adds `/{observable}`. These ids are local to this study.
