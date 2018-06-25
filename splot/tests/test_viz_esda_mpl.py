import matplotlib.pyplot as plt
import libpysal.api as lp
from libpysal import examples
import geopandas as gpd

from esda.moran import Moran_Local
from splot.esda import (moran_loc_scatterplot,
                        plot_local_autocorrelation,
                        lisa_cluster)


def test_moran_loc_scatterplot():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = Moran_Local(y, w)

    # try with p value so points are colored
    fig, _ = moran_loc_scatterplot(moran_loc, p=0.05)
    plt.close(fig)

    # try with p value and different figure size
    fig, _ = moran_loc_scatterplot(moran_loc, p=0.05, figsize=(10,5))
    plt.close(fig)

def test_lisa_cluster():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = Moran_Local(y, w)

    fig, _ = lisa_cluster(moran_loc, df)
    plt.close(fig)


def test_plot_local_autocorrelation():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = Moran_Local(y, w)

    fig, _ = plot_local_autocorrelation(moran_loc, df, 'HOVAL', p=0.05)
    plt.close(fig)

    # also test with quadrant and mask
    fig, _ = plot_local_autocorrelation(moran_loc, df, 'HOVAL', p=0.05,
                                     region_column='POLYID',
                                     mask=['1', '2', '3'], quadrant=1)
    plt.close(fig)