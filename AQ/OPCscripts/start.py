#!/usr/bin/env python
#imports 
from __future__ import print_function
import threading as th
import multiprocessing as mp
import serial
import time
import struct
import datetime
import sys
import os.path
import variables as V

if V.DHTON=="ON":
    from DHT import DHT
#import GPSGET
#import GPS2

MODE=V.MODE
if MODE=="GPS":
    from GPS2 import Work #IF GPS is on import module
    
from opcn2_rec import Opcn2
from opcn3_rec import Opcn3



  
#Gloabl varaibles
FOLDER=V.FOLDER #Folder location for data save
LOCATION=V.LOC[0] #RPI3 operation location
lat=V.LOC[1]#location latatuide
lon=V.LOC[2]#location longatuide
RPI=V.RPINAME
def initFile(date,RPI,FOLDER,LOCATION,SENSORS):
    #create columes depending on sensors and OPRATION
    columns="time"
    NAMES=""
    if MODE =="GPS":
        LOCATION=LOCATION+"_GPS"
        columns=columns+",lat,lon,alt"
    if V.DHTON=="ON":
        for sen in V.DHTNAMES:
            columns=columns+",DHT-RH,DHT-T"
    if V.OPCON=="ON":
        for sen in SENSORS:
            #check which sensors are running to add to the csv filre name (If multiple add the togher in order data is made)
            if NAMES=="":
                NAMES=NAMES+sen
            else:
                NAMES=NAMES+","+str(sen)#solution to odd error, when python does not think str are str
            #loop through sensors to create columns 
            if "OPCN3" in sen:
                columns=columns+",b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,MToF,period,FlowRate,OPC-T,OPC-RH,pm1,pm2,pm10,Check"
            elif "OPCN2" in sen:
                columns=columns+",b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,ct,flowrate,temp_pressure,period,checksum,pm1,pm2,pm10"
            
     #create the csv
    csvnames=NAMES.replace(",","-") #replace the commers from the Sensors names to add tio file name
    ofile= FOLDER + LOCATION +"_"+ RPI+'_' +csvnames+"_"+ str(date).replace('-','') + ".csv"
    print("Opening Output File:")
    if(not os.path.isfile(ofile)):
        print("creat new file ",ofile)
        f=open(ofile,'w+')#open file 
        #First add time period
        ts = time.time()
        tnow = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 
        print("Time Period,start:,"+tnow+",end:,",file=f)
        #Add sensors information
        print("Sensors:,"+NAMES,file=f)
        #Add locations
        print("Location:,"+LOCATION+",Lat-Lon,"+lat+","+lon,file=f)
        #Add interval time
        print("Interval time,"+str(V.integration),file=f)
        #Add data columns 
        print(columns,file=f)
        
    else:
        f=open(ofile,'a')
        #if already created append to file     
    return f


if __name__ == "__main__":
    #run sensors
    runsen=V.RUNSEN
    if V.DHTON=="ON":
        for DHTN in V.DHTNAMES:
            runsen.append(DHTN)
    print(V.RPINAME, " Starting in Mode: ",V.MODE, "Sensors:", V.RUNSEN," Time: ", datetime.datetime.now(),"Location:",V.LOC[0])
    inter=V.integration#Interval time between readings 
   
    P=V.RUNPORT
    R=V.RUNSEN
    #Array for operational sensors class calls
    opsen=[]
    for r in R:
        if "OPCN2" in r:
            opsen.append(Opcn2)
        elif "OPCN3" in r:
            opsen.append(Opcn3)
    
    #get the processes to run
    print("Starting AQ RPI, Mode:", V.MODE)
    print("**************************************************")
    print("integration time (seconds)",inter)
    print("**************************************************")
    #processes=[mp.Process(target=c,args=(p,r)) for c,p ,r in zip(opsen,P,R)]
    
    #run all the processes
    if V.OPCON=="ON":
        Sen=[]
        for sen, p, r in zip(opsen,P,R):
            Start=sen(p,r) #initiate the sensors
            Sen.append(Start)
            print(r," Ready")
        print(len(Sen))
    time.sleep(4)
    points=0 #data point longer 
    while time.time() % inter != 0:
        pass
    
        print("Looping")
        while True:
            #set stars
            datestart = datetime.date.today()
            starttime = datetime.datetime.now()
            #Create file if not alrady created
            f = initFile(datestart,RPI,FOLDER,LOCATION,R)
            ts = time.time()
            tnow = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')   
            data=tnow  

            if MODE=="GPS":  #IF GPS is attahced and turned on, get GPS data
              lat,lon,alt= Work()
              data=data+","+str(lat)+","+str(lon)+","+str(alt)
            if V.DHTON=="ON": #Get DHT data, for all DHT attached
                for DH, PIN in zip(V.DHTNAMES,V.DHTPINS):
                    HT=DHT()
                    RH, T= HT.getData(DH,PIN)
                    data=data+","+str(RH)+","+str(T)
            #run through each sensors reading there data
            if V.OPCON=="ON":
                for pro, r,p in zip(Sen,R,P): #loop through OPC
                    newdata=pro.getData(p,r)
                    data=data+","+newdata
                    #printe all data  and write it to the file
                    
            print(data,file=f)
            points=points+1#add a point to point arraw
            #prase to csv
            f.flush()
            if (datetime.date.today() - datestart).days > 0:
                #add end info 
                #too do add write point and end time to top data
                
                f.close()
                datestart = datetime.date.today()
                f = initFile(datestart,RPI,FOLDER,LOCATION,R)

            secondsToRun = (datetime.datetime.now()-starttime).total_seconds() % inter
            time.sleep(inter-secondsToRun)

        
        
        
