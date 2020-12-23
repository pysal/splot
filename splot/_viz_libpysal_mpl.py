import numpy as np
import libpysal
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

import warnings

"""
Lightweight visualizations for libpysal using Matplotlib and Geopandas

TODO
* make gdf argument in plot_spatial_weights optional
"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def plot_spatial_weights(w, gdf=None, data=None, indexed_on=None, ax=None,
                         figsize=(10, 10), node_kws=None, edge_kws=None,
                         nonplanar_edge_kws=None):
    """
    Plot spatial weights network.
    NOTE: Additionally plots `w.non_planar_joins` for
    libpysal.W objects if `libpysal.weights.util.nonplanar_neighbors()`
    was applied.

    Parameters
    ----------
    w : libpysal.W or libpysal.WSP object
        Values of libpysal weights object.
    gdf : geopandas.GeoDataFrame
        The original shapes whose topological relations
        are modelled in W/ WSP.
    data : geopandas.GeoDataFrame or xarray.DataArray
        The original shapes or raster, 2D or 3D DataArray with
        shape=(layer, lat, lon), whose topological relations
        are modelled in W/ WSP.
    indexed_on : str, optional
        Column of gdf which the weights object uses as an index.
        Default =None, so the geodataframe's index is used.
    ax : matplotlib axis, optional
        Axis on which to plot the weights.
        Default =None, so plots on the current figure.
    figsize : tuple, optional
        W, h of figure. Default =(10,10)
    node_kws : keyword argument dictionary, optional
        Dictionary of keyword arguments to send to pyplot.scatter,
        which provide fine-grained control over the aesthetics
        of the nodes in the plot. Default =None.
    edge_kws : keyword argument dictionary, optional
        Dictionary of keyword arguments to send to pyplot.plot,
        which provide fine-grained control over the aesthetics
        of the edges in the plot. Default =None.
    nonplanar_edge_kws : keyword argument dictionary, optional
        Dictionary of keyword arguments to send to pyplot.plot,
        which provide fine-grained control over the aesthetics
        of the edges from `weights.non_planar_joins` in the plot.
        Default =None.

    Returns
    -------
    fig : matplotlip Figure instance
        Figure of spatial weight network.
    ax : matplotlib Axes instance
        Axes in which the figure is plotted.

    Examples
    --------
    Imports

    >>> from libpysal.weights.contiguity import Queen
    >>> import geopandas as gpd
    >>> import libpysal
    >>> from libpysal import examples
    >>> import matplotlib.pyplot as plt
    >>> from splot.libpysal import plot_spatial_weights

    Data preparation and statistical analysis

    >>> gdf = gpd.read_file(examples.get_path('map_RS_BR.shp'))
    >>> weights = Queen.from_dataframe(gdf)
    >>> wnp = libpysal.weights.util.nonplanar_neighbors(weights, gdf)

    Plot weights

    >>> plot_spatial_weights(weights, gdf)
    >>> plt.show()

    Plot corrected weights

    >>> plot_spatial_weights(wnp, gdf)
    >>> plt.show()

    """
    if gdf is not None:
        warnings.warn(
            '`gdf` will be replaced by `data` from the 1.1.5 release onwards,'
             'use `data` to pass the geopandas.GeoDataFrame instead',
            FutureWarning, stacklevel=2
        )
        
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

        # default for node_kws
    if node_kws is None:
        node_kws = dict(
            markersize=10,
            facecolor='#4d4d4d',
            edgecolor='#4d4d4d',
        )

        # default for edge_kws
    if edge_kws is None:
        edge_kws = dict(colors='#4393c3')

        # default for nonplanar_edge_kws
    if nonplanar_edge_kws is None:
        edge_kws.setdefault('lw', 0.7)
        nonplanar_edge_kws = edge_kws.copy()
        nonplanar_edge_kws['colors'] = '#d6604d'

    node_has_nonplanar_join = []
    if hasattr(w, 'non_planar_joins'):
        # This attribute is present when an instance is created by the user
        # calling `weights.util.nonplanar_neighbors`. If so, treat those
        # edges differently by default.
        node_has_nonplanar_join = w.non_planar_joins.keys()

    segments = []
    non_planar_segments = []

    # test if data is not a GeoDataFrame, to avoid xarray import
    if gdf is None and not isinstance(data, gpd.GeoDataFrame):
        from shapely.geometry import Polygon
        
        def _buildPoly(df, x, y, res):
            geometry = Polygon(
                [(df[x]-res[0], df[y]-res[1]),
                    (df[x]+res[0], df[y]-res[1]),
                    (df[x]+res[0], df[y]+res[1]),
                    (df[x]-res[0], df[y]+res[1])])
            return geometry

        index = w.index
        df = index.to_frame(False)
        y, x = data.dims[-2:]
        res = np.empty(2)
        res[0] = (max(data[x].values)-min(data[x].values))/(data.shape[-1]*2)
        res[1] = (max(data[y].values)-min(data[y].values))/(data.shape[-2]*2)
        df["geometry"] = df.apply(_buildPoly, x=x, y=y, res=res, axis=1)
        gdf = gpd.GeoDataFrame(df)

        centroids_shp = gdf.centroid.values
        sparse = w.sparse
        for idx in range(len(index)):
            if sum(sparse[idx].indices) == 0:
                continue
            origin = np.array(centroids_shp[idx].coords)[0]
            for jdx in sparse[idx].indices:
                dest = np.array(centroids_shp[jdx].coords)[0]
                if (idx in node_has_nonplanar_join) and (jdx in w.non_planar_joins[idx]):
                    non_planar_segments.append([origin, dest])
                else:
                    segments.append([origin, dest])

    else:
        if isinstance(data, gpd.GeoDataFrame):
            gdf = data
        
        centroids_shp = gdf.centroid.values
        if indexed_on is not None:
            dict_index = dict(zip(gdf[indexed_on].values, range(len(gdf))))
            for idx in w.id_order:
                if idx in w.islands:
                    continue
                # Find the centroid of the polygon we're looking at now
                origin = np.array(centroids_shp[dict_index[idx]].coords)[0]
                for jdx in w.neighbors[idx]:
                    dest = np.array(centroids_shp[dict_index[jdx]].coords)[0]
                    if (idx in node_has_nonplanar_join) and (
                        jdx in w.non_planar_joins[idx]):
                        # This is a non-planar edge
                        non_planar_segments.append([origin, dest])
                    else:
                        segments.append([origin, dest])
        else:
            for idx in w.id_order:
                if idx in w.islands:
                    continue

                # Find the centroid of the polygon we're looking at now
                origin = np.array(centroids_shp[idx].coords)[0]
                for j in w.neighbors[idx]:
                    jdx = w.id2i[j]
                    dest = np.array(centroids_shp[jdx].coords)[0]
                    if (idx in node_has_nonplanar_join) and (
                        jdx in w.non_planar_joins[idx]):
                        # This is a non-planar edge
                        non_planar_segments.append([origin, dest])
                    else:
                        segments.append([origin, dest])

    # Plot the polygons from the geodataframe as a base layer
    gdf.plot(ax=ax, color='#bababa', edgecolor='w')

    # plot polygon centroids
    gdf.centroid.plot(ax=ax, **node_kws)

    # plot weight edges
    non_planar_segs_plot = LineCollection(
        np.array(non_planar_segments),
        **nonplanar_edge_kws
    )
    segs_plot = LineCollection(np.array(segments), **edge_kws)
    ax.add_collection(segs_plot)
    ax.add_collection(non_planar_segs_plot)
    if isinstance(data, gpd.GeoDataFrame):
        ax.set_axis_off()
    ax.set_aspect('equal')
    return fig, ax
