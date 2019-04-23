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
from DHT import DHT

MODE=V.MODE
#if MODE=="FULL":
from opcn2_rec import Opcn2
from opcn3_rec import Opcn3



  
#Gloabl varaibles
FOLDER=V.FOLDER #Folder location for data save
LOCATION=V.LOCATION #RPI3 operation location
RPI=V.RPINAME
def initFile(date,RPI,FOLDER,LOCATION,SENSORS):
    #create columes depending on sensors and OPRATION
    columns="time"
    NAMES=""
   
    if V.DHTON=="ON":
        for sen in V.DHTNAMES:
            columns=columns+","+sen+",RH,T"
            NAMES=NAMES+","+sen #put temp senosrs make first to aprear in the csv
    if V.OPCON=="ON":
        for sen in SENSORS:
            #check which sensors are running to add to the csv filre name (If multiple add the togher in order data is made)
            NAMES=NAMES+","+sen
            if "OPCN3" in sen:
                columns=columns+","+sen+",b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,period,FlowRate,Temp,RH,pm1,pm2,pm10,Check"
            elif "OPCN2" in sen:
                columns=columns+","+sen+",b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,ct,flowrate,temp_pressure,period,checksum,pm1,pm2,pm10"
          
                
     #create the csv
    ofile= FOLDER + LOCATION +"_"+ RPI+'_' + str(date).replace('-','') + ".csv"
    print("Opening Output File:")
    if(not os.path.isfile(ofile)):
        print("creat new file")
        f=open(ofile,'w+')
        print(columns,file=f)
        print(NAMES,file=f)
    else:
        f=open(ofile,'a')
            
    return f


if __name__ == "__main__":
    #run sensors
    print(V.RPINAME, " Starting in Mode: ",V.MODE, "Sensors:", V.RUNSEN," Time: ", datetime.datetime.now())
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

     
            if V.DHTON=="ON":
                for DH, PIN in zip(V.DHTNAMES,V.DHTPINS):
                    HT=DHT()
                    RH, T= HT.getData(DH,PIN)
                    data=data+","+DH+","+str(RH)+","+str(T)
            #run through each sensors reading there data
            if V.OPCON=="ON":
                for pro, r,p in zip(Sen,R,P):
                    print(r)
                    newdata=pro.getData(p,r)
                    data=data+","+r+","+newdata
                    #printe all data  and write it to the file
                    
            print(data,file=f)
            #prase to csv
            f.flush()
            if (datetime.date.today() - datestart).days > 0:
                f.close()
                datestart = datetime.date.today()
                f = initFile(datestart,RPI,FOLDER,LOCATION,R)

            secondsToRun = (datetime.datetime.now()-starttime).total_seconds() % inter
            time.sleep(inter-secondsToRun)

        
        
        
