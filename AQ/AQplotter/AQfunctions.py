import matplotlib.dates as mdates
import matplotlib.pyplot as mplot
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from scipy import stats
import matplotlib.ticker as ticker
import matplotlib
import matplotlib as mpl
import seaborn as sns
import OPCPM as PMCON #PM convertion for OPC
from sklearn.linear_model import LinearRegression
import GRIMM as GM
import matplotlib.pylab as plt
import codecs
import math as mp
import os


def ISVrawvals(dataset,name,vals):
    OPCN3={}
    OPCN2={}
    SDS={}
    OP3=0
    OP2=0
    S=0
    groups=[]
    dics=[]
    
    for k, item in dataset.items():
        #print(k,item)
        if "OPCN3" in k:
            OPCN3[k]=item
            if OP3==0:
                groups.append("OPCN3")
                OP3=1
        elif "OPCN2" in k:
            OPCN2[k]=item
            if OP2==0:
                groups.append("OPCN2")
                OP2=1
        elif "SDS" in k:
            SDS[k]=item
            if S==0:
                groups.append("SDS")
                S=1
    posgroups={"OPCN3":OPCN3,"OPCN2":OPCN2,"SDS":SDS}
    for group, dic in posgroups.items():
        if group in groups:
            dics.append(dic)
    writer = pd.ExcelWriter("Plots//DISSPLOTS//ISV"+name+'.xlsx', engine='xlsxwriter') #create excel sheet
    ISVdata=pd.DataFrame(columns=vals,index=groups)

    for dic,g in zip(dics,groups):
     #   print(dic.keys())
        for val in vals:
                data=pd.DataFrame(index=list(dic.keys()))    
                for k, item in dic.items():
                    x=item[val].mean()
                    data.at[k,val]=x
                print(data)
                des=data.describe()
              #  print(data)
                ISV=((des.loc["max"][0]-des.loc["min"][0])/des.loc["mean"][0])*100
                ISVdata.at[g,val]=ISV
              #  del data[k]
                print(g+":"+val+"-ISV",ISV," %")
        
    
    ISVdata.index.name=name  
    ISVdata.to_excel(writer,sheet_name=name)
    writer.save()
            
def ISVCount(dataset,name,val):
    OPCN3={}
    OPCN2={}
    for k, item in dataset.items():
        if "OPCN3" in k:
            OPCN3[k]=item
        elif "OPCN2" in k:
            OPCN2[k]=item
       
    writer = pd.ExcelWriter("Plots//DISSPLOTS//ISV"+name+'.xlsx', engine='xlsxwriter') #create excel sheet
    ISVdata=pd.DataFrame(columns=[val],index=["OPCN3","OPCN2"])
    groups=["OPCN3","OPCN2"]
    dics=[OPCN3,OPCN2]
    for dic,g in zip(dics,groups):
                print(dic.keys())
                data=pd.DataFrame(index=list(dic.keys()))    
                for k, item in dic.items():
                    x=item.mean()
                    data.at[k]=x
                des=data.describe()
              #  print(data)
                ISV=((des.loc["max"][0]-des.loc["min"][0])/des.loc["mean"][0])*100
                ISVdata.at[g,val]=ISV
              #  del data[k]
                print(g+":"+val+"-ISV",ISV," %")
        
    
    ISVdata.index.name=name  
    ISVdata.to_excel(writer,sheet_name=name)
    writer.save()
               

def ISVTrend(dataset,val):
    data=pd.DataFrame()
    for k,item in dataset.items():
        x=item[val]
        data[k+val]=x
    data["ISV"]=0
    data=data.dropna()
    for i in data.index:
        data.loc[i,"ISV"]=(max(data.loc[i])-min(data.loc[i]))/np.mean(data.loc[i])*100
   # print("Inter sensors variability",ISV," %")
    data.index=pd.to_datetime(data.index)
    data["ISV"].plot()
    """
#related code to 6OPCN3 anaysis
OPCN2=2
OPCN3=0
fig,ax=plt.subplots(1,1,figsize=(10,10))
NOPC={}
JOPC={}
for k,item in OPC6.items():
    item=Timecut(item,["2019-03-23","2019-04-04"])
    if "OPCN3_N" in k:
        NOPC[k]=item
    else:
        JOPC[k]=item
NOPCFW=ISVTrend(NOPC,"FlowRate")
JOPCFW=ISVTrend(JOPC,"FlowRate")
ax.plot(Timecut(JOPCFW["ISV"],["2019-03-23","2019-04-04"]),label="J-OPCN3, Mean="+str(round(JOPCFW["ISV"].mean(),2))+"%",color="Blue")
ax.plot(Timecut(NOPCFW["ISV"],["2019-03-23","2019-04-04"]),label="N-OPCN3 Mean="+str(round(NOPCFW["ISV"].mean(),2))+"%",color="Green")
ax.grid()
ax.set_ylabel("ISV (%)",fontsize=20)
myFmt = mdates.DateFormatter('%d/%m')
ax.legend( prop={'size': 15})
ax.xaxis.set_major_formatter(myFmt)
fig.savefig("D:\MRES!!!!!!! 勝とう\\Project\\Code\\Maincode\\Plots\\DISSPLOTS\\ISV-6OPC-FLOWRate.png",dpi=300,format='png',bbox_inches='tight')


"""
    return data







def ISV(dataset,val):
    data=pd.DataFrame()
    for k,item in dataset.items():
        x=item[val]
        data[k+val]=x
    ISV=((max(data.mean())-min(data.mean()))/np.mean(data.mean()))*100
    print("Inter sensors variability",ISV," %")
    """
#use full code to use with ISV above
Val=["PM-pm1","PM-pm2.5","PM-pm10"]
for ave in aves:
    print("=========",ave,"===========")
    OPCN3={}
    OPCN2={}
    for k,item in RAWOPC.items():
        item.resample(ave).mean()
        if "OPCN2" in k:
            OPCN2[k]=item
        elif "OPCN3" in k:
            OPCN3[k]=item
    for val in Val:
        print("OPCN3",val)
        ISV(OPCN3,val)
        print("OPCN2",val)
        ISV(OPCN2,val)
"""
    return ISV



def Timecut(df,Dates):
    '''
    Function to get certain time in dat, account for single day and time intervals 
    
    '''
    if len(Dates)>1:
       
        df=df[(df.index > Dates[0]) & (df.index <= Dates[1])]
    else:
    
        df=df[Dates[0]]
        
    return df
      

def createdir(dirname):
    date=datetime.today().strftime("%Y%m%d")
    dirname=dirname+"_"+date
    if not os.path.exists("Plots//"+dirname):
        os.mkdir("Plots//"+dirname)
        print("新しいDIRを使いた")
    else:
        print("このDIRはまた存在している")
    dirname=dirname+"//"
    return dirname 



def droperror(data,col,limit,condition):
    '''
    Error data cutter fuction, does not cut all the other data but set that columns error to None values 
    '''
    
  #  print("-------------------Cutting data", col, limit, condition)
    
    #print(max(data[col]))
    if condition =="greater":
        indexNames = data[ data[col] > limit ].index
       
        data.drop(indexNames , inplace=True)

        #mask=data[col]>int(limit)
    elif condition == "equal":
         indexNames = data[ data[col] == limit ].index
         data.drop(indexNames , inplace=True)
        
    elif condition =="less":
        indexNames = data[ data[col] < limit ].index
        data.drop(indexNames , inplace=True)
   # data.loc[mask,col]=None 
   # print(condition+col," Cut data points",len(indexNames))
   # print(max(data[col]))
    return data

def gencount(Data,sensor):
    """
       does not work
    """
    cols=[]
    GRIMM2col=[] #generate a 2nd partilce count for the grimm with out fist bin
    for col in Data.columns:
        if "b" in col or "um" in col:  #OPC bin data is b0 b1 b2 ... GRIMM bin data is 0.3um 0.5um ....
           # print(col)
           # Data[col].fillna(0,inplace=True)
           if col != "checksum":
               cols.append(col)
               if "GRIMM" in sensor:
                   if col != "0.3um":
                       GRIMM2col.append(col)
    
  #  print("Generate Total Partile count")
  #  print(cols)
    Data["ParticleCount"]=Data[cols].sum(axis=1)
    if "GRIMM" in  sensor:
        Data["ParticleCount-EQ"]=Data[GRIMM2col].sum(axis=1)
   # print(Data["ParticleCount"])
    return Data
def genratio(Data,col1,col2):
    rationame=col1+"VS"+col2
    Data[rationame]=Data[col1]/Data[col2]
    return Data
def Readfiles(Folder,sensor):
     sfiles=[]
     for file in glob.glob(Folder+'***.csv'):
           # print(file)
            if sensor in file:
                sfiles.append(file)
     data=pd.DataFrame()
     
     for file in sfiles:
            with codecs.open(file, "br",encoding="utf8", errors='ignore') as test:
            #    print(test)
                for i, row in  enumerate(test):
                    if "time" in row:
             #           print(i,row)
                        header=i
            if "GRIMM" in file:
                dataloop=pd.read_csv(file,header=header,error_bad_lines=False,engine='python')
            else:
               
                dataloop=pd.read_csv(file,header=header,error_bad_lines=False,engine='python')
                if "SDS" in sensor:
                     dataloop=dataloop.loc[:,"time":"sds-pm10"]
                else:
                     dataloop.rename(columns={"pm2":"pm2.5","RH":"OPC-RH","Temp":"OPC-T","b24":"cut"},inplace=True)

                
            data=pd.concat([data,dataloop], ignore_index=False, axis=0,sort=True)  
            
     data["time"]=pd.to_datetime(data.time)     
     data.set_index('time', inplace=True)         
     return data



    
