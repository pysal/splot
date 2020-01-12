.. Installation

Installation
============

Installing dependencies
-----------------------

`splot` is compatible with Python `3.6`_ and `3.7`_ and
depends on GeoPandas 0.4.0 or later and matplotlib 2.2.2 or later.
Please make sure that you are operating in a Python 3 environment.

splot also uses

* numpy
* seaborn
* mapclassify
* Ipywidgets

Depending on your spatial analysis workflow and the PySAL objects
you would like to visualize, splot relies on:

PySAL >=2.0

or the installation of separate packages found in the PySAL stack:

* esda
* libpysal
* spreg
* giddy


Installing the newest release
-----------------------------

There are two ways of accessing splot. First, splot is installed with
the PySAL 2.0 metapackage through:

```$ pip install -U pysal```

or 

```$ conda install -c conda-forge pysal```

Second, splot can be installed as a separate package. If you are
using Anaconda, install splot via the conda utility:

```$ conda install -c conda-forge splot```

Otherwise, you can install splot from PyPI with pip:

```$ pip install splot```


Troubleshooting
---------------
Most common installation errors are due to splot's dependency on GeoPandas.

It often helps to first install GeoPandas separately from conda-forge with:

```$ conda install --channel conda-forge geopandas```

before installing splot (preferably also from conda, alternatively from pip).

For more information on troubleshooting the installation of GeoPandas with pip, see the `GeoPandas`_ docuemntation.

It is also possible to install splot with a later Python version (>3.7)
through the separate installation of GeoPandas or through installation wiht conda-forge.
(Note that splot is currently oonly tested for Python version 3.6 and 3.7)


Installing the development version
----------------------------------

Potentially, you might want to use the newest features in the development
version of splot on github - `pysal/splot`_ while have not been incorporated
in the Pypi released version. You can achieve that by installing `pysal/splot`_
by running the following from a command shell::

  pip install git+https://github.com/pysal/splot.git

You can  also `fork`_ the `pysal/splot`_ repo and create a local clone of
your fork. By making changes
to your local clone and submitting a pull request to `pysal/splot`_, you can
contribute to the splot development.

.. _3.6: https://docs.python.org/3.6/
.. _3.7: https://docs.python.org/3.7/
.. _GeoPandas: http://geopandas.org/install.html
.. _pysal/splot: https://github.com/pysal/splot
.. _fork: https://help.github.com/articles/fork-a-repo/

