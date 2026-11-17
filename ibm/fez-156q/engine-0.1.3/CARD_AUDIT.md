# Card audit

Each round stores two suite-level cards for the same 22 active qubits. Neither card contains an account, an instance, a job identifier, or a timestamp.

`provider_target_card` keeps `error_1q`, `t1_us`, `t2_us`, `prob_meas1_prep0`, and `prob_meas0_prep1` on each qubit, and `error_2q` on each edge. Its `calibration_sha256` is the published preflight properties digest `c61ebc1290d2dba44fdbeb33cb559c6df443caf937c7792567fd0011e689a943`. That digest witnesses the provider snapshot. It is not the hash of the sanitized JSON in this directory. The same digest is attached to every `provider_target_card` receipt.

`in_session_card` copies those gate and coherence fields and replaces `prob_meas1_prep0` and `prob_meas0_prep1` with the rates from that round's `__readout_all_zero.json` and `__readout_all_one.json`. Those are the same rates `m3_in_session` uses. Its `calibration_sha256` is SHA-256 of the canonical `{"edges","qubits"}` object, with sorted keys and no extra whitespace. `reproduce.py` recomputes that digest and checks it against the card and against every `in_session_card` receipt.

`single_run_zero_telemetry` sets `calibration_applied` to false and carries no card hash.

Native circuits in `manifest.json` use the Heron basis `rz`, `sx`, `x`, `id`, and `cz`. Each count file stores `qasm_sha256` of the group circuit in the manifest.