def GetDataset(Folder,sensors,ave):
    Data={}#set array to hold file names
    #  folder=Folder
    #import data sent 
    for sensor in sensors:
       # print(sensor)
        sfiles=[]
        for file in glob.glob(Folder+'***.csv'):
           # print(file)
            if sensor in file:
                sfiles.append(file)
               #1 print(file)
        sfiles=sorted(sfiles)
       # print(len(sfiles))
        print(sfiles)
        data=pd.DataFrame()
        if len(sfiles)==1:
             with codecs.open(sfiles[0], "br",encoding="utf8", errors='ignore') as test:
                #print(test)
                row=""
                for i, row in  enumerate(test):
                    if "time" in row:
           #             print(i,row)
                        header=i
             if "GRIMM" in sfiles[0]: #account for GRIMM data header=1
                 data=pd.read_csv(sfiles[0],header=header,error_bad_lines=False,engine='python')
                 
             else:
                
                 data=pd.read_csv(sfiles[0],header=header,error_bad_lines=False,engine='python')
                 if "SDS" in sensor:
                     if "sds-pm2.5" not in data.columns: #older sds data did not have sds in columns names 
                         data.rename(columns={"pm2.5":"sds-pm2.5","pm10":"sds-pm10"},inplace=True)
                         
                     data=data.loc[:,"time":"sds-pm10"]
                # else:
                 #    data.rename(columns={"Temp":"OPC-T"},inplace=True)
                     #data.rename(columns={"RH":""})
                    
                  #   data.rename(columns={"pm2":"pm2.5","RH":"OPC-RH","T":"OPC-T","b24":"cut"},inplace=True)
                   #  data.rename(columns={"RH.1":"OPC-RH"},)
        else:
          
            for file in sfiles:
                with codecs.open(file, "br",encoding="utf8", errors='ignore') as test:
                #    print(test)
                    for i, row in  enumerate(test):
                        if "time" in row:
                 #           print(i,row)
                            header=i
                if "GRIMM" in file:
                    dataloop=pd.read_csv(file,header=header,error_bad_lines=False,engine='python')
                else:
                    dataloop=pd.read_csv(file,header=header,error_bad_lines=False,engine='python')
                    if "SDS" in sensor.upper():
                         if "sds-pm2.5" not in dataloop.columns: #older sds data did not have sds in columns names 
                           #  print(dataloop.columns)
                             dataloop.rename(columns={"pm2.5":"sds-pm2.5","pm10":"sds-pm10"},inplace=True)
                            # print(dataloop.head(3))
                         dataloop=dataloop.loc[:,"time":"sds-pm10"]
                    else:
                         dataloop.rename(columns={"pm2":"pm2.5","RH":"OPC-RH","Temp":"OPC-T","b24":"cut"},inplace=True)

                    
                data=pd.concat([data,dataloop], ignore_index=False, axis=0,sort=True)  
        #print(data.head(4))
        
      
        sen=sensor
      #  print(data.head(4))
        data["time"]=dateparse(data["time"])#pd.to_datetime(data.time,yearfirst=True, dayfirst=False)   
        data.set_index('time', inplace=True)  
        print("---------------"+sen+"-----------------------------")
     #   print(data.columns)
        
        #deal with non float varaible types 
        for k,c in data.iteritems():
            typ=str(c.dtype)
            if "float" not in typ:
       #         print(k)
                data[k]=pd.to_numeric(data[k], errors='coerce')
                data[k]=data[k].astype('float64')
        data = data.loc[~data.index.duplicated(keep='first')]
       
        if "OPC" in sensor: #generate real PM 
         #   print(data.columns)
            #nana data for flow rate and period is repalce with mean data
            if "OPCN2" in sensor:
                mask=np.isnan(data["flowrate"])
                data["flowrate"].loc[mask]=np.mean(data["flowrate"])
                mask=np.isnan(data["period"])
                data["period"].loc[mask]=np.mean(data["period"])
            elif "OPCN3" in sensor:  
                mask=np.isnan(data["FlowRate"])
                data["FlowRate"].loc[mask]=np.mean(data["FlowRate"])
                mask=np.isnan(data["period"])
                data["period"].loc[mask]=np.mean(data["period"])
            
            #account for nan flowrate and perid
            data=PMCON.Binmass(data,"NO",sensor,"pm2.5","Binplot"+sensor)
           # print("---PM recaculated---")
        #drop error data  
        cols=[]
        for col in data.columns :
           # print(col)
            if "pm" in col: 
                if "VS" in col:
                    pass
                else:
    
            
                    data=droperror(data,col,1000,"greater")
                    data=droperror(data,col,0, "equal")
                    data=droperror(data,col,0,"less")
                    
            elif col=="ParticleCount":
                data=droperror(data,col,100000,"greater")
                data=droperror(data,col,0,"less")
                
            elif col=="DHT-RH":
    #             print(col)
                 data=droperror(data,col,100,"greater")
                 data=droperror(data,col,0,"less")
            if "b" in col or "um" in col:
                if "M"  not in col or "W" in col:
                    cols.append(col)    
         
        #drop nan index data 
        #data=data.index.dropna()
        
        if "SDS" in sensor:
            if "pm10VSpm2.5" not in cols:
                data=genratio(data,"sds-pm10","sds-pm2.5") #gen pm10/pm2.5
        elif "OPC" in sensor.upper():
            if "pm10VSpm2.5" not in cols:
                data=genratio(data,"PM-pm10","PM-pm2.5") #gen pm10/pm2.5
                data=genratio(data,"PM-pm2.5","PM-pm1") #gen pm2.5/pm1
               
            #generate calibrated RH and T based on DHT22
         #   if "OPCN3" in sensor:
          #       if "DHT-RH" in data.columns:
           #         if "OPC-RH-CAL" not in cols:
            #             Data=droperror(data,"DHT-RH",100,"greater")
             #            Data=droperror(Data,"DHT-RH",0,"less")
                #         data=VariableCalPlot(data,"OPC-RH","DHT-RH",sen)
                 #        data=VariableCalPlot(data,"OPC-T","DHT-T",sen)
                
                
        elif "GRIMM" in sensor.upper():
            
            sen=sensor
            #conver to volume weighted diameter  See seen in Evaluation of a low-cost optical particle countee (Alphasense OPC-N2) for ambient air monitoring https://www.atmos-meas-tech.net/11/709/2018/
   #         print(data)
            #account for log being in UTC
            flowrate=1.0512*(1.66667e-5)#l/min to m^3/s
            period=6 #12 second sampe period
            data.index=data.index+timedelta(hours=1) 
            data=GM.binmass(data, flowrate,period)
            data=gencount(data,sensor.upper())
            for col in data.columns :
                # print(col)
                if "pm" in col: 
                    data=droperror(data,col,1000,"greater")
                    data=droperror(data,col,0, "equal")
                    data=droperror(data,col,0,"less")
            
           # data=genratio(data,"PM-pm10","PM-pm2.5") #gen pm10/pm2.5
       #     data=genratio(data,"PM-pm2.5","PM-pm1") #gen pm2.5/pm1
            
            
        #print(sen)
        if ave != "RAW": #If there is a avearege then get mean, if RAW dont take mean
            #print(data.dtypes)
            for k,c in data.iteritems():
                typ=str(c.dtype)
                if "float" not in typ:
           #         print(k)
                    data[k]=pd.to_numeric(data[k], errors='coerce')
                    data[k]=data[k].astype('float64')
         #   print(data.dtypes)
            #Get mean data  
            data=data.resample(ave).mean()
            
            """
            #for count columne and partile count, get the sum instead
            if "SDS" not in sen:
                print(cols)
                print("Summing count data")
                data=gencount(data,sensor.upper())
                cols.append("ParticleCount")
                print(Data[cols].describe())
                sumdata=data[cols].resample(ave).sum()
                Data[cols]=sumdata[cols] #add new sum data
                print(Data[cols].describe())
                
            """
         #   print(data.columns)
       
     #   print(Data.describe())
        
        Data[sen]=data
    return Data








##############################################################################
##############################################################################
####################
def gencsv(Datadic,Location):
    """
    Generate large data csv from data dictionay for sensors
    #Location=["JIMSOffice",	"Lat-Lon",	"53.805781",	"-1.555851"]	

    Current: SDS, OPCN2,OPCN3
    """
    #Cirrenty can only get one extra header, what i though adding the Sensors location
   
    for k ,v in Datadic.items():
        print(k)
        #csv file name 
        #Add timeperiod
        
        start=pd.to_datetime(min(v.index))
        end=pd.to_datetime(max(v.index))
        starttime=start.strftime("%Y%m%d")
        endtime=end.strftime("%Y%m%d")
        name="Dataset//"+Location[0]+'_'+k+'_'+starttime+'_'+endtime+'.csv'
        #Generate data info
        with open(name, "w+") as f:
            #Add timeperiod
            starttime=start.strftime("%Y-%m-%d %H:%M:%S")
            endtime=end.strftime("%Y-%m-%d  %H:%M:%S")
            Time='Time Period,start:, '+starttime+',end:,'+endtime
            print(Time,file=f)
            #add sensors 
            print('Sensor:,'+k,file=f)
            #add location 
            Loc='Location:,'+Location[0]+',Lat-Lon,'+Location[2]+","+Location[3]
            print(Loc,file=f)
            #add interval time 
            print("Interval time,10",file=f)
            #add data lenght 
            Len='Data points,'+str(len(v))+',Days of Data,'+str((end-start).days)
            print(Len,file=f)
            f.close()
        #Append dic data 
        with open(name, "a") as f:
            v.to_csv (f, index = True, header=True)
            f.close()    
            
            
            

def dateparse (timestamp):
    time=pd.to_datetime(timestamp, yearfirst=True, dayfirst=False)
 #   print(time)
  #  time.strftime(time, '%Y-%m-%d %H:%M:%S')
    return time 



def DHTData(Locs,ave,Start,Stop):
    
    data=pd.DataFrame()
    for loc in Locs:
        dataloop=pd.read_csv(loc,parse_dates=['time'], error_bad_lines=False)
        data=pd.concat([data,dataloop], ignore_index=True, axis=0)
    try:
        df=pd.DataFrame({'time': data['time'], 'RH':data['humidity'], 'T':data['temperature']})
        df.set_index('time', inplace=True, drop=True)
        df=df.drop(df[df["RH"]>100].index)
        df=df[(df.index > Start) & (df.index < Stop)]
        if ave != "RAW":
            df=df.resample(ave).mean()
    
        return df
    except:
        pass
 

