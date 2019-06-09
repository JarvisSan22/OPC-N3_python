# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 10:51:23 2019

@author: Jarvis

Functions 
"""
import glob #used in to read in all the fles
import pandas as pd
import numpy as np
from datetime import datetime#
from datetime import timedelta 
import glob #used in to read in all the fles
from scipy import stats
import matplotlib
import seaborn as sns
from sklearn.linear_model import LinearRegression
import GRIMM as GM
import matplotlib.pylab as plt
import codecs
import AQMapfunctions as AQMap



def droperror(data,col,limit,condition):
    '''
    Error data cutter fuction, does not cut all the other data but set that columns error to None values 
    '''
    
    print("-------------------Cutting data", col, limit, condition)
    
    print(max(data[col]))
    if condition =="greater":
        indexNames = data[ data[col] > limit ].index
        data.drop(indexNames , inplace=True)

        #mask=data[col]>int(limit)
    elif condition =="less":
        indexNames = data[ data[col] < limit ].index
        data[col].drop(indexNames , inplace=True)
   # data.loc[mask,col]=None 
  
    print(max(data[col]))
    return data

def gencount(Data):
    """
       does not work
    """
    cols=[]
    for col in Data.columns:
        if "b" in col or "um" in col:  #OPC bin data is b0 b1 b2 ... GRIMM bin data is 0.3um 0.5um ....
           # print(col)
           # Data[col].fillna(0,inplace=True)
           if col != "checksum":
               cols.append(col)
    
    print("Generate Total Partile count")
    print(cols)
    Data["ParticleCount"]=Data[cols].sum(axis=1)
    print(Data["ParticleCount"])
    return Data
def genratio(Data,col1,col2):
    rationame=col1+"VS"+col2
    Data[rationame]=Data[col1]/Data[col2]
    return Data

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
                        print(i,row)
                        header=i
             if "GRIMM" in sfiles[0]: #account for GRIMM data header=1
                 data=pd.read_csv(sfiles[0],header=header,error_bad_lines=False,engine='python')
                 
             else:
                
                 data=pd.read_csv(sfiles[0],header=header,error_bad_lines=False,engine='python')
                 if "SDS" in sensor:
                     data=data.loc[:,"time":"sds-pm10"]
                 else:
                     
                     data.rename(columns={"pm2":"pm2.5","RH":"OPC-RH","T":"OPC-T","b24":"cut"},inplace=True)
               
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
                    if "SDS" in sensor:
                         dataloop=dataloop.loc[:,"time":"sds-pm10"]
                    else:
                         dataloop.rename(columns={"pm2":"pm2.5","RH":"OPC-RH","Temp":"OPC-T","b24":"cut"},inplace=True)

                    
                data=pd.concat([data,dataloop], ignore_index=False, axis=0,sort=True)  
        #print(data.columns)
        if "GRIMM" not in sensor:
            split=sfiles[0].split("_")
            file=sfiles[0]
            sen="" #varable place holder 
            if "OPCN3" in file:
                 loc=file.find("OPCN3_")
                 
         
            elif "SDS" in split[2]:
                 loc=file.find("SDS011")
            elif "OPCN2" in split[2]:
                 loc=file.find("OPCN2_")
            
            #find location 
            
            Loc=file.find("AQ")
            Loc=Loc-1 
            Loc=file[len(Folder)-1:Loc]
            if "GPS" in file:
                Loc=Loc+"-GPS"
            sen=Loc+":"+sensor
            print(data.head(4))
            data["time"]=pd.to_datetime(data.time)   
            data.set_index('time', inplace=True)  
            print("---------------"+sen+"-----------------------------")
            print(data.columns)
            
            #deal with non float varaible types 
            for k,c in data.iteritems():
                typ=str(c.dtype)
                if "float" not in typ:
           #         print(k)
                    data[k]=pd.to_numeric(data[k], errors='coerce')
                    data[k]=data[k].astype('float64')
            data = data.loc[~data.index.duplicated(keep='first')]
          
            
            #drop error data  
            for col in data.columns :
                if "pm" in col:   
                    try:
                        data=droperror(data,col,1000,"greater")
                        data=droperror(data,col,0,"less")
    
                    except:
                        pass
                 
                elif col=="DHT-RH":
                     print(col)
                     data=droperror(data,col,100,"greater")
                   #  data=droperror(data,col,0,"less")
                    
             
            
            
            if "SDS" in sensor:
                data=genratio(data,"sds-pm10","sds-pm2.5") #gen pm10/pm2.5
            else:
                data=genratio(data,"pm10","pm2.5") #gen pm10/pm2.5
                data=genratio(data,"pm2.5","pm1") #gen pm2.5/pm1
                data=gencount(data)
                #generate calibrated RH and T based on DHT22
                if "OPCN3" in sensor:
                     if "DHT-RH" in data.columns:
                         data=VariableCalPlot(data,"OPC-RH","DHT-RH",sen)
                         data=VariableCalPlot(data,"OPC-T","DHT-T",sen)
                    
                
        else:
            sen=sensor
            GRIMM1108size = [0.3,0.4,0.5,0.65,0.8,1,1.6,2,3,4,5,7.5,10,15,20]
            print(data)
            data["time"]=pd.to_datetime(data.time) 
            
            data.time=data.time+timedelta(hours=1) #account for log being in UTC
            
            data.set_index('time', inplace=True, drop=True)
            
            data=GM.binmass(data,GRIMM1108size)
            data=gencount(data)
            data=genratio(data,"pm10","pm2") #gen pm10/pm2.5
            data=genratio(data,"pm2","pm1") #gen pm2.5/pm1
        #print(sen)
        if ave != "RAW": #If there is a avearege then get mean, if RAW dont take mean
            #print(data.dtypes)
            for k,c in data.iteritems():
                typ=str(c.dtype)
                if "float" not in typ:
           #         print(k)
                    data[k]=pd.to_numeric(data[k], errors='coerce')
                    data[k]=data[k].astype('float64')
            print(data.dtypes)
            data=data.resample(ave).mean()
         #   print(data.columns)
       
       # print(data)
        
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
            
            
            
print("--------------------")
def dateparse (timestamp):
    time=pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
    return time 

def GetRPIdataV2(Folder,RPI,ave):
    '''
    Function to get the all OPC Data from RPI and put it in a directory,
    Allowing further use and plotting.
    Need 
    Folder location for data
    The RPI name in the CSV file 
    ave- the averageing what wanted to be applied
    ave: 5T - 5 mim, 30T - 30 min, RAW - raw data no avarage 
    
    16/04/2019
    -removes nan data, and deals with resample issue
    -find sen in the first line of CSV
    '''
    #Get files 
    sfiles = [] #set array to hold file names
     #  folder=Folder
    for file in glob.glob(Folder+'***.csv'):
            if RPI in file:
                sfiles.append(file)
       # print(sfiles)
    sfiles=sorted(sfiles) #does them in a random order , so need to be sorted
    #Read the data into a panda array
  #  print(sfiles)
    df=pd.DataFrame()
    sen=[]

    for loc in sfiles:
        #read in data 
        dataloop=pd.read_csv(loc,skiprows=[1],error_bad_lines=False,parse_dates=True, date_parser=dateparse)
        sen=pd.read_csv(loc,skiprows=1, nrows=1,header=None)
       
    
   #     print(dataloop.head(4))
        #cut out error sen in first line 
        sen=sen.T[1:len(sen.T)].as_matrix()
        sen=sen[:,0]
        sen=sen[pd.notnull(sen)]
       
        #return sen
        
        #re read csv but get the sensor info
       # try:
        #except:
         #   pass
      #  print(dataloop.columns)
        df=pd.concat([df,dataloop], ignore_index=True, axis=0)   
       # print(df.head(4))

    #print("sen",sen)
    df.set_index('time', inplace=True, drop=True)
    
    d={}
    OPC=0
    OPCN3cols='b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16','b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'b23', 'cut', 'period','FlowRate', 'Temp', 'RH', 'pm1', 'pm2', 'pm10', 'Check'
    OPCN2cols='b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15','ct','FlowRate', 'temp_pressure','period', 'Check','pm1', 'pm2', 'pm10'
   # print(df.head(4))
    #pd.DataFrame()
    for I,S in enumerate(sen):
        #print(I,S,sen[len(sen)-1])
        #Set the Temp into its own array
        if "DHT" in S:
    #        print("DHTcheck",len(df["RH"]),len(df["T"]))
        #gt data 
            #df = df.reset_index()
            d[S]=pd.concat([df["RH"],df["T"]],axis=1)
           
            #d[S].columns=["RH","T"]
     #       print(d[S].head(4))
           # d[S]=pd.DataFrame(data=[df["RH"],df["T"]])
            
        #transpose it  
            d[S]=d[S]
           # d[S]=d[S].drop(d[S][d[S]["RH"]==None].index)
            #d[S]=d[S].drop(d[S][d[S]["RH"]>100].index)
        #make usre the index name is correct    
        
            d[S].index.names = ['time']
            #deal with None data 
            d[S].replace('None', np.nan, inplace=True)
            d[S]=d[S][d[S]["RH"].notnull()]
            d[S]=d[S][d[S]["T"].notnull()]
      #      print(d[S].head(4))
            
        elif "OPC" in S:
            #find  sensors index
            ScolInd=df.columns.get_loc(S)
            #if just one OPC or the last out of all OPC running get data
            if I == len(sen)-1:
                data=df.iloc[:,ScolInd:len(df.columns)]
            else:
                #If not the Last OPC, get data between the two sensors
                  #Define the end index
                
                ScolInd2=df.columns.get_loc(sen[I+1])
                data=df.iloc[:,ScolInd:ScolInd2]
               # print(data.head(3))
            
            d[S]=pd.DataFrame(data)
           # print(S,d[S].columns)
             #add a colums name       
            if "OPCN3" in S:
                sencols=("Name",)+OPCN3cols  #set a name colums#
            elif "OPCN2" in S:
                sencols=("Name",)+OPCN2cols  #set a name colums#
            d[S].columns=sencols #update the colums names to deal with the b1.1 or b1.2 for multiple sensors 
            #cut the name colums as it get in the way of the avarage, and no longer needed
            #d[S]=d[S].rename(S)
            d[S].drop("Name",axis=1)   
            #make shure the time index is named correctly
            d[S].index.names = ['time']
            d[S]=d[S][d[S].notnull()]
            OPC=OPC+1
#        pd.concat(d, axis=1)    
            
       # print("issue",d[S].head(30))
        #avarage the data if desired, if not type RAW    
        if ave != "RAW":
            try:
                #mean data based on the set resample length
                d[S].index=pd.to_datetime(d[S].index)
                d[S]=d[S].resample(ave).mean()
            except:
                #deal with a data error what comes about when the None data is cut from the DHT22
                
                d[S]=d[S].astype(float)
                d[S]=d[S].resample(ave).mean()
                
   # print("d",d)
    return d ,sen  
def GetRPIdataV1(Folder,RPI,ave,sen):
    '''
    Function to get the all OPC Data from RPI and put it in a directory,
    Allowing further use and plotting.
    Need 
    Folder location for data
    The RPI name in the CSV file 
    ave- the averageing what wanted to be applied
    ave: 5T - 5 mim, 30T - 30 min, RAW - raw data no avarage 
    
    #Created :11/04/2019
    Daniel Jarvis 
    For the first calibration test with the data looking like "JimsOffice_AQRPI5_(,DHT22_3,OPCN3_6,OPCN3_N1)_20190410.csv "
    This format is no longer used, as the CMAC people compalined, even though they wanted all the info in the heading in the first place.
    To account for this the sen varable was added, not futer version of the code will have an featuer to fins sen in the file.
    
    '''
   #Get files 
    sfiles = [] #set array to hold file names
     #  folder=Folder
    for file in glob.glob(Folder+'***.csv'):
            if RPI in file:
                sfiles.append(file)
                print(sfiles)
    sfiles=sorted(sfiles) #does them in a random order , so need to be sorted
    
    #Read the data into a panda array
    df=pd.DataFrame()
    for loc in sfiles:
        
        dataloop=pd.read_csv(loc,parse_dates=['time'],error_bad_lines=False,engine='python')
        print(dataloop.head(3))
        df=pd.concat([df,dataloop], ignore_index=True, axis=0)
       
    df.set_index('time', inplace=True, drop=True)
    print("Check all data",df.head(3))
   # df=df[(df.index > Start) & (df.index < Stop)]
    
    d={}
    OPC=0
    OPCN3cols='b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16','b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'b23', 'b24', 'period','FlowRate', 'Temp', 'RH', 'pm1', 'pm2', 'pm10', 'Check'
    
    #pd.DataFrame()
    for I,S in enumerate(sen):
        #print(I,S,sen[len(sen)-1])
        #Set the Temp into its own array
        if "DHT" in S:
            print(df["RH"].head(3),df["T"].head(5))
        #gt data 
            d[S]=pd.DataFrame(data=[df["RH"],df["T"]])
        #transpose it  
            d[S]=d[S].T
            
            #drop nan data 
            d[S]=d[S][d[S]['RH'].notnull()]
         #   d[S]=d[S].drop(d[S][d[S]["RH"]>100].index)
        #make usre the index name is correct    
            d[S].index.names = ['time']
        elif "OPCN3" in S:
            #find sensoe
            ScolInd=df.columns.get_loc(S)
            #if just one OPC or the last out of all OPC running
            if I == len(sen)-1:
    #            print("End")
     #           print(ScolInd,len(df.columns)-1)
                data=df.iloc[:,ScolInd:len(df.columns)]
            else:
                #Need to get data betwwn the two sensors
               # print("Split")
                  #Define the end index
                ScolInd2=df.columns.get_loc(sen[len(sen)-1])
                data=df.iloc[:,ScolInd:ScolInd2]
               # print(data.head(3))
    
            
            d[S]=pd.DataFrame(data)
           
            
            sencols=("Name",)+OPCN3cols  #set a name colums
            
            d[S].columns=sencols
            d[S].drop("Name",axis=1)  #cut the name colums as it get in the way of the avarage
            d[S].index.names = ['time']
            OPC=OPC+1
        if ave != "RAW":
            d[S]=d[S].resample(ave).mean()
    
        pd.concat(d, axis=1)
    return d ,sen


def getfiles(sensor,folder,ave,Start,Stop):
    """
    The sensors is iver "SDS", "OPC", "PMS" for it corrisponds to the director the test data is in
    
    """
    sfiles = [] #set array to hold file names
  #  folder=Folder
    for file in glob.glob(folder+'***.csv'):
    #   print(file)
        if sensor in file:   
    #        print(file)
            #If statment to plot the sensors name, needs to be similer to t
            sfiles.append(file)
   # print(sfiles)
    sfiles=sorted(sfiles) #does them in a random order , so need to be sorted
   
    if "OPCN3" in sensor:
        sendata=OPCN3Data(sfiles,ave,Start,Stop)
        sendata.head(5)
        return sendata
    elif "SDS" in sensor:
        sendata=SDSData(sfiles,ave,Start,Stop)
        return sendata
    elif "OPCN2" in sensor:
        sendata=OPCData(sfiles,ave,Start,Stop)
        return sendata
    elif "PMS" in sensor:
        sendata=PMSData(sfiles,ave,Start,Stop)
        return sendata
    #elif "DHT11" in sensor:
      #  sendata=DHTData(sfiles,ave,Start,Stop)
       # return sendata
       

def OPCData(Locs,ave,Start,Stop):
    '''
    Combines the OPC N2 Data , and deals with error data 
    
    Note OPC do no have PM2.5 only PM2!!!!!!!!!!!!
    '''
    df=pd.DataFrame()
    for loc in Locs:
        dataloop=pd.read_csv(loc,parse_dates=['time'],error_bad_lines=False)
        df=pd.concat([df,dataloop], ignore_index=True, axis=0)
   
    #df=pd.DataFrame({'time': data['time'] ,'PM1':data['pm1'], 'PM2.5':data['pm2'], 'PM10':data['pm10'],'period':data['period']})
    
    df.drop(df[df['pm2']<0].index, inplace=True,axis=0)
    df.drop(df[df['pm2']>9999].index, inplace=True,axis=0)
    df.drop(df[df['pm10']<0].index, inplace=True,axis=0)
    df.drop(df[df['pm10']>9999].index, inplace=True,axis=0)
    #print(df.head(12))
    df.set_index('time', inplace=True, drop=True)
    #deadling with error date 
    #drop odd time periods 
  #  df=df.drop(df[df['period']>10].index)
    #df=df.drop(df[df['period']<5].index)
    df=df.drop(['period'], axis=1)
    #drop off data
    if (Stop=="" or Stop is None):   
        df=df[Start]
    else:
        df=df[Start:Stop]
    #df=df[(df.index > Start) & (df.index < Stop)]
    if ave != "RAW":
        df=df.resample(ave).mean()
    return df

def myparser(x):
    try:
         a=datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    except:
     #   print("Error")
        a="nan"
    return a

def OPCN3Data(Locs,ave,Start,Stop):
    '''
    Combines the OPC N3 Data , and deals with error data 
    Needs  a files as Locs, an data average , a Start and a Stop time
    '''
    df=pd.DataFrame()
    for loc in Locs:
        print(loc)
        dataloop=pd.read_csv(loc,parse_dates=True,error_bad_lines=False)
        if dataloop !="nan":  
            print(dataloop.head(5))
          #  dataloop.set_index('time', inplace=True, drop=True)
            print(dataloop.head(5))
            df=pd.concat([df,dataloop], ignore_index=False, axis=0)
            print(df.head(5))
   # df.set_index('time', inplace=True, drop=True)
    print("Cut time",df.head(5))
    #df.set_index('time', inplace=True, drop=True)
    
   
    #df.drop(df[df['pm2']<0].index, inplace=True,axis=0)
    #df.drop(df[df['pm2']>9999].index, inplace=True,axis=0)
    #df.drop(df[df['pm10']<0].index, inplace=True,axis=0)
    #df.drop(df[df['pm10']>9999].index, inplace=True,axis=0)
   # df.head(5)
    #deadling with error date 
    #drop odd time periods 
  
  

   # print(df.head(12))
    #df=df[(df.index > Start) & (df.index < Stop)]
    #print(df.head(10))
    if ave != "RAW":
        df=df.resample(ave).mean()
    return df

def OPCN3Data2(Locs,ave,Start,Stop):
    '''
    Combines the OPC N3 Data , and deals with error data 
    Needs  a files as Locs, an data average , a Start and a Stop time
    '''
    df=pd.DataFrame()
    for loc in Locs:
        #print(loc)
        dataloop=pd.read_csv(loc,parse_dates=["time"],date_parser=myparser, error_bad_lines=False)
        print(dataloop.head(5))
        dataloop.set_index('time', inplace=True, drop=True)
        print(dataloop.head(5))
        df=pd.concat([df,dataloop], ignore_index=False, axis=0)
        print(df.head(5))
   # df.set_index('time', inplace=True, drop=True)
    print("Cut time",df.head(5))
    #df.set_index('time', inplace=True, drop=True)
    
   
    #df.drop(df[df['pm2']<0].index, inplace=True,axis=0)
    #df.drop(df[df['pm2']>9999].index, inplace=True,axis=0)
    #df.drop(df[df['pm10']<0].index, inplace=True,axis=0)
    #df.drop(df[df['pm10']>9999].index, inplace=True,axis=0)
   # df.head(5)
    #deadling with error date 
    #drop odd time periods 
  
  

   # print(df.head(12))
    df=df[(df.index > Start) & (df.index < Stop)]
    #print(df.head(10))
    if ave != "RAW":
        df=df.resample(ave).mean()
    return df



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
    
def SDSData(Locs,ave,Start,Stop):
    '''
   Combines the SDSll data, and deal with the error values 
    '''
    data=pd.DataFrame()
    for loc in Locs:
        dataloop=pd.read_csv(loc,parse_dates=['time'], error_bad_lines=False)
        data=pd.concat([data,dataloop], ignore_index=True, axis=0)
    #print(data.head(10))
    df=pd.DataFrame({'time': data['time'], 'PM2.5':data['pm2.5'], 'PM10':data['pm10'],'Check':data['Check']})
    #print(len(df))
    #error data has the check =999
    df=df.drop(df[df["Check"]==999].index)
    #print(len(df))
    #print(df.head(12))
    df.set_index('time', inplace=True, drop=True)
    if ave != "RAW":
        df=df.resample(ave).mean()
    return df

def PMSData(Locs,ave,Start,Stop):
    '''
   Combines the PMS data, and deal with the error values 
    '''
    data=pd.DataFrame()
    for loc in Locs:
        dataloop=pd.read_csv(loc,parse_dates=['time'])
        data=pd.concat([data,dataloop], ignore_index=True, axis=0)
    print(data.head(10))
    df=pd.DataFrame({'time': data['time'],'PM1':data['pm1(STD)'], 'PM2.5':data['pm2.5(STD)'], 'PM10':data['pm10(STD)']})
    print(len(df))
    print(df.head(12))
    df.set_index('time', inplace=True, drop=True)
    df=df[(df.index > Start) & (df.index < Stop)]
    if ave != "RAW":
        df=df.resample(ave).mean()
    return df
 



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
    print("Pre length:",pre)
    if cond==">":
        data.drop(data[data[val]>limit].index, inplace=True,axis=0)
    elif cond =="<":
        data.drop(data[data[val]<limit].index, inplace=True,axis=0)
    elif cond =="==":
        data.drop(data[data[val]==limit].index, inplace=True,axis=0)
    elif cond =="<=":
        data.drop(data[data[val]<=limit].index, inplace=True,axis=0)
    elif cond =="=>":
        data.drop(data[data[val]<=limit].index, inplace=True,axis=0)    
    elif cond =="!=":
        data.drop(data[data[val]!=limit].index, inplace=True,axis=0)     
    print("After",len(data)," Data points droped=",pre-len(data))
    return data
def ValLimDropArray(DataArray,val,limit,cond):
    for n,opc in enumerate(DataArray):
        opc=ValLimDrop(opc,val,limit,cond)
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
    
def CombineStat(df1,df2,S1,S2,VAL):
    
    '''
    Statistanca anayslsi fuction to run states.lineregression for diffrent varaibes
    '''
    #Combine the data fram in a easy way, all the non over laps show up as NAN
#    print(df1[VAL].head(4))
 #   print(df2[VAL].head(4))
    newdf=pd.concat([df1[VAL],df2[VAL]],axis=1)
    newdf.columns=VAL,VAL+"_2"
    
   
    #nana chack
    mask = ~np.isnan(newdf[VAL]) & ~np.isnan(newdf[VAL+"_2"])
    newdf=newdf[mask]
    slope, intercept, r_value, p_value, std_err = stats.linregress(newdf[VAL],newdf[VAL+"_2"])
   # slope, intercept, r_value p_value, std_err = stats.linregress(x,y)
    print(S1,'_VS_',S2, ' p=',p_value, " r=" , r_value)
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
        points = ax.scatter(D1[VAL], D1[VAL2],c=D1.mapval, s=75, cmap="jet",label=None)
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
    
    
def VariableCalPlot(DF,VAL,VAL2,SENNAME):
    '''
    
    Data frame variable calibration, i.e for RH and Temp if a DHT22 is in the dataframe 
    
    2019/06/08
    '''
    #df=pd.DataFrame()
    df=DF[[VAL,VAL2]].dropna()
    df[VAL]=pd.to_numeric(df[VAL], errors='coerce')
    df[VAL2]=pd.to_numeric(df[VAL2], errors='coerce')
    df = df.loc[~df.index.duplicated(keep='first')]
    mask = ~np.isnan(df[VAL]) & ~np.isnan(df[VAL2])
    df=df[mask]
    print(df.columns,df.index)
    #df = df.reset_index()
    df=pd.DataFrame([df[VAL],df[VAL2]]).T #just get wanted data in array, speeds up the procesee
    print(df.head(2))
    #S1 VS S2
    #print(df.describe())
    print(df.corr())
    df=df.dropna() #drop nan data 
    fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,12))
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[VAL],df[VAL2])
    
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
    print(df.describe())
    #add calibration to old data set
    DF[VAL+"-CAL"]=slope*df[VAL]+intercept
    return DF
    

