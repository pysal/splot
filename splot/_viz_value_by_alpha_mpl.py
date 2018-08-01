import matplotlib.pyplot as plt
from matplotlib import colors
import collections
import matplotlib.cm as cm
from pysal.esda.mapclassify import (Box_Plot,
                                    Quantiles,
                                    Equal_Interval,
                                    Fisher_Jenks)

"""
Creating Value by Alpha maps

"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def value_by_alpha_cmap(x, y, cmap='GnBu', divergent=False):
    """
    Calculates Value by Alpha rgba values
    
    Parameters
    ----------
    x : array
        Variable determined by color
    y : array
        Variable determining alpha value
    cmap : str or list of str
        Matplotlib Colormap or list of colors used
        to create vba_layer
    divergent : bool, optional
        Creates a divergent alpha array with high values at the extremes and
        low, transparent values in the middle of the input values.
    
    Returns
    -------
    rgba : ndarray (n,4)
        RGBA colormap, where the alpha channel represents one
        attribute (x) and the rgb color the other attribute (y)
    """
    # option for cmap or colorlist input
    if isinstance(cmap, str):
        cmap = cm.get_cmap(cmap)
    elif isinstance(cmap, collections.Sequence):
        cmap = colors.LinearSegmentedColormap.from_list('newmap', cmap)
    
    rgba = cmap((x - x.min()) / (x.max() - x.min()))
    rgba[:, 3] = (y - y.min()) / (y.max() - y.min())
    if divergent is not False:
        a_under_0p5 = rgba[:, 3] < 0.5
        rgba[a_under_0p5, 3] = 1 - rgba[a_under_0p5, 3]
        rgba[:, 3] = (rgba[:, 3] - 0.5) * 2
    return rgba


def vba_choropleth(x, y, gdf, cmap='GnBu', divergent=False,
                   alpha_mapclassify=None,
                   rgb_mapclassify=None,
                   ax=None):
    """
    Value by Alpha Choropleth 
    
    Parameters
    ----------
    x : array
        Variable determined by color
    y : array
        Variable determining alpha value
    gdf : geopandas dataframe instance
        The Dataframe containing information to plot.
    cmap : str or list of str
        Matplotlib Colormap or list of colors used
        to create vba_layer
    divergent : bool, optional
        Creates a divergent alpha array with high values at the extremes and
        low, transparent values in the middle of the input values.
    alpha_mapclassify : dict
        Keywords used for binning input values and
        classifying alpha values with `mapclassify`.
        Note: valid keywords are eg.g dict(classifier='quantiles', k=5, hinge=1.5).
    rgb_mapclassify : dict
        Keywords used for binning input values and
        classifying rgb values with `mapclassify`.
        Note: valid keywords are eg.g dict(classifier='quantiles', k=5, hinge=1.5).
    ax : matplotlib Axes instance, optional
        Axes in which to plot the figure in multiple Axes layout.
        Default = None
    
    Returns
    -------
    fig : matplotlip Figure instance
        Figure of LISA cluster map
    ax : matplotlib Axes instance
        Axes in which the figure is plotted
    
    Examples
    --------
    
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()
    
    if rgb_mapclassify is not None:
        rgb_mapclassify.setdefault('k', 5)
        rgb_mapclassify.setdefault('hinge', 1.5)
        classifier = rgb_mapclassify['classifier']
        k = rgb_mapclassify['k']
        hinge = rgb_mapclassify['hinge']
        rgb_bins = mapclassify_bin(x, classifier, k, hinge)
        x = rgb_bins.yb

    if alpha_mapclassify is not None:
        alpha_mapclassify.setdefault('k', 5)
        alpha_mapclassify.setdefault('hinge', 1.5)
        classifier = alpha_mapclassify['classifier']
        k = alpha_mapclassify['k']
        hinge = alpha_mapclassify['hinge']
        alpha_bins = mapclassify_bin(y, classifier,
                                     k, hinge)
        y = alpha_bins.yb

    rgba = value_by_alpha_cmap(x=x, y=y, cmap=cmap,
                               divergent=divergent)
    
    gdf.plot(color=rgba, ax=ax)
    return fig, ax


def mapclassify_bin(y, classifier, k=5, hinge=1.5):
    """
    
    Parameters
    ----------
    y : array
        (n,1), values to classify
    classifier : str
        pysal.mapclassify classification scheme
    k : int, optional
        The number of classes.
    hinge : float, optional
        Multiplier for IQR when `Box_Plot` classifier used.
    
    Returns
    -------
    bins : pysal.mapclassify object
        A mapclassify object with attributes:
        yb (bin id for eachobservation),
        bins (array of upper bounds of each class),
        k (number of classes)
        counts (number of observations in each class)
    """
    schemes = {}
    schemes['equal_interval'] = Equal_Interval
    schemes['quantiles'] = Quantiles
    schemes['fisher_jenks'] = Fisher_Jenks
    schemes['box_plot'] = Box_Plot
    classifier = classifier.lower()
    if classifier not in schemes:
        raise ValueError("Invalid scheme. Scheme must be in the"
                         " set: %r" % schemes.keys())
    if classifier == 'box_plot':
        bins = schemes[classifier](y, hinge)
    else:
        bins = schemes[classifier](y, k)
    return bins