import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib
import collections
import matplotlib.cm as cm

"""
Creating Value by Alpha maps

"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def value_by_alpha(x, y, gdf, cmap='GnBu'):
    # option to put in other 
    if isinstance(cmap, collections.Sequence):
        cmap = colors.LinearSegmentedColormap.from_list('cmap', cmap)
    cmap = cm.get_cmap(cmap)
    rgba = cmap(x)
    rgba[:, 3] = y/y.max()
    return rgba

def choropleth_vba(gdf, rgba)
    ax = gdf.plot(color=rgba)
    return ax

