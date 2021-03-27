# GeoData_WS2020_II_Final_Group_Jonas

### Part 1: Correlation of Mean Annual Temperature with Altitude in Bavaria

#### Task 1:
Plot the annual mean temperatures of years 2017, 2018, and 2019 versus altitude for the DWD stations in Bavaria. At first use the altitudes from the station description file.

* Gathering FTP directory listings and query the description file for the required options:
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
    * Verwaltungsgebiete, Maßstab 1:25000, EPSG:25832
        http://www.geodaten.bayern.de/opendata/Verwaltungsgebiete_shp_epsg25832.zip<br>
        Metadaten: https://geoportal.bayern.de/geoportalbayern/anwendungen/details?0&resId=bf9ff4ed-62c7-4935-9318-d5251108acc3<br>
        Regierungsbezirke Bayern: regbez_ex.shp