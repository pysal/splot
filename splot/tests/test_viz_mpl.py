import matplotlib.pyplot as plt
import libpysal.api as lp
from libpysal import examples
import geopandas as gpd
import esda

from splot.mpl import plot_local_autocorrelation, lisa_cluster


def test_lisa_cluster():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = esda.moran.Moran_Local(y, w)

    fig, _ = lisa_cluster(moran_loc, df)
    plt.close(fig)


def test_plot_local_auto():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = esda.moran.Moran_Local(y, w)

    fig = plot_local_autocorrelation(moran_loc, df, 'HOVAL', p=0.05)
    plt.close(fig)
    
    # also test with quadrant and mask
    fig = plot_local_autocorrelation(moran_loc, df, 'HOVAL', p=0.05,
                                     region_column='POLYID',
                                     mask=['1', '2', '3'], quadrant=1)
    plt.close(fig)