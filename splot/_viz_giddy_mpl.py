import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import esda

from ._viz_utils import moran_hot_cold_spots
from ._viz_mpl import lisa_cluster

"""
Lightweight visualizations for pysal dynamics using Matplotlib and Geopandas

TODO
implement **kwgs
"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def _dynamic_lisa_heatmap_data(moran_locy, moran_locx, p=0.05):
    '''
    Utility function to calculate dynamic lisa heatmap table
    and diagonal color mask
    '''
    clustery = moran_hot_cold_spots(moran_locy, p=p)
    clusterx = moran_hot_cold_spots(moran_locx, p=p)

    # to put into seaborn function
    # and set diagonal elements to zero to see the rest better
    heatmap_data = np.zeros((5, 5), dtype=int)
    mask = np.zeros((5, 5), dtype=bool)
    for row in range(5):
        for col in range(5):
            yr1 = clustery == row
            yr2 = clusterx == col
            heatmap_data[row, col] = (yr1 & yr2).sum()
            if row == col:
                mask[row, col] = True
    return heatmap_data, mask

def _moran_loc_from_rose_calc(rose):
    """
    Calculate esda.moran.Moran_Local values from giddy.rose object
    """
    old_state = np.random.get_state()
    moran_locy = esda.moran.Moran_Local(rose.Y[:, 0], rose.w)
    np.random.set_state(old_state)
    moran_locx = esda.moran.Moran_Local(rose.Y[:, 1], rose.w)
    np.random.set_state(old_state)
    return moran_locy, moran_locx

def dynamic_lisa_heatmap(rose, p=0.05, ax=None):
    """
    Heatmap indicating significant transition of LISA values
    over time in Moran Scatterplot

    Parameters
    ----------
    rose : giddy.directional.Rose instance
        A ``Rose`` object, which contains (among other attributes) LISA
        values at two time points, and a method to perform inference on those.
    p : float, optional
        The p-value threshold for significance. Default =0.05
    ax : Matplotlib Axes instance, optional
        If given, the figure will be created inside this axis.
        Default =None.

    Returns
    -------
    fig : Matplotlib Figure instance
        Moran scatterplot figure
    ax : matplotlib Axes instance
        Axes in which the figure is plotted
    """
    moran_locy, moran_locx = _moran_loc_from_rose_calc(rose)
    fig, ax = _dynamic_lisa_heatmap(moran_locy, moran_locx, p=p, ax=ax)
    return fig, ax
    
def _dynamic_lisa_heatmap(moran_locy, moran_locx, p, ax):
    """
    Create dynaimc_lisa_heatmap figure from esda.moran.Moran_local values
    """
    heatmap_data, mask = _dynamic_lisa_heatmap_data(moran_locy, moran_locx, p=p)

    # set name for tick labels
    xticklabels = ['ns', 'HH', 'HL', 'LH', 'LL'] 
    yticklabels = ['ns', 'HH', 'HL', 'LH', 'LL']  

    ax = sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu",
                xticklabels=xticklabels, yticklabels=yticklabels,
                mask=mask, center=20, ax=ax, cbar=False, square=True)
    fig = ax.get_figure()
    return fig, ax


def dynamic_lisa_rose(rose, attribute=None, ax=None):
    """
    Plot the rose diagram.

    Parameters
    ----------
    rose : giddy.directional.Rose instance
        A ``Rose`` object, which contains (among other attributes) LISA
        values at two time points, and a method to perform inference on those.
    attribute : (n,) ndarray, optional
        Points will be colored by attribute values.
        Variable to specify colors of the colorbars. Default =None
    ax : Matplotlib Axes instance, optional
        If given, the figure will be created inside this axis.
        Default =None. Note, this axis should have a polar projection.

    Returns
    -------
    fig : Matplotlib Figure instance
        Moran scatterplot figure
    ax : matplotlib Axes instance
        Axes in which the figure is plotted
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        can_insert_colorbar = True
    else:
        fig = ax.get_figure()
        can_insert_colorbar = False

    ax.set_rlabel_position(315)

    if attribute is None:
        c = ax.scatter(rose.theta, rose.r)
    else:
        c = ax.scatter(rose.theta, rose.r, c=attribute)
        if can_insert_colorbar:
            fig.colorbar(c)
    return fig, ax


