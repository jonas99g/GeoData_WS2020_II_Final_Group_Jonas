global topic_dir = "/annual/kl/historical/"
global ftp_server = "opendata.dwd.de"
global ftp_user = "anonymous"
global ftp_passwd = ""
global ftp_dir =  "/climate_environment/CDC/observations_germany/climate"+topic_dir
global station_desc_pattern = "_Beschreibung_Stationen.txt"
global state = "Bayern"
global opt1 = "ja_tt"
global opt2 = "altitude"

iyear = 2017, 2018, 2019
date_from = datetime.strptime((year_selected + '-01-01'), "%Y-%m-%d")
date_to = datetime.strptime((year_selected + '-12-31'), "%Y-%m-%d")




    print("Loading...\n")
    create_dir()
    connect_ftp()
    global df_ftpdir = gen_df_from_ftp_dir_listing(ftp, ftp_dir)
    global df_zips = df_ftpdir[df_ftpdir["ext"]==".zip"]
    df_zips.set_index("station_id", inplace = True)
    station_grab()
    global basename = os.path.splitext(station_fname)[0]
    global df_stations = station_desc_txt_to_csv(local_ftp_station_dir + station_fname, local_station_dir + basename + ".csv")
    global station_ids_selected = df_stations[df_stations['state'].str.contains(state)].index
    download_stations()
    global df_merged_ts
    df_merged_ts = ts_merge()
    df_merged_ts.to_csv(local_ts_merged_dir + "ts_merged.csv",sep=";")
    global df_appended_ts = ts_append()
    df_appended_ts.to_csv(local_ts_appended_dir + "ts_appended.csv",sep=";")
    
    plot()

def connect_ftp(): #establishing connection to ftp server and check if it was successfull
    global ftp = ftplib.FTP(ftp_server)
    res = ftp.login(user=ftp_user,passwd=ftp_passwd)
    ret = ftp.cwd(".") # A dummy action to check the connection and to provoke an exception if necessary.

def create_dir(): #create directories for datasets
    dor = os.getcwd()
    global local_ftp_dir         = dor+"data/original/DWD/"
    global local_ftp_station_dir = local_ftp_dir + topic_dir
    global local_ftp_ts_dir      = local_ftp_dir + topic_dir
    global local_generated_dir   = dor+"data/generated/DWD/"
    global local_station_dir     = local_generated_dir + topic_dir
    global local_ts_merged_dir   = local_generated_dir + topic_dir
    global local_ts_appended_dir = local_generated_dir + topic_dir
    os.makedirs(local_ftp_dir,exist_ok = True)
    os.makedirs(local_ftp_station_dir,exist_ok = True)
    os.makedirs(local_ftp_ts_dir,exist_ok = True)
    os.makedirs(local_generated_dir,exist_ok = True)
    os.makedirs(local_station_dir,exist_ok = True)
    os.makedirs(local_ts_merged_dir,exist_ok = True)
    os.makedirs(local_ts_appended_dir,exist_ok = True)
    
def gen_df_from_ftp_dir_listing(ftp):
    lines = []
    flist = []
    try:    
        res = ftp.retrlines("LIST"+ftpdir, lines.append)
    except:
        return
    for line in lines:
        [ftype, fsize, fname] = [line[0:1], int(line[31:42]), line[56:]]
        fext = os.path.splitext(fname)[-1]
        if fext == ".zip":
            station_id = int(fname.split("_")[2])
        else:
            station_id = -1 
        flist.append([station_id, fname, fext])
    df_ftpdir = pd.DataFrame(flist,columns=["station_id", "name", "ext",])

def grabFile(ftpfullname,localfullname):
    try:
        localfile = open(localfullname, 'wb')
        ftp.retrbinary('RETR ' + ftpfullname, localfile.write, 1024)
        localfile.close()
    except ftplib.error_perm:
        print("FTP ERROR. Operation not permitted. File not found?")
    except ftplib.error_temp:
        print("FTP ERROR. Timeout.")
    except ConnectionAbortedError:
        print("FTP ERROR. Connection aborted.")

def station_grab():
    global station_fname
    station_fname = df_ftpdir[df_ftpdir['name'].str.contains(station_desc_pattern)]["name"].values[0]
    grabFile(ftp_dir + station_fname, local_ftp_station_dir + station_fname)

def station_desc_txt_to_csv(txtfile, csvfile):
    file = codecs.open(txtfile,"r","utf-8")
    r = file.readline()
    file.close()
    colnames_de = r.split()
    translate =     {'Stations_id':'station_id',
     'von_datum':'date_from',
     'bis_datum':'date_to',
     'Stationshoehe':'altitude',
     'geoBreite': 'latitude',
     'geoLaenge': 'longitude',
     'Stationsname':'name',
     'Bundesland':'state'}
    colnames_en = [translate[h] for h in colnames_de]
    df = pd.read_fwf(txtfile,skiprows=2,infer_nrows=1155,names=colnames_en, parse_dates=["date_from","date_to"],index_col = 0)
    df.to_csv(csvfile, sep = ";")
    return(df)

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
