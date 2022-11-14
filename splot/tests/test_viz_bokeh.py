# Tests are enabled even though Bokeh functionality is private for now,
# in order to keep code coverage good.
# Bokeh versions are not intended for release
# but will be picked up later

import esda
import geopandas as gpd
import pytest
from libpysal import examples
from libpysal.weights.contiguity import Queen

from splot._bk import (
    lisa_cluster,
    moran_scatterplot,
    plot_choropleth,
    plot_local_autocorrelation,
)


@pytest.mark.skip(reason="to be deprecated")
def test_plot_choropleth():
    link = examples.get_path("columbus.shp")
    df = gpd.read_file(link)

    w = Queen.from_dataframe(df)
    w.transform = "r"

    TOOLS = "tap,help"
    plot_choropleth(df, "HOVAL", title="columbus", reverse_colors=True, tools=TOOLS)


@pytest.mark.skip(reason="to be deprecated")
def test_lisa_cluster():
    link = examples.get_path("columbus.shp")
    df = gpd.read_file(link)

    y = df["HOVAL"].values
    w = Queen.from_dataframe(df)
    w.transform = "r"

    moran_loc = esda.moran.Moran_Local(y, w)

    TOOLS = "tap,reset,help"
    lisa_cluster(moran_loc, df, p=0.05, tools=TOOLS)


@pytest.mark.skip(reason="to be deprecated")
def test_moran_scatterplot():
    link = examples.get_path("columbus.shp")
    df = gpd.read_file(link)

    y = df["HOVAL"].values
    w = Queen.from_dataframe(df)
    w.transform = "r"

    moran_loc = esda.moran.Moran_Local(y, w)

    moran_scatterplot(moran_loc, p=0.05)


@pytest.mark.skip(reason="to be deprecated")
def test_plot_local_autocorrelation():
    link = examples.get_path("columbus.shp")
    df = gpd.read_file(link)

    y = df["HOVAL"].values
    w = Queen.from_dataframe(df)
    w.transform = "r"

    moran_loc = esda.moran.Moran_Local(y, w)

    plot_local_autocorrelation(moran_loc, df, "HOVAL")
