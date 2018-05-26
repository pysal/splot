"""
Lightweight visualizations for pysal using Matplotlib and Geopandas

TODO
add Examples
change function input naming to be in line with bokeh functionality
"""
__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")

import matplotlib.pyplot as plt
import geopandas as gpd
import pysal as ps
import splot.plot

from matplotlib import patches, colors

from ._viz_utils import mask_local_auto


def lisa_cluster(moran_loc, df, p=0.05, figsize=None, ax=None,
                 legend=True, legend_kwds=None):
    """
    Create a LISA Cluster map
    
    Parameters
    ----------
    moran_loc : esda.moran.Moran_Local instance
        Values of Moran's Local Autocorrelation Statistic
    df : geopandas dataframe instance, optional
        If given, assign df['labels'] per row.  Note that `df` will be
        modified, so calling functions should use a copy of the user
        provided `df`.
    p : float, optional
        The p-value threshold for significance. Points will
        be colored by significance.
    figsize: tuple, optional
        W, h of figure. Default = None
    ax : matplotlib Axes instance, optional
        Axes in which to plot the figure in multiple Axes layout. Default = None
    legend : boolean, optional
        If True, legend for maps will be depicted. Default = True
    legend_kwds : dict, optional
        Dictionary to control legend formatting options.
        Example ``legend_kwds={'loc': 'upper left', 'bbox_to_anchor': (0.92, 1.05)}``
        Default = None
        
    Returns
    -------
    fig : matplotlip Figure instance
        Figure of LISA cluster map 
    """
    # retrieve colors5 and labels from mask_local_auto
    _, colors5, _, labels = mask_local_auto(moran_loc, p=p, df=df)
    
    # define ListedColormap
    hmap = colors.ListedColormap(colors5)
    
    if ax is None:
        fig, ax = plt.subplots(1, figsize=figsize)
    else:
        fig = ax.get_figure()
    
    df.assign(cl=labels).plot(column='cl', categorical=True,
        k=2, cmap=hmap, linewidth=0.1, ax=ax,
        edgecolor='white', legend=legend, legend_kwds=legend_kwds)
    ax.set_axis_off()
    return fig


def plot_local_autocorrelation(moran_loc, df, attribute, p=0.05, region_column=None,
                               mask=None, mask_color='gold', quadrant=None,
                               figsize=(15, 4), legend=True, scheme='Quantiles', cmap='GnBu'):
    '''
    Produce three-plot visualization of Moran Scatteprlot, LISA cluster
    and Choropleth, with Local Moran region and quadrant masking
    
    Parameters
    ----------
    moran_loc : esda.moran.Moran_Local instance
        Values of Moran's Local Autocorrelation Statistic
    df : geopandas dataframe
        The Dataframe containing information to plot the two maps.
    attribute : str
        Column name of attribute which should be depicted in Choropleth map.
    p : float, optional
        The p-value threshold for significance. Points and polygons will
        be colored by significance. Default = 0.05.
    region_column: string, optional
        Column name containing mask region of interest. Default = None
    mask: str, optional
        Identifier or name of the region to highlight. Default = None
    mask_color: str, optional
        Color of mask. Default = 'gold'
    quadrant : int, optional
        Quadrant 1-4 in scatterplot masking values in LISA cluster and
        Choropleth maps. Default = None
    figsize: tuple, optional
        W, h of figure. Default = (15,4)
    legend: boolean, optional
        If True, legend for maps will be depicted. Default = True
    scheme: str, optional
        Name of PySAL classifier to be used. Default = 'Quantiles'
    cmap: str, optional
        Name of matplotlib colormap used for plotting the Choropleth. Default = 'GnBU'
    
    Returns
    -------
    fig : Matplotlib figure instance
        Moran Scatterplot, LISA cluster map and Choropleth
    
        '''
    fig, axs = plt.subplots(1, 3, figsize=figsize,
                            subplot_kw={'aspect':'equal'})
    #Moran Scatterplot
    splot.plot.mplot(moran_loc, xlabel='Response', ylabel='Spatial Lag',
                     title='Moran Scatterplot', p=p, ax=axs[0])
    axs[0].set_aspect('auto')
    
    # Lisa cluster map
    #TODO: Fix legend_kwds: display boxes instead of points, 
    lisa_cluster(moran_loc, df, p=p, ax=axs[1], legend=legend,
                     legend_kwds={'loc': 'upper left', 
                    'bbox_to_anchor': (0.92, 1.05)})
    
    #Choropleth for attribute
    df.plot(column=attribute, scheme=scheme, cmap=cmap,
            legend=legend, legend_kwds={'loc': 'upper left',
                                        'bbox_to_anchor': (0.92, 1.05)},
            ax=axs[2], alpha=1)
    axs[2].set_axis_off()
    
    #MASKING QUADRANT VALUES
    if quadrant is not None:
        #Quadrant masking in Scatterplot
        mask_angles = {1: 0, 2: 90, 3: 180, 4: 270} #rectangle angles
        # We don't want to change the axis data limits, so use the current ones
        xmin, xmax = axs[0].get_xlim()
        ymin, ymax = axs[0].get_ylim()
        # We are rotating, so we start from 0 degrees and 
        # figured out the right dimensions for the rectangles for other angles
        mask_width = {1: abs(xmax),
                      2: abs(ymax),
                      3: abs(xmin),
                      4: abs(ymin)}
        mask_height = {1: abs(ymax),
                      2: abs(xmin),
                      3: abs(ymin),
                      4: abs(xmax)}
        axs[0].add_patch(patches.Rectangle((0,0), width=mask_width[quadrant],
                                           height=mask_height[quadrant],
                                           angle=mask_angles[quadrant],
                                           color='grey', zorder=-1, alpha=0.8))
        # quadrant selection in maps
        non_quadrant = ~(moran_loc.q==quadrant)
        mask_quadrant = df[non_quadrant]
        df_quadrant = df.iloc[moran_loc.q == quadrant] 
        union2 = df_quadrant.unary_union.boundary
        
        # LISA Cluster mask and cluster boundary
        mask_quadrant.plot(column=attribute, scheme=scheme, color='white', ax=axs[1], alpha=0.7, zorder=1)
        gpd.GeoSeries([union2]).plot(linewidth=2, ax=axs[1], color='darkgrey')
        
        #CHOROPLETH MASK
        mask_quadrant.plot(column=attribute, scheme=scheme, color='white', ax=axs[2], alpha=0.7, zorder=1)
        gpd.GeoSeries([union2]).plot(linewidth=2, ax=axs[2], color='darkgrey')
    
    # REGION MASKING
    if region_column is not None:
        # masking inside axs[0] or Moran Scatterplot
        ix = df[region_column].isin(mask)
        df_mask = df[ix]
        x_mask = moran_loc.z[ix]
        y_mask = ps.lag_spatial(moran_loc.w, moran_loc.z)[ix]
        axs[0].plot(x_mask, y_mask, color=mask_color, marker='o', markersize=14,
                    alpha=.8, zorder=-1)
        
        
        #masking inside axs[1] or Lisa cluster map
        union = df_mask.unary_union.boundary
        gpd.GeoSeries([union]).plot(linewidth=2, ax=axs[1], color=mask_color)
        
        #masking inside axs[2] or Chloropleth
        gpd.GeoSeries([union]).plot(linewidth=2, ax=axs[2], color=mask_color)
    return fig