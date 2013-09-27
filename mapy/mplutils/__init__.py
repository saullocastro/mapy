'''
<:mod:`mapy.mplutils`> brings together many convenient utilities
developed for common tasks using matplotlib.
The defaults are optimized for scientific publications so that the user
may want to change it in order to achieve the desired result.


======================================================
Matplotlib utils <:mod:`mapy.mplutils`>
======================================================

.. currentmodule:: mapy.mplutils

.. autosummary::
    :toctree: generated/

    create_fig          -- useful to plot many curves reading from a txt
    savefig             -- save a figure applying nice defaults
'''
from input_from_txt import create_fig
from plot_defaults import save_fig
