---
title: 'splot: Visual Analytics for Spatial Statistical Analysis in PySAL'
tags:
  - Python
  - visualization
  - spatial analysis
  - spatial statistics
authors:
  - name: Stefanie Lumnitz
    orcid: 0000-0002-7007-5812
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Author 2
    orcid: 0000-0000-0000-0000
    affiliation: 2
affiliations:
 - name: University of British Columbia
   index: 1
 - name: Spatial Sciences Center, University of California Riverside
   index: 2
date: 13 August 2017
bibliography: paper.bib
---

# Summary

* contains statement of need
* introduction to package
* maybe quick example

Geography is an intensely-visual domain. Its longstanding dependence on visualisation and cartography show as much, with John Snow’s cholera map serving as one of the first instances of scientific visualization in pursuit of data analysis [@johnson2007ghost,@Arribas-Bel2017], and the perennial presence of maps as statistical displays in seminal works on visualization [@tufte2001visual]. As such, the existence and continued focus on maps in geographical analysis demands serious, dedicated attention in scientific computing. However, existing methods in Python, specifically for *statistical* visualization of spatial data, are somewhat lacking. General-purpose mapping provided by `geopandas` is not fine-tuned enough for analytical/statistical analysis. The more analytically-oriented views offered by `geoplot`, while useful, are limited in their statistical applications. Thus, the need remains for a strong, analytically-oriented toolbox for geographical analysis.

This need is explicitly heightened by the fact that the collection and generation of geographical data is becoming more pervasive [@goodchild2007citizen,@arribas-bel2014accidental]. With the proliferation of high-accuracy GPS data, many datasets are now *becoming* spatial datasets; their analysis and visualization increasingly requires explicitly spatial methods that account for the various special structures in geographical data [@anselin1988spatial]. Geographical questions about dependence, endogeneity, heterogeneity, and non-stationarity often require special statistical tools to diagnose, and spatial analytic software to visualize [@anselin2014modern]. Further with the increasing importance of code and computation in geographical curricula [@rey2009show,@rey2018code,@ucgis2019geographic], it has become critical for both pedagogical and research reasons to support geographical analysis with robust visualization tools.  

HELP NEEDED: idea collection for statement of need
* paragraph3: splot as solution, this is what we can do for different audiences

It is this niche that `splot` is designed to fill. As a visual steering tool, `splot` facilitates analysis, interpretation of results, and makes the process of model selection easier and more clear. 

* paragraph4: more technical description

Implemented in Python, splot extends both PySAL's analytics and matplotlib visualization functionality in visualising spatial analysis workflows and result presentation. It provides users quick access through a high level API to visualise popular PySAL objects. We hereby aim to implement a multitude of views for different spatial analysis workflows, to provide users the opportunity to view a problem from different angles. The splot package facilitates the creation of both static plots ready for publication and interactive visualisations for quick iteration and spatial data exploration. 

* paragraph 5: concluding sentence, what follows



# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

# Figures

Figures can be included like this: ![Example figure.](figure.png)

# Acknowledgements

We acknowledge contributions from XYZ
Thank you, Joris Van den Bossche and the geopandas team to time releases in accordance to splot delevopments.
Thank you, Rebecca Bilbro and Benjamin Bengfort for sharing your insights in how to structure and build API's for visualizations.

### References