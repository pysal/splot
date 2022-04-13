# Changes

# Version 1.1.5 (2022-04-13)

Minor patch release.

- [BUG] set viz defaults for LineStrings in lisa_cluster (#140)
- Import ABC from collections.abc for Python 3.10 compatibility. (#150)

The following individuals contributed to this release:

- Stefanie Lumnitz
- James Gaboardi
- Martin Fleischmann
- Karthikeyan Singaravelan

# Version 1.1.4 (2021-07-27)

We closed a total of 39 issues (enhancements and bug fixes) through 12 pull requests, since our last release on 2020-03-23.

## Issues Closed

- Streamline & upgrade CI (#135)
- update conf.py (#134)
- Migrating testing & coverage services (#124)
- [MAINT] rename 'master' to 'main' (#121)
- ipywidgets dependency (#130)
- REF: make ipywidgets optional dependency (#132)
- [WIP] update testing procedure with new datasets (#133)
- MatplotlibDeprecationWarning from ax.spines[label].set_smart_bounds() (#115)
- [DOC] include libpysal.example api changes & reinstall splot for testing (#128)
- [MAINT] remove `.set_smart_bounds()` (#125)
- Gha testing (#126)
- GitHub Actions for continuous integration (#111)
- [MAINT] change in`pandas.isin()` affecting `plot_local_autocorrelation` (#123)
- [BUG] enforce dtype in `mask` in `plot_local_autocorrelation()` (#122)
- [MAINT] AttributeError: 'NoneType' object has no attribute 'startswith' in all Moran plots (#117)
- [BUG] 'color' and 'c' in `test_viz_giddy_mpl.test_dynamic_lisa_vectors` (#116)
- [MAINT] update links to Guerry dataset in `_test_data()` (#119)
- [BUG] Build failing due to change in Seaborn (#110)
- [BUG] pin seaborn to v0.10.0 for testing new functionality (#114)
- Topological colouring (#94)
- vba_choropleth --> ValueError: Invalid RGBA argument: (#100)
- Pyviz affiliation (#75)
- BUG: Bokeh needed for testing (#107)
- [JOSS] add Joss badge to README.md (#106)
- [JOSS] doi reference correction (#105)
- Fixing BibTeX entry pages. (#104)
- Release1.1.3 (#103)

## Pull Requests

- Streamline & upgrade CI (#135)
- REF: make ipywidgets optional dependency (#132)
- [DOC] include libpysal.example api changes & reinstall splot for testing (#128)
- [MAINT] remove `.set_smart_bounds()` (#125)
- Gha testing (#126)
- [BUG] enforce dtype in `mask` in `plot_local_autocorrelation()` (#122)
- [MAINT] update links to Guerry dataset in `_test_data()` (#119)
- BUG: Bokeh needed for testing (#107)
- [JOSS] add Joss badge to README.md (#106)
- [JOSS] doi reference correction (#105)
- Fixing BibTeX entry pages. (#104)
- Release1.1.3 (#103)

The following individuals contributed to this release:

- Stefanie Lumnitz
- James Gaboardi
- Martin Fleischmann
- Dani Arribas-Bel
- Serge Rey
- Arfon Smith

# Version 1.1.3 (2020-03-18)

We closed a total of 15 issues (enhancements and bug fixes) through 6 pull requests, since our last release on 2020-01-18.

## Issues Closed

- add permanent links to current version of no's to joss paper (#102)
- [BUG] set colors as list in _plot_choropleth_fig() (#101)
- Remove the links around figures in the JOSS paper (#99)
- Release prep for 1.1.2 (#98)
- Installation instructions; pip install fails on macOS (#88)
- Usage in readme is a fragment (#90)
- JOSS: missing figure captions (#92)
- [DOC] update installation instruction (#96)
- [DOC] add example links to README.md & figure captions in joss article (#97)

## Pull Requests

- add permanent links to current version of no's to joss paper (#102)
- [BUG] set colors as list in _plot_choropleth_fig() (#101)
- Remove the links around figures in the JOSS paper (#99)
- Release prep for 1.1.2 (#98)
- [DOC] update installation instruction (#96)
- [DOC] add example links to README.md & figure captions in joss article (#97)

The following individuals contributed to this release:

- Stefanie Lumnitz
- Levi John Wolf
- Leonardo Uieda
- Serge Rey

# Version 1.1.2 (2020-01-18)

We closed a total of 33 issues (enhancements and bug fixes) through 13 pull requests, since our last release on 2019-07-13.

## Issues Closed

- Installation instructions; pip install fails on macOS (#88)
- Usage in readme is a fragment (#90)
- JOSS: missing figure captions (#92)
- [DOC] update installation instruction (#96)
- [DOC] add example links to README.md & figure captions in joss article (#97)
- [BUG] vba_choropleth failure (#83)
- BUG: Fix breakage due to mapclassify deprecation (#95)
- addressing pysal/pysal#1145 & adapting testing examples (#93)
- Fix docstring for plot_spatial_weights (#89)
- JOSS paper submission (#59)
- Fix format for multiple citations in JOSS paper (#87)
- Joss paper, finalise title (#86)
- [JOSS] work on `paper.md` (#62)
- [ENH] change doc badge to latest doc (#85)
- [BUG] require geopandas>=0.4.0,<=0.6.0rc1 for vba_choropleth testing (#84)
- `plot_moran_simulation` weird dimensions (#82)
- Colors are not fixed is LISA maps (#80)
- Release 1.1.1 (#79)
- add ipywidgets to requirements_dev.txt (#78)
- add descartes to `requirements.txt` (#77)

## Pull Requests

- [DOC] update installation instruction (#96)
- [DOC] add example links to README.md & figure captions in joss article (#97)
- BUG: Fix breakage due to mapclassify deprecation (#95)
- addressing pysal/pysal#1145 & adapting testing examples (#93)
- Fix docstring for plot_spatial_weights (#89)
- Fix format for multiple citations in JOSS paper (#87)
- Joss paper, finalise title (#86)
- [JOSS] work on `paper.md` (#62)
- [ENH] change doc badge to latest doc (#85)
- [BUG] require geopandas>=0.4.0,<=0.6.0rc1 for vba_choropleth testing (#84)
- Release 1.1.1 (#79)
- add ipywidgets to requirements_dev.txt (#78)
- add descartes to `requirements.txt` (#77)

The following individuals contributed to this release:

- Stefanie Lumnitz
- Serge Rey
- James Gaboardi
- Martin Fleischmann
- Leonardo Uieda
- Levi John Wolf
- Wei Kang

# Version 1.1.1 (2019-07-13)

We closed a total of 8 issues (enhancements and bug fixes) through 4 pull requests, since our last release on 2019-06-27.

## Issues Closed

- add ipywidgets to requirements_dev.txt (#78)
- add descartes to `requirements.txt` (#77)
- [ENH] read long_description from README.md (#76)
- Rel1.1.0 (#74)

## Pull Requests

- add ipywidgets to requirements_dev.txt (#78)
- add descartes to `requirements.txt` (#77)
- [ENH] read long_description from README.md (#76)
- Rel1.1.0 (#74)

The following individuals contributed to this release:

- Stefanie Lumnitz
- Levi John Wolf

# Version 1.1.0 (2019-06-27)

We closed a total of 54 issues (enhancements and bug fixes) through 21 pull requests, since our last release on 2018-11-13.

## Issues Closed

- LISA cluster map colours mixed when cluster value not present (#72)
- [ENH] select colour by presence of value in list in `mask_local_auto` (#73)
- Moran Scatterplots with equal bounds on X and Y axes? (#51)
- Add aspect_equal argument to Moran functionality (#70)
- set up dual travis tests for pysal dependencies (pip and github)  (#69)
- API changes of mapclassify propagate to splot (#65)
- [DOC] include rtree and descartes in `requirements_dev.txt` (#68)
- Readme update (#67)
- docs building using readthedocs.yml version 2 (#64)
- [DOC] add test for missing code cove % (#57)
- Add tests for warnings and ValueErrors (#61)
- Update travis for testing (#1)
- travis ci testing: migrate from 3.5 and 3.6 to 3.6 and 3.7 (#63)
- create paper directory (#58)
- clean and rerun notebooks (#56)
- `vba_choropleth` API (#45)
- allow string (default) in vba_choropleth function of tests (#52)
- migrating to readthedocs II (#54)
- migration to readthedocs (#53)
- Make docs (#46)
- Segmentation fault in running tests on TravisCI (#47)
- code 139 memory segmentation fault: RESOLVED (#48)
- pip install on linux fails on pyproj (#41)
- update archaic Miniconda build (#44)
- adjusting markdown font (#43)
- add `moran_facette` functionality and merge `esda.moran` plots to `moran_scatterplot` (#27)
- (ENH) speed up plot_spatial_weights for plotting spatial weights (#42)
- Travis testing against esda and giddy master branch (#31)
- 1.0.0 Release (#40)
- merge Sprint with master branch (#39)
- Change documentation style (#38)
- add travis build badge to README.md (#37)
- fix current documentation for sprint (#36)

## Pull Requests

- [ENH] select colour by presence of value in list in `mask_local_auto` (#73)
- Add aspect_equal argument to Moran functionality (#70)
- set up dual travis tests for pysal dependencies (pip and github)  (#69)
- Readme update (#67)
- docs building using readthedocs.yml version 2 (#64)
- Add tests for warnings and ValueErrors (#61)
- travis ci testing: migrate from 3.5 and 3.6 to 3.6 and 3.7 (#63)
- create paper directory (#58)
- clean and rerun notebooks (#56)
- allow string (default) in vba_choropleth function of tests (#52)
- migrating to readthedocs II (#54)
- migration to readthedocs (#53)
- Make docs (#46)
- code 139 memory segmentation fault: RESOLVED (#48)
- update archaic Miniconda build (#44)
- adjusting markdown font (#43)
- (ENH) speed up plot_spatial_weights for plotting spatial weights (#42)
- 1.0.0 Release (#40)
- merge Sprint with master branch (#39)
- Change documentation style (#38)
- fix current documentation for sprint (#36)

The following individuals contributed to this release:

- Stefanie Lumnitz
- Wei Kang
- James Gaboardi
- Renanxcortes
- Dani Arribas-Bel

# Version 1.0.0 (2018-11-30)

We closed a total of 52 issues (enhancements and bug fixes) through 23 pull requests, since our last release on 2017-05-09.

## Issues Closed

- merge Sprint with master branch (#39)
- Change documentation style (#38)
- add travis build badge to README.md (#37)
- fix current documentation for sprint (#36)
- `value_by_alpha` prototype (#28)
- Clean up of current code base (#30)
- Value By Alpha specification (#24)
- nonplanar example update (#33)
- add README.md (#29)
- issues in some docstrings for giddy (#26)
- debug `splot` documentation (#25)
- collection of cleanups for`splot.giddy`  (#23)
- created `esda.moran.Moran_Local_BV` visualisations (#20)
- add `esda.moran.Moran_BV` visualizations to `splot.esda` (#18)
- add `seaborn` and `matplotlib` to `install_requirements` in `setup.py` (#19)
- prototype `moran_scatterplot()`, `plot_moran_simulation()` and `plot_moran()` for `esda` (#17)
- include utility functions `shift_colormap` and `truncate_colormap` (#15)
- fix setup.py so files are installed with "pip install ." (#16)
- `plot_spatial_weights` including network joins for `non_planar_joins` (#14)
- adapting existing `esda` functionality to `splot.esda` namespace and allow `.plot()` method (#13)
- adding license (#4)
- add `giddy` dynamic LISA functionality under `splot.giddy` (#11)
- start sphinx html documentation (#12)
- add visualization option with significance to mplot (#7)
- Visualising Local Autocorrelation (#8)
- Copy new changes made to viz module into split (#5)
- run 2to3 for splot (#6)
- Fix for Pysal#930 (#3)
- Add a Gitter chat badge to README.md (#2)

## Pull Requests

- merge Sprint with master branch (#39)
- Change documentation style (#38)
- fix current documentation for sprint (#36)
- `value_by_alpha` prototype (#28)
- Clean up of current code base (#30)
- add README.md (#29)
- debug `splot` documentation (#25)
- collection of cleanups for`splot.giddy`  (#23)
- created `esda.moran.Moran_Local_BV` visualisations (#20)
- add `esda.moran.Moran_BV` visualizations to `splot.esda` (#18)
- add `seaborn` and `matplotlib` to `install_requirements` in `setup.py` (#19)
- prototype `moran_scatterplot()`, `plot_moran_simulation()` and `plot_moran()` for `esda` (#17)
- include utility functions `shift_colormap` and `truncate_colormap` (#15)
- fix setup.py so files are installed with "pip install ." (#16)
- `plot_spatial_weights` including network joins for `non_planar_joins` (#14)
- adapting existing `esda` functionality to `splot.esda` namespace and allow `.plot()` method (#13)
- add `giddy` dynamic LISA functionality under `splot.giddy` (#11)
- start sphinx html documentation (#12)
- add visualization option with significance to mplot (#7)
- Visualising Local Autocorrelation (#8)
- run 2to3 for splot (#6)
- Fix for Pysal#930 (#3)
- Add a Gitter chat badge to README.md (#2)

The following individuals contributed to this release:

- Stefanie Lumnitz
- Dani Arribas-Bel
- Levi John Wolf
- Serge Rey
- Thequackdaddy
- Jsignell
- Serge
