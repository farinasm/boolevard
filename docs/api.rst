API Reference
=============

This page contains the API reference for the Neko package. Boolevard can be imported as follows:

.. code-block:: python
    import boolevard as blv

Loading an object of BooLEV class
-------------

BooLEVARD uses objects of ``BooLEV`` class, generated from Boolean models in ``.bnet`` format. A ``BooLEV`` object is generated using the ``Load`` function:

.. autofunction:: boolevard.io.Load
    :no-index:

Using BooLEV objects
-------------

BooLEVARD's main feature is to count the number of paths leading to the activation or inactivation of a given node within a given stable state or across the stable states reached by a Boolean model stored in an object of ``BooLEV`` class. This can be achieved by calling ``CountPaths``, one of the methods integrated in ``BooLEV`` objects, which together with ``Drivers`` and ``Pert`` methods, will be introduced in the following sections.

.. automethod:: boolevard.io.BooLEV.CountPaths

The disjunctive normal function (cDNF) of a Boolean expression can be seen as the expression of the potential paths a node has get activated (cDNF) or inactivated (cNDNF). This is stable-state-specific and can be computed using the ``Drivers`` method.

.. automethod:: boolevard.io.BooLEV.Drivers


.. automethod:: boolevard.io.BooLEV.Pert
