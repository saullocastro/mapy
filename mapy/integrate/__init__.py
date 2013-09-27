'''
<:mod:`mapy.integrate`> brings together many convenient algorithms
for numerical integration that are not available in SciPy. More specifically
the integration of vector valued functions.
The aim is to integrate this in SciPy one day...

======================================================
Algorithms for numeric integration <:mod:`mapy.integrate`>
======================================================

.. currentmodule:: mapy.integrate

.. autosummary::
    :toctree: generated/

    trapzv              -- 1-D trapezoidal rule of vector-valued function (vvf)
    polyv               -- 1-D n-th order polynomial integration of vvf
    trapz2d             -- 2-D trapezoidal rule of vvf
    simps2d             -- 2-D simpsons rule of vvf
'''
from integratev import trapzv, polyv
from integratev import _trapz2d as trapz2d
from integratev import _simps2d as simps2d
