# BooLEVARD

<a href="[Logo](https://github.com/farinasm/boolevard/blob/main/docs/Logo.svg)">
    <img src="https://github.com/farinasm/boolevard/blob/main/docs/Logo.svg" alt="Logo" width="250">
</a>

[![PyPI version](https://img.shields.io/pypi/v/boolevard)](https://pypi.org/project/boolevard/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/farinasm/boolevard/blob/main/LICENSE/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://github.com/farinasm/boolevard/)

BooLEVARD is a Python package designed to compute the number of paths leading to node activations or inactivations in Boolean models.

## Features

- Import Boolean models in `.bnet` format.
- Compute the number of paths leading to the local states of a list of nodes.
- Perform model perturbations.
- Export back models to `.bnet` format.

## Instalation from PyPI:

To install BooLEVARD from PyPi, install the main package using pip:

```bash
pip install boolevard
```

The dependencies can be installed by running the following code:

```bash
pip install -r https://raw.githubusercontent.com/farinasm/boolevard/main/requirements.txt
```

## Installation from source

To install the latest development version, BooLEVARD can also be installed from the source:

```bash
git clone https://github.com/farinasm/boolevard.git
cd boolevard
pip install .
pip install -r requirements.txt
```

## Installation with conda

To install BooLEVARD using conda, install the main package using conda:

```bash
conda install farinasm::boolevard
```

## Documentation and Tutorials

For full BooLEVARD documentaiton visit our [GitHub Documentation](https://farinasm.github.io/boolevard) page.

BooLEVARD tutorials can be found [here](https://github.com/farinasm/boolevard/tree/main/tutorials).

## Citing BooLEVARD and Contributors

*Fariñas, M et al. (2025): BooLEVARD: Boolean Logical Evaluation of Activation and Repression in Directed pathways. [DOI: 10.1101/2025.03.24.644921](https://doi.org/10.1101/2025.03.24.644921)*

**Contributors:** Marco Fariñas, Eirini Tsirvouli, John Zobolas, Tero Aittokallio, Åsmund Flobak, Kaisa Lehti.

**Contact:** Marco Fariñas - farinasm.git@gmail.com
