import os #access to host system to create directories and write files
import ftplib #libary to access ftp server
import urllib3 
import codecs
from zipfile import ZipFile #used for unzipping zip files
import numpy as np #for replacing bad values with true NotaNumber from numpy
import pandas as pd


ftp_server = "opendata.dwd.de"
ftp_user = "anonymous"
ftp_passwd = ""
ftp_dir =  "/climate_environment/CDC/observations_germany/climate/annual/kl/historical/"
state = "Bayern"
years = [2017, 2018, 2019]
nyears = len(years)
stations_fname = ""
'''
def process():
    ftp = connect_ftp()
    df_ftp_dir = gen_df_ftp_dir()
    df_station_desc = gen_df_station_desc()
    station_ids_selected = []
    grab_stations(station_ids_selected)

    global df_stations = station_desc_txt_to_csv(local_ftp_station_dir + station_fname, local_station_dir + basename + ".csv")
    global station_ids_selected = df_stations[df_stations['state'].str.contains(state)].index
    download_stations()
    global df_merged_ts
    df_merged_ts = ts_merge()
    df_merged_ts.to_csv(local_ts_merged_dir + "ts_merged.csv",sep=";")
    global df_appended_ts = ts_append()
    df_appended_ts.to_csv(local_ts_appended_dir + "ts_appended.csv",sep=";")
'''
def connect_ftp(): #establishing connection to ftp server and check if it was successfull
    ftp = ftplib.FTP(ftp_server) # creating ftp server instance
    res = ftp.login(user=ftp_user,passwd=ftp_passwd) # logging in to server
    ret = ftp.cwd(ftp_dir) # Changing into correct ftp directory
    return ftp

def gen_df_ftp_dir():
    lines = []
    flist = []
    try:    
        res = ftp.retrlines("NLST", lines.append)
    except:
        return
    global stations_fname
    stations_fname = lines[0]
    lines.pop(0)
    for line in lines:
        pname = "produkt_klima_jahr_"+line.split("_")[3]+"_"+line.split("_")[4]+"_"+line.split("_")[2]+".txt"
        flist.append([int(line.split("_")[2]), line, pname])
    df_ftp_dir = pd.DataFrame(flist,columns=["station_id", "fname", "pname"])
    df_ftp_dir.set_index("station_id")
    return df_ftp_dir

def gen_df_station_desc():
    try:
        ftp.retrbinary('RETR '+ stations_fname, open(stations_fname, 'wb').write)
    except:
        return
    df_station_desc = pd.read_fwf(stations_fname, skiprows = 2, header=None) # maybe fix encoding for German Umlaute
    df_station_desc.columns = ["station_id", "date_from", "date_to", "altitude", "latitude", "longitude","name", "state"]
    df_station_desc.set_index("station_id")
    return df_station_desc
