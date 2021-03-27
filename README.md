# GeoData_WS2020_II_Final_Group_Jonas

## Part 1: Correlation of Mean Annual Temperature with Altitude in Bavaria

### Task 1:
* Gathering FTP directory listings and query the description file for the required options:
    * Yearly average temperature data
    * Years 2017-2019 available
    * For the state Bavaria

* Downloading relevant station zip archives, unzip product files, add station_id, yearly average temperature of relevant years to dataframes, merge altitudes, geolocation and name and plot yearly average temperatures vs station altitude for each year

* Found in: Part_1_query_download_plot.ipynb

* Exports:
    * df_station_desc_query.csv
    * df_ftp_dir_query.csv
    * df_all.csv
    * png image of ploted data

### Task 2:
* Files:
    * DTM of Bavaria with 50m horizontal resolution in EPSG:25852 as GeoTiff: http://www.geodaten.bayern.de/opendata/DGM50_UTM32/dgm50_epsg25832.tif
    * Verwaltungsgebiete, Maßstab 1:25000, EPSG:25832
        http://www.geodaten.bayern.de/opendata/Verwaltungsgebiete_shp_epsg25832.zip<br>
        Metadaten: https://geoportal.bayern.de/geoportalbayern/anwendungen/details?0&resId=bf9ff4ed-62c7-4935-9318-d5251108acc3<br>
        Regierungsbezirke Bayern: regbez_ex.shp