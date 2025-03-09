API Reference
=============

This page contains the API reference for the Neko package.

BooLEV Class

-------------

BooLEVARD uses objects of ``BooLEV`` class, generated from Boolean models in ``.bnet`` format. A ``BooLEV`` object is generated as follows:

.. code-block:: python

    import boolevard as blv

    model = blv.Load("PATH STORING THE MODEL")

``BooLEV``objects include the following attributes:


``BooLEV`` objects integrate the following methods:

.. autofunction:: boolevard.io.Load
