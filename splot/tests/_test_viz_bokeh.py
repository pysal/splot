import matplotlib.pyplot as plt
import libpysal.api as lp
from libpysal import examples
import geopandas as gpd
import esda

from splot._viz_bokeh import (plot_choropleth_bokeh, lisa_cluster_bokeh,
                              mplot_bokeh, three_plot_bokeh)

def test_plot_choropleth_bokeh():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    TOOLS = "tap,help"
    fig = plot_choropleth_bokeh(df, 'HOVAL', title='columbus',
                                reverse_colors=True, tools=TOOLS)
    plt.close(fig)


def test_lisa_cluster_bokeh():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = esda.moran.Moran_Local(y, w)

    TOOLS = "tap,reset,help"
    fig = lisa_cluster_bokeh(moran_loc, df, p=0.05, tools=TOOLS)
    plt.close(fig)


def test_mplot_bokeh():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = esda.moran.Moran_Local(y, w)

    fig = mplot_bokeh(moran_loc, p=0.05)
    plt.close(fig)


def test_three_plot_bokeh():
    link = examples.get_path('columbus.shp')
    df = gpd.read_file(link)

    y = df['HOVAL'].values
    w = lp.Queen.from_dataframe(df)
    w.transform = 'r'

    moran_loc = esda.moran.Moran_Local(y, w)

    fig = three_plot_bokeh(moran_loc, df, 'HOVAL')
    plt.close(fig)