import numpy as np

def plot(w, gdf, indexed_on=None, ax=None, color='k',
         node_kws=dict(marker='*', color='k'), edge_kws=None, nonplanar_edge_kws=None):
    """
    Plot spatial weights objects.
    NOTE: Requires matplotlib, and implicitly requires geopandas 
    dataframe as input.

    Arguments
    ---------
    w :
    
    gdf : geopandas dataframe 
        the original shapes whose topological relations are 
        modelled in W. ß
    indexed_on : str 
        column of gdf which the weights object uses as an index.
        (Default: None, so the geodataframe's index is used)
    ax : matplotlib axis
        axis on which to plot the weights. 
        (Default: None, so plots on the current figure)
    color : string
        matplotlib color string, will color both nodes and edges
        the same by default. 
    node_kws : keyword argument dictionary
        dictionary of keyword arguments to send to pyplot.scatter,
        which provide fine-grained control over the aesthetics
        of the nodes in the plot
    edge_kws : keyword argument dictionary
        dictionary of keyword arguments to send to pyplot.plot,
        which provide fine-grained control over the aesthetics
        of the edges in the plot.
    nonplanar_edge_kws : keyword argument dictionary
                  TODO

    Returns
    -------
    fig,ax : matplotlib figure,axis on which the plot is made. 

    NOTE: if you'd like to overlay the actual shapes from the 
          geodataframe, call gdf.plot(ax=ax) after this. To plot underneath,
          adjust the z-order of the geopandas plot: gdf.plot(ax=ax,zorder=0)

    Examples
    --------
    >>> import libpysal.api as lp
    >>> import geopandas
    >>> gdf = geopandas.read_file(lp.get_path("columbus.shp"))
    >>> weights = lp.Queen.from_dataframe(gdf)
    >>> tmp = weights.plot(gdf, color='firebrickred', node_kws=dict(marker='*', color='k'))

    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("W.plot depends on matplotlib.pyplot, and this was"
                          "not able to be imported. \nInstall matplotlib to"
                          "plot spatial weights.")
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    if node_kws is not None:
        if 'color' not in node_kws:
            node_kws['color'] = color
    else:
        node_kws=dict(color=color)

    if edge_kws is not None:
        if 'color' not in edge_kws:
            edge_kws['color'] = color
    else:
        edge_kws=dict(color=color)

    edge_kws.setdefault('lw', 0.5)
    if nonplanar_edge_kws is None:
        nonplanar_edge_kws = edge_kws.copy()
        nonplanar_edge_kws['color'] = 'darkgrey'

    node_has_nonplanar_join = []
    if hasattr(w, 'non_planar_joins'):
        # This attribute is present when an instance is created by the user
        # calling `weights.util.nonplanar_neighbors`. If so, treat those
        # edges differently by default.
        node_has_nonplanar_join = w.non_planar_joins.keys()

    # Plot the polygons from the geodataframe as a base layer
    gdf.plot(ax=ax, color='lightgrey', edgecolor='w')

    for idx, neighbors in w:
        if idx in w.islands:
            continue

        if indexed_on is not None:
            neighbors = gdf[gdf[indexed_on].isin(neighbors)].index.tolist()
            idx = gdf[gdf[indexed_on] == idx].index.tolist()[0]

        # Find centroid of each polygon that's a neighbor, as a numpy array (x, y)
        centroids = gdf.loc[neighbors].centroid.apply(lambda p: (p.x, p.y))
        centroids = np.vstack(centroids.values)
        # Find the centroid of the polygon we're looking at now
        focal = np.hstack(gdf.loc[idx].geometry.centroid.xy)
        seen = set()
        for nidx, neighbor in zip(neighbors, centroids):
            if (idx, nidx) in seen:
                continue
            seen.update((idx, nidx))
            seen.update((nidx, idx))

            # Plot current edge as line: plot([x0, x1], [y0, y1])
            if (idx in node_has_nonplanar_join) and (nidx in w.non_planar_joins[idx]):
                # This is a non-planar edge
                ax.plot(*list(zip(focal, neighbor)), marker=None, **nonplanar_edge_kws)
            else:
                ax.plot(*list(zip(focal, neighbor)), marker=None, **edge_kws)

    # Plot the nodes
    ax.scatter(gdf.centroid.apply(lambda p: p.x),
               gdf.centroid.apply(lambda p: p.y),
               **node_kws)
    return fig, ax