# Estimating Predictability in Human Mobility

This repository contains a library that computes several metrics related to individual human mobility. 


## Usage

First, clone the repository by running:

```
git clone https://github.com/dougct/predictability.git
```

To import the library, type `import predictability` from outside the `predictability` directory.

To run the unit tests, type `python -m pytest tests.py` from inside the `predictability` directory.


## Examples

The examples below show how to use several functions in the library.

### Metrics

```python
import predictability

locations = ['H', 'H', 'W', 'S', 'H']
reg = predictability.regularity(locations)
print(reg)
```

```
0.4
```

```python
import predictability

locations = ['H', 'H', 'W', 'S', 'H']
st = predictability.stationarity(locations)
print(st)
```

```
0.25
```

```python
import predictability

locations = ['H', 'H', 'W', 'S', 'H']
div = predictability.diversity(locations)
print(div)
```

```
0.8666666666666667
```

### Entropy


```python
import predictability

locations = ['H', 'H', 'W', 'S', 'H']
ent = predictability.unc_entropy(locations)
print(ent)
```

```
1.3709505944546687
```


```python
import predictability

locations = ['H', 'H', 'W', 'S', 'H']
ent = predictability.entropy_kontoyiannis(locations)
print(ent)
```

```
1.934940079072802
```


```python
import predictability

locations = ['H', 'H', 'W', 'S', 'H'] * 10
ent = predictability.entropy_kontoyiannis(locations)
print(ent)
```

```
0.4679814419382027
```


### Predictability

```python
import predictability

locations = ['H', 'H', 'W', 'S', 'H'] * 10
ent = predictability.entropy_kontoyiannis(locations)
n = len(set(locations))
pred = predictability.max_predictability(ent, n)
print(pred)
```

```
0.923
```

### Context

```python
import random
import predictability

sequence_size = 100
X = [str(random.randint(0, 10)) for _ in range(sequence_size)]
Y = [str(random.randint(0, 10)) for _ in range(sequence_size)]

# Computes the entropy using the sequence-splitting strategy
seq_split = predictability.sequence_splitting(X, Y)
print(seq_split)

# Computes the entropy using the sequence-merging strategy
seq_merge = predictability.sequence_merging(X, Y)
print(seq_merge)
```

```
2.4411207658032263
1.2122442585972815
```

For more details about how to run each function in the library, please take a look at file `tests.py`.


## Citation

If you happen to use this library, we would appreciate if you could cite one of our papers below, which build upon [Song et al.'s work](https://science.sciencemag.org/content/327/5968/1018) on predictability in human mobility.


```
@article{Teixeira:2021,
    author = {Teixeira, Douglas Do Couto and Viana, Aline Carneiro and Almeida, Jussara M. and Alvim, Mrio S.},
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


