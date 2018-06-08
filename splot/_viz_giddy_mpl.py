import seaborn as sns
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import libpysal.api as lp

from ._viz_utils import moran_hot_cold_spots
from ._viz_mpl import lisa_cluster

"""
Lightweight visualizations for pysal dynamics using Matplotlib and Geopandas

TODO
"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def _space_time_heatmap_data(moran_loc1, moran_loc2, p=0.05):
    '''
    Utility function to calculate heatmap table
    '''
    cluster = moran_hot_cold_spots(moran_loc1, p=p)
    cluster2 = moran_hot_cold_spots(moran_loc2, p=p)

    # to put into seaborn function
    # and set diagonal elements to zero to see the rest better
    heatmap_data = np.zeros((5, 5), dtype=int)
    mask = np.zeros((5, 5), dtype=bool)
    for row in range(5):
        for col in range(5):
            yr1 = cluster == row
            yr2 = cluster2 == col
            heatmap_data[row, col] = (yr1 & yr2).sum()
            if row == col:
                mask[row, col] = True
    return heatmap_data, mask

def space_time_heatmap(moran_loc1, moran_loc2, p=0.05, ax=None):
    """
    Heatmap indicting significant transition of LISA values in Moran Scatterplot

    Parameters
    ----------

    Returns
    -------
    """
    heatmap_data, mask = _space_time_heatmap_data(moran_loc1, moran_loc2, p=p)

    # set name for tick labels
    xticklabels = ['ns', 'HH', 'HL', 'LH', 'LL'] 
    yticklabels = ['ns', 'HH', 'HL', 'LH', 'LL']  

    fig, ax = sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu",
                xticklabels=xticklabels, yticklabels=yticklabels,
                mask=mask, center=20, ax=ax, cbar=False, square=True)
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
        Variable to specify colors of the colorbars.
    ax : Matplotlib Axes instance, optional
        If given, the Moran plot will be created inside this axis.
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


def plot_vectors(rose, attribute=None, ax=None):
    """
    Plot vectors of positional transition of LISA values
    in Moran scatterplot for two years

    Parameters
    ----------
    rose : giddy.directional Rose object

    attribute : (n,) ndarray, optional
        Variable to specify colors of the colorbars.
    ax : Matplotlib Axes instance, optional
        If given, the Moran plot will be created inside this axis.
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
    for i in range(len(rose.Y)):
        xs = rose.Y[i,:]
        ys = rose.wY[i,:]
    
    if attribute is None:
        c = ax.plot(xs, ys)
    else:
        c = ax.plot(xs, ys, c=attribute)
        if can_insert_colorbar:
            fig.colorbar(c)
    ax.axis('equal')
    ax.xlim(xlim)
    ax.ylim(ylim)
    return fig, ax

def space_time_correl(gdf, timex, timey,
                      p=0.05, figsize=(13,10)):
    
    #prepare data for plotting:
    import libpysal as lp
    import esda
    w = lp.Queen.from_dataframe(gdf)
    w.transform = 'r'
    y1 = gdf[timex].values
    y2 = gdf[timey].values
    
    # Moran_Local uses random numbers, which we cannot change between the two years!
    old_state = np.random.get_state()
    moran_loc1 = esda.moran.Moran_Local(y1, w)
    np.random.set_state(old_state)
    moran_loc2 = esda.moran.Moran_Local(y2, w)
    np.random.set_state(old_state)

    fig = plt.figure(figsize=figsize)
    fig.suptitle('Space-time autocorrelation', fontsize=20)
    axs = []
    axs.append(plt.subplot(221))
    axs.append(plt.subplot(222))
    axs.append(plt.subplot(223, projection='polar'))
    axs.append(plt.subplot(224))
    
    # space_time_heatmap
    fig = space_time_heatmap(moran_loc1, moran_loc2, p=p, ax=axs[0])
    fig.xaxis.set_ticks_position('top')
    fig.set_xlabel(timex)
    fig.xaxis.set_label_position('top')
    fig.set_ylabel(timey)

    # Lisa_clusters
    lisa_cluster(moran_loc1, gdf, p=p, ax=axs[1], legend=True,
                 legend_kwds={'loc': 'upper left',
                 'bbox_to_anchor': (0.92, 1.05)})
    lisa_cluster(moran_loc2, gdf, p=p, ax=axs[3], legend=True,
                 legend_kwds={'loc': 'upper left',
                 'bbox_to_anchor': (0.92, 1.05)})

    # Rose diagram: Moran movement vectors:
    Y = np.array([y1, y2]).T
    print(Y.shape)

    rose = Rose(Y, w, k=5)
    rose.plot(ax=axs[2])
    return fig, ax