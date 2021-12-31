# Estimating Predictability in Human Mobility

This repository contains a library that computes several metrics related to predictability of individual human mobility.

## Usage

First, clone the repository by running:

```
git clone https://github.com/dougct/predictability.git
```

To import the whole library, type `import predictability` from outside the `predictability` directory. Alternatively, you can import individual modules from the library by running `from predictability import MODULE-NAME`. The available modules are `metrics`, `entropy`, `pred_lims`, and `context`. Examples showing how to use functions in each of these modules can be found below.

To run the unit tests, type `python -m pytest tests.py` from inside the `predictability` directory.

## Examples

The examples below show how to use several functions in the library.

### Metrics

We can use the library to compute some metrics about a person's mobility, described in our [paper](https://dl.acm.org/doi/10.1145/3459625) on the subject.

```python
from predictability import metrics

locations = ['H', 'H', 'W', 'S', 'H']
reg = metrics.regularity(locations)
print(reg)
```

```
0.4
```

```python
from predictability import metrics

locations = ['H', 'H', 'W', 'S', 'H']
st = metrics.stationarity(locations)
print(st)
```

```
0.25
```

```python
from predictability import metrics

locations = ['H', 'H', 'W', 'S', 'H']
div = metrics.diversity(locations)
print(div)
```

```
0.8666666666666667
```

### Entropy

We first compute the _uncorrelated entropy_ (Shannon entropy) of a sequence:

```python
from predictability import entropy

locations = ['H', 'H', 'W', 'S', 'H']
ent = entropy.shannon_entropy(locations)
print(ent)
```

```
1.3709505944546687
```

We can also compute the compression-based entropy of a sequence, using the entropy estimator proposed by [Kontoyiannis](https://ieeexplore.ieee.org/abstract/document/669425) _et al._:

```python
from predictability import entropy

locations = ['H', 'H', 'W', 'S', 'H']
ent = entropy.entropy_kontoyiannis(locations)
print(ent)
```

```
1.934940079072802
```

Compression-based entropy estimates tend to lower and more robust for longer sequences, so let's create a bigger sequence and compute its entropy:

```python
from predictability import entropy

locations = ['H', 'H', 'W', 'S', 'H'] * 10
ent = entropy.entropy_kontoyiannis(locations)
print(ent)
```

```
0.4679814419382027
```

We can also compute the baseline entropy, as described in our [paper](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00304-8):

```python
from predictability import entropy

# We need longer sequences to obtain a good approximation for
# the baseline entropy using the closed-formula
locations = ['H', 'H', 'W', 'S', 'H'] * 25

# Baseline entropy buiding the sequence and then running
# Kontoyiannis's estimator on it
baseline_ent_konto = entropy.entropy_kontoyiannis(locations)
print(baseline_ent_konto)

# Baseline entropy via closed-formula
baseline_ent = entropy.baseline_entropy(locations)
print(baseline_ent)
```

```
0.226279375151
0.226397045133
```

### Predictability

We can also compute the predictability of an input sequence, using the [technique](https://science.sciencemag.org/content/327/5968/1018) originally proposed by Song _et al._:

```python
from predictability import entropy, pred_lims

locations = ['H', 'H', 'W', 'S', 'H'] * 10
ent = entropy.entropy_kontoyiannis(locations)
n_unique = len(set(locations))
pred = pred_lims.max_predictability(ent, n_unique)
print(pred)
```

```
0.923
```

### Context

The library also allows us to compute predictability taking into account an additional input sequence, describing extra information associated to each symbol in the original sequence. More details can be found in our [paper](https://dl.acm.org/doi/10.1145/3459625) on the subject.

```python
import random
from predictability import context

sequence_size = 100
X = [str(random.randint(0, 10)) for _ in range(sequence_size)]
Y = [str(random.randint(0, 10)) for _ in range(sequence_size)]

# Compute the entropy using the sequence-splitting strategy
seq_split = context.sequence_splitting(X, Y)
print(seq_split)

# Compute the entropy using the sequence-merging strategy
seq_merge = context.sequence_merging(X, Y)
print(seq_merge)
```

```
2.4411207658032263
1.2122442585972815
```

For more details about how to run each function in the library, please take a look at file `tests.py`.


## Citation

If you happen to use this library, we would appreciate if you could cite one of our papers below:


```
@article{Teixeira:2021,
    author = {Teixeira, Douglas Do Couto and Viana, Aline Carneiro and Almeida, Jussara M. and Alvim, Mario S.},
    title = {The Impact of Stationarity, Regularity, and Context on the Predictability of Individual Human Mobility},
    year = {2021},
    issue_date = {June 2021},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    volume = {7},
    number = {4},
    issn = {2374-0353},
    url = {https://doi.org/10.1145/3459625},
    doi = {10.1145/3459625},
    journal = {ACM Trans. Spatial Algorithms Syst.},
    month = jun,
    articleno = {19},
    numpages = {24},
    keywords = {predictability, entropy estimators, Human mobility, contextual information}
}
```

```
@article{Teixeira:2021a,
    author={Teixeira, Douglas do Couto and Almeida, Jussara M. and Viana, Aline Carneiro},
    title={On estimating the predictability of human mobility: the role of routine},
    journal={EPJ Data Science},
    year={2021},
    month={Sep},
    day={29},
    volume={10},
    number={1},
    pages={49},
    issn={2193-1127},
    doi={10.1140/epjds/s13688-021-00304-8},
    url={https://doi.org/10.1140/epjds/s13688-021-00304-8}
}
```

```
@inproceedings{Teixeira:2019,
    author = {Teixeira, Douglas do Couto and Viana, Aline Carneiro and Alvim, M\'{a}rio S. and Almeida, Jussara M.},
    title = {Deciphering Predictability Limits in Human Mobility},
    booktitle = {Proceedings of the 27th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems},
    series = {SIGSPATIAL '19},
    year = {2019},
    isbn = {978-1-4503-6909-1},
    location = {Chicago, IL, USA},
    pages = {52--61},
    numpages = {10},
    url = {http://doi.acm.org/10.1145/3347146.3359093},
    doi = {10.1145/3347146.3359093},
    acmid = {3359093},
    publisher = {ACM},
    address = {New York, NY, USA},
    keywords = {entropy estimators, human mobility, predictability},
} 
```
