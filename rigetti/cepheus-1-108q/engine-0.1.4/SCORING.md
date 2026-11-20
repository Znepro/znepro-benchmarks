# Scoring

Absolute error is the absolute deviation from the registered reference in the baseline manifest.

For a component primary, the absolute error is the mean absolute deviation of the registered components. For a weighted primary, it is the absolute deviation of the constant plus the weighted Pauli terms. The H2 primary uses all 14 non-identity terms.

Reduction is raw absolute error minus mitigated absolute error. A round is better when that reduction is strictly positive. A three-round mean is lower when the mean of the three reductions is strictly positive.

The main denominator is the 25 pre-registered cases. The five examined cases stay outside that denominator. Family mean absolute error is the mean of the per-round mitigated absolute errors inside that family. Family mean reduction is the mean of the case-level three-round means.

`diag_near_zero_2q` and `ising_6_mag_step1` have a near-zero reference. Their absolute error is the size of the estimate.

The 0.1.4 value is accepted only when it equals the stored 0.1.3 mitigated expectation for the same case, group, round, and observable. The baseline receipts are read and not rewritten.
