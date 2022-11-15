import geopandas as gpd
import libpysal as lp
import matplotlib.pyplot as plt
import numpy as np
import pytest
from esda.moran import Moran, Moran_BV, Moran_BV_matrix, Moran_Local, Moran_Local_BV
from libpysal import examples
from libpysal.weights.contiguity import Queen

from splot._viz_esda_mpl import (
    _moran_bv_scatterplot,
    _moran_global_scatterplot,
    _moran_loc_bv_scatterplot,
    _moran_loc_scatterplot,
)
from splot.esda import (
    lisa_cluster,
    moran_facet,
    moran_scatterplot,
    plot_local_autocorrelation,
    plot_moran,
    plot_moran_bv,
    plot_moran_bv_simulation,
    plot_moran_simulation,
)


def _test_data():
    guerry = examples.load_example("Guerry")
    link_to_data = guerry.get_path("guerry.shp")
    gdf = gpd.read_file(link_to_data)
    return gdf


def _test_data_columbus():
    columbus = examples.load_example("Columbus")
    link_to_data = columbus.get_path("columbus.shp")
    df = gpd.read_file(link_to_data)
    return df


def _test_LineString():
    link_to_data = examples.get_path("streets.shp")
    gdf = gpd.read_file(link_to_data)
    return gdf


def test_moran_scatterplot():
    gdf = _test_data()
    x = gdf["Suicids"].values
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"

    # Calculate `esda.moran` Objects
    moran = Moran(y, w)
    moran_bv = Moran_BV(y, x, w)
    moran_loc = Moran_Local(y, w)
    moran_loc_bv = Moran_Local_BV(y, x, w)

    # try with p value so points are colored or warnings apply
    with pytest.warns(UserWarning, match="`p` is only used for plotting"):
        fig, _ = moran_scatterplot(moran, p=0.05, aspect_equal=False)
        plt.close(fig)

    fig, _ = moran_scatterplot(moran_loc, p=0.05)
    plt.close(fig)

    with pytest.warns(UserWarning, match="`p` is only used for plotting"):
        fig, _ = moran_scatterplot(moran_bv, p=0.05)
        plt.close(fig)

    fig, _ = moran_scatterplot(moran_loc_bv, p=0.05)
    plt.close(fig)


def test_moran_global_scatterplot():
    # Load data and apply statistical analysis
    gdf = _test_data()
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    # Calc Global Moran
    w = Queen.from_dataframe(gdf)
    moran = Moran(y, w)
    # plot
    fig, _ = _moran_global_scatterplot(moran)
    plt.close(fig)
    # customize
    fig, _ = _moran_global_scatterplot(
        moran, zstandard=False, aspect_equal=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)


def test_plot_moran_simulation():
    # Load data and apply statistical analysis
    gdf = _test_data()
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    # Calc Global Moran
    w = Queen.from_dataframe(gdf)
    moran = Moran(y, w)
    # plot
    fig, _ = plot_moran_simulation(moran)
    plt.close(fig)
    # customize
    fig, _ = plot_moran_simulation(moran, fitline_kwds=dict(color="#4393c3"))
    plt.close(fig)


def test_plot_moran():
    # Load data and apply statistical analysis
    gdf = _test_data()
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    # Calc Global Moran
    w = Queen.from_dataframe(gdf)
    moran = Moran(y, w)
    # plot
    fig, _ = plot_moran(moran)
    plt.close(fig)
    # customize
    fig, _ = plot_moran(
        moran, zstandard=False, aspect_equal=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)


def test_moran_bv_scatterplot():
    gdf = _test_data()
    x = gdf["Suicids"].values
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    # Calculate Bivariate Moran
    moran_bv = Moran_BV(x, y, w)
    # plot
    fig, _ = _moran_bv_scatterplot(moran_bv)
    plt.close(fig)
    # customize plot
    fig, _ = _moran_bv_scatterplot(
        moran_bv, aspect_equal=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)


def test_plot_moran_bv_simulation():
    # Load data and calculate weights
    gdf = _test_data()
    x = gdf["Suicids"].values
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    # Calculate Bivariate Moran
    moran_bv = Moran_BV(x, y, w)
    # plot
    fig, _ = plot_moran_bv_simulation(moran_bv)
    plt.close(fig)
    # customize plot
    fig, _ = plot_moran_bv_simulation(
        moran_bv, aspect_equal=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)


def test_plot_moran_bv():
    # Load data and calculate weights
    gdf = _test_data()
    x = gdf["Suicids"].values
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    # Calculate Bivariate Moran
    moran_bv = Moran_BV(x, y, w)
    # plot
    fig, _ = plot_moran_bv(moran_bv)
    plt.close(fig)
    # customize plot
    fig, _ = plot_moran_bv(
        moran_bv, aspect_equal=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)