def AURNData(Folder,Loc,dates):
    
    '''
    Updated 31/05/2019
    
    '''
    sfiles = [] #set array to hold file names
    data=pd.DataFrame()
    print(Folder)
    for file in glob.glob(Folder+'***.csv'):
        print(file)
        if Loc in file:
            #If statment to plot the sensors name, needs to be similer to t
            sfiles.append(file)
            data=pd.read_csv(file,skiprows=4,error_bad_lines=False)
    #Create time and date into one collums
    print(data.head(4))
    #AURN data is 1 to 24 hours, but datetime only works from 0 to 23  so convertion is needed
    #An odd error pop up on accation that the firt time will be nana, but when dealing with it, the time changed format
    #from24:00 to 24:00:00, dont know why but it can be delt witi in a for loop. Note this toop 2 days to figure out
    print(data.columns)
    if data["time"][0] =="01:00":
     #   print("First go")
      #print(data["time"].head(24))
      timec=data['time'].replace('24:00','23:59')
      #print(timec.head(24))

    else:
       # print("First is nan")
        #print(data["time"].head(24))
        data=data[data["time"].notnull()]
        #print("Cut Nana",data["time"].head(24))
        timec=data['time'].replace('24:00:00','23:59')
      #  print("Check replace",timec.head(24))
        #cut nan data 
    timec=timec[timec.notnull()]
    data=data[data["time"].notnull()]
    #print(data["time"].head(4))
    
    #create a time varable from the two serpate data colums for date and time
    data["time"]=data["Date"].map(str) +' '+ timec.map(str) #AURN data has no seconds just hours and mins 

    
    data["time"]=pd.to_datetime(data.time)    
    
    data=data[data['time'].notnull()]
    data["time"]=data['time'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
   #print(data.head(10))
    
  
    #Cut nana
    data=data[data["time"].notnull()] 
    #set time index
    data.set_index('time', inplace=True, drop=True)
    #print(data.head(10)) #check

    #get data between time range
    
    data.index = pd.to_datetime(data.index)
    print("----------------------------------------",data.index)
    print("Cut time intervals",dates)
    
    if len(dates)>1:
        data=data[(data.index > dates[0]) & (data.index <= dates[1])]
     
    else:
        data=data[dates[0]]
    coln=data.columns
    for col in coln:
        if "PM<sub>" in col:
            pass
     #       print(col)
         #   if "Volatile" in col: #drop the voltiale PM
          #       data.drop([col], 1, inplace=True)
          #  elif "Non" in col:
           #       data.drop([col], 1, inplace=True)
        else:
            data.drop([col], 1, inplace=True)
     #print(data.head(10))
    #cut unwanted colums 
   # data.drop(['End Date','End Time','Status/units','Status/units.7','M_DIR', 'Status/units.1', 'M_SPED', 'Status/units.2', 'M_T', 'Status/units.3', 'Status/units.4', 'Status/units.5','Status/units.6','Status/units.8'], axis=1,inplace=True)
    #rename columns NV- non volitle, V= volitile 
    try:
        data.columns = ['pm10','NV-pm10','NV-pm2.5','pm2.5','V-pm10','V-pm2.5']
    except:
         data.columns = ['pm10','pm2.5']
   
#    pr#int(data.head(10))
    data=genratio(data,"pm10","pm2.5") #gen pm10/pm2.5
    #have a look
    try:
        print("Done")
        data.plot()
    except:
        pass
    return data


"""
----------------------------Set value limit----------------------------------

"""

def ValLimDrop(data,val,limit,cond):
    """
    fuctions to drop data from a fuction from a  boalien operator
    i.e if RH > 70 cut such data
    
    Take in a data frame, a val what is a columns heading, the limit 
    and the condtion for the boalien operator

    """
    pre=len(data)
  #  print("Pre length:",pre," Condition ",cond,limit)
    if cond==">":
        data=data[data[val]>limit]
    elif cond =="<":
        data=data[data[val]<limit]
    elif cond =="==":
        data=data[data[val]==limit]
    elif cond =="<=":
        data=data[data[val]<=limit]
    elif cond =="=>":
        data=data[data[val]<=limit]
    elif cond =="!=":
        data=data[data[val]!=limit]    
    drop=(1-(pre-len(data))/pre)*100 #persentage of total data 
    print("After",len(data)," Data points droped=",pre-len(data), " Data left=",str(round(drop,2)))
    
    return data,drop
def ValLimDropArray(DataArray,val,limit,cond):
    for n,opc in enumerate(DataArray):
        opc,drop=ValLimDrop(opc,val,limit,cond)
        DataArray[n]=opc
    return DataArray
"""
----------------------------Mean data----------------------------------

"""
def meansen(senarray,val):
    #senarray len can vary so need to account for that
    senlen=len(senarray)
    df=senarray[0][val]
    for i in range(senlen-1):
        df2=senarray[i+1][val]
        #reset index 
       # df = df.reset_index(drop=True)
        #df2 = df2.reset_index(drop=True)
        df=pd.concat([df,df2],axis=1)
    data=df.mean(axis=1)
    #this sadly cut the colum heading 
    data=pd.DataFrame(data, columns = [val])
    return data

#################################################################################################################
    #######################
    ####################
    
    
    """
   --------------------------------------------------------------- 
    PLOT FUNCTIONS 
    --------------------------------------------------------------- 
   
    
    """



"""
Time Series 
"""

def plotcol(Data,Cols):
    """
    Function to check data , for chosesn columns 
    
    """
    
    axes=( locals()['ax%d'%i] for i in range( 1 , len(Cols)))
    fig,(axes) = plt.subplots(len(Cols),1,figsize=(15,20))
    #Add error check in cols in not in Data.columns
    for ax, var  in zip(axes,Cols):
        ax.plot(Data[var])
        if "PM" or "pm" in var:
            ax.set_ylabel( var+"($\mu g/m^3$)")
        elif "RH" or "rm" in var:
            ax.set_ylabel(var+"(%)")
        elif ("TEMP" or "Temp" or "temp") in var:
            ax.set_ylabel(var+"($^\dot$C)")
        else:
            ax.set_ylabel(var)
        fig.tight_layout()
        
        
def plotcolDHT(Data,DHT,Cols):
    axes=( locals()['ax%d'%i] for i in range( 1 , len(Cols)))
    fig,(axes) = plt.subplots(len(Cols),1,figsize=(15,20))
    #Add error check in cols in not in Data.columns
    for ax, var  in zip(axes,Cols):
        ax.plot(Data[var])
        if "PM" or "pm" in var:
            ax.set_ylabel( var+"($\mu g/m^3$)")
        elif "RH" or "rm" in var:
            ax.plot(DHT["RH"],"--r")
            ax.set_ylabel(var+"(%)")
        elif ("TEMP" or "Temp" or "temp") in var:
            ax.plot(DHT["T"])
            ax.set_ylabel(var+"($^\dot$C)")
        else:
            ax.set_ylabel(var)
        fig.tight_layout()        
def MultySenColPlotAURN(Datas,Names,AURN,AURNNAME,Cols,title,begin,stop):
    """"
    Functions polted wanted Colums in subplot, for multiple sensors 
    and add the mean to the sensors.
    Needs an Data array, the sensors names in the order inputed in the Data array
    and wanted Cols
    """
    #define number of axises 
    axes=( locals()['ax%d'%i] for i in range( 1 , len(Cols)))
    #def figure 
    fig,(axes) = plt.subplots(len(Cols),1,figsize=(15,20))
    
    #sensors colors, keepingthe colos the same even, for sensors type 
    SDS=0 #dumy varaible for SDS colors 
    OPCN2=0 #DUmy varaible for OPC colors 
    OPCN3=0
    OPCNN=0 #neelys opcs
    PMS=0
  
    
    move=50 #how much you want to color to changes each time 
    
    #get means
    
    """
    Neely=[]
    Jim=[]
    for sen, df in zip(Names,Datas):
        if "Neely" in sen:
            Neely.append(df)
        else:
            if "OPCN3" in sen:
                Jim.append(df)
    ND=pd.DataFrame()
    JD=pd.DataFrame()
    for col in Cols:
        df=meansen(Neely,col)
        dfj=meansen(Jim,col)
        
        ND=pd.concat([ND,df],axis=1)
        JD=pd.concat([JD,dfj],axis=1)
    
    ND.columns=Cols
    JD.columns=Cols
    Datas.append(ND)
    Datas.append(JD)
    Names.append("OPCN3_NeelyMean")
    Names.append("OPCN3_JimMean")
      """
     #add in AURN data by defults, if present
    try:
        axes[1].scatter(AURN.index,AURN['PM2.5'], marker="^",color="black",label=AURNNAME)
        #    elif var=="PM10" or "pm10":
        axes[2].scatter(AURN.index,AURN['PM10'], marker="^",color="black",label=AURNNAME)
    except:
        pass
  
    for Data, sen in zip(Datas,Names):
        
        #get sensors colors 
        if "OPC" in sen:
            if "N3" in sen:
                if "Neely" in sen:
                    if "Mean" in sen:
                        color="Black"
                    else:
                        color=plt.cm.winter(OPCNN)
                        OPCNN=OPCNN+move
                elif "Mean" in sen:
                    color="Green"
                else:
                    color=plt.cm.RdPu(OPCN3)
                    OPCN3=OPCN3+move
            if "N2" in sen:
                color=plt.cm.autumn(OPCN2)
                OPCN2=OPCN2+move
        #plot data 
        for ax, var  in zip(axes,Cols):
            try:
                ax.plot(Data[var],label=sen,color=color,alpha=0.7)
                ax.legend()
                ax.grid()
                ax.set_xlim(begin,stop)
                if "PM" or "pm" in var:
                    ax.set_ylabel( var+"($\mu g/m^3$)")
            
                elif "RH" or "rm" in var:
                    ax.set_ylabel(var+"(%)")
                elif ("TEMP" or "Temp" or "temp") in var:
                    ax.set_ylabel(var+"($^\dot$C)")
                    
                else:
                    ax.set_ylabel(var)
            except KeyError:
                pass
        for ax in axes[0:3]:
            ax.set_ylim(0,60)
    today=datetime.today().strftime("%Y%m%d")
    fig.show()
    
    fig.savefig("C:\\Users\\Jarvi\\Documents\\MRES!!!!!!! 勝とう\\Project\\Code\\JIMSOffice\\Time_plots\\"+title+"_("+today+").png",dpi=300,format='png')
           
def MultySenColPlot(Datas,Names,Cols,title,begin,stop):
    """"
    Functions polted wanted Colums in subplot, for multiple sensors 
    and add the mean to the sensors.
    Needs an Data array, the sensors names in the order inputed in the Data array
    and wanted Cols
    """
    #define number of axises 
    axes=( locals()['ax%d'%i] for i in range( 1 , len(Cols)))
    #def figure 
    fig,(axes) = plt.subplots(len(Cols),1,figsize=(15,20))
    fig.suptitle(title, fontsize=16)
    #sensors colors, keepingthe colos the same even, for sensors type 
    SDS=0 #dumy varaible for SDS colors 
    OPCN2=0 #DUmy varaible for OPC colors 
    OPCN3=0
    OPCNN=0 #neelys opcs
    PMS=0
    move=50 #how much you want to color to changes each time 
    for Data, sen in zip(Datas,Names):
    
        #get sensors colors 
        if "OPC" in sen:
            if "N3" in sen:
                if "N3_N" in sen:
                    if "Mean" in sen:
                        color="Black"
                    else:
                        color=plt.cm.winter(OPCNN)
                        OPCNN=OPCNN+move
                elif "Mean" in sen:
                    color="Green"
                else:
                    color=plt.cm.plasma(OPCN3)
                    OPCN3=OPCN3+move
            if "N2" in sen:
                color=plt.cm.autumn(OPCN2)
                OPCN2=OPCN2+move
        #plot data 
        for ax, var  in zip(axes,Cols):
            #try:
            ax.plot(Data[var],label=sen,color=color,alpha=0.7)
            ax.legend()
            ax.grid()
            ax.set_xlim(begin,stop)
            print(var)
            
        #current issue in getting all the colums unit right 
            if var == "RH":
                ax.set_ylabel(var+"(%)")
            if "PM" or "pm" in var:
                ax.set_ylabel( var+"($\mu g/m^3$)")
            if var=="FlowRate":
                ax.set_ylabel(var+"(L/min)")
            if var==("T" or "TEMP" or "Temp" or "temp"):
                ax.set_ylabel(var+"($^\dot$C)")
                
            else:
                ax.set_ylabel(var)
                
           
            #except KeyError:
             #   pass
       # for ax in axes[0:3]:
            #ax.set_ylim(0,round(max[Data[var]],0)+1)
    today=datetime.today().strftime("%Y%m%d")
    #set figure title
    #fig.suptitle(title, fontsize=16)
    fig.tight_layout()
   # fig.show()
    fig.savefig("C:\\Users\\Jarvi\\Documents\\MRES!!!!!!! 勝とう\\Project\\Code\\JIMSOffice\\Time_plots\\"+title+"_("+today+").png",dpi=300,format='png',bbox_inches='tight')

    """
    Mass concentration plots 
    """
def R2Othertime(dfs,refdf,sens,S2,Dates,VAL):
    #get wanted time period 
    
    refdf=Timecut(refdf,Dates)
    start=Dates[0]
    stop=Dates[1]
    Dayarray=np.arange(start,stop,dtype='datetime64[D]')
    Data=pd.DataFrame(index=Dayarray,columns=sens)
    #return refdf,df
    for k,df in dfs.items():
        df=Timecut(df,Dates)
        print(k)
        for day in Dayarray:
            try:
                ref=refdf[str(day)].resample("10T").mean()
                tar=df[str(day)].resample("10T").mean()
                print(day,len(tar),len(ref))
                if len(tar) !=0:
                    if len(ref) !=0:
                        newdf, s, i, r, p, std_err=CombineStat(ref,tar,k,S2,VAL)
                        Data.loc[day,k]=r**2
            except:
                pass
    Data.plot()
    
def CombineStat(df1,df2,S1,S2,VAL):
    
    '''
    Statistanca anayslsi fuction to run states.lineregression for diffrent varaibes
    '''
    #Combine the data fram in a easy way, all the non over laps show up as NAN
 #   print(df1[VAL].head(4))
  #  print(df2[VAL].head(4))
     #df1 refrence df2 targer sensors
    newdf=pd.concat([df1[VAL],df2[VAL]],axis=1,ignore_index=False)
    newdf.columns=VAL,VAL+"_2"   
    #nana chack
    mask = ~np.isnan(newdf[VAL]) & ~np.isnan(newdf[VAL+"_2"])
    newdf=newdf[mask]
   # print(mask)
    #print(newdf)
    slope, intercept, r_value, p_value, std_err = stats.linregress(newdf[VAL],newdf[VAL+"_2"])
   # slope, intercept, r_value p_value, std_err = stats.linregress(x,y)
 #   print("-----"+VAL+"----",S1,'_VS_',S2, ' p=',str(p_value), " r=" , str(r_value), "STD-error",str(std_err),"------")
   # print("y="+str(slope)+"x"+"+"+str(intercept))
    return newdf,  slope, intercept, r_value, p_value, std_err
def CombineStatNM(df1,df2,S1,S2,VAL):
    
    '''
    Statistanca anayslsi fuction to run states.lineregression for diffrent varaibes
    No Mask vertion
    '''
    #Combine the data fram in a easy way, all the non over laps show up as NAN
 #   print(df1[VAL].head(4))
  #  print(df2[VAL].head(4))
     #df1 refrence df2 targer sensors
    newdf=pd.concat([df1[VAL],df2[VAL]],axis=1,ignore_index=False)
    newdf.columns=VAL,VAL+"_2"   
    #nana chack
  #  mask = ~np.isnan(newdf[VAL]) & ~np.isnan(newdf[VAL+"_2"])
   # newdf=newdf[mask]
   # print(mask)
    #print(newdf)
    slope, intercept, r_value, p_value, std_err = stats.linregress(newdf[VAL],newdf[VAL+"_2"])
   # slope, intercept, r_value p_value, std_err = stats.linregress(x,y)
    print("-----"+VAL+"----",S1,'_VS_',S2, ' p=',str(p_value), " r=" , str(r_value), "STD-error",str(std_err),"------")
    print("y="+str(slope)+"x"+"+"+str(intercept))
    return newdf,  slope, intercept, r_value, p_value, std_err
def MassArraryConPlot(dfref,dfs,VAL,mapval,AVE,REFNAME,SENNAMES,Dates,title):
    '''
    Mass concentraion plots with comparion to a refrence sensors, made in an array to cycle through multiple sensors.
    
    23/05/2019
    added color based of the timeindex, and subplots
    with Dates 
    '''
    DFs=[]
    
    if len(Dates)>1:
        dfref=dfref[(dfref.index > Dates[0]) & (dfref.index <= Dates[1])]
        for df in dfs: 
            DF=df[(df.index > Dates[0]) & (df.index <= Dates[1])]
            DFs.append(DF)
    else:
        dfref=dfref[Dates[0]]
        for df in dfs:
            DF=df[Dates[0]]
            DFs.append(DF)
    
    #S1 VS S2
    N=len(dfs)
    axes=( locals()['ax%d'%i] for i in range(0,N))
    fig,axes = plt.subplots(N,1,figsize=(8,15))

    for ax, df,sen in zip(axes, DFs,SENNAMES):
     
        begin=str(min(df.index))
        stop=str(max(df.index))
    
        D1,S1,I1,R1,P1,STD1 = CombineStat(dfref,df,REFNAME,sen,VAL)
        #Plot figures 
        #First sensors 
        VAL2=VAL+"_2"
        #set title to include coeffiecet of determination
        ax.set_title(REFNAME+" VS "+sen+" $R^2$="+str(round(R1**2,2)))
        
        #plot regrettion line 
        points = ax.scatter(D1[VAL], D1[VAL2])#,c=D1.mapval, s=75, cmap="jet",label=None)
       # plt.colorbar(points,ax,ax)
        im1=sns.regplot(x=VAL,y=VAL2, data=D1,ax=ax, scatter=False,label=REFNAME+" VS "+sen+" y={0:.1f}x+{1:.1f}".format(S1,I1))
        
        #create a 1 to 1 line for comparison 
        try:
            #deals with high values being above the plottable size range
            x=np.arange(0,max(dfref[VAL]),1)
        except ValueError:
            x=np.arange(0,100,1)
        y=x
        ax.plot(x,y,linestyle = "--",color="black",label="y=x")
        #Make the grapht look nice with labes title and save figure 
        #ax1.autoscale(enable=True, axis='both')
        try:
            ax.set_ylim(0,max(dfref[VAL]))
        except  ValueError:
            ax.set_ylim(0,60)
        #ax1.set_xlim(0,4)
        ax.legend()
        ax.grid()
        ax.set_xlabel(REFNAME+" Mass concetration ($\mu g/m^3$) \n",fontsize=10)
        ax.set_ylabel(" Mass concetration ($\mu g/m^3$)",fontsize=10)
        plt.tight_layout()
    fig.subplots_adjust(top = 0.9) 
    fig.suptitle(title+"\n Time span: Start:("+begin+") Stop:("+stop+")\n "+VAL+" Coefficient of determination ("+(AVE)+") \n ")
    
def MassArrayComboPlot(dfref,dfs,VAL,AVE,REFNAME,SENNAMES,Dates,savetitle):
    '''
    Mass concentraion plots  for all sensors in a dic compared to a seprate ref dataset
  
  

    '''
  
    #Dates i,e ["2019-05-03","2019-06-06"]
   
    if len(Dates)>1:
        dfref=dfref[(dfref.index > Dates[0]) & (dfref.index <= Dates[1])]
        for k,df in dfs.items():
            if REFNAME not in k:
                dfs[k]=df[(df.index > Dates[0]) & (df.index <= Dates[1])]
        
    else:
        dfref=dfref[Dates[0]]
        df=df[Dates[0]]
        for k,df in dfs.items():
             if REFNAME not in k:
                 dfs[k]=df[Dates[0]]
    #cut the ref if it in the dfs 
                
    
    #S1 VS S2
    N=len(dfs)
    a=1
    b=1
    if N==9:
        a=3
        b=3
    elif N==6:
        a=3
        b=2
    else:
        a=N
        b=1
    
    axes=( locals()['axe%d'%i] for i in range(0,N))    
    fig,axes = plt.subplots(a,b,figsize=(15,15))
    #Color varaible place holders 
    OPCN2=2
    OPCN3=0
    SDS=0

    color="BLUE"
    i=0
    j=0
    
    for k, df in dfs.items():
        SENNAME=k
        print(i,j)
        ax=axes[j,i]
        i=i+1
        if i==3:
            i=0
            j=j+1
        #print(SENNAME)
      #  print(i,x)
        D1,S1,I1,R1,P1,STD1 = CombineStat(dfref,df,REFNAME,SENNAME,VAL)
        ME=round(1/len(D1)*(abs(D1[VAL+"_2"]-D1[VAL])).sum(),2) #mean error
        MB=100*((D1[VAL+"_2"]/D1[VAL])-1).mean() #mean bias 
        #First sensors 
        VAL2=VAL+"_2"
     
        
        #plot regrettion line 
        #mask
        cpmask=~np.isnan(D1[VAL]) & ~np.isnan(D1[VAL2])
        D1=D1[cpmask]
        #get color   
        if "OPCN2" in  SENNAME or "OPCN3_N" in SENNAME:
            color=sns.color_palette("YlGn", 5)[OPCN2]
            OPCN2=OPCN2+1 #color counter
            LC="TEAL"
        elif "OPCN3" in  SENNAME:
            color=sns.color_palette("Blues_d",5)[OPCN3]
            OPCN3=OPCN3+1
            LC="BLUE"
        elif "SDS" in  SENNAME:
            color=sns.color_palette("Wistia", 5)[SDS]
            SDS=SDS+1
            LC="RED"
      
        print(SENNAME,REFNAME)
        title=SENNAME +"VS"+ REFNAME
       
        #ax.scatter(Data[VAL], Data[VAL2] ,c=df[cpmask][mapval], s=10, alpha=0.8, cmap="winter",label=None)

        label="y={0:.1f}x+{1:.1f}".format(S1,I1) + "\n MAE:$\pm$"+str(ME)+ "$\mu g/m^3$ \n MB:"+str(round(MB,2)) +"%"
        im1=sns.regplot(x=VAL,y=VAL2, data=D1,ax=ax, scatter=True,label=label,color=color,scatter_kws={'s':30},line_kws={"color": LC})
       
        
        try:
            #deals with high values being above the plottable size range
            x=np.arange(0,max(dfref[VAL]),1)
        except ValueError:
            x=np.arange(0,100,1)
        #create a 1 to 1 line for comparison 
        y=x
        ax.legend(title=title)
        ax.plot(x,y,linestyle = "--",color="black")
        #Make the grapht look nice with labes title and save figure 
        #ax1.autoscale(enable=True, axis='both')
        
        ax.set_ylim(0,50)
        ax.set_xlim(0,50)
      
        ax.grid()
        ax.set_title=(title)
        ax.set_xlabel(REFNAME+" Mass concetration ($\mu g/m^3$) \n",fontsize=10)
        ax.set_ylabel(SENNAME+" Mass concetration ($\mu g/m^3$)",fontsize=10)
   # plt.tight_layout()
    #fig.subplots_adjust(top = 0.9) 
   # print("\n Time span: Start:("+begin+") Stop:("+stop+")\n "+VAL+" Coefficient of determination ("+(AVE)+") \n ")
    
    

    fig.tight_layout()
    fig.subplots_adjust(top = 0.9) 
    fig.suptitle(savetitle,fontsize=30)
    fig.savefig("D:\MRES!!!!!!! 勝とう\\Project\\Code\\Maincode\\Plots\\DISSPLOTS\\"+savetitle+".png",dpi=300,format='png',bbox_inches='tight')
    
  

def MassArrayPlotEXCon(dfref,df,VAL,mapval,cons,AVE,REFNAME,SENNAME,Dates,title):
    '''
    Mass concentraion plots with comparion to a refrence sensors, for 1 sen vs ref 
    -Addon to Mass ArrayPlot what will do plot three lines for diffrent vales of mapval, currenlty just less than 
    i.e all data RH < 100, <90   <80 <70 plot scatter for 1st condtions only 
    11/06/2019
    Added color bar, sized legend, save location
    '''
  
    #Dates i,e ["2019-05-03","2019-06-06"]
    if len(Dates)>1:
        dfref=dfref[(dfref.index > Dates[0]) & (dfref.index <= Dates[1])]
        
        df=df[(df.index > Dates[0]) & (df.index <= Dates[1])]
        
    else:
        dfref=dfref[Dates[0]]
        df=df[Dates[0]]
      
                
    
    #S1 VS S2
   

    begin=str(min(df.index))
    stop=str(max(df.index))
    first=0
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    colors=["red","pink","orange","green","blue"]
    for con,color in zip(cons,colors):
        DFref,refdrop=ValLimDrop(dfref,mapval,con,"<")
        DF,drop=ValLimDrop(df,mapval,con,"<")
        #print(df.head(5))
        DFref=DFref[DFref[VAL].notna()]
        DF=DF[DF[VAL].notna()]
        Data,s,i,r,p,STD = CombineStat(DFref,DF,REFNAME,SENNAME,VAL)
        me=round(1/len(Data)*(abs(Data[VAL+"_2"]-Data[VAL])).sum(),2) #mean error
        VAL2=VAL+"_2"
        #set title to include coeffiecet of determination
        #plot regrettion line 
        #create a mask for the color map
        cpmask=~np.isnan(Data[VAL]) & ~np.isnan(df[VAL])
        if first==0:
            points = ax.scatter(Data[VAL], Data[VAL2] ,c=df[cpmask][mapval], s=10, alpha=0.8, cmap="winter",label=None)
            first=1
       # plt.colorbar(points,ax,ax)
        cax = fig.add_axes([1.02, 0.1, 0.04, 0.8]) # left, bottom, width, height
        #cbar=fig.colorbar(points,cax,ticks=[10,30,50,70,90,100])
        
        cbar=fig.colorbar(points,cax,ticks=[10,30,50,70,90,100],norm=mpl.colors.Normalize(vmin=0, vmax=100))
        cbar.set_clim(0, 100)
        cbar.ax.set_ylabel('RH (%)',fontsize=10, rotation=270)
        sns.regplot(x=VAL,y=VAL2, data=Data,ax=ax, scatter=False,label="RH <"+str(con)+","+str(round(drop,1))+"%"+", R^2="+str(round(r**2,2))+" y={0:.1f}x+{1:.1f}".format(s,i)+", ME:"+str(me) ,line_kws={'color':color,"lw":4})
        
    ax.set_title(VAL.upper()+" "+AVE+"\n"+REFNAME+" VS "+SENNAME,fontsize=20)
    #create a 1 to 1 line for comparison 
    try:
        #deals with high values being above the plottable size range
        x=np.arange(0,max(dfref[VAL]),1)
    except ValueError:
        x=np.arange(0,100,1)
    y=x
    ax.plot(x,y,linestyle = "--",color="black",label="y=x")
    #Make the grapht look nice with labes title and save figure 
    #ax1.autoscale(enable=True, axis='both')
    try:
         
        ax.set_ylim(0,30)
        ax.set_xlim(0,25)
    except  ValueError:
        ax.set_ylim(0,60)
        ax.set_xlim(0,60)
    ax.legend( prop={'size': 18})
    ax.grid()
    ax.set_xlabel(REFNAME+" Mass concetration ($\mu g/m^3$) \n",fontsize=20)
    ax.set_ylabel(SENNAME+" Mass concetration ($\mu g/m^3$)",fontsize=20)
   # plt.tight_layout()
    
   # fig.subplots_adjust(top = 0.9) 
    print("\n Time span: Start:("+begin+") Stop:("+stop+")\n "+VAL+" Coefficient of determination ("+(AVE)+") \n ")
    title="MASSCON-"+VAL+"-"+title+"_AVE-"+AVE+"_REF-"+REFNAME+"_SEN-"+SENNAME
    fig.savefig("D:\MRES!!!!!!! 勝とう\\Project\\Code\\Maincode\\Plots\\DISSPLOTS\\"+title+".png",dpi=300,format='png',bbox_inches='tight')
    
    #fig.suptitle(title)



def MassArrayPlotEXCon(dfref,df,VAL,mapval,cons,AVE,REFNAME,SENNAME,Dates,title):
    '''
    Mass concentraion plots with comparion to a refrence sensors, for 1 sen vs ref 
    -Addon to Mass ArrayPlot what will do plot three lines for diffrent vales of mapval, currenlty just less than 
    i.e all data RH < 100, <90   <80 <70 plot scatter for 1st condtions only 
    11/06/2019
    Added color bar, sized legend, save location
    '''
  
    #Dates i,e ["2019-05-03","2019-06-06"]
    if len(Dates)>1:
        dfref=dfref[(dfref.index > Dates[0]) & (dfref.index <= Dates[1])]
        
        df=df[(df.index > Dates[0]) & (df.index <= Dates[1])]
        
    else:
        dfref=dfref[Dates[0]]
        df=df[Dates[0]]
      
                
    
    #S1 VS S2
   

    begin=str(min(df.index))
    stop=str(max(df.index))
    first=0
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    colors=["red","pink","orange","green","blue"]
    for con,color in zip(cons,colors):
        DFref,refdrop=ValLimDrop(dfref,mapval,con,"<")
        DF,drop=ValLimDrop(df,mapval,con,"<")
        #print(df.head(5))
        DFref=DFref[DFref[VAL].notna()]
        DF=DF[DF[VAL].notna()]
        Data,s,i,r,p,STD = CombineStat(DFref,DF,REFNAME,SENNAME,VAL)
        me=round(1/len(Data)*(abs(Data[VAL+"_2"]-Data[VAL])).sum(),2) #mean error
        VAL2=VAL+"_2"
        #set title to include coeffiecet of determination
        #plot regrettion line 
        #create a mask for the color map
        cpmask=~np.isnan(Data[VAL]) & ~np.isnan(df[VAL])
        if first==0:
            points = ax.scatter(Data[VAL], Data[VAL2] ,c=df[cpmask][mapval], s=10, alpha=0.8, cmap="winter",label=None)
            first=1
       # plt.colorbar(points,ax,ax)
        cax = fig.add_axes([1.02, 0.1, 0.04, 0.8]) # left, bottom, width, height
        #cbar=fig.colorbar(points,cax,ticks=[10,30,50,70,90,100])
        
        cbar=fig.colorbar(points,cax,ticks=[10,30,50,70,90,100],norm=mpl.colors.Normalize(vmin=0, vmax=100))
        cbar.set_clim(0, 100)
        cbar.ax.set_ylabel('RH (%)',fontsize=10, rotation=270)
        sns.regplot(x=VAL,y=VAL2, data=Data,ax=ax, scatter=False,label="RH <"+str(con)+","+str(round(drop,1))+"%"+", R^2="+str(round(r**2,2))+" y={0:.1f}x+{1:.1f}".format(s,i)+", ME:"+str(me) ,line_kws={'color':color,"lw":4})
        
    ax.set_title(VAL.upper()+" "+AVE+"\n"+REFNAME+" VS "+SENNAME,fontsize=20)
    #create a 1 to 1 line for comparison 
    try:
        #deals with high values being above the plottable size range
        x=np.arange(0,max(dfref[VAL]),1)
    except ValueError:
        x=np.arange(0,100,1)
    y=x
    ax.plot(x,y,linestyle = "--",color="black",label="y=x")
    #Make the grapht look nice with labes title and save figure 
    #ax1.autoscale(enable=True, axis='both')
    try:
         
        ax.set_ylim(0,30)
        ax.set_xlim(0,25)
    except  ValueError:
        ax.set_ylim(0,60)
        ax.set_xlim(0,60)
    ax.legend( prop={'size': 18})
    ax.grid()
    ax.set_xlabel(REFNAME+" Mass concetration ($\mu g/m^3$) \n",fontsize=20)
    ax.set_ylabel(SENNAME+" Mass concetration ($\mu g/m^3$)",fontsize=20)
   # plt.tight_layout()
    
   # fig.subplots_adjust(top = 0.9) 
    print("\n Time span: Start:("+begin+") Stop:("+stop+")\n "+VAL+" Coefficient of determination ("+(AVE)+") \n ")
    title="MASSCON-"+VAL+"-"+title+"_AVE-"+AVE+"_REF-"+REFNAME+"_SEN-"+SENNAME
    fig.savefig("D:\MRES!!!!!!! 勝とう\\Project\\Code\\Maincode\\Plots\\DISSPLOTS\\"+title+".png",dpi=300,format='png',bbox_inches='tight')
    
    #fig.suptitle(title)

def rollingCV(data,val,ave):
   # hunt=ave.find("T")
    #ave=int(ave[0:hunt])#find average from 10T, 60T format
    #only perfore for the 60 and 24 time periods
    #measuremt period is 10 seconds 
    period=60
    if ave==1:
        period="6T" # each 
    elif ave=="10T":
        period=60
    elif ave=="60T":
        period=120
    elif ave=="1D":
        period=24*60*60
   # print(period)
    #caculate a rolling cv
    data["CV-"+val]=data[val].rolling(period).std()/data[val].rolling(period).mean()
   # print(data["CV-"+val].describe())
    return data
    
def plotdateheat(data,dates):
     data=Timecut(data,dates)
     COL=[]
     b=""
     for col in data.columns:
         if "um" in col or "b" in col:
             if "um" in col:
                 a=col.find("um")
                 b="um"
             elif "b" in col:
                 a=col.find("b")
                 b="b"
             if "W" not in col or "M" not in col:
                 
                 COL.append(col[0:a])
             
    
     COL = [float(x) for x in COL]
     COL.sort()
     #print(COL)
     col=[]
     for C in COL:
         C=str(C)+b
         if ".0" in C:
             hunt=C.find(".0")
             F=C[0:hunt]
             B=C[hunt+2:len(C)]
             C=F+B
         col.append(C)
  #   print(col)
     fig,ax = plt.subplots(1,1,figsize=(8,8))
     sns.heatmap(data[col].T,ax=ax, cmap='YlOrRd', xticklabels=data.index.strftime('%H'))
     

     #ax.xaxis.set_major_formatter(axHM)
     
def likelikeV2(Dataset,Dates,Sens,vals,ave,maskYN,plotYN,title):
   """
    Data analyis Function, COmpare all sensors in Dataset to one another, on R^2 , 
    Linerarit (Slorp and Intersept),  CV,mean bias , #Mean error, #ROOT Mean square error 
    
    Plot the R^2 onto a heat map
    
    And has option to apply a full mask, i.e to analyis when all sensors are acitive "YES" . 
    If "NO" i will just plot data when the both compared snesors are active 
   Creation:24/06/2019
   
   -25/06/2019
   PlotYN added, with CV begin cacualed, from the rolling avaerage as well
   And the accuacy of the mean measurmet being cacualed too
   """
    
    
   # writer = pd.ExcelWriter(title+'.xlsx', engine='xlsxwriter')
   #make the super mask
   valmask={}
   for val in vals:
       i=0
       mask="Maskholder"
       for sen,item in Dataset.items():
           item=Timecut(item,Dates)
           if i==0:
               #print(sen)
               mask= ~np.isnan(item[val])
               i=i+1
           else:
               nextmask= ~np.isnan(item[val])
               mask= mask & nextmask
            
       valmask[val]=mask #save the mask for the value     
   
   writer = pd.ExcelWriter("Plots//DISSPLOTS//"+title+'.xlsx', engine='xlsxwriter') #create excel sheet
   for val in vals:   
        RR=pd.DataFrame(columns=Sens,index=Sens)  #R2
        MB=pd.DataFrame(columns=Sens,index=Sens) #mean bias , #Mean error, #ROOT Mean square error and normaise all into one array
        ME=pd.DataFrame(columns=Sens,index=Sens)
        RMS=pd.DataFrame(columns=Sens,index=Sens)
        NMB=pd.DataFrame(columns=Sens,index=Sens) #normalized mean bias
        NME=pd.DataFrame(columns=Sens,index=Sens) #normlizedmean error
        CC=pd.DataFrame(columns=Sens,index=Sens)   #Spearmans rank
        AC=pd.DataFrame(columns=Sens,index=Sens) #acccaury of measurment
        LOD=pd.DataFrame(columns=Sens,index=Sens) #Cacualre limit of detecton
        Descount=len(Sens) #sensors number
        EQ=pd.DataFrame(columns=Sens,index=Sens)  #Trend line eqn 
        m=pd.DataFrame(columns=Sens,index=Sens)  #gradient
        a=pd.DataFrame(columns=Sens,index=Sens)  #intercept
        STDerr=pd.DataFrame(columns=Sens,index=Sens)   #standard error of gradient 
        maskV=valmask[val]
        #labes for plots
        labels=pd.DataFrame(columns=Sens,index=Sens)
       # maskV=Timecut(maskV,Dates)
        if "b" not in val:
            if val=="RH":
                val="OPC-RH"
            elif val=="T":
                val="OPC-T"
            for key1, df1 in Dataset.items():
               # print(df1.columns)
                if "-" in key1:
                    a=key1.find("-")
                    key1=key1[0:a]
                df1=Timecut(df1,Dates)
                if maskYN.upper()=="YES":
                    df1=df1[maskV]
                #Add describe data to the CVS
                des=df1[val].describe()
                #add CV to bottom for whoe data 
                #print(des)
                des.loc["CV"]=des.iloc[2]/des.iloc[1] #STD/mean
                des.index.name=key1 #add name of sensors to description
                des["Sensor"]=key1 #add name of sensors to description
                #Add to bottom of R^2 sheet
                des.to_excel(writer, sheet_name='Main-'+val, startrow=len(Sens)+2, startcol=Descount)
                #add the rolling CV to the data
                if "CV-"+val not in df1.columns:
                    df1=rollingCV(df1,val,ave) #create CV if not there (Note may not work)
                #if already threre is should work ok
                dfcv=df1["CV-"+val].describe()
                dfcv["Sensor"]=key1 #add name of sensors to description
                dfcv.to_excel(writer, sheet_name='Main-'+val, startrow=len(Sens)+2, startcol=2*len(sen)+Descount)
                Descount=Descount-1
                
                for key2, df2 in Dataset.items():
                    if "-" in key2:
                        a=key2.find("-")
                        key2=key2[0:a]
                    df2=Timecut(df2,Dates)
                    if maskYN.upper()=="YES":
                        df2=df2[maskV]
            
                #    print("------------",key1,key2,"---------------")
                 
                #    print(df2[val])
               #     print(df1[val])
                    df,s,i,r,p,stderr=CombineStat(df1,df2,key1,key2,val) 
    
                    #caculate mean bias nad mean error 
                   #mean bias , #Mean error, #ROOT Mean square error and normaise all into one array
                    mb=100*((df[val+"_2"]/df[val])-1).mean() #mean bias
                    me=1/len(df)*(abs(df[val+"_2"]-df[val])).sum() #mean error
                    rmse=np.sqrt(1/len(df)*((df[val+"_2"]-df[val])**2).sum()) #root mean suare error
                    nmb=(df[val+"_2"]-df[val]).sum()/(df[val]).sum() #normilzed mean bias 
                    nme=(abs(df[val+"_2"]-df[val])).sum()/(df[val]).sum()  #nromalize mean error 
                    
                    #Caculate mean LOD # only really matter for the GRIMM but inresting to see for the other sensors too
                    LOD.at[key1,key2] =df[val+"_2"][df[val]<1].std()/s
                                       
                    #add to arrays 
                    RR.at[key1,key2]=r**2
                 
                    m.at[key1,key2]=s
                    a.at[key1,key2]=i
                    STDerr.at[key1,key2]=str(stderr)
                    CC.at[key1,key2]=df.corr(method='pearson').iloc[1,0]
                    MB.at[key1,key2]=mb
                    ME.at[key1,key2]=me
                    RMS.at[key1,key2]=rmse
                    NMB.at[key1,key2]=nmb
                    NME.at[key1,key2]=nme
                    AC.at[key1,key2]=100-(abs(df[val+"_2"].mean()-df[val].mean())/df[val].mean())*100 #mean accuary agains target sentos 
                  #  if key2 in k2holder:
                    des2=df2[val].describe()
                    c=des2.iloc[0]
                    labels.at[key1,key2]=c #count label
                   # else:
                    #    labels.at[key1,key2]=r**2
                     #   k2holder.append(key2)
                        
                        
                    
                    
                    
        CC.index.name="PPC"
        RR.index.name="R^2"
        m.index.name="slope"
        a.index.name="intercept"
        STDerr.index.name="STD-err"
        MB.index.name="Mean Bias"
        ME.index.name="Mean error"
        RMS.index.name="Root mean square"
        NMB.index.name="Normalized mean bias"
        NME.index.name="Normalized mean error"
        AC.index.name="Accuracy"
        LOD.index.name="LOD"
       
        #add data to excel sheet    
        RR.to_excel(writer, sheet_name='Main-'+val, startrow=0, startcol=0)
        CC.to_excel(writer, sheet_name='Main-'+val, startrow=0, startcol=2*len(Sens)+2) 
        AC.to_excel(writer, sheet_name='Main-'+val, startrow=0, startcol=len(Sens)+1) 
        LOD.to_excel(writer, sheet_name='Main-'+val, startrow=0, startcol=3*len(Sens)+3) 
        #add colume sutt ot collume
        m.to_excel(writer, sheet_name='slope'+val, startrow=0, startcol=0)
        a.to_excel(writer, sheet_name='slope'+val, startrow=len(Sens)+2, startcol=0) 
        STDerr.to_excel(writer, sheet_name='slope'+val, startrow=2*len(Sens)+4, startcol=0) 
        #add mean bias and error 
        MB.to_excel(writer, sheet_name='Bias&Errors'+val, startrow=0, startcol=0)
        ME.to_excel(writer, sheet_name='Bias&Errors'+val, startrow=len(Sens)+2, startcol=0)
        RMS.to_excel(writer, sheet_name='Bias&Errors'+val, startrow=2*len(Sens)+4, startcol=0)
        NMB.to_excel(writer, sheet_name='Bias&Errors'+val, startrow=0, startcol=len(Sens)+2)
        NME.to_excel(writer, sheet_name='Bias&Errors'+val, startrow=len(Sens)+2, startcol=len(Sens)+2)
       
        
        
        #set everyhing to float so its plots 
        RR=RR[RR.columns].astype(float)
        CC=CC[CC.columns].astype(float)
     
        
        if plotYN.upper()=="YES": #option to plot data or not
         #   RR.to_excel(writer, sheet_name='R^2'+val, startrow=0, startcol=0)
            fig,ax = plt.subplots(1,1,figsize=(25,25))
            
            
            #heatmap
            
            
            
            #mask creation for R^2 bottom left, and count to right
            mask=np.full(np.shape(RR), True, dtype=bool)
            mask[np.triu_indices_from(mask,k=1)] = False
         #   return mask, RR, labels
            RR2=RR
            mask2=~np.array(mask)
            RR2[mask2]=0
            labels[mask]=0
            #labels=labels.values
            #labels= ["("+str(x)+")" for x in labels]
            labels=labels+RR2
            #with sns.axes_styRRle("white"):
              #  ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True)
            cmap=plt.cm.get_cmap('coolwarm', 50)
            newc=cmap(np.linspace(0, 1, 50))
            newc[0]=[0,1,0,0]
            newcmap = ListedColormap(newc)
            sns.heatmap(RR2,vmin=0,vmax=1,robust=True,ax=ax, annot = labels,annot_kws={"size": 15} ,cmap=newcmap,linewidths=1)
           # print(labels)
            ax.set_title("$R^2$ (bottom left), Data points (top right) \n"+title+" ("+val+")",fontsize=30)
            ax.yaxis.label.set_size(20)
            # Rotate the tick labels and set their alignment.
            plt.setp(ax.get_xticklabels(), fontsize = 16, rotation=45, ha="right",rotation_mode="anchor")
            plt.setp(ax.get_yticklabels(), fontsize = 16, rotation=45, ha="right",rotation_mode="anchor")
            ax.set_ylabel("")
            #drop spaced and drop '
            #Title=title.replace(" ", "")
           # Title=Title.replace("'","")
            fig.savefig("Plots//DISSPLOTS//R2-"+title+"-"+val+"-"+maskYN+".png",dpi=300,format='png')
            
      
    #save corrlations 
  
   writer.save()
   return RR,labels


def Histplot(Datas,Dates,val,title):
    #make the data equal 
    i=0
    mask="Maskholder"
    for sen,item in Datas.items():
       print(sen)
       item=Timecut(item,Dates)
       if i==0:
           mask= ~np.isnan(item[val])
           i=i+1
       else:
           nextmask= ~np.isnan(item[val])
           mask= mask & nextmask
       Datas[sen]=item 
    
    fig,ax=plt.subplots(figsize=(10,5))
    
     #color counters
    OPCN2=2
    OPCN3=0
    SDS=0
    ref=0
    color="Red"
    
    for k, item in Datas.items():
        if "OPCN2" in k or "OPCN3_N" in k:
            color=sns.color_palette("YlGn", 5)[OPCN2]
            OPCN2=OPCN2+1 #color counter
        elif "OPCN3" in k:
            color=sns.color_palette("Blues_d",5)[OPCN3]
            OPCN3=OPCN3+1
        elif "SDS" in k:
            color=sns.color_palette("Wistia", 5)[SDS]
            SDS=SDS+1
        elif "GRIMM" in k:
            color="RED"
       # print(color)
        n=len(item[mask][val])
        X=item[mask][val]
        nor=((X)/X.std())
       # sns.kdeplot(nor,ax=ax,shade=False,color=color,label=k)
        sns.distplot(X,ax=ax,hist=False,kde=True,bins=30,kde_kws={'linewidth': 2},color=color,label=k)
       # ax.plot(item[mask][val],density(item[mask][val]))
       # ax.hist(item[mask][val],bins=30,label=k,normed=True,histtype='step', linewidth=3)
    ax.grid(True)
    if "pm2.5" in val:
        ax.set_xlim(0,35)
    elif "pm10" in val:
        ax.set_xlim(0,100)
    ax.set_ylabel("Density",fontsize=15)
    ax.set_xlabel(val+" Mass concentration",fontsize=15)
    ax.set_title(title,fontsize=15)
    ax.legend( prop={'size': 10},title="Sensors")
    fig.savefig("Plots//DISSPLOTS//Hist-"+title+".png",dpi=300,format='png')
def Boxplot(dataset,val,title):
    
    
    sen=[]
    Data=pd.DataFrame()
    for k,item in dataset.items():
        Data=pd.concat([Data,item[val]], ignore_index=False, axis=1,sort=True)
        Data.rename(columns={val:k},inplace=True)
        sen.append(k)
    print(Data.columns)
    fig,ax= plt.subplots(1,1,figsize=(10,10))
    ax=Data.boxplot(column=sen,patch_artist=True,notch = True)
    colors=["red","blue","green"]
    for i, col in enumerate(colors):
        ax.findobj(matplotlib.patches.Patch)[i].set_facecolor(col)
    ax.set_ylim(0,30)
    
    ax.set_ylabel(val+ " ($\mu g/m^3$)",fontsize=20)
    ax.set_title(title,fontsize=20)
    myFmt = mdates.DateFormatter('%H:%M')
    ax.legend( prop={'size': 15})
    ax.xaxis.set_major_formatter(myFmt)
    ax.suptitle(title, fontsize=16)
    fig.savefig("Plots//DISSPLOTS//Boxplot"+title+".png",dpi=300,format='png')

def SizeDistandDeteff(Dataset,ref,refname,Dates,title):
    
   
    
    #Get righttime of data 
    for k,item in Dataset.items():
        item=Timecut(item,Dates)
        Dataset[k]=item
        
    
    #Get count eff    
    Deteff(Dataset,ref,refname,title) 
    #Plot size distribtuin
    DisD=Mulsizedist(Dataset,Dates,title)
 #   WF="Dataset//Leedweather.csv"
    
    
    return DisD
   
def Dataplotter(Dataset,Dates,VAL,title):

    #get the weather data 
    WD=pd.read_csv('Dataset//Leedweather.csv',header=0,error_bad_lines=False,engine='python')
    WD.set_index('Timestamp (UTC)', inplace=True)
    WD.index=pd.to_datetime(WD.index)
    WD=Timecut(WD.resample("10T").mean(),Dates)

    #if len(Dates)==1: #plot the data 
    DHT={}
    for k,item in Dataset.items():
        if "DHT-RH" in item.columns:
            item=item[["DHT-RH","DHT-T"]]
            DHT["DHT-"+k]=Timecut(item,Dates)
            
    fig,(axup,ax)=plt.subplots(2,1,figsize=(10,15),gridspec_kw={'height_ratios': [1, 3]})
    axup.plot(WD["Humid %"],color="Purple")
   
   # cur_axup = mplot.gca()   # cur_axup.axes.get_xaxis().set_visible(False)
   
    
    axup.set_ylabel("WD-RH (%)",color="Purple",fontsize=20)
    axup.tick_params('y', colors='Purple')
    ax2=axup.twinx()
    ln2=ax2.plot(WD["Temp C"],"-",color="Red",alpha=1)
    ax2.set_ylabel('WD-T (C)', color='Red',fontsize=20)
    ax2.tick_params('y', colors='Red')
    for k,item in DHT.items():
        axup.plot(item["DHT-RH"],color="Blue",alpha=0.8)
        ax2.plot(item["DHT-T"],"-",color="pink",alpha=0.8)
        
    axup.set_ylim(0,100)
    axup.grid()
    if len(Dates)==1:
        if len(Dates[0])>8:
            myFmt = mdates.DateFormatter('%H:%M')
        else:
            myFmt = mdates.DateFormatter('%d/%m')
    else:
        myFmt = mdates.DateFormatter('%d/%m')
    axup.xaxis.set_major_formatter(myFmt)
    
    #fig.axup.get_xaxis().set_visible(False)
               # ax.set_ylim(0,60)
    OPCN2=2
    OPCN3=0
    SDS=0
    ref=0
    color="Red"
    for k,item in Dataset.items():
        if "OPCN2" in k or "OPCN3_N" in k:
            color=sns.color_palette("YlGn", 5)[OPCN2]
            OPCN2=OPCN2+1 #color counter
        elif "OPCN3" in k:
            color=sns.color_palette("Blues_d",5)[OPCN3]
            OPCN3=OPCN3+1
        elif "SDS" in k:
            color=sns.color_palette("Wistia", 5)[SDS]
            SDS=SDS+1
        elif "GRIMM" in k:
            color="RED"
    #    Dates=[Dates[0][0:10]] #just get the day not the time 
     
        item=Timecut(item,Dates)
        item=item.resample("10T").mean()
        if VAL in item.columns:
            ax.plot(item[VAL],label=k,color=color)
        ax.xaxis.set_major_formatter(myFmt)
        ax.set_title(title+"\n "+VAL, fontsize=15)
        #ax.set_ylim(0,10)
    ax.legend( prop={'size': 15})
    ax.grid()  
    ax.set_ylabel("Mass concentration ($\mu g/m^3$)",fontsize=15)
    fig.savefig("Plots//DISSPLOTS//Plot"+title+".png",dpi=300,format='png')
def Deteff(Dataset,ref,refname,title):
    
    """
    Detection efficeny subplot,
    
    Created 30/06/2019
    
    
    """
    #Cut all SDS data
    dataset={}
    for k,item in Dataset.items():
        if "SDS" not in k:
            dataset[k]=item
    
    writer = pd.ExcelWriter("Plots//DISSPLOTS//Deff"+title+'.xlsx', engine='xlsxwriter') 
    OPCPM1=["b0","b1","b2"] #0.35um to 1um OPCN3, 0.38 to 1um OPCN2
    OPCPM3=["b3","b4","b5","b6"] #1um to 3um OPCN3 and OPCN2
    OPCPM10=["b7","b8","b9","b10","b11"] #3um to 10um
    FullOPC=["b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","b11","b12","b13","b14","b15"] #OPCN2 0.38 to 17um OPCN3 0.35 to 18um
  #  FullOPCN2=["b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","b11","b12","b13","b14","b15","b16"] #OPCN2 0.38 to 17um OPCN3 0.35 to 18um
   #"0.3um",
    refPM1=["0.4um","0.5um","0.65um","0.8um"] #b0 to b4 #["0.4um","0.5um","0.65um","0.8um","1um"]
    refPM3=["1um","1.6um","2um"	] #b6 to #b7
    refPM10=[ "3um","4um","5um","7.5um"] #b8 to b11
    FullRef=["0.3um","0.4um","0.5um","0.65um","0.8um","1um","1.6um","2um", "3um","4um","5um","7.5um","10um","15um","20um"]
    refBins=[refPM1,refPM3,refPM10,FullRef]
    Bins=[OPCPM1,OPCPM3,OPCPM10,FullOPC]
    subtitles=["< PM1","PM1→PM3","PM3→PM10","Full count"]
    Bindata={}
    fig,axes = plt.subplots(2,2,figsize=(12,12))
    I=0
    Fir=0
    cols=list(dataset.keys())
    CountD={}
    if refname in cols:
        cols.remove(refname)
    X=0# save colume infro
    for Bin,refBin,st,ax in zip(Bins,refBins,subtitles,axes.flat):
        data=pd.DataFrame(index=ref.index,columns=cols)
        color=[]
        I=I+1 
        print(I)
        for k,item in dataset.items():
            if refname not in k:
                if "OPCN2" in k or "OPCN3_N" in k:
                    color.append("GREEN")
                elif "OPCN3" in k:
                    color.append("BLUE")
               
                if "OPCN3" in k:
                    CF=0.001*0.01*item["period"]*item["FlowRate"]
                  #  print(CF)
                elif "OPCN2" in k:
                    CF=0.1*item["period"]*2.2
                   # print(CF)
                    
                refdf=ref[refBin].sum(axis = 1, skipna = True)/(6*1.0512) 
                ref[st]=refdf #/(3*1.0512) #(1.66667e-5))
                if I==4:
                    if "OPCN3" in k:
                        Bin3=["b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","b11","b12","b13","b14","b15","b16"]
                        itemdf=(item[Bin3]).sum(axis = 1, skipna = True)/CF
                    else:
                        itemdf=(item[Bin]).sum(axis = 1, skipna = True)/CF
                else:
                    itemdf=(item[Bin]).sum(axis = 1, skipna = True)/CF
                item[st]=itemdf
                newdf=pd.concat([refdf,itemdf],axis=1,ignore_index=False)
                newdf.columns="ref","sen"   
                #nana chack
                #drop zero data, to sop devtion by zero
                newdf["ref"] = newdf["ref"].replace(0, np.nan)
                newdf["ref"] = newdf["ref"].dropna(how='all', axis=0)
                
    
                mask = ~np.isnan(newdf["ref"]) & ~np.isnan(newdf["sen"])
                newdf=newdf[mask]
                data[k]=(newdf["sen"]/newdf["ref"])*100
                data[k].dropna(how='all', axis=0)
          #      data[k]=data[k].replace(np.nan, 0)
       # print(data.columns)
        #print(data.astype)
        
        dataset[k]=item #return count information to the sensors
        data.boxplot(column=cols,ax=ax,patch_artist=True,notch = True,showfliers=False)
        ax.set_title(st,fontsize=15)
        ax.set_ylabel("Detection efficiency (%)",fontsize=15)
       
        for i, col in enumerate(color):
            ax.findobj(matplotlib.patches.Patch)[i].set_facecolor(col)
        #save the details of count efficeny
        des=data.describe()
        CountD[st]=data
       # ISVrawvals(data,"Deceff"+st,st)
      #  print(des)
        des.index.name=st
        des.to_excel(writer,sheet_name=title,startrow=X,startcol=0)
        X=X+len(des)+3
    if refname in list(dataset.keys()):
        del dataset[refname]
    dataset[refname]=ref #add the new ref data 
    fig.savefig("Plots//DISSPLOTS//DetEff"+title+".png",dpi=300,format='png')
    writer.save()
    
    return dataset
def BoxplotGROUP(dataset,vals,title):
    
    axes=( locals()['ax%d'%i] for i in range(0,len(vals)))
    fig,axes = plt.subplots(len(vals),1,figsize=(8,20))
    for val,ax in zip(vals,axes):
        #color counters
        OPCN2=2
        OPCN3=0
        SDS=4
        ref=0
        color=[]
        sen=[]
        Data=pd.DataFrame()
        for k,item in dataset.items():
            Data=pd.concat([Data,item[val]], ignore_index=False, axis=1,sort=True)
            Data.rename(columns={val:k},inplace=True)
            sen.append(k)
            if "OPCN2" in k or "OPCN3_N" in k:
                color.append("GREEN")
                OPCN2=OPCN2+1 #color counter
            elif "OPCN3" in k:
                color.append("BLUE")
                OPCN3=OPCN3+1
            elif "SDS" in k:
                color.append("ORANGE")
                SDS=SDS+1
            elif "GRIMM" in k:
                color.append("RED")    
                
        print(Data.columns)
        #Data["RH"]=WD["Humid %"]
        #Data=Data.T
       # print(Data)
      #  sns.boxplot(y="", x='continent', 
       #              data=df1, 
        #             palette="colorblind",
         #            hue='year')
        Data.boxplot(column=sen,ax=ax,patch_artist=True,notch = True,showfliers=False)
        ax.set_ylabel(val +" ($\mu g/m^3$)",fontsize=15)
        ax.set_title(val,fontsize=15)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
        
        #colors=["red","blue","green"]
        for i, col in enumerate(color):
            ax.findobj(matplotlib.patches.Patch)[i].set_facecolor(col)
    fig.suptitle(title,fontsize=15)
    fig.savefig("Plots//DISSPLOTS//Boxplot-"+title+".png",dpi=300,format='png')
    
    
def Calval(item,val,S,I):
    """
    Function to applys a linear calbration eqn to a value

    """
    item["Cal-"+val]=S*item[val]+I
    return item
    
def SensorsBias(REF,RefName,Datas,val,Dates,plotYN,title):
    """
    Caculate and Plot sensors bias against a refrence sensors 
    21/06/2019
    """

    if "YES" in plotYN.upper():
        fig,ax=plt.subplots(figsize=(10,10))
    for k,item in Datas.items():
        item["Bias-"+val]=0
        if "RefName" not in k:
            print(k)
            item=Timecut(item,Dates)
            Ref=Timecut(REF,Dates)
            for i,row in item.iterrows():
                #print(Ref.loc[i][val],row[val])  #,row)
                REFI=Ref.loc[i]
                item["Bias-"+val].loc[i]=((row[val]/REFI[val])-1)*100
                #print(((row[val]/REFI[val])-1)*100)
            Datas[k]=item
            if "YES" in plotYN.upper():
                print(item["Bias-"+val].describe())
                ax.plot(item["Bias-"+val],label=k)
                ax.set_ylabel("Bias (%) (Against REF: "+RefName+")")
                ax.legend()
                ax.grid(True)
                fig.autofmt_xdate()
                fig.save_html(fig,"Plots//"+title+REFName+".html")
            
    return Datas
    
def VariableHypoTest(DF,VAL,VAL2,SENNAME):
    '''
    Hypotesis testing 
    https://towardsdatascience.com/inferential-statistics-series-t-test-using-numpy-2718f8f9bf2f
    
    Test two Values from a data frame are statistical significant
    
    2019/06/15
    
    '''
    
    #1st sort out ther data
    df=DF[[VAL,VAL2]].dropna()
    df[VAL]=pd.to_numeric(df[VAL], errors='coerce')
    df[VAL2]=pd.to_numeric(df[VAL2], errors='coerce')
    df = df.loc[~df.index.duplicated(keep='first')]
    mask = ~np.isnan(df[VAL]) & ~np.isnan(df[VAL2])
    df=df[mask]
   # print(df.columns,df.index)
    #df = df.reset_index()
    df=pd.DataFrame([df[VAL],df[VAL2]]).T #just get wanted data in array, speeds up the procesee
 # 
    #print(df.describe())
    #  print(df.corr())
    df=df.dropna() #drop nan data 
    #print(df.var()[VAL])
    #2nd get degrees of freedom
    DF=2*len(df) - 2
    #3rd std deviation
    var_a = df.var(ddof=1)[0]
    var_b = df.var(ddof=1)[1]
    s = np.sqrt((var_a + var_b)/2)
    #4th Calculate the t-statistics
    t = (df[VAL].mean() - df[VAL2].mean())/(s*np.sqrt(2/DF))
    # 5th p-value after comparison with the t 
    p = 1 - stats.t.cdf(t,df=df)
    print("T and P values, Derived")
    print("t = " + str(t))
    print("p = " + str(p[0][1]))
    try:
        print("log10(p) =" +str(-mp.log10(p[0][1])))
    except:
        print("Error in Log-Worth")
        pass
    
    #compare to other methos 
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[VAL],df[VAL2])
    print("Stats line regression"," R:",r_value," P:",p_value)
    t,p=stats.ttest_ind(df[VAL],df[VAL2])
    print("Stats ttest T:",t," P:", p)
    """
    df[VAL+"-CAL"]=slope*df[VAL]+intercept
    
    ax.set_title(SENNAME+": "+VAL+" VS "+VAL2+"\n $R^2$="+str(round(r_value**2,2)))
    #plot regrettion line 
    points = ax.scatter(df[VAL], df[VAL2],label=None)
    im1=sns.regplot(x=VAL,y=VAL2, data=df,ax=ax, scatter=False,label=" y={0:.1f}x+{1:.1f}".format(slope,intercept))
    x=np.arange(0,100,1)
    y=x
    ax.plot(x,y,linestyle = "--",color="black",label="y=x")
    #ax1.set_xlim(0,4)
    ax.legend()
    ax.grid()
    #box plot
    ax2=df.boxplot(column=[VAL, VAL2, VAL+"-CAL"],patch_artist=True)
    colors=["red","blue","green"]
    for i, col in enumerate(colors):
        ax2.findobj(matplotlib.patches.Patch)[i].set_facecolor(col)
    
     #accuray
    df["ac"]=100-(abs(df[VAL+"-CAL"]-df[VAL2])/df[VAL2])*100
  #  print(df.describe())
    #add calibration to old data set
    DF[VAL+"-CAL"]=slope*df[VAL]+intercept
    
    """

    
    
    
