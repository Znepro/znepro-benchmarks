# IBM Fez utility scale, 50Q to 100Q, engine 0.1.4

This directory is the ZNEPro team's utility-scale evaluation on IBM Fez. The device is a 156-qubit Heron r2 processor. Nine native circuits, at 50, 80, and 100 qubits, use the basis `rz`, `sx`, `x`, and `cz`. The largest program has 732 `cz` gates. The scored arms are `single_run_zero_telemetry`, `provider_target_card`, and `in_session_card` on engine 0.1.4. `m3_in_session` is rebuilt in `reproduce.py` from the stored all-zero and all-one histograms.

The hardware plan is 9 circuits, 27 observables, three rounds, 27 benchmark tasks, and 6 readout calibration tasks. Each task is 4,096 shots. Benchmark shots are 110,592. Total shots are 135,168. The active register is 103 physical qubits.

Each observable is one stabilizer, `Z`, `ZZ`, or `ZZZZ`, with reference `+1` or `-1`. All four arms have lower absolute error than raw in all three rounds for 27 of 27 observables. Against `m3_in_session`, `in_session_card` is strictly lower on 76 of 81 case-rounds and `provider_target_card` is strictly lower on 65 of 81.

Receipts cover every observable: 81 for each arm and 243 in total. A receipt is accepted only when its own `status` is COMPLETED and its own `engine_version` is 0.1.4. All 243 receipts meet that check.

## Reproduce

From this directory:

```bash
python3 reproduce.py
```

The command uses no network and no credential. It reads `manifest.json`, `counts/`, `cards/`, and `receipts/`. Raw values come from the counts. `m3_in_session` comes from those counts and the in-session readout histograms. The three ZNEPro arms come from the COMPLETED 0.1.4 receipts. The files under `reproduced/` are outputs of this command, not its inputs.

## Files

- `SUMMARY.md` is the one-page result.
- `DECK.md` is the five-slide briefing.
- `ibm-fez-utility-100q-v1.pdf` is that briefing.
- `manifest.json` defines the circuits, observables, references, and active 103-qubit maps.
- `BIT_ORDER.md` states the `q0_left` convention.
- `SCORING.md` states how absolute error is reduced.
- `counts/` holds one histogram per circuit and the readout calibration histograms.
- `cards/` holds one provider card and one in-session card per round.
- `receipts/zero_telemetry/`, `receipts/provider_target_card/`, and `receipts/in_session_card/` hold the public receipts.

A task id has the form `r{round}/{case_id}/g0`. A receipt id adds `/{observable}`. These ids are local to this study.
