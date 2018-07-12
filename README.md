# splot
=======

The goal of this project is to design and implement a visualization module in PySAL, the splot package. This will meet the growing demand for a simple to use, lightweight interface that connects PySAL to different popular visualization toolkits. The splot package will ultimately provide the users with both static plots ready for publication and interactive visualizations that allow for quick iteration and data exploration. In a first phase we will therefore create different visualizations in both a static version with Matplotlib and an interactive version with Bokeh. We will then create a common API for easy access to both versions. After adding documentation we will be able to provide a complete and user friendly package. Finally, we will explore how alternative visualization packages, like Vega, could be integrated into the splot package in future.

TODO: intro

## Installation

### Dependencies

scikit-learn requires:

Python (>= 2.7 or >= 3.4)
NumPy (>= 1.8.2)
SciPy (>= 0.13.3)
For running the examples Matplotlib >= 1.3.1 is required. A few examples require scikit-image >= 0.9.3 and a few examples require pandas >= 0.13.1.

scikit-learn also uses CBLAS, the C interface to the Basic Linear Algebra Subprograms library. scikit-learn comes with a reference implementation, but the system CBLAS will be detected by the build system and used if present. CBLAS exists in many implementations; see Linear algebra libraries for known issues.
splot requires:

* Python (>= 3.5)
* numpy 
* geopandas (>= 0.4.0)
* seaborn
* mapclassify
* esda
* libpysal

**Optional dependencies depending on analysis to visualize:**
* spreg
* giddy
* Ipywidgets




### User installation


## Development

## Help and Support

### Documentation


### Communication