def Accuracy(dfs,dfref,refname,val,plotYN,dates):
    """
    Scrpts to generate the accuray to Refrence methods 
    """
    
    
    for k, item in dfs.items():
        #caculare accuracy 
        item["A-"+val]=100-(abs(item[val]-dfref[val])/dfref[val])*100
        print(item["A-"+val].describe())
        
        dfs[k]=item
    if "Y" in plotYN.upper():
        fig,ax= plt.subplots(1,1,figsize=(10,10))
        for k, item in dfs.items():
            
            ax.plot(Timecut(item["A-"+val],dates),label=k)
            ax.legend()
            ax.grid()
            ax.set_ylim(0,100)
            ax.set_ylabel("Accurracy %")
    return dfs  
        
    
    
def Mulsizedist(datas,dates,title):
    """
    Size ditributon plotter functon for multiple sensors.
    
    """
    
    #Cut all SDS data
    dataset={}
    for k,item in datas.items():
        if "SDS" not in k:
            #print(k,item)
            dataset[k]=item
    datas=dataset
    #bin sized arrays in um
    GRIMM1108size = [0.3,0.4,0.5,0.65,0.8,1,1.6,2,3,4,5,7.5,10,15,20]
    OPCN2size= [0.38,0.54,0.78,1,1.3,2.1,3,1.6,4,5,6.5,8,10,12,14,16,17]
    OPCN3size=[0.35,0.45,0.66,1,1.3,1.7,2.3,3,4,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37,40]
    #volumentric size 
    OPCN3sizeVWD=[0.407,0.57,0.84,1.16,1.51,2.01,2.67,3.52,4.63,5.87,7.28,9.04,11.03,13.03,15.02,17.02,19.02,21.02,23.53,26.53,29.53,32.52,35.52,38.52]
    OPCN2sizeVWD=[0.4646,0.6672,0.8945,1.1565,1.4552,1.8612,2.5762,3.5236,4.5184,5.7824,7.2758,9.0369,11.0302,13.0256,15.0222,16.5050]
    GRIMM1108sizeVWD= [0.3524,0.4518,0.5782,0.7276,0.9037,1.3227,1.8074,2.5329,3.5236,4.5184,6.3322,8.8091,12.6645,17.6182,20.0000]
            
            
              #define fingure
    SizeD={}
    fig,ax= plt.subplots(1,1,figsize=(10,10))
    fig2,ax2= plt.subplots(1,1,figsize=(10,10))
    fig3,ax3= plt.subplots(1,1,figsize=(10,10))
    for k, item in datas.items():  
        item=Timecut(item,dates)
        Sizedata=pd.DataFrame(columns=["Size","dN/dr","SDEV","dN/dV","dN/dM"])
        Sizedata.set_index('Size', inplace=True, drop=True)
        size=[] #place holder to code to run
        if "GRIMM" in k.upper():
            size=GRIMM1108size
            CF=3*1.0512
            Stop="20um"
        elif "OPCN3" in k.upper():
            size=OPCN3size
            Stop="b24" #Stop before last bin
            CF=0.001*0.01*item["period"]*item["FlowRate"]
        elif  "OPCN2" in k.upper():
            size=OPCN2size
            Stop="b16" #Stop before last bin
            CF=0.1*item["period"]*2.2
         
        
        #find mode bin 
        cols=[]
        colm={}
        i=0
        for S in size:
            if "GRIMM" in k.upper():
                col=str(S)+"um"
                if col!=Stop:
                    cols.append(col) 
                    colm[col]=S
            else:
                col="b"+str(i)
                if col!=Stop:
                    i=i+1
                    cols.append(col) 
                    colm[col]=S
        
       
       
        modetest=item[cols].mode()
        modecol=sorted(modetest)[0] #assue top col is mode 
     #   print(modecol)
        i=0
        Mpv=""
        #generate the volumet weghted diamter for the mean size bin
        for S, col in zip(size,cols):
         #  print(S,col)
           i=i+1 #for upper size bin
           if col==modecol:     
               Mpv=S*(1/4*(1+(size[i]/S)**2)*(1+(size[i]/S)))**(1/3)
              # print(modecol, Mpv)
          
        i=0
        #content=pd.DataFrame() #creata a dict for the partile count 
        Lx=[]
        vals=["dN/Log($D_{pv}$)","dN/Log($V_{pv}$)","dN/Log($M_{pv}$)"]
        size=sorted(size)
        #print(k,size)
        for S in size:
            if i==len(size)-1:
                pass #issue of last bin, just pass and use prevous width
            else:
                BW=size[i+1]-S #Binwidth
                #print(S,BW)
            if "GRIMM" in k.upper():
               # print(S)
                col=str(S)+"um"
              
                content=item[col]  
                sy="-^"
            
            else:
                col="b"+str(i)
                if col!=Stop:
                    content=item[col]  
                
                sy="-o"
            
          #  item=content[S]
          #  print(col,i-1)
        
            N=content/CF # Count array
            SD=content.std() #standard deviaton of the count 
           # print(SD)
            if SD==0:
                SD=1
                Sizedata.loc[S]=0 #if no count dont to the math just set to zero
                
            if i==len(size)-1:
                Dpv=size[i]
            else:    
                Dpv=size[i]*(1/4*(1+(size[i+1]/size[i])**2)*(1+(size[i+1]/size[i])))**(1/3)
            
            #if "GRIMM" in k:
           # print(k,Dpv)
            i=i+1  
            for val in vals:
                if "$D_{pv}$" in val:
                    dpv=Dpv
                    L=mp.log1p(dpv) # logarithm of the radii
                    val="dN/dr"
                    
                    
                elif "$V_{pv}$" in val:
                    dpv= (1/6)*mp.pi*Dpv**3
                    L=mp.log1p(dpv) # logarithm of the volme
                    val="dN/dV"
                elif "$M_{pv}$" in val:
                    dpv= (1/6)*mp.pi*Dpv**3*1.65e+12 #times desinty of 1.65g/cm^3
                    L=mp.log1p(dpv) # logarithm of the volme
                    val="dN/dN"
                Lx.append(L)
                Nd1=(N/SD)*(np.sqrt(2*mp.pi))
                Nd2=mp.exp((Mpv-L)/(2*SD**2))
                Nor=mp.log1p(BW) #Normilvization log of the bin width
                Ndis=Nd1*Nd2*(1/Nor) 
                Sizedata.loc[Dpv,val]=Ndis.sum()
                Sizedata.loc[Dpv,val+"SDEV"]=Ndis.std()
           
        col=Sizedata.columns
        #Sizedata["SDEV"]=Sizedata["SDEV"])
        #ax.semilogx(Lx,Sizedata["dN/dr"],sy,label=k)
        ax.plot(Sizedata["dN/dr"],sy,label=k)
        ax2.plot(Sizedata["dN/dV"],sy,label=k)
        ax3.plot(Sizedata["dN/dM"],sy,label=k)
        #ax.errorbar(Sizedata.index,"dN/dr",yerr="SDEV",data=Sizedata,fmt=sy,lw=2,capsize=3,label=k)
        SizeD[k]=Sizedata
    #ax.xaxis.set_major_locator(ticker.LogLocator(base=1.0, numticks=15))
    axes=[ax,ax2,ax3]
   
    for ax, val in zip(axes,vals):
        ax.set_xscale('symlog', linthreshy=0.1) #, linthreshy=0.1)
        ax.set_yscale('symlog', linthreshy=5)#,  linthreshy=0.1)    
        
        #ax.axis([0.1,1,2.5,5,10,15])
        #ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        ax.set_xticks([0.3,0.5,1,1.5,2,2.5,5,10,15,20,30,40])
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        #ax.set_xticklabels([0.1,1,10])   
        if "D" in val:
        
            ax.set_ylim(0,1.5*10**6)
        ax.set_xlim(0.3,40)
   # ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_ylabel(val,fontsize=20)
        ax.set_xlabel("Volumetric particle diameter (um)",fontsize=20)
        ax.grid(True)
        ax.legend(prop={'size': 15})
        ax.set_title(title,fontsize=20)
    fig.savefig("Plots//DISSPLOTS//dNdLogDplot"+title+".png",dpi=300,format='png')
    writer = pd.ExcelWriter("Plots//DISSPLOTS//dNdlogDvp"+title+'.xlsx', engine='xlsxwriter') 
    col=0
    for k,item in SizeD.items():
        item.index.name=k
        item.to_excel(writer,sheet_name=title,startrow=0,startcol=col)
        col=col+3
    writer.save()
    
    
    
    
    """
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    # Sets the ticks to be on the left and bottom axes.
    """  
    return SizeD



