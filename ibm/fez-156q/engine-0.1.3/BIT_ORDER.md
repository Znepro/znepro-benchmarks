# Bit order

Every benchmark histogram and both readout histograms are stored with `bit_order: q0_left`. The leftmost character is qubit 0.

`source_bit_order` is `qiskit`. In that source order the rightmost character is qubit 0. The published keys were reversed into `q0_left` before they were stored here. Do not reverse them again.

For a benchmark task, character `i` is logical qubit `i` of that circuit. The Pauli label uses the same index: `P_i` is logical qubit `i`. `logical_to_physical` maps that logical index onto the device qubit used for the layout.

For a readout histogram, character `i` is active physical qubit `physical_qubits[i]`. The active list is the same 22 qubits in every round. `m3_in_session` reads `prob_meas1_prep0` from the all-zero histogram and `prob_meas0_prep1` from one minus the all-one rate, then maps those rates through `logical_to_physical`.
