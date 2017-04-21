import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSION = "0.15.0"

setup(
    name = "mapy_package",
    version = VERSION,
    author = "Saullo G. P. Castro",
    author_email = "castrosaullo@gmail.com",
    description = ("Modeling and Analysis in Python"),
    license = "BSD",
    keywords = "finite element modeling analysis",
    url = "https://github.com/saullocastro/mapy",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=["alg3dpy"],
)

with open("./mapy/version.py", "wb") as f:
    f.write(b"__version__ = %s\n" % VERSION.encode())

