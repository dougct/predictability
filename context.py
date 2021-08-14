# -*- coding: utf-8 -*-

import numpy as np

from .entropy import entropy_kontoyiannis


def sequence_splitting(X, C):
    ents = []
    w = []
    for context in set(C):
        sequence = [str(X[i]) for i in range(len(X)) if C[i] == context]
        ents.append(entropy_kontoyiannis(sequence))
        w.append(len(sequence) / len(X))
    return np.average(ents, weights=w)


def sequence_merging(X, Y):
    assert(len(X) == len(Y))
    XY = [str(X[i]) + str(Y[i]) for i in range(len(X))]
    return entropy_kontoyiannis(XY) - entropy_kontoyiannis(Y)


def sequence_concatenating(X, Y):
    assert(len(X) == len(Y))
    return entropy_kontoyiannis(Y + X) - entropy_kontoyiannis(Y)
