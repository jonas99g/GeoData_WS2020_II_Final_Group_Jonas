# GeoData_WS2020_II_Final_Group_Jonas

### Part 1: Correlation of Mean Annual Temperature with Altitude in Bavaria
 * Folder: Part_1

#### Task 1:
Plot the annual mean temperatures of years 2017, 2018, and 2019 versus altitude for the DWD stations in Bavaria. At first use the altitudes from the station description file.

* Application requirements (base ipynb):
    * ipynb application (Visual Studio Code, jupyter extention)
    * Python 3.9.2
    * ftplib
    * zipfile
    * numpy
    * matplotlib
    * pandas

* Gathering FTP directory listings

* Query the description file for the required options:
    * Annual mean temperature data
    * Years 2017-2019 available
    * For the state Bavaria

* Downloading relevant station zip archives, unzip product files, add station_id, annual mean temperature of relevant years to dataframes, merge altitudes, geolocation and name and plot yearly average temperatures vs station altitude for each year

* Found in: Task_1_query_download_plot.ipynb

* Exports:
    * df_station_desc_query.csv
    * df_ftp_dir_query.csv
    * df_all.csv
    * bavaria_dwd_altitude_vs_annual_mean_temperature_2017_2019_plot.png
    * bavaria_dwd_altitude_vs_annual_mean_temperature_2017_2019_plot_woo.png
    * bavaria_dwd_altitude_vs_annual_mean_temperature_2017_2019_plot_woo_na.png

#### Task 2:
Create a decent map (including title, alnnotations, scale, north arrow, etc.) with all DWD temperature stations in Bavaria which were active in the years of concern (2017, 2018, 2019). Label the stations with their station id (number). Use the DTM as background information. Use the DTM in the background. Try to find the digital administrative boundaries of Bavaria and overlay the disctrict boundaries as well as the boundary of the federal state. Crop the DTM to the boundary of Bavaria precisely.

* Files:
    * DTM of Bavaria with 50m horizontal resolution in EPSG:25852 as GeoTiff: http://www.geodaten.bayern.de/opendata/DGM50_UTM32/dgm50_epsg25832.tif
        dgm50_epsg25832.tif
    * Verwaltungsgebiete, scale 1:25000, EPSG:25832
        http://www.geodaten.bayern.de/opendata/Verwaltungsgebiete_shp_epsg25832.zip<br>
        Metadaten: https://geoportal.bayern.de/geoportalbayern/anwendungen/details?0&resId=bf9ff4ed-62c7-4935-9318-d5251108acc3<br>
        District boundries: regbez_ex.shp
        Federal state boundries: bayern_ex.shp
        Extracted to Verwaltungsgebiete_shp_epsg25832 folder

    * Screenshot from map as label: opentopomap_label.png
    * Station dataset: df_all.csv

* Application requirements:
    * QGIS 3 (3.19.0-Master 7f2c7c83302 used) [Living on the edge ;D]
    * Plugins:
        * QuickMapServices (Open Street Maps)
        * Easy Raster Splitter

* Found in Project file: DTM.qgz
    * Creating QGIS project
    * Setting CRS in project properties to ETRS89 / UTM zone 32N / EPSG:25832
    * Import OpenTopoMap by using QuickMapServices (These are live cached OSM raster tiles)
    * Adding dgm50_epsg25832.tif as raster layer
    * Adding bayern_ex.shp as vector layer from Verwaltungsgebiete_shp_epsg25832 folder
    * Use Easy Raster Splitter Plugin: Input: dgm50_epsg25832, Input polygon data: bayern_ex, Output name: dgm50_epsg25832_clipped and press ok
    * Add exported dgm50_epsg25832_clipped.tif as raster layer
    * Hide dgm50_epsg25832 and bayern_ex
    * Adding regbez_ex.shp as vector layer from Verwaltungsgebiete_shp_epsg25832 folder and change appearance like outline blue
    * Adding a delimeted text layer from df_all.csv with CRS EPSG:4326 WGS 84 and change appearance to red points, change to points size, choose single label to display station_id, #ee0000 red 9 points text, add #ffffff white 0.3 points buffer to text and a black shadow to make it easier to read
    * Click New Print Layout to create a map
    * Name: DTM50
    * Export resolution 100 dpi
    * Add Map, Interactively adjust position, Scale: 1850000
    * Add north arrow to top right of map
    * Add scale to bottom right
    * Add Label and type the heading for the map
    * Add legend, under legend idems uncheck auto update, remove unused layers, rename layers to full names
    * Add Raster Image opentopomap_label.png in front of Open Topo Map legend item
    * Export to pdf


* Map template file: DTM_Bavaria.qpt

* Exports:
    * map_dgm50_bavaria_dwd_station_2017_2019_annual_mean_temperature_100dpi.pdf
    * dgm50_epsg25832_clipped.tif
    * DGM50.qgz
    * DGM50_map.qpt


#### Task 3:
Sample the DTM at the locations of the DWD stations.

* Files:
    * DGM50.qgz
    * dgm50_epsg25832_clipped.tif
    * df_all.csv

Open previous QGIS project DGM50.qgz.
Using Processing - Toolbox - Raster Analysis - Sample Raster Values to sample the altitude values from dgm50_epsg25832_clipped at station geopositions and store them as a new field without prefix in temporary layer
Rename to df_all_dgm50 and export this layer as df_all_dgm50.csv with save features as csv in EPSG:4326

* Exports:
    * df_all_dgm50.csv

Compare the original altitudes from the DWD station file to the heights derived from the DTM. Where and why are the strongest deviations?

* Files:
    * df_all_dgm50.csv

* Software requirements:
    * scikit-learn

* Found in: Task_3_altitude_dwd_vs_dgm50.ipynb

* Exports:
    * dgm_50_sampled_altitude_vs_dwd_altitude_plot.png
    * dgm_50_sampled_altitude_vs_dwd_altitude_lr_woo.png
    * dgm_50_sampled_altitude_vs_dwd_altitude_lr.png



#### Task 4:
Plot the mean annual temperatures versus the DTM heights for the DWD stations in Bavaria. Do you find a ways to perform a linear regression to the data with numpy? What is the temperature gradient, i.e. the slope of the regression line in units K/m or °C/m?

* Application requirements in addition to base ipynb:
    * sklearn

* Files:
    * df_all_dgm50.csv

* Found in: Task_4_amt_vs_dgm50_regression.ipynb

* Exports:
    * bavaria_dgm50_altitude_vs_annual_mean_temperature_2017_2019_plot_lr.png

### Part 2:
 * Folder: Part_2

Produce a video on DWD hourly precipitation data by means of QGIS Time Manager.
Produce your own video for BAVARIA by applying the processing chain to a period of 40 days covering an interesting rain event in 2017. You have to use the historical hourly precipitation data in 2017. Find an interesting sequence of rain events first by plotting a few time series.

* historical
* hourly precipitation
* 2017
* df time series

* Found in:
    * time_series.ipynb