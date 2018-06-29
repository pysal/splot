import matplotlib.pyplot as plt
import libpysal.api as lp
from libpysal import examples
import geopandas as gpd

from esda.moran import Moran_Local, Moran, Moran_BV
from splot.esda import (moran_scatterplot,
                        plot_moran_simulation,
                        plot_moran,
                        moran_bv_scatterplot,
                        plot_moran_bv_simulation,
                        plot_moran_bv,
                        moran_loc_scatterplot,
                        plot_local_autocorrelation,
                        lisa_cluster)


def test_moran_scatterplot():
    # Load data and apply statistical analysis
    link_to_data = examples.get_path('Guerry.shp')
    gdf = gpd.read_file(link_to_data)
    y = gdf['Donatns'].values
    w = lp.Queen.from_dataframe(gdf)
    w.transform = 'r'
    # Calc Global Moran
    w = lp.Queen.from_dataframe(gdf)
    moran = Moran(y, w)
    # plot
    fig, _ = moran_scatterplot(moran)
    plt.close(fig)
    # customize
    fig, _ = moran_scatterplot(moran, zstandard=False, figsize=(4, 4))
    plt.close(fig)


def test_plot_moran_simulation():
    # Load data and apply statistical analysis
    link_to_data = examples.get_path('Guerry.shp')
    gdf = gpd.read_file(link_to_data)
    y = gdf['Donatns'].values
    w = lp.Queen.from_dataframe(gdf)
    w.transform = 'r'
    # Calc Global Moran
    w = lp.Queen.from_dataframe(gdf)
    moran = Moran(y, w)
    # plot
    fig, _ = plot_moran_simulation(moran)
    plt.close(fig)
    # customize
    fig, _ = plot_moran_simulation(moran, figsize=(4, 4))
    plt.close(fig)


def test_plot_moran():
    # Load data and apply statistical analysis
    link_to_data = examples.get_path('Guerry.shp')
    gdf = gpd.read_file(link_to_data)
    y = gdf['Donatns'].values
    w = lp.Queen.from_dataframe(gdf)
    w.transform = 'r'
    # Calc Global Moran
    w = lp.Queen.from_dataframe(gdf)
    moran = Moran(y, w)
    # plot
    fig, _ = plot_moran(moran)
    plt.close(fig)
    # customize
    fig, _ = plot_moran(moran, zstandard=False, figsize=(4, 4))
    plt.close(fig)

def test_moran_bv_scatterplot():
    link_to_data = examples.get_path('Guerry.shp')
    gdf = gpd.read_file(link_to_data)
    x = df['Suicids'].values
    y = gdf['Donatns'].values
    w = lp.Queen.from_dataframe(gdf)
    w.transform = 'r'
    # Calculate Bivariate Moran
    moran_bv = Moran_BV(x, y, w)
    # plot
    fig, _ = moran_bv_scatterplot(moran_bv)
    plt.close(fig)
    # customize plot
    fig, _ = moran_bv_scatterplot(moran_bv, zstandard=False, figsize=(4,4))
    plt.close(fig)


def test_plot_moran_bv_simulation():
    # Load data and calculate weights
    link_to_data = examples.get_path('Guerry.shp')
    gdf = gpd.read_file(link_to_data)
    x = df['Suicids'].values
    y = gdf['Donatns'].values
    w = lp.Queen.from_dataframe(gdf)
    w.transform = 'r'
    # Calculate Bivariate Moran
    moran_bv = Moran_BV(x, y, w)
    # plot
    fig, _ = plot_moran_bv_simulation(moran_bv)
    plt.close(fig)
    # customize plot
    fig, _ = plot_moran_bv_simulation(moran_bv, figsize=(4,4))
    plt.close(fig)

def test_plot_moran_bv():
    # Load data and calculate weights
    link_to_data = examples.get_path('Guerry.shp')
    gdf = gpd.read_file(link_to_data)
    x = df['Suicids'].values
    y = gdf['Donatns'].values
    w = lp.Queen.from_dataframe(gdf)
    w.transform = 'r'
    # Calculate Bivariate Moran
    moran_bv = Moran_BV(x, y, w)
    # plot
    fig, _ = plot_moran_bv(moran_bv)
    plt.close(fig)
    # customize plot
    fig, _ = plot_moran_bv(moran_bv, figsize=(4,4))
    plt.close(fig)


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
    fig, _ = moran_loc_scatterplot(moran_loc, p=0.05, figsize=(10, 5))
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
