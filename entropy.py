# -*- coding: utf-8 -*-

import math
import numpy as np


def uniform_entropy(sequence):
    """
    Computes the "random entropy", that is, the entropy of a uniform distribution.

    Equation:
        $H_{uniform} = \log_{2}(n)$, where n is the number of unique symbols in the input sequence.

    Args:
        sequence: a list of symbols.

    Returns:
        A float representing the random entropy of the input sequence.
    """
    n_unique = len(set(sequence))
    if n_unique == 0:
        return 0.0
    return np.log2(n_unique)


def shannon_entropy(sequence):
    """
    Computes H(sequence) using Shannon's formula.

    Equation:
    $H_{shannon} = - \sum p(i) \log_2{p(i)}$, for each symbol i in the input sequence.

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float representing the Shannon entropy of the input sequence.
    """
    n = len(sequence)
    if n == 0:
        return 0.0
    _, counts = np.unique(sequence, return_counts=True, axis=0)
    probs = counts / n
    return np.sum((-1) * probs * np.log2(probs))


def joint_entropy(X, Y):
    """
    Computes H(X, Y), the joint entropy of X and Y.
    """
    probs = []
    for xi in set(X):
        for yi in set(Y):
            probs.append(np.mean(np.logical_and(X == xi, Y == yi)))
    return np.sum(-p * np.log2(p) for p in probs if p > 0)


def conditional_entropy(X, Y):
    """
    Computes the conditional entropy of X given Y.

    Equation:
        $H(X | Y) = H(X, Y) - H(Y)$
    """
    return joint_entropy(X, Y) - shannon_entropy(Y)


def entropy_kontoyiannis(sequence):
    """
    Estimate the entropy rate of the sequence using Kontoyiannis' algorithm.

    Reference:
        Kontoyiannis, I., Algoet, P. H., Suhov, Y. M., & Wyner, A. J. (1998).
        Nonparametric entropy estimation for stationary processes and random
        fields, with applications to English text. IEEE Transactions on Information
        Theory, 44(3), 1319-1327.

        Limits of Predictability in Human Mobility. Chaoming Song, Zehui Qu, 
        Nicholas Blumm1, Albert-László Barabási. Vol. 327, Issue 5968, pp. 1018-1021.
        DOI: 10.1126/science.1177170

    Equation:
        $H_{kontoyiannis} = \left( \frac{1}{n} \sum \Lambda_{i} \right)^{-1}\log_{2}(n)$

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float representing an estimate of the entropy rate of the sequence.
    """
    n = len(sequence)
    if n == 0:
        return 0.0
    
    # For the pattern matching below, items in the sequence have to be strings
    sequence = [str(item) for item in sequence]

    lambdas = 0
    for i in range(n):
        current_sequence = ''.join(sequence[0:i])
        match = True
        k = i
        while match and k < n:
            k += 1
            match = ''.join(sequence[i:k]) in current_sequence
        lambdas += (k - i)
    return (1.0 * n / lambdas) * np.log2(n)


def longest_match_length(s, i):
    sequence = ''.join(s[0:i])
    k = i
    while k < len(s) and ''.join(s[i:k]) in sequence:
        k += 1
    return k - i


def entropy_kontoyiannis_longest_match(sequence):
    """
    Estimate the entropy rate of the sequence using Kontoyiannis' estimator.

    Reference:
        Kontoyiannis, I., Algoet, P. H., Suhov, Y. M., & Wyner, A. J. (1998).
        Nonparametric entropy estimation for stationary processes and random
        fields, with applications to English text. IEEE Transactions on Information
        Theory, 44(3), 1319-1327.

    Equation:
        $S_{real} = \left( \frac{1}{n} \sum \Lambda_{i} \right)^{-1}\log_{2}(n)$

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float representing an estimate of the entropy rate of the sequence.
    """
    n = len(sequence)
    if n == 0:
        return 0.0

    # For the pattern matching below, items in the sequence have to be strings
    sequence = [str(item) for item in sequence]

    lambdas = 0
    for i in range(n):
        match_length = longest_match_length(sequence, i)
        lambdas += (match_length + 1)
    return (1.0 * n / lambdas) * np.log2(n)


def baseline_entropy_kontoyiannis(sequence):
    """"
    Computes the baseline entropy of the input sequence by creating a baseline
    sequence and running Kontoyiannis et al.'s entropy estimator on it.

    Reference: 
        https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00304-8

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float indicating an estimate of the baseline entropy of the sequence.
    """
    if not sequence:
        return 0.0

    n = len(sequence)
    unique_symbols = set(sequence)
    n_unique = len(unique_symbols)
    baseline_sequence = [sequence[0]] * (n - n_unique) + list(unique_symbols)
    return entropy_kontoyiannis(baseline_sequence)


def baseline_entropy(sequence):
    """"
    Computes the baseline entropy of the input sequence using a closed-formula. 
    The baseline entropy is the entropy of a sequence with the same size as the
    original sequence, the same number of symbols in the novelty component, and 
    a completely predictable routine component. 

    Notice that for sequences of size less than 100, the estimates are not very
    reliable. For longer sequences, this closed formula should give a very good
    approximation for the baseline entropy, without having to build the 
    sequence and then run Kontoyiannis et al.'s entropy estimator on it.

    Reference: 
        https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00304-8

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float indicating an estimate of the baseline entropy of the sequence.
    """
    n = len(sequence)
    m = len(set(sequence))
    k = n - m + 1
    baseline_routine_size = math.ceil((k * k) / 4 + k / 2)
    baseline_novelty_size = m
    return (n * np.log2(n)) / (baseline_routine_size + baseline_novelty_size)


# The three functions below are wrappers to the functions previously defined.
# The sole purpuse of these functions below is to follow the naming conventions
# defined in Song et al.'s paper (Limits of Predictability in Human Mobility).
# In the paper, they define three types of entropy: s_rand, s_unc, and s_real.

def s_rand(sequence):
    return uniform_entropy(sequence)

def s_unc(sequence):
    return shannon_entropy(sequence)

def s_real(sequence):
    return entropy_kontoyiannis(sequence)

