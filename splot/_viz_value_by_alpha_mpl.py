import matplotlib.pyplot as plt
from matplotlib import colors
import collections
import matplotlib.cm as cm
from pysal.esda.mapclassify import (Box_Plot, Equal_Interval,
                                    Fisher_Jenks, HeadTail_Breaks,
                                    Jenks_Caspall_Forced, Max_P_Classifier,
                                    Maximum_Breaks, Natural_Breaks,
                                    Quantiles, Percentiles, Std_Mean,
                                    User_Defined)

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
        Creates a divergent alpha array with high values
        at the extremes and low, transparent values
        in the middle of the input values.
    
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
        Creates a divergent alpha array with high values at
        the extremes and low, transparent values in the
        middle of the input values.
    alpha_mapclassify : dict
        Keywords used for binning input values and
        classifying alpha values with `mapclassify`.
        Note: valid keywords are eg. dict(classifier='quantiles', k=5,
        hinge=1.5). For other options check `splot.mapping.mapclassify_bin`.
    rgb_mapclassify : dict
        Keywords used for binning input values and
        classifying rgb values with `mapclassify`.
        Note: valid keywords are eg.g dict(classifier='quantiles', k=5,
        hinge=1.5).For other options check `splot.mapping.mapclassify_bin`.
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
        rgb_mapclassify.setdefault('multiples', [-2,-1,1,2])
        rgb_mapclassify.setdefault('mindiff', 0)
        rgb_mapclassify.setdefault('initial', 100)
        rgb_mapclassify.setdefault('bins', [20, max(x)])
        classifier = rgb_mapclassify['classifier']
        k = rgb_mapclassify['k']
        hinge = rgb_mapclassify['hinge']
        multiples = rgb_mapclassify['multiples']
        mindiff = rgb_mapclassify['mindiff']
        initial = rgb_mapclassify['initial']
        bins = rgb_mapclassify['bins']
        rgb_bins = mapclassify_bin(x, classifier, k, hinge,
                                   multiples, mindiff, initial, bins)
        x = rgb_bins.yb

    if alpha_mapclassify is not None:
        alpha_mapclassify.setdefault('k', 5)
        alpha_mapclassify.setdefault('hinge', 1.5)
        alpha_mapclassify.setdefault('multiples', [-2,-1,1,2])
        alpha_mapclassify.setdefault('mindiff', 0)
        alpha_mapclassify.setdefault('initial', 100)
        alpha_mapclassify.setdefault('bins', [20, max(y)])
        classifier = alpha_mapclassify['classifier']
        k = alpha_mapclassify['k']
        hinge = alpha_mapclassify['hinge']
        multiples = alpha_mapclassify['multiples']
        mindiff = alpha_mapclassify['mindiff']
        initial = alpha_mapclassify['initial']
        bins = alpha_mapclassify['bins']
        alpha_bins = mapclassify_bin(y, classifier,
                                     k, hinge, multiples, mindiff,
                                     initial, bins)
        y = alpha_bins.yb

    rgba = value_by_alpha_cmap(x=x, y=y, cmap=cmap,
                               divergent=divergent)
    
    gdf.plot(color=rgba, ax=ax)
    return fig, ax


def mapclassify_bin(y, classifier, k=5, pct=[1,10,50,90,99,100],
                    hinge=1.5, multiples=[-2,-1,1,2], mindiff=0,
                    initial=100, bins=None):
    """
    
    Parameters
    ----------
    y : array
        (n,1), values to classify
    classifier : str
        pysal.mapclassify classification scheme
    k : int, optional
        The number of classes. Default=5.
    pct  : array, optional
        Percentiles used for classification with `percentiles`.
        Default=[1,10,50,90,99,100]
    hinge : float, optional
        Multiplier for IQR when `Box_Plot` classifier used.
        Default=1.5.
    multiples : array, optional
        The multiples of the standard deviation to add/subtract from
        the sample mean to define the bins using `std_mean`.
        Default=[-2,-1,1,2].
    mindiff : float, optional
        The minimum difference between class breaks
        if using `maximum_breaks` classifier. Deafult =0.
    initial : int
        Number of initial solutions to generate or number of runs
        when using `natural_breaks` or `max_p_classifier`.
        Default =100.
        Note: setting initial to 0 will result in the quickest
        calculation of bins.
    bins : array, optional
        (k,1), upper bounds of classes (have to be monotically  
        increasing) if using `user_defined` classifier.
        Default =None, Example =[20, max(y)].

    
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
    schemes['box_plot'] = Box_Plot
    schemes['equal_interval'] = Equal_Interval
    schemes['fisher_jenks'] = Fisher_Jenks
    schemes['headtail_breaks'] = HeadTail_Breaks
    schemes['jenks_caspall'] = Jenks_Caspall_Forced
    schemes['max_p_classifier'] = Max_P_Classifier
    schemes['maximum_breaks'] = Maximum_Breaks
    schemes['natural_breaks'] = Natural_Breaks
    schemes['quantiles'] = Quantiles
    schemes['percentiles'] = Percentiles
    schemes['std_mean'] = Std_Mean
    schemes['user_defined'] = User_Defined
    classifier = classifier.lower()
    if classifier not in schemes:
        raise ValueError("Invalid scheme. Scheme must be in the"
                         " set: %r" % schemes.keys())
    if classifier == 'box_plot':
        bins = schemes[classifier](y, hinge)
    if classifier == 'headtail_breaks':
        bins = schemes[classifier](y)
    if classifier == 'percentiles':
        bins = schemes[classifier](y, pct)
    if classifier == 'std_mean':
        bins = schemes[classifier](y, multiples)
    if classifier == 'maximum_breaks':
        bins = schemes[classifier](y, k, mindiff)
    if classifier in ['natural_breaks', 'max_p_classifier']:
        bins = schemes[classifier](y, k, initial)
    if classifier == 'user_defined':
        bins = schemes[classifier](y, bins)
    else:
        bins = schemes[classifier](y, k)
    return bins