import matplotlib.pyplot as plt
import libpysal
from libpysal.api import queen_from_shapefile
from esda.moran import Moran, Moran_Local
from libpysal.io.geotable import read_files

from splot.plot import mplot


def test_mplot():
    link = libpysal.examples.get_path('columbus.shp')

    db = read_files(link)
    y = db['HOVAL'].values
    w = queen_from_shapefile(link)
    w.transform = 'R'

    m = Moran(y, w)

    fig = mplot(m, xlabel='Response', ylabel='Spatial Lag',
                title='Moran Scatterplot', figsize=(7,7))
    plt.close(fig)

    # also try with p-value (so points get colored)
    m = Moran_Local(y, w)
    fig = mplot(m, xlabel='Response', ylabel='Spatial Lag',
                title='Moran Scatterplot', figsize=(7,7),
                p=0.05)
    plt.close(fig)