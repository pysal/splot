import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib

"""
Creating Value by Alpha maps

"""

__author__ = ("Stefanie Lumnitz <stefanie.lumitz@gmail.com>")


def value_by_alpha(x, alphay, gdf):
    



def value_by_alpha(x='attribute', y='alpha_attribute', c, data=geodataframe):
    rgb = matplotlib.colors.to_rgba_array(c)
    alpha_channel = x/y.max()
    rgba = np.vstack((rgb, np.asarray(alpha_channel).reshape(-1,1)))
    fig, ax = geodataframe.plot(x, color=rgba)
    return fig, ax

def make_RGBA_array_from_attribute(x):
    

"""
cols = matplotlib.colors.to_rgba_array(['r', 'r', 'r', 'r'])

cols[:, -1] = [0.5, 0.7, 0.9, 0.2]

s = geopandas.GeoSeries([Polygon([(random.random(), random.random()) for i in range(3)]) for _ in range(4)])

s.plot(color=cols)
"""