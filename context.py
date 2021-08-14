# -*- coding: utf-8 -*-

import numpy as np

from .entropy import entropy_kontoyiannis


def sequence_splitting(X, C):
    """"
    Computes the conditional entropy of sequence X, given sequence C,
    using the sequence-splitting strategy.

    Reference: https://dl.acm.org/doi/10.1145/3459625
    """
    assert len(X) == len(C), "sequences must have the same size"
    ents = []
    w = []
    for context in set(C):
        sequence = [str(X[i]) for i in range(len(X)) if C[i] == context]
        ents.append(entropy_kontoyiannis(sequence))
        w.append(len(sequence) / len(X))
    return np.average(ents, weights=w)


def sequence_merging(X, C):
    """"
    Computes the conditional entropy of sequence X, given sequence C,
    using the sequence-merging strategy.

    Reference: https://dl.acm.org/doi/10.1145/3459625
    """    
    assert len(X) == len(C), "sequences must have the same size"
    XY = [str(X[i]) + str(C[i]) for i in range(len(X))]
    return entropy_kontoyiannis(XY) - entropy_kontoyiannis(C)


def sequence_concatenating(X, C):
    """"
    Computes the conditional entropy of sequence X, given sequence C,
    using the sequence-concatenating strategy.
    """    
    assert len(X) == len(C), "sequences must have the same size"    
    return entropy_kontoyiannis(C + X) - entropy_kontoyiannis(C)
