"""
Canned Views using PySAL and Matplotlib
"""

__author__ = "Marynia Kolak <marynia.kolak@gmail.com>"

import pysal as ps
import esda
import matplotlib.pyplot as plt
from matplotlib import colors


__all__ = ['mplot']


def mplot(m, xlabel='', ylabel='', title='', figsize=(7,7), p=None, ax=None,
          alpha=0.6):
    """
    Produce basic Moran Plot 

    Parameters
    ----------
    m : esda.moran.Moran_Local instance
        values of Moran's I Global Autocorrelation Statistic
    xlabel : str
        label for x axis
    ylabel : str
        label for y axis
    title : str
        title of plot
    figsize : tuple
        dimensions of figure size
    p : float
        If given, the p-value threshold for significance.  Points will
        be colored by significance.  By default it will not be colored. 
    ax : Matplotlib Axes instance, optional
        If given, the Moran plot will be created inside this axis.

    Returns
    -------
    fig : Matplotlib Figure instance
        Moran scatterplot figure

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import pysal as ps
    >>> import esda
    >>> from pysal.contrib.pdio import read_files
    >>> from splot.plot import mplot

    >>> link = ps.examples.get_path('columbus.shp')
    >>> db = read_files(link)
    >>> y = db['HOVAL'].values
    >>> w = ps.queen_from_shapefile(link)
    >>> w.transform = 'R'

    >>> m = esda.moran.Moran_Local(y, w)
    >>> mplot(m, xlabel='Response', ylabel='Spatial Lag',
    ...       title='Moran Scatterplot', figsize=(7,7), p=0.05)

    >>> plt.show()
            
    """
    lag = ps.lag_spatial(m.w, m.z)
    fit = ps.spreg.OLS(m.z[:, None], lag[:,None])

    if p is not None:
        if not isinstance(m, esda.moran.Moran_Local):
            raise ValueError("`m` is not a Moran_Local instance")

        sig = 1 * (m.p_sim < p)
        HH = 1 * (sig * m.q==1)
        LL = 3 * (sig * m.q==3)
        LH = 2 * (sig * m.q==2)
        HL = 4 * (sig * m.q==4)
        spots = HH + LL + LH + HL       

        hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])

    # Customize plot
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    ax.spines['left'].set_position(('axes', -0.05))
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position(('axes', -0.05))
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if p is not None:
        ax.scatter(m.z, lag, c=spots, cmap=hmap, s=60, alpha=alpha)
    else:
        ax.scatter(m.z, lag, s=60, color='k', alpha=alpha)

    ax.plot(lag, fit.predy, color='k', alpha=.8)

    ax.axvline(0, alpha=0.5, linestyle='--')
    ax.axhline(0, alpha=0.5, linestyle='--')

    return fig
