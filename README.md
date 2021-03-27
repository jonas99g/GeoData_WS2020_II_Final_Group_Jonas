# GeoData_WS2020_II_Final_Group_Jonas

### Part 1: Correlation of Mean Annual Temperature with Altitude in Bavaria

#### Task 1:
Plot the annual mean temperatures of years 2017, 2018, and 2019 versus altitude for the DWD stations in Bavaria. At first use the altitudes from the station description file.

* Gathering FTP directory listings

* Query the description file for the required options:
    * Annual mean temperature data
    * Years 2017-2019 available
    * For the state Bavaria

* Downloading relevant station zip archives, unzip product files, add station_id, annual mean temperature of relevant years to dataframes, merge altitudes, geolocation and name and plot yearly average temperatures vs station altitude for each year

* Found in: Part_1_query_download_plot.ipynb

* Exports:
    * df_station_desc_query.csv
    * df_ftp_dir_query.csv
    * df_all.csv
    * png image of ploted data

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
    * Screenshot from map as label: osm_label.png
    * Station dataset: df_all.csv

* Application requirements:
    * QGIS 3 (3.18 used)
    * Plugins:
        * QuickMapServices (Open Street Maps)

* Found in Project file: DTM.qgz
    * Creating QGIS project
    * Setting CRS in project properties to ETRS89 / UTM zone 32N / EPSG:25832
    * Import OpenTopoMap by using QuickMapServices (These are live cached OSM raster tiles)
    * Adding dgm50_epsg25832.tif as raster layer
    * Adding bayern_ex.shp as vector layer
    * Use Raster - Extraction - Clip Raster by Extent (Input: dgm50_epsg25832, Clipping extent: bayern_ex, Clipped extent: dgm50_epsg25832_clipped.tif)
    * Hide dgm50_epsg25832 and bayern_ex
    * Adding regbez_ex.shp as vector layer and change appearance like outline blue
    * Adding a delimeted text layer from df_all.csv with CRS EPSG:4326 WGS 84 and change appearance to red points, choose label to display station_id, add white sourrounding to text and a dark shadow to make it easier to read
    * 


* Map template file: DTM_Bavaria.qpt

* Exports:
    * map_dtm50_bavaria_dwd_station_2017_2019_annual_mean_temperature_100dpi.pdf
    * dgm50_epsg25832_clipped.tif
    * DTM.qgz
    * DTM_Bavaria.qpt


#### Task 3:
Sample the DTM at the locations of the DWD stations.

* Files:
    * DTM.qgz
    * dgm50_epsg25832_clipped.tif
    * df_all.csv

Open previous QGIS project DTM.qgz.
Using Processing - Toolbox - Raster Analysis - Sample Raster Values to sample the altitude values from dgm50_epsg25832_clipped.tif at station geopositions and store them as a new field in df_all_dgm50 and export this new layer as df_all_dgm50.csv

* Exports:
    * df_all_dgm50.csv

Compare the original altitudes from the DWD station file to the heights derived from the DTM. Where and why are the strongest deviations?

* Files:
    * DTM.qgz
    * dgm50_epsg25832_clipped.tif
    * df_all.csv
