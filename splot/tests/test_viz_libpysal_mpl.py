import geopandas as gpd
import libpysal
import matplotlib.pyplot as plt
import pytest
from libpysal import examples
from libpysal.weights.contiguity import Queen

from splot.libpysal import plot_spatial_weights


@pytest.mark.filterwarnings("ignore:Geometry is in a geographic CRS.")
def test_plot_spatial_weights():
    # get data
    rio_grande_do_sul = examples.load_example("Rio Grande do Sul")
    gdf = gpd.read_file(rio_grande_do_sul.get_path("43MUE250GC_SIR.shp"))

    # calculate weights
    weights = Queen.from_dataframe(gdf, silence_warnings=True)

    # plot weights
    fig, _ = plot_spatial_weights(weights, gdf)
    plt.close(fig)

    # calculate nonplanar_joins
    wnp = libpysal.weights.util.nonplanar_neighbors(weights, gdf)
    # plot new joins
    fig2, _ = plot_spatial_weights(wnp, gdf)
    plt.close(fig2)

    # customize
    fig3, _ = plot_spatial_weights(wnp, gdf, nonplanar_edge_kws=dict(color="#4393c3"))
    plt.close(fig3)

    # plot in existing figure
    fig4, axs = plt.subplots(1, 3)
    plot_spatial_weights(wnp, gdf, ax=axs[0])
    plt.close(fig4)

    # uses a column as the index for spatial weights object
    weights_index = Queen.from_dataframe(
        gdf, idVariable="CD_GEOCMU", silence_warnings=True
    )
    fig, _ = plot_spatial_weights(weights_index, gdf, indexed_on="CD_GEOCMU")
    plt.close(fig)
