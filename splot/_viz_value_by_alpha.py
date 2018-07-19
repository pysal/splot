import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib
import collections
import matplotlib.cm as cm

"""
Creating Value by Alpha maps

"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def value_by_alpha_cmap(x, y, cmap='GnBu'):
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
    
    Returns
    -------
    rgba : ndarray (n,4)
        RGBA colormap, where the alpha channel represents one
        attribute (x) and the rgb color the other attribute (y)
    """
    # option for cmap or colorlist input
    if isinstance(cmap, collections.Sequence):
        cmap = colors.LinearSegmentedColormap.from_list('cmap', cmap)
    cmap = cm.get_cmap(cmap)
    rgba = cmap(x)
    rgba[:, 3] = y/y.max()
    return rgba


def value_by_alpha_choropleth(x, y, gdf, cmap='GnBu', ax=ax)
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
    ax : matplotlib Axes instance, optional
        Axes in which to plot the figure in multiple Axes layout.
        Default = None
    
    Returns
    -------
    fig : matplotlip Figure instance
        Figure of LISA cluster map
    ax : matplotlib Axes instance
        Axes in which the figure is plotted
    """
    if ax is None:
        figsize = kwargs.pop('figsize', None)
        fig, ax = plt.subplots(1, figsize=figsize)
    else:
        fig = ax.get_figure()
    
    rgba = value_by_alpha_cmap(x=x, y=y, cmap=cmap)
    
    gdf.plot(color=rgba)
    return fig, ax