"""
--------------------------------------------------------------------------------------------
                                        RH Effect Code 
--------------------------------------------------------------------------------------------                                        
"""

def CiRH(item,K,val,RHval):

#cirrly C-factor
    item["Ci-C"]=1
    item["Ci-"+val]=item[val]/item["Ci-C"]
    
    #Option to add more controll
   #  data["Ci-"+val]=data[val]/data["Ci-C"]
    for index, row in item.iterrows():
        if row[RHval]>50:
            C=1+(K/1.65)/((100/row[RHval])-1)
            item.loc[index,"Ci-C"]=C
            item.loc[index,"Ci-"+val]=row[val]/C
          #  print(item.columns)        
    return item

def RHanal(RawData,ave,Dates,title,vals,kfactor):
    
    
     #Get Weather data
    WF="Dataset//Leedweather.csv"
    wd=pd.read_csv(WF,header=0,error_bad_lines=False,engine='python')
    wd.set_index('Timestamp (UTC)', inplace=True)
    wd.index=pd.to_datetime(wd.index)
    if ave !="1T":
        WD=wd.resample(ave).mean()
    else:
        WD=wd.resample(ave).ffill()
    Data={}
    for k,item in RawData.items():
        item=Timecut(item,Dates)
        item=item.resample(ave).mean()
        item["WD-RH"]=WD["Humid %"]
        item["WD-T"]=WD["Temp C"]
        Data[k]=item
    RHval="WD-RH"
    #GRIMM calibration 1 
    
    
    

     #control
  #  r,l=AQ.likelikeV2(Data,Dates,list(Data.keys()),vals,ave,"NO",plot,title)
    print("--------Control---------")
    Histplot(Data,Dates,vals[0],title)
    BoxplotGROUP(Data,vals,title)
   # AQ.ISVrawvals(Data,title,vals)
   # RHvsMassplotMul(Data,Dates,vals[0],"WD-RH",ave+"Control")
    #RH cut 
    print("--------85 RH cut-----------")
    Data85={}
    for k,item in Data.items():
        item,drop=ValLimDrop(item,"WD-RH",85,"<")
        Data85[k]=item
   # AQ.ISVrawvals(Data85,title+"RH-85cut",cals)
   # AQ.likelikeV2(Data85,Dates,list(Data.keys()),vals,ave,"NO",plot,title+"RH85")
    #RHvsMassplotMul(Data85,Dates,"PM-pm2.5","WD-RH",ave+"CAL-RHCUT85")
    Histplot(Data85,Dates,vals[0],title+"RH-85cut")
    BoxplotGROUP(Data85,vals,title+"RH-85cut")
    #AQ.likelikeV2(Data85,Dates,list(Data.keys()),["PM-pm2.5","PM-pm10"],ave,"YES",plot,title+"-RH-85")
    print("-------Ci 2018 ----------")
    DataRHC={}
    for k,item in Data.items():
        item=item[vals+["WD-RH","WD-T"]]#free up memenor
        RHval="WD-RH"
        for v in vals:
            K=kfactor
            item.is_copy = False
            item=CiRH(item,K,v,RHval)
            #Option to add more controll
            # data["Ci-"+val]=data[val]/data["Ci-C"]
         #   for index, row in item.iterrows():
          #      if row[RHval]>75:
           #         C=1+(K/1.65)/((100/row[RHval])-1)
            #        item.loc[index,"Ci-C"]=C
             #       item.loc[index,"Ci-"+v]=row[v]/C
                   # print(item.columns)
            DataRHC[k]=item  
  #  AQ.ISVrawvals(DataRHC,title,["Ci-PM-pm2.5","Ci-PM-pm10"])
    Histplot(DataRHC,Dates,"Ci-PM-pm2.5",title+"RH-Ci")
    BoxplotGROUP(DataRHC,["Ci-PM-pm2.5","Ci-PM-pm10"],title+"RH-Ci")
    return DataRHC, Data85, Data