def test_moran_loc_scatterplot():
    df = _test_data_columbus()

    x = df["INC"].values
    y = df["HOVAL"].values
    w = Queen.from_dataframe(df)
    w.transform = "r"

    moran_loc = Moran_Local(y, w)
    moran_bv = Moran_BV(x, y, w)

    # try without p value
    fig, _ = _moran_loc_scatterplot(moran_loc)
    plt.close(fig)

    # try with p value and different figure size
    fig, _ = _moran_loc_scatterplot(
        moran_loc, p=0.05, aspect_equal=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)

    # try with p value and zstandard=False
    fig, _ = _moran_loc_scatterplot(
        moran_loc, p=0.05, zstandard=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)

    # try without p value and zstandard=False
    fig, _ = _moran_loc_scatterplot(
        moran_loc, zstandard=False, fitline_kwds=dict(color="#4393c3")
    )
    plt.close(fig)

    pytest.raises(ValueError, _moran_loc_scatterplot, moran_bv, p=0.5)
    pytest.warns(
        UserWarning,
        _moran_loc_scatterplot,
        moran_loc,
        p=0.5,
        scatter_kwds=dict(c="#4393c3"),
    )


def _test_calc_moran_loc(gdf, var="HOVAL"):
    y = gdf[var].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"

    moran_loc = Moran_Local(y, w)
    return moran_loc


def test_lisa_cluster():
    df = _test_data_columbus()
    moran_loc = _test_calc_moran_loc(df)

    fig, _ = lisa_cluster(moran_loc, df)
    plt.close(fig)

    # test LineStrings
    df_line = _test_LineString()
    moran_loc = _test_calc_moran_loc(df_line, var="Length")

    fig, _ = lisa_cluster(moran_loc, df_line)
    plt.close(fig)


def test_plot_local_autocorrelation():
    df = _test_data_columbus()
    moran_loc = _test_calc_moran_loc(df)

    fig, _ = plot_local_autocorrelation(moran_loc, df, "HOVAL", p=0.05)
    plt.close(fig)

    # also test with quadrant and mask
    with pytest.warns(UserWarning, match="Values in `mask` are not the same dtype"):
        fig, _ = plot_local_autocorrelation(
            moran_loc,
            df,
            "HOVAL",
            p=0.05,
            region_column="POLYID",
            aspect_equal=False,
            mask=["1", "2", "3"],
            quadrant=1,
        )
        plt.close(fig)

    # also test with quadrant and mask
    with pytest.warns(UserWarning, match="Values in `mask` are not the same dtype"):
        pytest.raises(
            ValueError,
            plot_local_autocorrelation,
            moran_loc,
            df,
            "HOVAL",
            p=0.05,
            region_column="POLYID",
            mask=["100", "200", "300"],
            quadrant=1,
        )


def test_moran_loc_bv_scatterplot():
    gdf = _test_data()
    x = gdf["Suicids"].values
    y = gdf["Donatns"].values
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    # Calculate Univariate and Bivariate Moran
    moran_loc = Moran_Local(y, w)
    moran_loc_bv = Moran_Local_BV(x, y, w)
    # try with p value so points are colored
    fig, _ = _moran_loc_bv_scatterplot(moran_loc_bv)
    plt.close(fig)

    # try with p value and different figure size
    fig, _ = _moran_loc_bv_scatterplot(moran_loc_bv, p=0.05, aspect_equal=False)
    plt.close(fig)

    pytest.raises(ValueError, _moran_loc_bv_scatterplot, moran_loc, p=0.5)
    pytest.warns(
        UserWarning,
        _moran_loc_bv_scatterplot,
        moran_loc_bv,
        p=0.5,
        scatter_kwds=dict(c="r"),
    )


def test_moran_facet():
    sids2 = examples.load_example("sids2")
    f = lp.io.open(sids2.get_path("sids2.dbf"))
    varnames = ["SIDR74", "SIDR79", "NWR74", "NWR79"]
    vars = [np.array(f.by_col[var]) for var in varnames]
    w = lp.io.open(examples.get_path("sids2.gal")).read()
    # calculate moran matrix
    moran_matrix = Moran_BV_matrix(vars, w, varnames=varnames)
    # plot
    fig, axarr = moran_facet(moran_matrix)
    plt.close(fig)
    # customize
    fig, axarr = moran_facet(
        moran_matrix, scatter_glob_kwds=dict(color="r"), fitline_bv_kwds=dict(color="y")
    )
    plt.close(fig)
