""" 
Utility functions for lightweight visualizations in splot

TODO fix coloring order"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")

import numpy as np
import mapclassify.api as classify

def mask_local_auto(moran_loc, df=None, p=0.5):
    '''
    Create Mask for coloration and labeling of local spatial autocorrelation
    
    Parameters
    ----------
    moran_loc : esda.moran.Moran_Local instance
        values of Moran's I Global Autocorrelation Statistic
    df : geopandas dataframe instance, optional
        If given, assign df['labels'] per row.  Note that `df` will be
        modified, so calling functions should use a copy of the user
        provided `df`.
    p : float
        The p-value threshold for significance. Points will
        be colored by significance.
    
    Returns
    -------
    cluster_labels : list of str
        List of labels - ['ns', 'HH', 'LH', 'LL', 'HL']
    colors5 : list of str
        List of colours - ['lightgrey', 'red', 'lightskyblue', 'mediumblue', 'pink']
    colors : array of str
        Array containing coloration for each input value/ shape.
    labels : list of str
        List of label for each attribute value/ polygon.
    '''
    # create a mask for local spatial autocorrelation
    sig = 1 * (moran_loc.p_sim < p)
    HH = 1 * (sig * moran_loc.q==1)
    LL = 3 * (sig * moran_loc.q==3)
    LH = 2 * (sig * moran_loc.q==2)
    HL = 4 * (sig * moran_loc.q==4)

    cluster = HH + LL + LH + HL
    cluster_labels = ['ns', 'HH', 'LH', 'LL', 'HL']
    labels = [cluster_labels[i] for i in cluster]
    # create a new column with label info
    if df is not None:
        df['labels_lisa'] = np.array(labels)

    colors5 = {0: 'lightgrey',
               1: 'red',
               2: 'lightblue',
               3: 'blue',
               4: 'pink'}
    colors = [colors5[i] for i in cluster]  # for Bokeh
    # for MPL:
    colors5 = (['red', 'pink', 'lightblue', 'blue', 'lightgrey'])

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

    # Create bin labels
    bin_edges = [attribute_values.min()] + bins.tolist()  # for use in legend
    bin_labels = []
    for i in range(k):
        bin_labels.append('{:1.1f}-{:1.1f}'.format(bin_edges[i], bin_edges[i+1]))
        
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
    # add labels to figure (workaround, legend with geojsondatasource doesn't work,
    # see https://github.com/bokeh/bokeh/issues/5904)
    for label, color in zip(labels, colors):
        fig.patches(xs=[], ys=[], fill_color=color, legend=label)