mapy (modeling-analysis-python)
====
Tool to integrate different pre-processor platforms (Abaqus, NASTRAN, SimXpert).
The models can be loaded in the Python environment and passed from one
platform to another.

Composite
---------
A lot of effort has been done in the composite module in order to provide
efficient and convenient means to calculate the stiffness matrix ABD of
a laminated composite structure.

SymPy utils
-----------
The highlight is the differential operator useful to represent and evaluate
strain-displacement matrices (kinematic relations).

Structural analysis
-------------------
More implementation effort has been applied on structural analysis,
but it can be improved for any finite element modeling purpose.

Already developed
-----------------
- capability to read NASTRAN cards
- multiple coordinate systems capability 
- a simple solver for truss elements (RODs)
- differential operator in SymPy to help on semi-analytical tools

Under development 
-----------------
- capability to interface (read/write) thourgh ABAQUS API 
- fitting cloud of measured points to a given shape function

To be developed
---------------
- a fixed object id for all grids, elements,
points etc which will keep all references

even if the user changes the entities' ids. Currently there is a lot of search based on python dictionaries by the entity id

- capability to write NASTRAN cards 
- capability to write ABAQUS cards 
- capability to interface with SimXpert? API (read/write) 
- finite element solver for linear analysis (rods, beams, plates and solids)
OBS: requires numpy, scipy. The project alg3dpy(Google code) is part of this project.

Requires
--------
- numpy
- alg3dpy (https://code.google.com/p/alg3dpy/)

Important
---------
- while the fixed object id for grids, elements etc is not implemented,
BE CAREFUL when renumbering any entity in the model, since it may loose
proper reference to the object

License
-------
Distrubuted in the 2-Clause BSD license (https://raw.github.com/saullocastro/mapy/master/LICENSE).

Contact: saullogiovani@gmail.com

