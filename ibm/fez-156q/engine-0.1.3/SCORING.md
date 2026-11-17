# Scoring

A bitstring contributes +1 when every non-identity Pauli sees a 0, and the sign flips once for each non-identity Pauli that sees a 1. The raw expectation is the shot-weighted mean of those signs.

`m3_in_session` uses the same shots. For each non-identity qubit, `gamma = 1 - p(1|0) - p(0|1)` and `delta = p(0|1) - p(1|0)`. The measured Z is +1 on bit 0 and -1 on bit 1. The corrected correlator is the mean of the product `(Z - delta)` divided by the product of the gammas.

A `components` case reports the mean absolute error of its Pauli components against `recorded_primary`. Every other case reports the absolute error of `constant + sum(coefficient * expectation)` against `recorded_primary`. H2 energy uses the registered constant and all 14 non-identity terms.

Absolute-error reduction is raw absolute error minus arm absolute error. A round is better when the arm absolute error is lower than raw. A case has a lower three-round mean when the mean of its three arm errors is lower than the mean of its three raw errors.

A family mean is the mean of the case-round absolute errors in that family. Each case-round has equal weight. The preregistered table uses the 25 `main_25` cases. The 30-case table adds the five `examined_5` cases.

Head-to-head counts a case-round as lower only when the arm absolute error is strictly lower than `m3_in_session`, and as higher only when it is strictly higher.
