# splot
=======

**Leightweight plotting and mapping to facilitate spatial analysis with PySAL.**

## What is splot?

splot connects spatial analysis done in PySAL to different popular visualization toolkits like `matplotlib`.
The splot package allows you to create both static plots ready for publication and interactive visualizations for quick iteration and spatial data exploration. The primary goal of splot is therefore to enable you to visualize popular PySAL objects and gives you different views on your spatial analysis workflow.

If you are new to splot and PySAL you will best get started with our documentation!

## Installing splot

### splot requires: TODO

splot is compatible with Python 3.5 or later and depends on `geopandas` 0.4.0 or later and `matplotlib` 2.2.2 or later.

splot aslo uses
* `numpy`
* `seaborne`
* `mapclassify`
* `Ipywidgets`

Depending on your spatial analysis workflow and the PySAL objects you would like to visualize, splot relies on:
* PySAL 2.0
or separate packages:
* esda
* libpysal
* spreg
* giddy

### Quick install:

There are two main ways of accessing splot. First, the overall library install of PySAL 2.0 includes splot.
PySAL 2.0 is available from PyPI or Anaconda:

    $ pip install pysal
    
    or 
    
    $ conda install -c conda-forge pysal


Second, splot can be installed separately. If you are using Anaconda, install splot via the conda utility:

    $ conda install -c conda-forge pysal


Otherwise you can install splot from PyPI with pip:

    $ pip install splot


## Developing splot

Splot is an open source project within the Python Spatial Analysis Library that is supported by a community of Geographers, visualization lovers, map fans, users and data scientists. As a community we work together to create splot as our own spatial visualization toolkit and will gratefully and humbly accept any contributions and ideas you might bring into this project. 

Feel free to check out our dicussion spaces and add ideas and contributions:
* Idea collection which PySAL objects to support and how new visualizations could look like: 
* Discussion about the splot API:
* Ideas how to integrate other popular visualization toolkits like `Bokeh` or `Altair`

If you have never contributed before or you are just discovering what PySAl and splot have to offer, reading through """Doc-strings""" and correcting our Documentation can be a great way to start. Check for spelling and grammar mistakes or use pep8 and pyflakes to clean our `.py` files. This will allow you to get used to working with git and generally allows you to familiarize yourself with the `splot` and `PySAL` code base.

If you have already used PySAl and splot and you are missing object-specific views for your analysis feel free to add or discuss your ideas to our code-base. Please make sure you include Uni-test, Documentation and Examples or (create an issue so someone else can work together with you). The common `splot` API design discussed here can help you to decide how to best integrate your visualization prototype into `splot`.

Beyond working on documentation and prototyping new visualizations you can always write a bug report or feature request on Github issues. Whether large or small, any contribution makes a big difference and we hope you enjoy beeing part of our community as much as we do!


## Community support

TODO link to gitter,...