'''
def grab_stations(station_ids_selected):
    for sel_station_id in station_ids_selected:
        fname = df_ftp_dir["station_id" == sel_station_id]["fname"]
        pname = df_ftp_dir["station_id" == sel_station_id]["pname"]
        try:
            ftp.retrbinary('RETR ' + fname, open( fname, 'wb').write)
        except:
            return
        
        with ZipFile(fname) as myzip:
            with myzip.open(pname) as myfile:
                pd.read_fwf(myfile)
'''
'''
def download_stations():
    global local_zip_list
    local_zip_list = []
    for station_id in station_ids_selected:
        try:
            fname = df_zips["name"][station_id]
            grabFile(ftp_dir + fname, local_ftp_ts_dir + fname)
            local_zip_list.append(fname)
        except:
            ("")

def kl_ts_to_df(fname): 
    dateparse = lambda dates: [datetime.strptime(str(d), '%Y%m%d') for d in dates]
    df = pd.read_csv(fname, delimiter=";", encoding="utf8", index_col="MESS_DATUM_BEGINN", parse_dates = ["MESS_DATUM_BEGINN", "MESS_DATUM_ENDE"], date_parser = dateparse, na_values = [-999.0, -999])
    df = df[(df.index >= date_from) & (df.index <= date_to)]
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df.index.name = df.index.name.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
    return(df)

def ts_merge():
    df = pd.DataFrame()
    for elt in local_zip_list:
        ffname = local_ftp_ts_dir + elt
        with ZipFile(ffname) as myzip:
            # read the time series data from the file starting with "produkt"
            prodfilename = [elt for elt in myzip.namelist() if elt.split("_")[0]=="produkt"][0] 
            with myzip.open(prodfilename) as myfile:
                dftmp = kl_ts_to_df(myfile)
                if len(dftmp) > 0:
                    s = dftmp["ja_tt"].rename(dftmp["stations_id"][0]).to_frame()
                    df = pd.merge(df, s, left_index=True, right_index=True, how='outer')
                else:
                    ("")
    df = df.dropna(axis='columns')
    df.index.rename(name = "time", inplace = True)
    return(df)

def ts_append():
    df = pd.DataFrame()
    for elt in local_zip_list:
        ffname = local_ftp_ts_dir + elt
        with ZipFile(ffname) as myzip:
            prodfilename = [elt for elt in myzip.namelist() if elt.split("_")[0]=="produkt"][0]
            with myzip.open(prodfilename) as myfile:
                dftmp = kl_ts_to_df(myfile)
                if len(dftmp) > 0:
                    dftmp = dftmp.merge(df_stations,how="inner",left_on="stations_id",right_on="station_id",right_index=True)
                    df = df.append(dftmp)
                else:
                    ("")
    df.index.rename(name = "time", inplace = True)
    
    df.replace(to_replace = -999,value = (np.nan),inplace=True)
    
    df = df.dropna(subset = [(str(o1)),(str(o2))])
    
    #ind1 = df[df[str(o1)]==-999].index
    #df.drop(ind1,inplace=True)
    #ind2 = df[df[str(o2)]==-999].index
    #df.drop(ind2,inplace=True)
    return(df)

def plot():
    retranslate = {"ja_tt":"Average Temperature","ja_tx":"Yearly Average Max Temperature","ja_tn":"Yearly Average Min Temperature","ja_fk":"Average Windforce","ja_sd_s":"Sum Yearly Sunshine Duration","ja_mx_tx":"Absolute Max Temperature","ja_mx_tn":"Absolute Min Temperature","ja_rr":"Sum Yearly Precipitation","ja_mx_rs":"Max Precipitation Height","altitude":"Altitude","latitude":"Latitude","longitude":"Longitude"}
    po1 = retranslate[(o1)]
    po2 = retranslate[(o2)]
    fpo1 = po1.replace(" ", "_")
    fpo2 = po2.replace(" ", "_")

    df_plot = df_appended_ts
    
    df_corr = pd.DataFrame(df_appended_ts.loc[:,o2])
    df_corr[o1] = df_appended_ts.loc[:,o1]
    Y = df_appended_ts.loc[:,o1].values.reshape(-1, 1)
    X = df_appended_ts.loc[:,o2].values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    score = linear_regressor.score(X, Y)
    Y_pred = linear_regressor.predict(X)

    
    fig1, ax1 = plt.subplots(dpi=136, figsize=(8,6))
    b = round((linear_regressor.intercept_[0]),4)
    m = round((linear_regressor.coef_[0][0]),4)
    sx = 0.35 * ax1.get_xlim()[1]
    sy = 1.69 * ax1.get_ylim()[0]
    r = round(score,4)
    ax1.plot(X, Y_pred, color='red')
    ax1.plot(df_plot[o2],df_plot[o1],".")
    ax1.set_ylabel(po1)
    ax1.set_xlabel(po2)
    ax1.set_title(po1+" vs. "+po2+" in Year " + year_selected + " at DWD Stations in " + state+"\ny="+str(m)+"*x+"+str(b)+", R^2= "+str(r))

    #ax1.text(x=sx,y=sy,s=("y="+str(m)+"*x + "+str(b)+", R^2= "+str(r)))

    ax1.grid(True)
    plt.show()
    fig1.savefig(fpo1+"_"+fpo2+"_"+year_selected+"_DWD_Stations_"+state+".png")
    print("A low R^2 value indicates, that the regression model is not fitting well (no strong correlation of data points).\n")
'''

ftp = connect_ftp()
df_ftp_dir = gen_df_ftp_dir()
df_station_desc = gen_df_station_desc()
station_ids_selected = ["00001"]
# grab_stations(station_ids_selected)
for sel_station_id in station_ids_selected:
    # fname = df_ftp_dir["station_id" == sel_station_id]["fname"]
    # pname = df_ftp_dir["station_id" == sel_station_id]["pname"]
    print(sel_station_id)
'''
    try:
        ftp.retrbinary('RETR ' + fname, open( fname, 'wb').write)
    except:
        return
        
    with ZipFile(fname) as myzip:
        with myzip.open(pname) as myfile:
            pd.read_fwf(myfile)
'''