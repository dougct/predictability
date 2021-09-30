# -*- coding: utf-8 -*-

import numpy as np


def entropy(Y):
    """
    Computes H(X) using Shannon's formula.
    """
    _, count = np.unique(Y, return_counts=True, axis=0)
    prob = count / len(Y)
    return np.sum((-1) * prob * np.log2(prob))


def joint_entropy(Y, X):
    """
    Computes H(X, Y), the joint entropy of X and Y.
    """
    XY = np.c_[X, Y]
    return entropy(XY)


def conditional_entropy(X, Y):
    """
    Computes the conditional entropy of X given Y, whose formula is H(X | Y) = H(X, Y) - H(Y).
    """
    return joint_entropy(X, Y) - entropy(Y)


def rand_entropy(sequence):
    """
    Computes the "random entropy", that is, the entropy of a uniform distribution.

    Equation:
        S_{rand} = \log_{2}(n), where n is the number of unique symbols in the input sequence.

    Args:
        sequence: 1-D array-like sequence of symbols.

    Returns:
        A float representing the random entropy of the input sequence.

    Reference: 
        Limits of Predictability in Human Mobility. Chaoming Song, Zehui Qu, 
        Nicholas Blumm1, Albert-László Barabási. Vol. 327, Issue 5968, pp. 1018-1021.
        DOI: 10.1126/science.1177170
    """
    alphabet_size = np.unique(sequence).size
    return np.log2(alphabet_size)


def unc_entropy(sequence):
    """
    Compute temporal-uncorrelated entropy (Shannon entropy).

    Equation:
    S_{unc} = - \sum p(i) \log_2{p(i)}, for each symbol i in the input sequence.

    Args:
        sequence: the input sequence of symbols.

    Returns:
        temporal-uncorrelated entropy of the input sequence.

    Reference: 
        Limits of Predictability in Human Mobility. Chaoming Song, Zehui Qu, 
        Nicholas Blumm1, Albert-László Barabási. Vol. 327, Issue 5968, pp. 1018-1021.
        DOI: 10.1126/science.1177170
    """
    _, counts = np.unique(sequence, return_counts=True)
    probabilities = counts / counts.sum()
    return -np.sum(probabilities * np.log2(probabilities))


def entropy_kontoyiannis(sequence):
    """
    Estimate the entropy rate of the sequence using Kontoyiannis' algorithm.

    Reference:
        Kontoyiannis, I., Algoet, P. H., Suhov, Y. M., & Wyner, A. J. (1998).
        Nonparametric entropy estimation for stationary processes and random
        fields, with applications to English text. IEEE Transactions on Information
        Theory, 44(3), 1319-1327.

    Equation:
        S_{real} = \left( \frac{1}{n} \sum \Lambda_{i} \right)^{-1}\log_{2}(n)

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float representing an estimate of the entropy rate of the sequence.
    """
    if not sequence:
        return 0.0
    
    # For the pattern matching below, items in the sequence have to be strings
    sequence = [str(item) for item in sequence]

    lambdas = 0
    n = len(sequence)
    for i in range(n):
        current_sequence = ''.join(sequence[0:i])
        match = True
        k = i
        while match and k < n:
            k += 1
            match = ''.join(sequence[i:k]) in current_sequence
        lambdas += (k - i)
    return (1.0 * len(sequence) / lambdas) * np.log2(len(sequence))


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
        S_{real} = \left( \frac{1}{n} \sum \Lambda_{i} \right)^{-1}\log_{2}(n)

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float representing an estimate of the entropy rate of the sequence.
    """
    if not sequence:
        return 0.0

    # For the pattern matching below, items in the sequence have to be strings
    sequence = [str(item) for item in sequence]

    lambdas = 0
    n = len(sequence)
    for i in range(n):
        match_length = longest_match_length(sequence, i)
        print(sequence[0:i], sequence[i:i+match_length])
        lambdas += (match_length + 1)
    print(lambdas)
    return (1.0 * len(sequence) / lambdas) * np.log2(len(sequence))


def baseline_entropy(sequence):
    """"
    Computes the baseline entropy of the input sequence using a closed-formula. 
    The baseline entropy is the entropy of a sequence with the same size as the
    original sequence, the same number of symbols in the novelty component, and 
    a completely predictable routine component.

    Reference: 
        https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00304-8

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float representing an estimate of the entropy rate of the sequence.
    """
    n = len(sequence)
    m = len(set(sequence)) - 1
    k = n - m
    baseline_routine_size = (k * k) / 4 + k / 2
    baseline_novelty_size = m
    return n * np.log2(n) / (baseline_routine_size + baseline_novelty_size)


def baseline_entropy_kontoyiannis(sequence):
    """"
    Computes the baseline entropy of the input sequence by creating a baseline
    sequence and running Kontoyiannis et al.'s entropy estimator on it.

    Reference: 
        https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00304-8

    Args:
        sequence: the input sequence of symbols.

    Returns:
        A float representing an estimate of the entropy rate of the sequence.
    """
    if not sequence:
        return 0.0
    n, n_unique = len(sequence), len(set(sequence))
    baseline_sequence = [sequence[0]] * (n - n_unique) + list(set(sequence))
    return entropy_kontoyiannis(baseline_sequence)
