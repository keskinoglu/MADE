# Project Plan

## Title
<!-- Give your project a short title. -->
Beer or Wine: the impact of climate change on upper Franconia's wine region

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Can upper Franconia produce more wine due to warmer weather?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Despite the negative effects of climate change, some wine varietals thrive in warmer climates. For instance, Bamberg, once a wine-producing region, could potentially regain its status due to rising temperatures. Analyzing climate data and comparing it to historical weather patterns will provide valuable insights.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Deutscher Wetterdienst (DWD)
* Metadata URL: https://cdc.dwd.de/portal/202209231028/mapview
* Data URL: https://cdc.dwd.de/portal/202209231028/mapview
* Data Type: CSV

This data is from the German weather service and collects temperature data from nodes throughout Germany, leading to accurate and local surface temperature on an hourly, daily, monthly and annually aggregated basis.

### Datasource2: Michael E. Mann Study
* Metadata URL: https://www.science.org/doi/suppl/10.1126/science.1177303/suppl_file/mann.som.pdf
* Data URL: https://www.science.org/doi/suppl/10.1126/science.1177303/suppl_file/multiproxyspatial09.zip
* Data Type: CSV

This data is from a 2009 study which used proxy data from around the world to estimate surface temperature from 500 A.D. to the mid-19th century.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Collect necessary data from Datasource1: Deutscher Wetterdienst (DWD) [#1][i1]
2. Understand and extract Datasource2: Michael E. Mann Study [#2][i2]
3. Connect the two data into a single time series for analysis [#3][i3]
4. Optimum temperatures for the current wine produced in the region [#4][i4]
5. Compare the pre- little ice age period to the current temperatures [#5][i5]

[i1]: https://github.com/keskinoglu/MADE/issues/1
[i2]: https://github.com/keskinoglu/MADE/issues/2
[i3]: https://github.com/keskinoglu/MADE/issues/3
[i4]: https://github.com/keskinoglu/MADE/issues/4
[i5]: https://github.com/keskinoglu/MADE/issues/5