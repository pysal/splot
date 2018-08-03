import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import patches
import collections
import matplotlib.cm as cm
import mapclassify.api as classify
import numpy as np
from ._viz_utils import _classifiers, format_legend

"""
Creating Value by Alpha maps

TODO:

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
    return rgba, cmap


def vba_choropleth(x, y, gdf, cmap='GnBu', divergent=False,
                   alpha_mapclassify=None,
                   rgb_mapclassify=None,
                   ax=None, legend=False):
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
    legend : bool, optional
        Adds a legend.
        Note: currently only available if data is classified,
        hence if `alpha_mapclassify` and `rgb_mapclassify` are used.
    
    Returns
    -------
    fig : matplotlip Figure instance
        Figure of Value by Alpha choropleth
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

    rgba, vba_cmap = value_by_alpha_cmap(x=x, y=y, cmap=cmap,
                                         divergent=divergent)
    gdf.plot(color=rgba, ax=ax)
    ax.set_axis_off()
    ax.set_aspect('equal')
    
    if legend:
        left, bottom, width, height = [0, 0.5, 0.2, 0.2]
        ax2 = fig.add_axes([left, bottom, width, height])
        vba_legend(alpha_bins, rgb_bins, vba_cmap, ax=ax2)
    return fig, ax


def mapclassify_bin(y, classifier, k=5, pct=[1,10,50,90,99,100],
                    hinge=1.5, multiples=[-2,-1,1,2], mindiff=0,
                    initial=100, bins=None):
    """
    Classify your data with `pysal.mapclassify`
    Note: Input parameters are dependent on classifier used.
    
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
    bins : pysal.mapclassify instance
        Object containing bin ids for each observation (.yb),
        upper bounds of each class (.bins), number of classes (.k)
        and number of onservations falling in each class (.counts)
    """
    classifier = classifier.lower()
    if classifier not in _classifiers:
        raise ValueError("Invalid scheme. Scheme must be in the"
                         " set: %r" % _classifiers.keys())
    if classifier == 'box_plot':
        bins = _classifiers[classifier](y, hinge)
    if classifier == 'headtail_breaks':
        bins = _classifiers[classifier](y)
    if classifier == 'percentiles':
        bins = _classifiers[classifier](y, pct)
    if classifier == 'std_mean':
        bins = _classifiers[classifier](y, multiples)
    if classifier == 'maximum_breaks':
        bins = _classifiers[classifier](y, k, mindiff)
    if classifier in ['natural_breaks', 'max_p_classifier']:
        bins = _classifiers[classifier](y, k, initial)
    if classifier == 'user_defined':
        bins = _classifiers[classifier](y, bins)
    else:
        bins = _classifiers[classifier](y, k)
    return bins


def vba_legend(alpha_bins, rgb_bins, cmap, ax=None):
    """
    Creates Value by Alpha heatmap used as choropleth legend.
    
    Parameters
    ----------
    alpha_bins : pysal.mapclassify instance
        Object of classified values used for alpha.
        Can be created with `mapclassify_bin()`
        or `pysal.mapclassify`.
    rgb_bins : pysal.mapclassify instance
        Object of classified values used for rgb.
        Can be created with `mapclassify_bin()`
        or `pysal.mapclassify`.
    ax : matplotlib Axes instance, optional
        Axes in which to plot the figure in multiple Axes layout.
        Default = None
    
    Returns
    -------
    fig : matplotlip Figure instance
        Figure of Value by Alpha heatmap
    ax : matplotlib Axes instance
        Axes in which the figure is plotted
    
    Examples
    --------
    
    """
    # VALUES
    rgba, legend_cmap = value_by_alpha_cmap(rgb_bins.yb, alpha_bins.yb, cmap=cmap)
    # separate rgb and alpha values
    alpha = rgba[:, 3]
    # extract unique values for alpha and rgb
    alpha_vals = np.unique(alpha)
    rgb_vals = legend_cmap((rgb_bins.bins - rgb_bins.bins.min()) / (
            rgb_bins.bins.max() - rgb_bins.bins.min()))[:, 0:3]
    
    # PLOTTING
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    for irow, alpha_val in enumerate(alpha_vals):
        for icol, rgb_val in enumerate(rgb_vals):
            rect = patches.Rectangle((irow, icol), 1, 1, linewidth=3,
                                     edgecolor='none',
                                     facecolor=rgb_val,
                                     alpha=alpha_val)
            ax.add_patch(rect)

    values_alpha, x_in_thousand = format_legend(alpha_bins.bins)
    values_rgb, y_in_thousand = format_legend(rgb_bins.bins)
    ax.plot([], [])
    ax.set_xlim([0, irow+1])
    ax.set_ylim([0, icol+1])
    ax.set_xticks(np.arange(irow+1) + 0.5)
    ax.set_yticks(np.arange(icol+1) + 0.5)
    ax.set_xticklabels(['< %1.1f' % val for val in values_alpha],
                       rotation=30, horizontalalignment='right')
    ax.set_yticklabels(['$<$%1.1f' % val for val in values_rgb])
    if x_in_thousand:
        ax.set_xlabel('alpha variable ($10^3$)')
    if y_in_thousand:
        ax.set_ylabel('rgb variable ($10^3$)')
    else:
        ax.set_xlabel('alpha variable')
        ax.set_ylabel('rgb variable')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return fig, ax
