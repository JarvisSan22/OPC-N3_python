# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 09:52:20 2019

@author: Jarvis
GRIMM Data import 
"""

import glob
from datetime import datetime as dt
import pandas as pd
import matplotlib.pylab as plt
import math as mp
import numpy as np

def pandaGRIMM(Folder,yearmonth):
    '''
    GRIMM raw data converter. Takes raw GRIMM files and added them to a Panda array format
    Needs: GRIMM data file location 
    Code will add all the datafiles in that location into one new data file
    By:Daniel Jarvis
    Date:16/04/2019
    '''
    Gfiles = [] #set array to hold file names
    # folder=Folder
    for file in glob.glob(Folder+'***.GRIMM'):
        if yearmonth in file:
            Gfiles.append(file)
    print(Gfiles)
    Gfiles=sorted(Gfiles) #does them in a random order , so need to be sorted
    #Create and PD dataframe ready  
    GBin = ["0.3um","0.4um","0.5um","0.65um","0.8um","1um","1.6um","2um","3um","4um","5um","7.5um","10um","15um","20um"]
    
   # GBin = ["b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","b11","b12","b13","b14"]
    Gdata=pd.DataFrame(columns=["time"]+GBin)
    i=0 #set and DataFrame index 
    #cylce through all GRIMM files  
    #run time marker
    L=len(Gfiles)
    M=0
    print("-----"+str(L)+"------")
    for Gfile in Gfiles:
        M=M+1
        print(M)
        if M==L/2:
            print("半分")
        elif M==1/4*L:
            print("1/4分")
        elif M==3/4*L:
            print("3/4分")
        
        #print(Gfile)
        #OPen the GRIMM file
        dG=open(Gfile, 'r')
        #Loop through each line
        firstP = 0 #deal with no P in the first reading
        for line in dG:
            #print(firstP) #check
            #print(line) #check
            #Split up the line 
            GBits=line.split()
            id=GBits[6] #Is it data or not
            #print(GBits) #cjecl
            if id == "P": #Then its date and time data 
                # print(id) #Check
               #  print(GBits[0:6])
                 year,month,day,hour,m = GBits[0:5] #get the time data
                # year = "20" + year
                 firstP = 1
            elif  firstP == 1: #Now we are Past the time data, we can read the bin data
                c=GBits[6]  #Iver a big C (1st 8 bins) or a little c (rest of the bins)
                #print(id) #cjecl
               #This is done of the GRIMM takes 2 reading in 6 seconds, One for the smaller partiles i,e First 8 bins
               #and the next for the larger partiles (c)
                #bin_data=[]
                if "C" in c:
                    BD=GBits[7:]
                elif "c" in c:
                    #taking the min and seconds are the c reading time 
                    minsec=GBits[5] # min and seconds are attaced and need there own split
                    msSplit=minsec.split(".")
                    second=msSplit[0]
                    #second=msSplit[1]# its given as fraction of a miniute 
                    #second convertion
                    #second=int(60*(float(second)/1000))
                    #Add to last lines data from C
                    BD = BD + GBits[7:14]
                    #add all times into a datetime format 
                   # print(len(BD))
                    time = dt(int(year),int(month),int(day),int(hour),int(m),int(second))
                    Gdata.loc[i]=[time,int(BD[0]),int(BD[1]),int(BD[2]),int(BD[3]),int(BD[4]),int(BD[5]),int(BD[6]),int(BD[7]),int(BD[8]),int(BD[9]),int(BD[10]),int(BD[11]),int(BD[12]),int(BD[13]),int(BD[14])]
                    i=i+1
        #set time as index    
    #print(Gdata)         
    Gdata.set_index('time', inplace=True, drop=True)
    Gdata=Gdata.astype(int) #deal with string data
    return Gdata


def binmass(data,size):
    #print(data)
    for s in size:
        col=str(s)+"um"
        print(col,s)
        v=4/3*mp.pi*((s*10**(-6))/2)**3 
       # print(data[col])
        m=data[col]*1.65e+12 # volume * count * density   
        flowrate=1.149*1.6667e-5 #l/min to m^3/s
        period=6 #12 second sampe period
        M=(m*v) /(flowrate*period)
        data[str(s)+"M"]=M
        
    s = [str(i)+"M" for i in size]    #conver the size into string for the columns in the panda arrau
   # print(s[0:6],s[6:8],s[8:13])
    data["pm1"]=data[s[0:6]].sum(axis = 1, skipna = True)
    data["pm2"]=data[s[0:8]].sum(axis = 1, skipna = True)
    data["pm10"]=data[s[0:13]].sum(axis = 1, skipna = True)
    data["pm20"]=data[s].sum(axis = 1, skipna = True)
    print(data["pm10"])
    fig,ax = plt.subplots(1,1,figsize=(8,8))
    Data=data.resample("15T").mean()
  #  data["pm2","pm10"].plot()
    ax.set_ylim([0,100])
    ax.plot(Data["pm1"])
    ax.plot(Data["pm2"])
    ax.plot(Data["pm10"])
    return data
    
    
def voldist(data,size):
    a=0
    Sizedata=pd.DataFrame(columns=["Size","dN/dr","dA/dr","dV/dr"])
    Sizedata.set_index('Size', inplace=True, drop=True)
    for col,content in data.iteritems():
        try:
            S=size[a]
            u=content.mean()
            N=content.sum()
            SD=content.std()
            #print(S,N,SD,mp.log1p(S)-S)
            Nd1=(N/mp.sqrt(2*mp.pi))*(1/(SD)*1/S)
            Nd2=mp.exp(-((mp.log1p(S)-u)**2)/(2*SD**2))
            Ndis=Nd1*Nd2
            #print(N,Ndis)
            area=4*mp.pi*S**2*Ndis
            vol=4/2*mp.pi*S**3*Ndis
        
            Sizedata.loc[S]=[Ndis,area,vol]
        except:
            pass
        a=a+1
    col=Sizedata.columns
    axes=( locals()['ax%d'%i] for i in range( 1 , len(col)))
    fig,(axes) = plt.subplots(len(col),1,figsize=(5,8))
    for ax, var  in zip(axes,col):
        ax.scatter(Sizedata.index,Sizedata[var])
        ax.plot(Sizedata[var])
        ax.set_ylabel(var)
        ax.set_xlabel("size um")
        ax.grid()
        plt.subplots_adjust(hspace=.3)
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        # Sets the ticks to be on the left and bottom axes.
        
    Sizedata["dN/dr"] 
    return Sizedata

def sizedist(data,size):
    
    Sizedata=pd.DataFrame(columns=["Size","dN/dr"])
    Sizedata.set_index('Size', inplace=True, drop=True)
    i=0
    for S in size:
        try:
            col=str(S)+"um"
            content=data[col]  
        except:
            col="b"+str(i)
            content=data[col]  
            pass
        print(col)
          
        u=content.mean()
        N=content.sum()
        SD=content.std()
        #print(S,N,SD,mp.log1p(S)-S)
        Nd1=(N/mp.sqrt(2*mp.pi))*(1/(SD)*1/S)
        Nd2=mp.exp(-((mp.log1p(S)-u)**2)/(2*SD**2))
        Ndis=Nd1*Nd2
        #print(N,Ndis)
        Sizedata.loc[S]=[Ndis]   
    
    col=Sizedata.columns
    fig,ax= plt.subplots(1,1,figsize=(8,8))
    for var  in col:
        ax.scatter(Sizedata.index,Sizedata[var])
        ax.plot(Sizedata[var])
        ax.set_ylabel(var)
      #  ax.set_yscale('log')
        ax.set_xlabel("size um")
        ax.grid()
        plt.subplots_adjust(hspace=.3)
        ax.set_title(str(min(data.index))+" - "+ str(max(data.index)))
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        # Sets the ticks to be on the left and bottom axes.
        
    Sizedata["dN/dr"] 
    return Sizedata

Folder="Data-old//JimsOffice-Data//GRIMM//"
    #Folder for GRIMM data
#size = [0.3,0.4,0.5,0.65,0.8,1,1.6,2,3,4,5,7.5,10,15,20]
    
yearmonth="1905"
#GRIMMdf=pandaGRIMM(Folder,yearmonth)
#data=binmass(GRIMMdf,size,"15T")
#a=voldist(GRIMMdf,size)   
#GRIMMdf.to_csv("GRIMM_20"+yearmonth+".csv",encoding='utf-8')
    
#delta=dt.timedelta(month=1)

    
#