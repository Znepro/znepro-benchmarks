# Scoring

A bitstring contributes +1 when every non-identity Pauli sees a 0, and the sign flips once for each non-identity Pauli that sees a 1. The raw expectation is the shot-weighted mean of those signs.

`m3_in_session` uses the same shots. For each non-identity qubit, `gamma = 1 - p(1|0) - p(0|1)` and `delta = p(0|1) - p(1|0)`. The measured Z is +1 on bit 0 and -1 on bit 1. The corrected correlator is the mean of the product `(Z - delta)` divided by the product of the gammas.

Absolute error is the absolute difference between the estimate and the stabilizer reference, which is `+1` or `-1`. A round is better when the arm absolute error is strictly lower than raw.

A width, circuit, or weight mean is the mean of the case-round absolute errors in that group. Each case-round has equal weight. Each published group contains 27 case-rounds.

Head-to-head counts a case-round as lower only when the arm absolute error is strictly lower than `m3_in_session`, and as higher only when it is strictly higher. There are 81 case-rounds.
