from libpysal.weights.contiguity import Queen
import libpysal
from libpysal import examples
from libpysal.weights import raster
import matplotlib.pyplot as plt
import geopandas as gpd

from splot.libpysal import plot_spatial_weights

def test_plot_spatial_weights():
    # get data for raster
    da = raster.testDataArray((1,5,10), rand=True)
    # get data for polygons
    rio_grande_do_sul = examples.load_example('Rio Grande do Sul')
    gdf = gpd.read_file(rio_grande_do_sul.get_path('43MUE250GC_SIR.shp'))
    gdf.head()
    # calculate weights
    weights_rast = raster.da2WSP(data = da)
    weights = Queen.from_dataframe(gdf)
    #plot weights for raster
    fig, _ = plot_spatial_weights(weights_rast, data = da)
    plt.close(fig)
    # plot weights
    fig1, _ = plot_spatial_weights(weights, data = gdf)
    plt.close(fig1)
    # calculate nonplanar_joins
    wnp = libpysal.weights.util.nonplanar_neighbors(weights, gdf)
    # plot new joins
    fig2, _ = plot_spatial_weights(wnp, gdf)
    plt.close(fig2)
    #customize
    fig3, _ = plot_spatial_weights(wnp, gdf, nonplanar_edge_kws=dict(color='#4393c3'))
    plt.close(fig3)
    # plot in existing figure
    fig4, axs = plt.subplots(1,3)
    plot_spatial_weights(wnp, gdf, ax=axs[0])
    plt.close(fig4)

    # uses a column as the index for spatial weights object
    weights_index = Queen.from_dataframe(gdf, idVariable="CD_GEOCMU")
    fig, _ = plot_spatial_weights(weights_index, gdf, indexed_on="CD_GEOCMU")
    plt.close(fig)
    
    #test for Errors
    assert_raises(ValueError, plot_spatial_weights, weights, da)
    assert_raises(ValueError, plot_spatial_weights, weights, gdf, da)
    assert_raises(ValueError, plot_spatial_weights, weights_rast, gdf, da)
    assert_raises(ValueError, plot_spatial_weights, weights_rast, gdf)