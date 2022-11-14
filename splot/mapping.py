"""
``splot.mapping``
=================

Provides Choropleth visualizations and mapping utilities.

Value-by-Alpha maps
-------------------

.. autosummary::
   :toctree: generated/

   value_by_alpha_cmap
   vba_choropleth
   vba_legend
   mapclassify_bin


Colormap utilities
------------------

.. autosummary::
   :toctree: generated/

   shift_colormap
   truncate_colormap

"""

from ._viz_utils import shift_colormap, truncate_colormap  # noqa F401
from ._viz_value_by_alpha_mpl import (  # noqa F401
    mapclassify_bin,
    value_by_alpha_cmap,
    vba_choropleth,
    vba_legend,
)
