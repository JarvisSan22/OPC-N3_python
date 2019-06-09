# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 08:57:39 2019

@author: Jarvis
"""


import matplotlib.pylab as plt
import mpld3
import pandas as pd
import glob 
import numpy as np
import AQMapfunctions as AQMap
import csv
import os 
from datetime import datetime
from datetime import timedelta
from Genlivehtml import genLivedash 
import sys 
import codecs



def droperror(data,col,limit,condition):
    '''
    Error data cutter fuction, does not cut all the other data but set that columns error to None values 
    '''
    try:
        if condition =="greater":
            mask=data[col]>int(limit)
        elif condition =="less":
            mask=data[col]<int(limit)
        data.loc[mask,col]=None 
    except:
        pass
    return data

def gencount(Data):
    """
       does not work
    """
    cols=[]
    for col in Data.columns:
        if "b" in col:
           # print(col)
           # Data[col].fillna(0,inplace=True)
            cols.append(col)
    print(cols)
    Data["ParticleCount"]=Data[cols].sum(axis=1)
    #print(Data["particle count"])
    return Data
def genratio(Data,col1,col2):
    rationame=col1+"VS"+col2
    Data[rationame]=Data[col1]/Data[col2]
    return Data

def GetDataset(Folder,sensors,ave):
    Data={}#set array to hold file names
    infos={}
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
        file=""
        if len(sfiles)==1:
             file=sfiles[0]
             with codecs.open(file, "br",encoding="utf8", errors='ignore') as test:
                #print(test)
                row=""
                for i, row in  enumerate(test):
                    if "time" in row:
                        print(i,row)
                        header=i
      
             data=pd.read_csv(file,header=header,error_bad_lines=False,engine='python')
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
              
                dataloop=pd.read_csv(file,header=header,error_bad_lines=False,engine='python')
                if "SDS" in sensor:
                     dataloop=dataloop.loc[:,"time":"sds-pm10"]
                else:
                     dataloop.rename(columns={"pm2":"pm2.5","RH":"OPC-RH","Temp":"OPC-T","b24":"cut"},inplace=True)
                data=pd.concat([data,dataloop], ignore_index=False, axis=0,sort=True)  
        #print(data.columns)
        #generate info from the last data file 
        with open(file) as f:
            reader=csv.reader(f) #read in the file
            info={}  #set dic
            i=0
            for row in reader:
                i=i+1
                if i<header:
                    print(row)
                    rowinfo=rowinfo=list(filter(None,row[1:5]))
                    info[row[0]]=rowinfo
        print("Printig Data file info ",info)
                    
    
    
        #genrate sensors name with locations 
        sen="" #varable place holder     
        Loc=file.find("AQ")
        Loc=Loc-1 
        Loc=file[len(Folder)-1:Loc]
        
       
        
        sen=Loc+":"+sensor
        
        data["time"]=pd.to_datetime(data.time)   
        data.set_index('time', inplace=True)  
        
        print("---------------"+sen+" Data Check-----------------------------")
        print("-----------------Data------------------")
        print(data.head(4))
        print("--------------Data columns-------------------------------")
        print(data.columns)
        
        if "SDS" in sensor:
            #add ratio
            data=genratio(data,"sds-pm10","sds-pm2.5") #gen pm10/pm2.5
        else:
            #add ratio
            data=genratio(data,"pm10","pm2.5") #gen pm10/pm2.5
            data=genratio(data,"pm2.5","pm1") #gen pm2.5/pm1
            data=gencount(data)

        if ave != "RAW": #If there is a avearege then get mean, if RAW dont take mean
            #print(data.dtypes)
            for k,c in data.iteritems():
                typ=str(c.dtype)
                if "float" not in typ:
           #         print(k)
                    data[k]=pd.to_numeric(data[k], errors='coerce')
            #data=data.astype('float64')
          #  print(data.dtypes)
            data=data.resample(ave).mean()
         #   print(data.columns)
         
        #drop odd data, negative and unreal values   
        for col in data.columns :
             if "pm" in col:   
                 try:
                     data=droperror(data,col,1000,"greater")
                     data=droperror(data,col,0,"less")
    
                 except:
                     pass
                 
             elif col=="DHT-RH":
                 try:
                     data=droperror(data,col,100,"greater")
                     data=droperror(data,col,0,"less")
                 except:
                     pass
       # print(data)
        
        Data[sen]=data
        infos[sen]=info
    return Data , infos




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
        
def ploter(Datas,Cols,Dates,filename,infos,ave):
    """
    Data plotter for OPC,SDS and DHTs.
    Take OPC Data as Datas, and DHT data though DHTs. It will generate a subplot for each varaible in Cols
    Plot for Date range in Dates, 
    in format [Start,End] where the dates have to be in "yyyy-mm-dd" format (i.e "2019-04-30").
    Read the data out into diffrent html files for each varaible what then can be implemented into a dashboard 
    Last edit
    
    18/05/2019
    
    -added make new directory for each plot "Date and filename"
    
    """
    locname=createdir(filename) #create new directory for output 
    print(locname)
    #loop through vraibles
    for var in Cols:
        #MAP Plots  
        if var.upper()=="STATICMAP":
            print("===================Generating Static Map==============================")
            titlename="Plots//"+locname+filename+'-'+var #save name 
            AQMap.GenStaticTimemap(Datas,"pm2.5",ave,titlename,infos)
        elif var.upper()=="GPSWALK":
            print("==================Generating GPS Walk map==========================")
            titlename="Plots//"+locname+filename+'-'+var #save name 
            AQMap.genmap(Datas,"pm2.5",titlename,infos)
        
        #Data Time series plots 
        else:
            print("===================Generating time plot=====================")
            #Create sfig for each varable 
            fig,ax = plt.subplots(1,1,figsize=(15,8))
            alpha=0.8 #faddin for plots
            titledate=""
            lns=[]
            labels=[]
            #color counters
            OPCN2=0
            OPCN3=0
            SDS=0
            color=plt.cm.autumn(SDS)
            DHT="" #place holder for DHT name  to stop errors in no DHT is in data
              #loop through data dictionary
            for k,df in Datas.items():
                print("---------Plotting "+k+"--Value "+var+"------------------------")
                info=infos[k]
                sensors=info["Sensors:"]
                sens=[] #array for OPC sensors 
                for s in sensors:
                    if "DHT" in s:
                        DHT=s #add DHT sensors 
                    else:
                        sens.append(s) #append sensords 
                        OPC=s
               
                  #  DHT=""
                #genrate colores based on sensors 
                if "OPCN2" in OPC:
                    color=plt.cm.cool(OPCN2)
                    OPCN2=OPCN2+60 #color counter
                elif "OPCN3" in OPC:
                    color=plt.cm.winter(OPCN3)
                    OPCN3=OPCN3+60
                elif "SDS" in OPC:
                    color=plt.cm.spring(SDS)
                    SDS=SDS+60
        
                try:
                    #plot data in deseried dates need format ["2019-04-29","2019-04-30"] or ["2019-04-30"]
                    try:
                        if len(Dates)>1:
                           DF=df[(df.index > Dates[0]) & (df.index <= Dates[1])]
                           #DF=df[Dates[0]:Dates[1]]
                           titledate=Dates[0]+"--"+Dates[1]
                        else:
                            DF=df[Dates[0]]
                            titledate=Dates[0]
                    except:
                        print("""
                        -------Time ERROR-------      
                        Is the Datas in the correct format ?
                        i.e  ["2019-04-29","2019-04-30"]  for an range 
                        or  ["2019-04-30"] for a sinlge day ?
                        """)
                    
                    try: #plot data 
                        print(var,OPC) 
                        if var=="RH" or var=="T": #if val is temp of RH 
                            try:
                                if "OPC" in OPC:
                                    ln=ax.plot(DF["OPC-"+var],label="OPC-"+var,color=color)
                                    labels.append(OPC)
                                    lns.append(ln)
                                    try:
                                        ln=ax.plot(DF["OPC-"+var+"-CAL"],label="OPC-"+var+"-CAL",linestyle="-.",color=color)
                                        labels.append(OPC)
                                        lns.append(ln)
                                    except:
                                        print("No calibration Data")
                                if "DHT-RH" in DF.columns:
                                    ln=ax.plot(DF[DHT+"-"+var],label=var,linestyle="--",color=color,alpha=alpha)
                                    labels.append(DHT+"-"+var)
                                    lns.append(ln)
                            except Exception as e: #If error occures
                                print("-------ERROR in Plotting RH or T values-----------")
                                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                                print(type(e))
                                print(e.args)
                                pass
                          
                         
                        else:#if not RH or T value 
                            if "SDS" in OPC:
                                print("PLOTTING SDS")
                                try:
                                    if "VS" in var: #Deal with ratios and new names of sds 
                                        Var="sds-"+var[0:var.find("VS")+2]+"sds-"+var[var.find("VS")+2:len(var)]
                                        ln=ax.plot(DF[Var],label=OPC,color=color,alpha=alpha)
                                    else:
                                        #plot normal data
                                        print(var)
                                        ln=ax.plot(DF["sds-"+var],label=OPC,color=color,alpha=alpha)
                                except Exception as e: #If error occures
                                    print("-------------ERROR in Plotting SDS data "+ var +"--------------")
                                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                                    print(type(e))
                                    print(e.args)
                                    pass
                            else:
                                
                                if var in DF.columns:
                                    ln=ax.plot(DF[var],label=OPC,alpha=alpha,color=color)
                        
                
                            
                            lns.append(ln)
                            labels.append(OPC)        
                            
                             
                    except Exception as e:
                            print("""
                            --------PLOT ERROR---------
                    
                            """)
                            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                            print(type(e))
                            print(e.args)
                            pass
                  
                except Exception as e: #If error occures
                        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                        print(type(e))
                        print(e.args)
                        pass
               # print("Check lables for mpld3 interactive legends", labels)
                interactive_legend = mpld3.plugins.InteractiveLegendPlugin(lns, labels, alpha_unsel=0.1,alpha_over=1, start_visible=True)
                mpld3.plugins.connect(fig, interactive_legend)
                #Add y axis labes depending of value 
                if ("pm" in var and "VS" not in var):
                    ax.set_ylabel("Mass concenration (ug/m^3)" , fontsize=20)
                   # ax.set_xlim([0,50]) 
                elif "RH" in var:
                     ax.set_ylabel("Realitivy Humidity (%)", fontsize=20)
                elif "T" in var:
                    ax.set_ylabel("Temprature (C)", fontsize=20)
                elif "Flow" in var:
                    ax.set_ylabel("Flow rate (ml/min)", fontsize=20)
             #   print(labels,len(labels))
              #  print(lns,len(lns))
                #Add axis title and legend 
                ax.set_title(filename+"-"+titledate+"\n ( "+var+" )",fontsize=20)
                ax.legend()
                ax.grid()
                fig.subplots_adjust(right=0.7)
                figname = "Plots//"+locname+filename+'-'+var #save name 
                mpld3.save_html(fig,figname+".html")
            
                #double columns does not work with intractive legends on mpld3 but it will work for normal plots 
                if var == "pm2.5" or var=="ParticleCount": #double axis for pm2.5 with RH
                    if "DHT-RH" in DF.columns:
                        ax2=ax.twinx()
                        ax2
                        x=DF.index
                        y=np.ones(len(x), dtype=int)*80 #create 80% RH line 
                        ax2.plot(x,y,linestyle = "--",color="black")
                        ln2=ax2.plot(DF["DHT-RH"],color="Teal",alpha=0.5)
                        ax2.set_ylabel('RH (%)', color='Teal')
                        ax2.tick_params('y', colors='Teal')
                        for tl in ax2.get_yticklabels():
                            tl.set_color('Teal')
                        lns.append(ln2)
                        split=OPC.split(":")
                        labels.append(split[0]+":DHT22")
            
            
            fig.savefig(figname+".png",dpi=300,format='png')
      
            
        
    #generate dashboard 
    genLivedash(locname,filename,Cols)


#Code to run the functions
Sens=["SDS011_1"]
#RPIs=[,"GRIMM"] #RPI3 naes 
vals=["pm2.5","GPSWALK","STATICMAP"] #colums
ave="1T"
#Get date for today and yesterday
today=datetime.today().strftime("%Y-%m-%d")
yesterday=datetime.today() - timedelta(days=1)
yesterday=yesterday.strftime("%Y-%m-%d")
#yesterday="2019-05-25"
Dates=["2019-05-24"]
#Dates=["2019-04"]
filename="RPI3PlotScriptstest"
#Generate PLOT
Folder="Dataset//Portsmouth//GPS//"
Data,infos=GetDataset(Folder,Sens,ave)
ploter(Data,vals,Dates,filename,infos,ave)



