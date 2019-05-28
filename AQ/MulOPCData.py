# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:17:45 2019

@author: Jarvis
"""

import pandas as pd
import glob

folder="Dataset//Summit//"


def ExtractOPCdata(folder,sens):
    """
    Functions to extract multiple OPC data from same CSV file, put them into seperate DataFrame all in one dic.
    Works for up to 4 sensors , and DHT. IF more are attaced at another elif to the 2nd loop
    
    28/05/2019
    """
    
    OPCdata={} #Data dictionary
    OPCcols={} #columns dictionary to get the right data from each sensors
    
    
    #for loop for the amount sensors running
    for sen in sens:
        OPCdata[sen]=pd.DataFrame()
        OPCcols[sen]=[]
    
    #Read file for loop
    for file in glob.glob(folder+"***.csv"):
        dataloop=pd.read_csv(file,header=4,error_bad_lines=False,engine='python')
        dataloop.set_index('time', inplace=True, drop=True)
        # print(dataloop.head(4))
        #seprate columns 
        
        
        #first check if DHT is attached
        if "DHT-T" in dataloop.columns:
            #if DHT temp and RH sensors attaced add to columns 
            for sen in sens:
                OPCcols[sen].append("DHT-T")
                OPCcols[sen].append("DHT-RH")
        
        #2nd loop though columns, seprationg them for diffrent sensors
        for col in dataloop.columns:
         #can account for 4 OPCN3   
            if ".1" in col:
                OPCcols[sens[1]].append(col)
            elif ".2" in col:
                OPCcols[sens[2]].append(col)
            elif ".3" in col:
                OPCcols[sens[3]].append(col)
            else:
                OPCcols[sens[0]].append(col)
        #2 print(OPCcols)
        #3rd Concat to the OPCdata data frames
        for sen in sens:
            #concat for the data dictionary 
            #3 print(sen,OPCcols[sen],OPCdata[sen])
            
            data=pd.concat([OPCdata[sen],dataloop[OPCcols[sen]]], ignore_index=False, axis=0,sort=True)  
            #3 print(data.head(4))
            for col in data.columns:
                #loop though colums getting rid of the .1 or .2 for multiple sensors 
                if "." in col:
                    a=col.find(".")
                    data.rename(columns={col:col[0:a]},inplace=True)
            data.rename(columns={"pm2":"pm2.5"},inplace=True)
            
            OPCdata[sen]=data
            
    return OPCdata

sens=["OPCN3_1","OPCN3_2","OPCN3_3"]    
OPCdata=ExtractOPCdata(folder,sens)

            
    
    
             