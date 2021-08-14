# -*- coding: utf-8 -*-

from collections import defaultdict


def regularity(sequence):
    """
    Compute the regularity of a sequence.

    The regularity basically measures what percentage of a user's
    visits are to a previously visited place.

    Parameters
    ----------
    sequence : list
        A list of symbols.

    Returns
    -------
    float
        1 minus the ratio between unique and total symbols in the sequence.
    """
    if len(set(sequence)) <= 1:
        return 1.0

    if len(set(sequence)) == len(sequence):
        return .0

    return 1 - (len(set(sequence)) / len(sequence))


def stationarity(sequence):
    """
    Compute the stationarity of a sequence.

    A stationary transition is one whose source and destination symbols
    are the same. The stationarity measures the percentage of transitions
    to the same location.

    Parameters
    ----------
    sequence : list
        A list of symbols.

    Returns
    -------
    float
        Percentage of the sequence that is stationary.
    """
    if len(sequence) <= 1:
        return 1.0

    if len(sequence) == len(set(sequence)):
        return .0

    stationary_transitions = 0
    for i in range(1, len(sequence)):
        if sequence[i - 1] == sequence[i]:
            stationary_transitions += 1
    return stationary_transitions / (len(sequence) - 1)


def _suffix_array_manber_myers(s):
    """
    Reference: http://algorithmicalley.com/archive/2013/06/30/suffix-arrays.aspx
    Reference: https://louisabraham.github.io/notebooks/suffix_arrays.html
    """
    def sort_bucket(s, bucket, order):
        d = defaultdict(list)
        for i in bucket:
            key = ''.join(s[i + order // 2:i + order])
            d[key].append(i)
        result = []
        for k, v in sorted(d.items()):
            if len(v) > 1:
                result += sort_bucket(s, v, 2 * order)
            else:
                result.append(v[0])
        return result

    return sort_bucket(s, range(len(s)), 1)


def _kasai(s, sa):
    """
    Reference: https://web.stanford.edu/class/cs166/lectures/03/Small03.pdf
    Reference: https://web.stanford.edu/class/archive/cs/cs166/cs166.1146/
    """
    n = len(s)
    k = 0
    lcp = [0] * n
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i
    for i in range(n):
        k = k - 1 if k > 0 else 0
        if rank[i] == n - 1:
            k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
    return lcp


def diversity(sequence):
    """
    Returns the ratio of distinct substrings over the total number of substrings in the sequence.
    Reference: https://www.youtube.com/watch?v=m2lZRmMjebw
    """
    if len(sequence) <= 1:
        return 0.0

    if len(sequence) == len(set(sequence)):
        return .0

    suffix_array = _suffix_array_manber_myers(sequence)
    lcp = _kasai(sequence, suffix_array)

    n = len(sequence)
    total_substrs = (n * (n + 1)) // 2
    distinct_substrs = total_substrs - sum(lcp)
    return distinct_substrs / total_substrs