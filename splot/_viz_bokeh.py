""" 
Leightweight interactive visualizations in Bokeh.

TODO: 
fix lisa_cluster_bokeh, 
mplot_bokeh coloring labels 
add Examples"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")

import pysal as ps
import esda
from bokeh.plotting import figure
from bokeh.models import (GeoJSONDataSource,
                          CategoricalColorMapper, Span)
from bokeh.layouts import gridplot

from ._viz_utils import (bin_labels_choropleth, add_legend,
                         mask_local_auto)


def plot_choropleth(df, attribute, title=None, plot_width=500,
                        plot_height=500, method='quantiles',
                        k=5, reverse_colors=False, tools=''):
    '''
    Plot Choropleth colored according to attribute
    
    Parameters
    ----------
    df : Geopandas dataframe
        Dataframe containign relevant shapes and attribute values.
    attribute : str
        Name of column containing attribute values of interest.
    title : str, optional
        Title of map. Default title=None
    plot_width : int, optional
        Width dimension of the figure in screen units/ pixels.
        Default = 500
    plot_height : int, optional
        Height dimension of the figure in screen units/ pixels.
        Default = 500
    method : str, optional
        Classification method to be used. Options supported:
        * 'quantiles' (default)
        * 'fisher-jenks'
        * 'equal-interval'
    k : int, optional
        Number of bins, assigning values to. Default k=5
    reverse_colors: boolean
        Reverses the color palette to show lightest colors for
        lowest values. Default reverse_colors=False
    
    Returns
    -------
    fig : Bokeh Figure instance
        Figure of Choropleth
    '''
    # We're adding columns, do that on a copy rather than on the users' input
    df = df.copy()
    
    # Extract attribute values from df
    attribute_values = df[attribute].values
    
    # Create bin labels with bin_labels_choropleth()
    bin_labels = bin_labels_choropleth(df, attribute_values, method, k)
    
    # Initialize GeoJSONDataSource
    geo_source = GeoJSONDataSource(geojson=df.to_json())
    
    from bokeh import palettes 
    colors = palettes.Blues[k]
    if reverse_colors is True:
        colors.reverse()  # lightest color for lowest values

    # Create figure
    fig = figure(title=title, plot_width=plot_width, plot_height=plot_height, tools=tools)
    fig.patches('xs', 'ys', fill_alpha=0.7, 
              fill_color={'field': 'labels',
                          'transform': CategoricalColorMapper(palette=colors,
                                                              factors=bin_labels)},
              line_color='white', line_width=0.5, source=geo_source)
    
    # add legend with add_legend()
    add_legend(fig, bin_labels, colors)
    
    # change layout
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.axis.visible = None
    return fig


def lisa_cluster(moran_loc, df, p=0.05, title=None, plot_width=500,
                     plot_height=500, tools=''): 
    '''
    Lisa Cluster map, coloured by local spatial autocorrelation
    
    Parameters
    ----------
    moran_loc : esda.moran.Moran_Local instance
        values of Moran's Local Autocorrelation Statistic
    df : geopandas dataframe instance
        In mask_local_auto(), assign df['labels'] per row. Note that 
        ``df`` will be modified, so calling functions uses a copy of
        the user provided ``df``.
    p : float, optional
        The p-value threshold for significance. Points will
        be colored by significance.
    title : str, optional
        Title of map. Default title=None
    plot_width : int, optional
        Width dimension of the figure in screen units/ pixels.
        Default = 500
    plot_height : int, optional
        Height dimension of the figure in screen units/ pixels.
        Default = 500
    
    Returns
    -------
    fig : Bokeh figure instance
        Figure of LISA cluster map, colored by local spatial autocorrelation

    Examples
    --------
    '''
    # We're adding columns, do that on a copy rather than on the users' input
    df = df.copy()
    
    # add cluster_labels and colors5 in mask_local_auto
    cluster_labels, colors5, _, _ = mask_local_auto(moran_loc, df=df, p=0.05)
    
    # load df into bokeh data source
    geo_source = GeoJSONDataSource(geojson=df.to_json())

    # Create figure
    fig = figure(title=title, toolbar_location='right',
          plot_width=plot_width, plot_height=plot_height, tools=tools)
    fig.patches('xs', 'ys', fill_alpha=0.8, 
              fill_color={'field': 'labels', 'transform': CategoricalColorMapper(palette=colors5,
                                                                                 factors=cluster_labels)}, 
              line_color='white', line_width=0.5, source=geo_source)
    
    # add legend with add_legend()
    add_legend(fig, cluster_labels, colors5)
    
    # change layout
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.axis.visible = None

    return fig


def mplot(moran_loc, p=None, plot_width=500, plot_height=500, tools=''): 
    '''
    Moran Scatterplot, optional coloured by local spatial autocorrelation
    
    Parameters
    ----------
    moran_loc : esda.moran.Moran_Local instance
        values of Moran's Local Autocorrelation Statistic
    p : float, optional
        The p-value threshold for significance. Points will
        be colored by significance.
    plot_width : int, optional
        Width dimension of the figure in screen units/ pixels.
        Default = 500
    plot_height : int, optional
        Height dimension of the figure in screen units/ pixels.
        Default = 500
    
    Returns
    -------
    fig : Bokeh figure instance
        Figure of Moran Scatterplot, optionally colored by
        local spatial autocorrelation

    Examples
    --------
    '''   
    lag = ps.lag_spatial(moran_loc.w, moran_loc.z)
    fit = ps.spreg.OLS(moran_loc.z[:, None], lag[:,None])
    
    if p is not None:
        if not isinstance(moran_loc, esda.moran.Moran_Local):
            raise ValueError("`moran_loc` is not a Moran_Local instance")
    
        _, _, colors, _ = mask_local_auto(moran_loc, p=0.05)
    
    else:
        colors = 'black'
    
    # Vertical line
    vline = Span(location=0, dimension='height', line_color='lightskyblue', line_width=2, line_dash = 'dashed')
    # Horizontal line
    hline = Span(location=0, dimension='width', line_color='lightskyblue', line_width=2, line_dash = 'dashed')
    
    # Create figure
    fig = figure(title="Moran Scatterplot", x_axis_label='Response', y_axis_label='Spatial Lag',
                 toolbar_location='left', plot_width=plot_width, plot_height=plot_height, tools=tools)
    fig.scatter(moran_loc.z, lag, color=colors, size=8, fill_alpha=.6)
    fig.renderers.extend([vline, hline])
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.line(lag, fit.predy.flatten(), line_width = 2) # fit line
    return fig


def plot_local_autocorrelation(moran_loc, df, attribute, p=0.05, plot_width=250,
                               plot_height=300,
                               reverse_colors=False):
    """
    Plot Moran Scatterplot, LISA cluster and Choropleth
    for Local Spatial Autocorrelation Analysis
    
    Parameters
    ----------
    moran_loc : esda.moran.Moran_Local instance
        values of Moran's Local Autocorrelation Statistic
    df : Geopandas dataframe
        Dataframe containing relevant polygon and attribute values.
    attribute : str
        Name of column containing attribute values of interest.
    plot_width : int, optional
        Width dimension of the figure in screen units/ pixels.
        Default = 250
    plot_height : int, optional
        Height dimension of the figure in screen units/ pixels.
        Default = 300
    method : str, optional
        Classification method to be used. Options supported:
        * 'quantiles' (default)
        * 'fisher-jenks'
        * 'equal-interval'
    k : int, optional
        Number of bins, assigning values to. Default k=5
    reverse_colors: boolean
        Reverses the color palette to show lightest colors for
        lowest values in Choropleth map. Default reverse_colors=False
    
    Returns
    -------
    fig : Bokeh Figure instance
        Figure of Choropleth 
    """
    TOOLS = "tap,reset,help"
    
    scatter = mplot(moran_loc, p=p, plot_width=plot_width, plot_height=plot_height, tools=TOOLS)
    LISA = lisa_cluster(moran_loc, df, p=p, plot_width=plot_width, plot_height=plot_height, tools=TOOLS)
    choro = plot_choropleth(df, attribute, reverse_colors=reverse_colors, plot_width=plot_width, plot_height=plot_height,
                                tools=TOOLS)
    
    fig = gridplot([[scatter, LISA, choro]],
                   sizing_mode='fixed')
    return fig
