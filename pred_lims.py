# -*- coding: utf-8 -*-

import math
import numpy as np

from .entropy import entropy_kontoyiannis, baseline_entropy_kontoyiannis


def max_predictability(S, N):
    """
    Estimate the maximum predictability of a sequence with
    entropy S and alphabet size N.

    Equation:
    $S = - H(\Pi) + (1 - \Pi)\log(N - 1), where $H(\Pi)$ is given by:$
        $H(\Pi) = \Pi \log_2(\Pi) + (1 - \Pi) \log_2(1 - \Pi)$

    Args:
        S: the entropy of the input sequence of symbols.
        N: the size of the alphabet (number of unique symbols)

    Returns:
        the maximum predictability of the sequence.

    Reference:
        Limits of Predictability in Human Mobility. Chaoming Song, Zehui Qu,
        Nicholas Blumm1, Albert-László Barabási. Vol. 327, Issue 5968, pp. 1018-1021.
        DOI: 10.1126/science.1177170
    """
    if S == 0.0 or N <= 1:
        return 1.0
    for p in np.arange(0.0001, 1.0000, 0.0001):
        h = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
        pi_max = h + (1 - p) * math.log2(N - 1) - S
        if abs(pi_max) <= 0.001:
            return round(p, 3)
    return 0.0


def predictability_gap(sequence):
    if not sequence:
        return 0.0

    n_unique = len(set(sequence))

    original_entropy = entropy_kontoyiannis(sequence)
    original_predictability = max_predictability(original_entropy, n_unique)

    baseline_entropy = baseline_entropy_kontoyiannis(sequence)
    baseline_predictability = max_predictability(baseline_entropy, n_unique)

    return original_predictability - baseline_predictability
