# EE_3.07 Geodata Management Systems - Final Assignment


## 0. General Remarks

1. Due date is **2021-03-21**. 
1. You do not have to write a formal report but you have to sketch the steps you have taken to do the analyses. Your documentation has to enable us to redo your work completely again! 
1. Use your own GitLab repository to document your work. THIS IS MANDATORY! Use a `REAMDE.md` file (and more .md-files, if needed) to describe your work. Upload your Python scripts as well as QGIS projects without large datasets to the repository.
1. Use Jupyter Notebook markdown cells to describe your Python code. 
1. You have to produce a presentation (Powerpoint or similar) and upload it to your Git repo. 
1. In the second or third week in March you have to give a **live presentation in the class** (in a video conference) so that I can assess better if you understood what you did. **The date will be announced.** 
1. You can work in groups of 1 - 3 students. You can do the group assignments in our Moodle course.
1. Create your own repo on the **University Gitlab server: https://git.hsrw.eu/**. <br>**USE THE FOLLWING REPO NAME:** `GeoData_WS2020_II_Final_<Group ID>`, (e.g. GeoData_WS2020_II_Final_Group_Z). (We still have a technical problem with the upload size but we will fix it).
1. I will clone your Gitlab repo at the end of deadline. That will be the main basis of my assessment.


## 1. Correlation of Mean Annual Temperature with Altitude in Bavaria

In the first lectures we analysed the annual temperature in NRW by means of long time series. The observed temperature increase particularly in the last decade is most likely an indication of climate. We also observed that the station "Kahler Asten" shows systematic lower temperatures than other stations. We presumed this being an effect of decreasing temperature with topographic height, since "Kahler Asten" is among the highest points in NRW. 

Verify this hypothesis by means of data in Bavaria. This federal state reveals the broadest range of topographic heights, from 100m to more than 2800m above Normal-Null (NN). 

**Task 1:** <br>
Plot the annual mean temperatures of **years 2017, 2018, and 2019** versus altitude for the DWD stations in Bavaria. At first use the **altitudes from the station description file** `KL_Jahreswerte_Beschreibung_Stationen.txt` for the data set `/annual/kl/historical/`.

**Task 2:** <br>
The DTM of Bavaria with 50m horizontal resolution in EPSG:25852 as GeoTiff (500 MB!) can be doenloaded here: \\
http://www.geodaten.bayern.de/opendata/DGM50_UTM32/dgm50_epsg25832.tif

Create a decent map (including title, alnnotations, scale, north arrow, etc.) with all DWD temperature stations in Bavaria which were active in the years of concern (2017, 2018, 2019). Label the stations with their station id (number). Use the DTM as background information. Use the DTM in the background. Try to find the digital administrative boundaries of Bavaria and overlay the disctrict boundaries as well as the boundary of the federal state. Crop the DTM to the boundary of Bavaria precisely.


**Task 3:** <br>
Sample the DTM at the locations of the DWD stations.

Use the QGIS Processing Toolbox to do so. Use the dialog *Sample Raster Values* from the *Raster Analysis Toolbox*.
Selecting the menu item *Processing -> Toolbox* toggles the visibility of the Toolbox pane. From this select *Raster Analysis*.

Add another field to the DWD stations attribute table with the altitudes sampled from the DTM. Compare the original altitudes from the DWD station file to the heights derived from the DTM. Where and why are the strongest deviations? 

**Task 4:** <br>
Plot the mean annual temperatures versus the DTM heights for the DWD stations in Bavaria. Do you find a ways to perform a linear regression to the data with numpy? What is the temperature gradient, i.e. the slope of the regression line in units K/m or °C/m?


## 2. DWD Precipitation Measurements in Bavaria: Create Movie with QGIS Time Manager

The first task for you will be to produce a video on **DWD hourly precipitation data** by means of QGIS Time Manager. 
Have a look at the sample video on YouTube showing the temporal precipitation development in NRW for May 2019:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=fdCQBbzyD84
" target="_blank"><img src="http://img.youtube.com/vi/fdCQBbzyD84/0.jpg" 
alt="QGIS Time Manager: DWD Precipitation Data for NRW" width="300" border="10" /></a>

_Fig.: YouTube video showing the temporal evolution of DWD precipitation data in NRW for May 2019._

THe processing chain consisting of Python code and QGIS project to create the video is found in the Git folder [**gdms0350_DWD_Stations_and_TS_for_TM_soln**](../gdms0350_DWD_Stations_and_TS_for_TM_soln/)

**Task 1:** <br> 
Produce your own video **for BAVARIA** by applying the processing chain to a period of **40 days** covering an **interesting rain event in 2017**. You have to use the **historical hourly precipitation data in 2017**. Find an interesting sequence of rain events first by plotting a few time series. 


## 3. Compare NDVI for Two Different Years

In the last lectures, we talked about remote sensing and how we could use satellite data (Sentinel-2) to obtain information about the earth’s surface based on the spectral properties (i.e. spectral reflectance) of materials such as vegetation and soil without being in contact with the surface itself. We discussed how normalized difference vegetation index (NDVI) can be used to assess the plant´s ability to absorb solar radiation and use this to characterize the plant’s health.
Your task is to analyse the NDVI in the summer periods (May-June) of the years 2018 and 2019 in your own regions of interest (ROI). Define your own ROIs by creating polygons delineating areas with one landuse class per polygon. You should create at least one polygon for each of the following landuse classes:
* Forest
* Water
* Crop Field
* Grassland (not artificially irrigated)
* Urban Area

