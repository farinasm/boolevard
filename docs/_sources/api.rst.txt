API Reference
=============

.. image:: https://img.shields.io/pypi/v/boolevard
    :target: https://pypi.org/project/boolevard/
    :alt: Version

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
    :target: https://github.com/farinasm/boolevard/blob/main/LICENSE/
    :alt: License

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
    :target: https://github.com/farinasm/boolevard/
    :alt: Documentation

This page contains the API reference for the Neko package. Boolevard can be imported as follows:

.. code-block:: python

    import boolevard as blv

Loading an object of BooLEV class
------------------------------------------------------------

BooLEVARD uses objects of ``BooLEV`` class, generated from Boolean models in ``.bnet`` format. A ``BooLEV`` object is generated using the ``Load`` function:

.. autofunction:: boolevard.core.Load
    :no-index:

Using BooLEV objects
------------------------------------------------------------

BooLEVARD's main feature is to count the number of paths leading to the activation or inactivation of a given node within a given stable state or across the stable states reached by a Boolean model stored in an object of ``BooLEV`` class. This can be achieved by calling ``CountPaths``, one of the methods integrated in ``BooLEV`` objects, which together with ``Drivers`` and ``Pert`` methods, will be introduced in the following sections.

.. automethod:: boolevard.core.BooLEV.CountPaths

The disjunctive normal function (cDNF) of a Boolean expression can be seen as the expression of the potential paths a node has get activated (cDNF) or inactivated (cNDNF). This is stable-state-specific and can be computed using the ``Drivers`` method.

.. automethod:: boolevard.core.BooLEV.Drivers

BooLEVARD also allows to perform node perturbations, in which node inhibitions or activations are simulated. Simulations can be either additive or non-additive. In additive perturbations, the regulatory effects of the perturbation are incorporated to the target's Boolean equation. In non-additive perturbations, these regulatory effects substitute the Boolean equation of the target node. Perturbations must be writen with the following structure (case sensitive): `"Node%INH"` (inhibitions), `"Node%ACT"` (activations).

.. automethod:: boolevard.core.BooLEV.Pert

Exporting BooLEV objects
------------------------------------------------------------

``BooLEV`` objects can be exported back to Boolean models calling the ``Export`` method.

.. automethod:: boolevard.core.BooLEV.Export
    :no-index:
