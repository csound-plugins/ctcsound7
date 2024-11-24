.. currentmodule:: ctcsound7.api6

Csound API, version 6
=====================

This is valid for versions of csound >= 6.18 and prior to version 7.
The correct API is imported automatically based in the version of
csound installed in the system. Both APIs (for csound 6 and
csound 7) are for the most part compatible. With time it is nevertheless
expected that the API for csound 7 will slowly drift away from the csound 6 version.

In general it can be said that the API has been reduced for csound 7. All methods which have been discontinued in csound 7 are marked in the documentation.

.. autosummary::
    Csound
    CsoundPerformanceThread


----------------------------


.. autoclass:: Csound
    :members:
    :autosummary:

.. autoclass:: CsoundPerformanceThread
    :members:
