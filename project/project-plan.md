# Project Plan

## Title
<!-- Give your project a short title. -->
Beer or Wine: the impact of climate change on Bamberg's vineyards

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Can Franconia's wine region now include Bamberg due to warmer weather?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Despite the negative effects of climate change, some wine varietals thrive in warmer climates. For instance, Bamberg, once a wine-producing region, could potentially regain its status due to rising temperatures. Analyzing climate data from nearby Würzburg, at the heart of the Franconian winemaking region, will yield results.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Deutscher Wetterdienst (DWD) Station 282 Bamberg
* Metadata URL: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/monthly/kl/historical/DESCRIPTION_obsgermany_climate_monthly_kl_historical_en.pdf
* Data URL: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/monthly/kl/historical/monatswerte_KL_00282_18810101_20231231_hist.zip
* Data Type: TXT

This data is from the German weather service DWD at node 282 in Bamberg. We'll be using the air temperature monthly aggregate from 1949 - 2024.

### Datasource2: Deutscher Wetterdienst (DWD) Station 5705 Würzburg
* Metadata URL: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/monthly/kl/historical/DESCRIPTION_obsgermany_climate_monthly_kl_historical_en.pdf
* Data URL: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/monthly/kl/historical/monatswerte_KL_05705_18810101_20231231_hist.zip
* Data Type: TXT

This data is from the German weather service DWD at node 5705 in Würzburg. We'll be using the air temperature monthly aggregate from 1949 - 2024.

### Datasource Header Information
* Metadata on header info URL: https://wetterdienst.readthedocs.io/en/latest/data/coverage/dwd/observation/monthly.html
* Metadata on DWD more broadly URL: https://opendata.dwd.de/climate_environment/CDC/Readme_intro_CDC_ftp.pdf

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