def RHvsMassplot(Data,TVal,RHVal,title):
    fig,ax=plt.subplots(figsize=(12,8))
    ax.scatter(x=Data[RHVal],y=Data[TVal], s=75)
    if "pm" in TVal:
        if "VS" not in TVal:
            ax.set_ylabel( TVal+"($\mu g/m^3$)", fontsize=10)
    else:
        ax.set_ylabel( TVal, fontsize=10)
    if "RH" in RHVal:
        ax.set_xlabel( RHVal+"(%)", fontsize=10)
    elif "T" in RHVal:
        ax.set_xlabel(RHVal+"($^\circ$C)", fontsize=10)
    ax.set_title(title,fontsize=10)
    fig.savefig("Plots//DISSPLOTS//RH-effect"+title+".png",dpi=300,format='png')
    ax.grid()
def RHvsMassplotMul(Datas,Dates,TVal,RHVal,title):   
    N=len(Datas)
    axes=( locals()['ax%d'%i] for i in range(0,N))
    fig,axes = plt.subplots(1,N,figsize=(12,8))
    i=0
    for k,Data in Datas.items():
        print("------",k,"----------")
        if i==0: 
            ylim=75
            print(ylim)
            print(Data[RHVal].describe())
            if "pm" in TVal:
                if "VS" not in TVal:
                    axes[i].set_ylabel( TVal+"($\mu g/m^3$)", fontsize=10)
            else:
                axes[i].set_ylabel( TVal, fontsize=20)
        Data=AQ.Timecut(Data,Dates)
        points=axes[i].scatter(x=Data[RHVal],y=Data[TVal],s=50,c=Data["WD-T"], cmap="jet")
        
        
        
       
        #cbar.set_clim(0, 100)
        
  
        if "RH" in RHVal:
            axes[i].set_xlabel( RHVal+"(%)", fontsize=10)
        elif "T" in RHVal:
            axes[i].set_xlabel(RHVal+"($^\circ$C)", fontsize=10)
        axes[i].grid()
        axes[i].set_title(k,fontsize=10)
        axes[i].set_ylim(0,ylim)
        i=i+1
    cax = fig.add_axes([0.92, 0.1, 0.04, 0.8]) # left, bottom, width, height
    #cbar.ax.set_yticklabels(['2.5'," '0', '> 1'])
    cbar=fig.colorbar(points,cax)
  #  cbar.ax.set_ylabel('Temp (C) \n',fontsize=20, rotation=270,labelpad=1)    
    fig.savefig("Plots//DISSPLOTS//RH-effect"+title+".png",dpi=300,format='png')
#    fig.subplots_adjust(left = 1.01) 
