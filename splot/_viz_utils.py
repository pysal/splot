import numpy as np
import mapclassify.api as classify
from bokeh.models import Legend

"""
Utility functions for lightweight visualizations in splot
"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def mask_local_auto(moran_loc, p=0.5):
    '''
    Create Mask for coloration and labeling of local spatial autocorrelation

    Parameters
    ----------
    moran_loc : esda.moran.Moran_Local instance
        values of Moran's I Global Autocorrelation Statistic
    p : float
        The p-value threshold for significance. Points will
        be colored by significance.

    Returns
    -------
    cluster_labels : list of str
        List of labels - ['ns', 'HH', 'LH', 'LL', 'HL']
    colors5 : list of str
        List of colours - ['lightgrey', 'red', 'lightblue','blue', 'pink']
    colors : array of str
        Array containing coloration for each input value/ shape.
    labels : list of str
        List of label for each attribute value/ polygon.
    '''
    # create a mask for local spatial autocorrelation
    sig = 1 * (moran_loc.p_sim < p)
    HH = 1 * (sig * moran_loc.q == 1)
    LL = 3 * (sig * moran_loc.q == 3)
    LH = 2 * (sig * moran_loc.q == 2)
    HL = 4 * (sig * moran_loc.q == 4)

    cluster = HH + LL + LH + HL
    cluster_labels = ['ns', 'HH', 'LH', 'LL', 'HL']
    labels = [cluster_labels[i] for i in cluster]

    colors5 = {0: 'lightgrey',
               1: '#d7191c',
               2: '#abd9e9',
               3: '#2c7bb6',
               4: '#fdae61'}
    colors = [colors5[i] for i in cluster]  # for Bokeh
    # for MPL:
    colors5 = (['#d7191c', '#fdae61', '#abd9e9', '#2c7bb6', 'lightgrey'])

    # HACK need this, because MPL sorts these labels while Bokeh does not
    cluster_labels.sort()
    return cluster_labels, colors5, colors, labels


def bin_values_choropleth(attribute_values, method='quantiles',
                          k=5):
    '''
    Create bins based on different classification methods.
    Needed for legend labels and Choropleth coloring.

    Parameters
    ----------
    attribute_values : array or geopandas.series instance
        Array containing relevant attribute values.
    method : str
        Classification method to be used. Options supported:
        * 'quantiles' (default)
        * 'fisher-jenks'
        * 'equal-interval'
    k : int
        Number of bins, assigning values to. Default k=5

    Returns
    -------
    bin_values : mapclassify instance
        Object containing bin ids for each observation (.yb),
        upper bounds of each class (.bins), number of classes (.k)
        and number of onservations falling in each class (.counts)
    '''
    classifiers = {
        'quantiles': classify.Quantiles,
        'fisher-jenks': classify.Fisher_Jenks,
        'equal-interval': classify.Equal_Interval
    }

    bin_values = classifiers[method](attribute_values, k)
    return bin_values


def bin_labels_choropleth(df, attribute_values, method='quantiles', k=5):
    '''
    Create labels for each bin in the legend

    Parameters
    ----------
    df : Geopandas dataframe
        Dataframe containign relevant shapes and attribute values.
    attribute_values : array or geopandas.series instance
        Array containing relevant attribute values.
    method : str, optional
        Classification method to be used. Options supported:
        * 'quantiles' (default)
        * 'fisher-jenks'
        * 'equal-interval'
    k : int, optional
        Number of bins, assigning values to. Default k=5

    Returns
    -------
    bin_labels : list of str
        List of label for each bin.
    '''
    # Retrieve bin values from bin_values_choropleth()
    bin_values = bin_values_choropleth(attribute_values, method=method, k=k)

    # Extract bin ids (.yb) and upper bounds for each class (.bins)
    yb = bin_values.yb
    bins = bin_values.bins

    # Create bin labels (smaller version)
    bin_edges = bins.tolist()
    bin_labels = []
    for i in range(k):
        bin_labels.append('<{:1.1f}'.format(bin_edges[i]))

    # Add labels (which are the labels printed in the legend) to each row of df
    labels = np.array([bin_labels[c] for c in yb])
    df['labels_choro'] = [str(l) for l in labels]
    return bin_labels


def add_legend(fig, labels, colors):
    """
    Add a legend to a figure given legend labels & colors.

    Parameters
    ----------
    fig : Bokeh Figure instance
        Figure instance labels should be generated for.
    labels : list of str
        Labels to use as legend entries.
    colors : Bokeh Palette instance
        Palette instance containing colours of choice.
    """
    # add labels to figure (workaround,
    # legend with geojsondatasource doesn't work,
    # see https://github.com/bokeh/bokeh/issues/5904)
    items = []
    for label, color in zip(labels, colors):
        patch = fig.patches(xs=[], ys=[], fill_color=color)
        items.append((label, [patch]))

    legend = Legend(items=items, location='top_left', margin=0,
                    orientation='horizontal')
    # possibility to define glyph_width=10, glyph_height=10)
    legend.label_text_font_size = '8pt'
    fig.add_layout(legend, 'below')
    return legend


def calc_data_aspect(plot_height,  plot_width, bounds):
    # Deal with data ranges:
    # make a meter in x and a meter in y the same in pixel lengths
    aspect_box = plot_height / plot_width   # 2 / 1 = 2
    xmin, ymin, xmax, ymax = bounds
    x_range = xmax - xmin  # 1 = 1 - 0
    y_range = ymax - ymin  # 3 = 3 - 0
    aspect_data = y_range / x_range  # 3 / 1 = 3
    if aspect_data > aspect_box:
        # we need to increase x_range,
        # such that aspect_data becomes equal to aspect_box
        halfrange = 0.5 * x_range * (aspect_data / aspect_box - 1)
        # 0.5 * 1 * (3 / 2 - 1) = 0.25
        xmin -= halfrange  # 0 - 0.25 = -0.25
        xmax += halfrange  # 1 + 0.25 = 1.25
    else:
        # we need to increase y_range
        halfrange = 0.5 * y_range * (aspect_box / aspect_data - 1)
        ymin -= halfrange
        ymax += halfrange

    # Add a bit of margin to both x and y
    margin = 0.03
    xmin -= (xmax - xmin) / 2 * margin
    xmax += (xmax - xmin) / 2 * margin
    ymin -= (ymax - ymin) / 2 * margin
    ymax += (ymax - ymin) / 2 * margin
    return xmin, xmax, ymin, ymax
