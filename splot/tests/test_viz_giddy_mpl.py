import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from libpysal import examples
from libpysal.weights.contiguity import Queen

try:
    import ipywidgets  # noqa F401

    HAS_IPYWIDGETS = True
except (ImportError, ModuleNotFoundError):
    HAS_IPYWIDGETS = False


def _data_generation():
    from giddy.directional import Rose

    # get csv and shp
    shp_link = examples.get_path("us48.shp")
    df = gpd.read_file(shp_link)
    income_table = pd.read_csv(examples.get_path("usjoin.csv"))
    # calculate relative values
    for year in range(1969, 2010):
        income_table[str(year) + "_rel"] = (
            income_table[str(year)] / income_table[str(year)].mean()
        )
    # merge
    gdf = df.merge(income_table, left_on="STATE_NAME", right_on="Name")
    # retrieve spatial weights and data for two points in time
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    y1 = gdf["1969_rel"].values
    y2 = gdf["2000_rel"].values
    # calculate rose Object
    Y = np.array([y1, y2]).T
    rose = Rose(Y, w, k=5)
    return gdf, y1, rose


def test_dynamic_lisa_heatmap():
    from splot.giddy import dynamic_lisa_heatmap

    _, _, rose = _data_generation()
    fig, _ = dynamic_lisa_heatmap(rose)
    plt.close(fig)

    fig2, _ = dynamic_lisa_heatmap(rose, cmap="GnBu")
    plt.close(fig2)


def test_dynamic_lisa_rose():
    from splot.giddy import dynamic_lisa_rose

    _, y1, rose = _data_generation()
    fig1, _ = dynamic_lisa_rose(rose)
    plt.close(fig1)

    fig2, _ = dynamic_lisa_rose(rose, attribute=y1)
    plt.close(fig2)

    fig3, _ = dynamic_lisa_rose(rose, c="r")
    plt.close(fig3)

    pytest.raises(ValueError, dynamic_lisa_rose, rose, attribute=y1, color="blue")


def test_dynamic_lisa_vectors():
    from splot.giddy import dynamic_lisa_vectors

    _, _, rose = _data_generation()
    fig1, _ = dynamic_lisa_vectors(rose)
    plt.close(fig1)

    fig2, _ = dynamic_lisa_vectors(rose, arrows=False)
    plt.close(fig2)

    fig3, _ = dynamic_lisa_vectors(rose, c="r")
    plt.close(fig3)

    fig4, axs = plt.subplots(1, 3)
    dynamic_lisa_vectors(rose, ax=axs[0], color="r")
    plt.close(fig4)


def test_dynamic_lisa_composite():
    from splot.giddy import dynamic_lisa_composite

    gdf, _, rose = _data_generation()
    fig, _ = dynamic_lisa_composite(rose, gdf)
    plt.close(fig)


@pytest.mark.skipif(HAS_IPYWIDGETS, reason="ipywidgets available")
def test_import_ipywidgets_error():
    with pytest.raises(ImportError, match="`ipywidgets` package is required"):
        from splot.giddy import dynamic_lisa_composite_explore

        gdf, _, rose = _data_generation()

        dynamic_lisa_composite_explore(rose, gdf)
