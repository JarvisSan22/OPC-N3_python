# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:47:40 2019

@author: Jarvis
OPCN2 Bin check 
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import mpld3
import glob
import seaborn as sns
import AQfunctions as AQ
from scipy import stats

def Binmass(data,plot,sen,val,figname):
   # print("Check bin")
    
    if "OPCN2" in sen:
        bininfo=pd.read_csv("OPCN2BinsConversions.csv",header=2,error_bad_lines=False)
    elif "OPCN3" or "AQRPI" in sen:
        bininfo=pd.read_csv("OPCN3BinsConversions.csv",header=2,error_bad_lines=False)
    bininfo.set_index("bins names",inplace=True,drop=True)
    #add the mass per columns 
   # for col in data.columns:
    #    if "b" in col:
     #       if col != col+"W":
      #          data[col+"W"]=0
    
    if "OPCN2" in sen:
        #Re Cacualte factory settings 
        for col in data.columns:
            if "b" in col:
                if "W" in col:
                    pass
                else:
                    #factors with bin weighing
                    data[col+"WF"]=data[col]*bininfo.loc[col]['Mass (ug)']*bininfo.loc[col]['bin weight']
                    #col info with mass
                    data[col+"W"]=data[col]*bininfo.loc[col]['Mass (ug)']
       
        #generate recalucated PM, from Respiraty convertion
            
            data["FC-pm1"]=0
            data["FC-pm2.5"]=0
            data["FC-pm10"]=0
            for col in data.columns:
                if "b" in col:
                    if "WF" in col: #use the bin weighting
                        #here the bins will be the WF bins but the bins with out are needed for the bininfo,
                        #so the WF is cut from the colums in the bininfo, to solve this problem 
                        data["FC-pm1"]=data["FC-pm1"]+(data[col]*bininfo.loc[col[0:len(col)-2]]['PM1 RC']/100)
                        data["FC-pm2.5"]=data["FC-pm2.5"]+(data[col]*bininfo.loc[col[0:len(col)-2]]['PM2.5 RC']/100)
                        data["FC-pm10"]=data["FC-pm10"]+(data[col]*bininfo.loc[col[0:len(col)-2]]['PM10 RC']/100)
            
    #Normalise for volums sample volume 
    #flow rate is in L/min, converting to m3/s and 0.1 seconds to seconds 
        LMcon=1.66667e-6
        #data["period"]=10
        data["flowrate"]=2.20
         #generate recalucated PM, from Respiraty convertion
        data["FM-pm1"]=data["FC-pm1"]/((data["flowrate"])*LMcon*data["period"])
        data["FM-pm2.5"]= data["FC-pm2.5"]/((data["flowrate"])*LMcon*data["period"])
        data["FM-pm10"]=  data["FC-pm10"]/((data["flowrate"])*LMcon*data["period"])
        #generate recaliaed PM2, from 2nd eqn, b5 and bellow
    
        data["PC-pm1"]=data['b0W']+data['b1W']+data['b2W']+data['b3W']
        data["PC-pm2.5"]=data['b0W']+data['b1W']+data['b2W']+data['b3W']+data['b4W']+data['b5W']+data['b6W']
        data["PC-pm10"]=data['b0W']+data['b1W']+data['b2W']+data['b3W']+data['b4W']+data['b5W']+data['b6W']+data['b7W']+data['b8W']+data['b9W']+data['b10W']+data['b11W']
        #Normalize for volume
        data["PM-pm1"]=data["PC-pm1"]/(data["flowrate"]*LMcon*data["period"])
        data["PM-pm2.5"]= data["PC-pm2.5"]/(data["flowrate"]*LMcon*data["period"])
        data["PM-pm10"]=  data["PC-pm10"]/(data["flowrate"]*LMcon*data["period"])
    elif "OPCN3" in sen:
        #data.rename(columns={"FlowRate":"flowrate"},inplace=True)
     #   print(data.columns)
        #no Respority convertion infromation for OPCN3, just pythiscs mass will be cacualted
        for col in data.columns:
            if "b" in col:
                if "W" in col:
                    pass
                else:
                #col info with mass
                    data[col+"W"]=data[col]*bininfo.loc[col]['Mass (ug)']
        #data["period"]=10
        #data["FlowRate"]=280
        data["PC-pm1"]=data['b0W']+data['b1W']+data['b2W']+data['b3W']
        data["PC-pm2.5"]=data['b0W']+data['b1W']+data['b2W']+data['b3W']+data['b4W']+data['b5W']+data['b6W']
        data["PC-pm10"]=data['b0W']+data['b1W']+data['b2W']+data['b3W']+data['b4W']+data['b5W']+data['b6W']+data['b7W']+data['b8W']+data['b9W']+data['b10W']+data['b11W']
        LMcon=1.66667e-5*0.001*0.01 #period to  second 0.01 , Flowrate 9n  L/min
        #normalize for sample volume 
        data["PM-pm1"]=data["PC-pm1"]/(data["FlowRate"]*LMcon*data["period"])
        data["PM-pm2.5"]= data["PC-pm2.5"]/(data["FlowRate"]*LMcon*data["period"])
        data["PM-pm10"]=  data["PC-pm10"]/(data["FlowRate"]*LMcon*data["period"])
      
 
    
  
    if plot.lower()=="yes":   
        df=data
        #just plot the 1st data data 
        #day1=str(df.maxxid.date())
        day1="2019-04-30"#str(data[val].idxmax().date())
        PDF=AQ.Timecut(df,[day1])
        fig,(axe,axe2) = plt.subplots(2,1,figsize=(10,15))
        axe.plot(PDF[val],label="Factory-"+val)    
        if "OPCN2" in sen:
            print(data["FM-"+val].describe())
            axe.plot(PDF[day1]["FM-"+val],label="New-Facotry-"+val,linestyle="-")

        axe.plot(PDF[day1]["PM-"+val],label="PM-"+val,linestyle=":")
        myFmt = mdates.DateFormatter('%H:%M')
        axe.xaxis.set_major_formatter(myFmt)
        axe.set_ylabel("Mass concentration (ug/m^3)",fontsize=15)
        axe.set_title(sen+" "+val+ " PM-Conversion \n" +"Plot Date:"+day1 ,fontsize=15)
        axe.grid()
        axe.legend(prop={'size': 15})
        start=str(min(df.index).date())
        stop=str(max(df.index).date())
       
             #Compare old to new data 
        mask= ~np.isnan(df[val]) & ~np.isnan(df["PM-"+val])
        slope, intercept, r_value2, p_value, std_err = stats.linregress(df[val][mask],df["PM-"+val][mask])
        print("S",slope, "I",intercept,"R",r_value2,"P", p_value,"Std-err", std_err )
        sns.regplot(x=val,y="PM-"+val, data=df,ax=axe2, scatter=True,label="Factory(x) VS PM(y) y={0:.1f}x+{1:.1f}".format(slope,intercept),scatter_kws={'s':10})
        axe2.set_title("Plot Date:"+start+"→"+stop+"\n ( Factory VS PM R^2="+str(round(r_value2**2,2)) +")",fontsize=15)
        axe2.set_xlabel("(x) Mass concentration ug/m^3",fontsize=15)
        axe2.set_ylabel("(y) Mass concentration ug/m^3",fontsize=15)
        x=np.arange(0,100,1)
        axe2.legend(prop={'size': 15})  
        axe2.grid()
        axe2.set_ylim(0,50)
        axe2.set_xlim(0,50)
        y=x
        axe2.plot(x,y,linestyle = "--",color="black",label="y=x")
        #add new data info to xlsx file
        writer = pd.ExcelWriter(figname+val+'.xlsx', engine='xlsxwriter') #create excel sheet
        new=data["PM-"+val].describe()
        old=data[val].describe()
        new.loc["PMvsFac-R^2"]=r_value2**2
        new.loc["PMvsFac-Slope"]=slope
        new.loc["PMvsFac-Intercept"]=intercept
        new.loc["PMvsFac-Std-err"]=std_err 
        new.to_excel(writer, sheet_name=sen+val, startrow=0, startcol=0)
        Next=len(new) #greata an array to place the OPCN2 addtion data at 
        old.to_excel(writer, sheet_name=sen+val, startrow=0, startcol=2)
        #df=df.notna()
        fig.savefig("OPC-Convertion"+figname+val+".png",dpi=300,format='png')
        if "OPCN2" in sen:
            fig2,axe3 = plt.subplots(1,1,figsize=(10,7.5))    
            #compare recacualted factor to Physica data 
            mask = ~np.isnan(df["FM-"+val]) & ~np.isnan(df["PM-"+val])
            slope, intercept, r_value, p_value, std_err = stats.linregress(df["FM-"+val][mask],df["PM-"+val][mask])
            print("New Factory vs PM S",slope, "I",intercept,"R", r_value,"P", p_value,"Std-err", std_err )
            im2=sns.regplot(x="FM-"+val,y="PM-"+val, data=df,ax=axe3, scatter=True,label="New-Factory(x) VS PM(y) y={0:.1f}x+{1:.1f}".format(slope,intercept),scatter_kws={'s':20})

            new=data["FM-"+val].describe()
            new.loc["FMvsPM-R^2"]=r_value**2
            new.loc["FMvsPM-Slope"]=slope
            new.loc["FMvsPM-Intercept"]=intercept
            new.loc["FMvsPM-Std-err"]=std_err 
           
           #New Factory vs Old Factory
            mask = ~np.isnan(df["FM-"+val]) & ~np.isnan(df[val])
            slope, intercept, r_value3, p_value, std_err = stats.linregress(df["FM-"+val][mask],df[val][mask])
            print("Factory vs New-Factory S",str(slope), "I",str(intercept),"R", r_value3,"P", p_value,"Std-err", std_err )
            im3=sns.regplot(x="FM-"+val,y=val, data=df,ax=axe3, scatter=True,label="New-Factory(x) VS Factory(y) y={0:.1f}x+{1:.1f}".format(slope,intercept),scatter_kws={'s':20})
            axe3.set_title("Plot Date:"+start+"→"+stop+"\n (Re-Factory vs PM R^2="+str(round(r_value**2,2))+") "+ "(Re-Factory vs Factory R^2="+str(round(r_value3**2,2))+")",fontsize=15)
            axe3.set_xlabel("(x) Mass concentration ug/m^3",fontsize=15)
            axe3.set_ylabel("(y) Mass concentration ug/m^3",fontsize=15)
            x=np.arange(0,100,1)
            axe3.legend(prop={'size': 15})  
            axe3.grid()
            axe3.set_ylim(0,50)
            axe3.set_xlim(0,50)
            y=x
            axe2.plot(x,y,linestyle = "--",color="black",label="y=x")
            fig2.savefig("OPC-Convertion-Factory"+figname+val+".png",dpi=300,format='png')
        
            new.loc["FMvsFac-R^2"]=r_value3**2
            new.loc["FMvsFac-Slope"]=slope
            new.loc["FMvsFac-Intercept"]=intercept
            new.loc["FMvsFac-Std-err"]=std_err 
            new.to_excel(writer, sheet_name=sen+val, startrow=0, startcol=4)
        writer.save()
        
    print("PM2.5 recacualted")
    return data 
    

#sen="JIMSOffice_AQRPI2_OPCN2_2_20190415_20190430.csv"
def genData(loc,Folder):
    sfiles=[]
    for file in glob.glob(Folder+"***.csv"):
        if loc in file:
            sfiles.append(file)
    sfiles=sorted(sfiles)
    if len(sfiles)>1:   
        df=pd.DataFrame()
        for file in sfiles: #add two data sets together
            dataloop=pd.read_csv(file,header=5,error_bad_lines=False,parse_dates=True)
            df=pd.concat([df,dataloop], ignore_index=True, axis=0)  
              
    else: #If just one data set
        if "GRIMM" in file:
              df=pd.read_csv(file,error_bad_lines=False) 
        else:   
            df=pd.read_csv(file,header=5,error_bad_lines=False)      
    df["time"]=pd.to_datetime(df.time) 
    df.set_index('time', inplace=True, drop=True)
    return df
