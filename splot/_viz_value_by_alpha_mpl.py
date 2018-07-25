import matplotlib.pyplot as plt
from matplotlib import colors
import collections
import matplotlib.cm as cm

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
    rgba = cmap(x)
    rgba[:, 3] = y/y.max()
    if divergent is not False:
        a_under_0p5 = rgba[:, 3] < 0.5
        rgba[a_under_0p5, 3] = 1 - rgba[a_under_0p5, 3]
        rgba[:, 3] = (rgba[:, 3] - 0.5) * 2
    return rgba


def vba_choropleth(x, y, gdf, cmap='GnBu', divergent=False, ax=None):
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
    
    rgba = value_by_alpha_cmap(x=x, y=y, cmap=cmap,
                               divergent=divergent)
    
    gdf.plot(color=rgba, ax=ax)
    return fig, ax


# def choropleth(gdf, x, y=None, cmap=None, classification=None, vba=None, divergent_vba=None, )