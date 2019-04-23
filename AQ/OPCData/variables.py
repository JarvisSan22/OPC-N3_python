# -*- coding: utf-8 -*-
"""
Created on Tsu Mar 26 16:18:15 2019
@author: Daniel Jarvis
Variables for the sensors operation
"""
#All the needed varaibles
#RPI3 Name
RPINAME="AQRPI8"
#Desired operation mode
#MODE="FULL" #Options: "FULL" "POWERSAVE"  "INTERVALS"

#folder locations 
FOLDER = '/home/pi/AQ/OPCData/' #for raw data
FOLDERCODE='/home/pi/AQ/OPCscripts/' #For the scpirs locaton 
#Operation location, if using with GPS use area name
LOCATION = 'JimsOffice' #Add test name into this too, say aersol and calbration ...
#Intergration names
integration=10
#UPloade data location

URL = ''

MODE="Normal"
#MODE= "GPS"  #"N" #"GPS"   #Powersave
#Note if GPS is on it takes up "/dev/ttyACM0" port, so for OPNC2 and N3 use be carfull and check /dev/

##Desired sensors to run on RPI3
OPCON="ON"
RUNSEN=["OPCN3_8"]
#RUNSEN=["OPCN3_7","OPCN3_N2"]
#Sensor ports for deried sensors, if you dont know checl the /dev folder
#RUNPORT=["/dev/ttyACM0","/dev/ttyUSB0"]
RUNPORT=["/dev/ttyACM0"]
#Temp sensors port number, if a DHT11 or 22 is running get the por
DHTON="OFF"  
#DHTON="ON"
DHTNAMES=["DHT22_1"]
DHTPINS=[14]
