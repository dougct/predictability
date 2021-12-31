import random


def test_regularity():
    from .metrics import regularity

    assert regularity([]) == 1.0
    assert regularity([1, 1, 1, 1]) == 1.0
    assert regularity([1, 2, 3, 4]) == 0.0
    assert regularity([1, 1, 2, 2]) == 0.5
    assert regularity([1, 1, 2, 1]) == 0.5
    assert regularity([1, 2, 1, 2]) == 0.5
    assert regularity([1, 2, 3, 1]) == 0.25
    assert round(regularity([1, 2, 1]), 2) == 0.33


def test_stationarity():
    from .metrics import stationarity

    assert stationarity([]) == 1.0
    assert stationarity([1, 1, 1, 1]) == 1.0
    assert stationarity([1, 2, 3, 4]) == .0
    assert round(stationarity([1, 1, 2, 2]), 2) == 0.67
    assert round(stationarity([1, 1, 2, 1]), 2) == 0.33
    assert stationarity([1, 2, 1, 2]) == .0
    assert stationarity([1, 2, 3, 1]) == .0
    assert stationarity([1, 2, 1]) == .0


def test_diversity():
    from .metrics import diversity

    assert diversity([]) == .0
    assert diversity(["H", "H", "H"]) == 0.5
    assert diversity(["HW", "HW", "HW"]) == 0.5
    assert round(diversity(["HW", "P", "HW", "S", "HW", "B"]), 2) == 0.90


def test_shannon_entropy():
    from .entropy import uniform_entropy, shannon_entropy

    nr_tests = 100
    sequence_size = 500
    for _ in range(nr_tests):
        X = [str(random.randint(0, 10)) for _ in range(sequence_size)]
        uniform_ent = uniform_entropy(X)
        shannon_ent = shannon_entropy(X)
        assert round(shannon_ent, 3) <= round(uniform_ent, 3)


def test_real_entropy():
    from .entropy import shannon_entropy, entropy_kontoyiannis

    nr_tests = 100
    sequence_size = 500
    for _ in range(nr_tests):
        X = [str(random.randint(0, 10)) for _ in range(sequence_size)]
        shannon_ent = shannon_entropy(X)
        song_ent = entropy_kontoyiannis(X)
        assert round(song_ent, 3) <= round(shannon_ent, 3)


def test_context():
    from .context import sequence_merging, sequence_splitting
    from .entropy import entropy_kontoyiannis

    nr_tests = 100
    sequence_size = 200
    for _ in range(nr_tests):
        X = [str(random.randint(0, 10)) for _ in range(sequence_size)]
        Y = [str(random.randint(0, 10)) for _ in range(sequence_size)]

        real_entropy = entropy_kontoyiannis(X)
        ss_entropy = sequence_splitting(X, Y)
        assert round(ss_entropy, 3) <= round(real_entropy, 3)

        sm_entropy = sequence_merging(X, Y)
        assert round(sm_entropy, 3) <= round(real_entropy, 3)
