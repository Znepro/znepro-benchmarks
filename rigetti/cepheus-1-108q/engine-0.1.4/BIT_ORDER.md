# Bit order

Every histogram used by this replay is stored with `q0_left` in `../engine-0.1.3/counts/`. Character 0 of a bitstring is logical qubit 0. The same index in a Pauli string is that qubit.

Receipts in this directory set `bit_order` to `q0_left`. The replay does not reverse those keys. A second reversal would score a different observable.
