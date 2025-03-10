Installation
=============

BooLEVARD is a Python package designed to compute the number of paths leading to node activations or inactivations in Boolean models.

Features
------------------------------
- Import Boolean models in `.bnet` format.
- Compute the number of paths leading to the local states of a list of nodes.
- Perform model perturbations.
- Export back models to `.bnet` format.
    

Instalation from PyPI
------------------------------

To install BooLEVARD from PyPi, install the main package using pip:

.. code-block:: bash

    pip install boolevard


The dependencies can be installed by running the following code:

.. code-block:: bash

    pip install -r https://raw.githubusercontent.com/farinasm/boolevard/main/requirements.txt

Installation with conda
------------------------------

To install BooLEVARD using conda, install the main package using conda:

.. code-block:: bash

    conda install farinasm::boolevard

Installation from source
------------------------------

To install the latest development version, BooLEVARD can also be installed from the source:

.. code-block:: bash

    git clone https://github.com/farinasm/boolevard.git
    cd boolevard
    pip install .
    pip install -r requirements.txt