To save time we identified five Sentinel products atmospherically corrected (Level 2A) and with low cloud coverage. Select (at least) **two appropriate satellite scenes** from the following list covering both years 2018 and 2019. Download and store them in an appropriate folder. 
 
| Date | Product’s name | Link |
| :---:  | :---: | :---: |
| 2018-06-30 | S2A_MSIL2A_20180630T105031_<br>N0208_R051_T31UGT_20180630T144133.SAFE | https://scihub.copernicus.eu/dhus/odata/v1/Products('2cdf37bf-5541-464c-8181-9069d80447c4')/$value | 
| 2018-05-11 | S2A_MSIL2A_20180511T105031_<br>N0207_R051_T32ULC_20180511T111332.SAFE | https://scihub.copernicus.eu/dhus/odata/v1/Products('57afb6dc-f32b-4b7b-8d54-d655251a0d5e')/$value | 
| 2018-04-06 | S2B_MSIL2A_20180406T105029_<br>N0207_R051_T32ULC_20180406T125448.SAFE | https://scihub.copernicus.eu/dhus/odata/v1/Products('4edd776f-276b-4f5d-98f9-0ef7b18aa138')/$value |
| 2019-06-27 | S2B_MSIL2A_20190627T104029_<br>N0212_R008_T31UGT_20190627T135004.SAFE | https://scihub.copernicus.eu/dhus/odata/v1/Products('bb9423ca-e076-41aa-830d-6afa8661df89')/$value |
| 2019-05-13 | S2A_MSIL2A_20190513T104031_<br>N0212_R008_T32ULC_20190513T134155.SAFE| https://scihub.copernicus.eu/dhus/odata/v1/Products('1bdaa4fe-84d8-44e0-8832-fe0e286959f6')/$value |

What does the difference of NDVI tell you for each polygon? Is NDVI enough to classify the different landuses?  
Notice that one polygon might contain more than one NDVI value (more than 1 pixel). So in order to estimate the NDVI for the whole area, you can calculate the statistical mean. 
(Optional task) Try calculating a different spectral index for the same polygons. For which polygons is this spectral index appropriate? Compare this with your NDVI results. 

**ATTENTION: Some of you have already chosen a different approach. This is totally acceptable!** We just want you to analyse Sentinel-2 images with respect to NDVI and its changes over time (here: only two years) as well as to reflect power and limitations of remote sensing.


## 4. Digitization: Burial Mounds in Uedemer Hochwald

<img src="images/Burial_Mounds.png" alt="Burial Mounds Map" width="600" border="10" /><br>
*Fig.: Burial mounds in Uedemer Hochwald.*

South west of the village Marienbaum (belongs to Xanten municipality) is the forest "Uedemer Hochwald" in which many burial mounds (German: Hügelgrab (sg.), Hügelgräber (pl.)) from our ancestors of the Hallstatt period (a Celtic culture
 between 850 and 450 BCE) can be found. The above picture shows a map section with some of the burial mounds indicated as grey dots. 
 
**Task 1:** <br> 
Georeference this picture by means of the QGIS Georeferencer together with the topographic map 1:10000 already imported from a WMS in the QGIS project `gdms0000_Burial_Mounds_Uedem_V001.qgz`. Use crossing forest trails, crossroads, road junctions and other features you can identify as land marks (aka ground control points, GCP) with known coordinates (can be read from the QGIS map canvas). Use EPSG:25832. 
 
**Task 2:** <br> 
Load the DTM hillshade model provided as a WMS. The German word for hillshade is "Schummerung". Plot the georeferenced map partly transparent on top of the hillshade model. What do you observe? How good is the map section showing the burial mounds? 
 
**Task 3:** <br> 
Load the DTM located in the project folder. Create your own hillshade model from it. Follow this QGIS video tutorial:  https://www.youtube.com/watch?v=GK9aBRVJdRo

**Task 4:** <br> 
Use the DTM and measure the typical mound heights above ground (niot above sealevel!). What is their typical elvation above ground?

**Task 5:** <br> 
Study the hillshade model in direction East-North-East of the burial mounds area and search for regular structures which are not paths. What do you observe? Do you have a guess about the origin of these patterns? Choose at least one of the structures and digitize it and save it as a geopackage.

## 5. FREE EXERCISE

Do something exiting!

## 6. Extra Exercise - PostGIS / PostgreSQL: Spatio-Temporal Precipition Anmination, 2nd Approach.

Produce another precipitation video for a period of 40 days in 2020 (recent hourly precipitation data in BAVARIA) by means of your own **PostGIS geodatabase**. Follow the **Jupyter Notebook tutorial** of [geo0930_PostGIS_Insert_DWD_Stations_and_TS](https://github.com/rolfbecker/opengeo/tree/main/geo0930_PostGIS_Insert_DWD_Stations_and_TS) together with the respective **YouTube tutorial** (search for geo0930 on YouTube). 

The new [opengeo repository](https://github.com/rolfbecker/opengeo) is under construction. I am using it to reorganize my teaching material. It will be filled step by step. 