def _add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()
    line.axes.annotate('', xytext=(xdata[0], ydata[0]),
                       xy=(xdata[1], ydata[1]),
                       arrowprops=dict(arrowstyle="->", color=color),
                       size=size)

def dynamic_lisa_vectors(rose, attribute=None, ax=None, arrows=True): #TODO: fix coloring by attribute
    """
    Plot vectors of positional transition of LISA values
    in Moran scatterplot

    Parameters
    ----------
    rose : giddy.directional.Rose instance
        A ``Rose`` object, which contains (among other attributes) LISA
        values at two time points, and a method to perform inference on those.
    attribute : (n,) ndarray, optional
        Points will be colored by attribute values.
        Variable to specify colors of the colorbars. Default =None
    ax : Matplotlib Axes instance, optional
        If given, the figure will be created inside this axis.
        Default =None.

    Returns
    -------
    fig : Matplotlib Figure instance
        Moran scatterplot figure
    ax : matplotlib Axes instance
        Axes in which the figure is plotted
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        can_insert_colorbar = True
    else:
        fig = ax.get_figure()
        can_insert_colorbar = False

    xlim = [rose.Y.min(), rose.Y.max()]
    ylim = [rose.wY.min(), rose.wY.max()]
 
    if attribute is None:
        attribute = 'b'
        can_insert_colorbar = False
        
    xs = []
    ys = []
    for i in range(len(rose.Y)):
        # Plot a vector from xy_start to xy_end
        xs.append(rose.Y[i,:])
        ys.append(rose.wY[i,:])
        
    xs = np.asarray(xs).T
    ys = np.asarray(ys).T
    lines = ax.plot(xs, ys, c=attribute)
    if can_insert_colorbar:
        fig.colorbar(lines)
        
    if arrows:
        for line in lines:
            _add_arrow(line)
        
    ax.axis('equal')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return fig, ax


def dynamic_lisa_composite(rose, gdf,
                      p=0.05, figsize=(13,10)):
    """
    Composite visualization for dynamic LISA values over two points in time.
    Includes dynamic lisa heatmap, dynamic lisa rose plot, and LISA cluster plot
    for both compared points in time.
    
    Parameters
    ----------
    rose : giddy.directional.Rose instance
        A ``Rose`` object, which contains (among other attributes) LISA
        values at two time points, and a method to perform inference on those.
    gdf : geopandas dataframe instance
        The Dataframe containing information and polygons to plot.
    p : float, optional
        The p-value threshold for significance. Default =0.05
    figsize: tuple, optional
        W, h of figure. Default =(13,10)

    Returns
    -------
    fig : Matplotlib Figure instance
        Moran scatterplot figure
    axs : matplotlib Axes instance
        Axes in which the figure is plotted
    """
    # Moran_Local uses random numbers, which we cannot change between the two years!
    moran_locy, moran_locx = _moran_loc_from_rose_calc(rose)
    
    # initialize figure
    fig = plt.figure(figsize=figsize)
    fig.suptitle('Space-time autocorrelation', fontsize=20)
    axs = []
    axs.append(plt.subplot(221))
    axs.append(plt.subplot(222))
    axs.append(plt.subplot(223, projection='polar'))
    axs.append(plt.subplot(224))
    
    # space_time_heatmap
    _dynamic_lisa_heatmap(moran_locy, moran_locx, p=p, ax=axs[0])
    axs[0].xaxis.set_ticks_position('top')
    axs[0].xaxis.set_label_position('top')

    # Lisa_cluster maps
    lisa_cluster(moran_locy, gdf, p=p, ax=axs[1], legend=True,
                 legend_kwds={'loc': 'upper left',
                 'bbox_to_anchor': (0.92, 1.05)})
    lisa_cluster(moran_locx, gdf, p=p, ax=axs[3], legend=True,
                 legend_kwds={'loc': 'upper left',
                 'bbox_to_anchor': (0.92, 1.05)})

    # Rose diagram: Moran movement vectors:
    dynamic_lisa_rose(rose, ax=axs[2])
    return fig, axs