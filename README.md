



# OPC N3 Python repository 
Author: Daniel Jarvis 
Contacts: ee18dj@leeds.ac.uk


Python library for the [Aplhasense OPC-N3](http://www.alphasense.com/WEB1213/wp-content/uploads/2018/02/OPC-N3.pdf), and [OPC-N2](http://stg-uneplive.unep.org/media/aqm_document_v1/Blue%20Print/Components/Microcomputer%20and%20sensors/B.%20Dust%20Sensor%20Specifications/B.1%20Alphasense%20OPC%20N1/072-0300%20OPC-N2%20manual%20issue%203.pdf), connected through an SPI interface to a raspberry pi. 

- Additonal support for SDS011 added 28/05/2019
- Dashboard Added in AQ/AQplotter



![OPC-N3](https://github.com/JarvisSan22/OPC-N3_python/blob/master/OPCN3.jpg)


# Repository details 


Basic functions scripts **"OPCN3_test.py"**  for direct control of the OPCN3 functions.  Basics log scripts **"OPCN3_rec.py"** to log the data to a CSV and a more advanced functional library under **AQ** currently operation at the University of Leed and Summit site in Greenland.  The AQ library designed to work for multiple OPC attached to the same RPI3 logging all the data to one CSV file.  

Dashbord **"AQ/AQplotter"** ( see repository for further instructions). Dashboard shows diffrent varaibles, as well as options for GPS maps and static maps, what work for multiple sensors in diffrent location. (More updates coming soon)
![Dashboard](https://github.com/JarvisSan22/OPC-N3_python/blob/master/AQ/AQplotter/Dashbord.gif)

### OPCscripts details:
- **opcn3_rec.py** OPCN3 functions script
- **opcn2_rec.py** OPCN2 function script
- **variables.py** sensors operation varaibles, for attaced sensors names and ports, log interval time, opration type (log or GPS) and location name with latitude and longitude coardinets 
- **start.py** Start oprataion scripts. RUN all sensors attaced and specified in **variables.py**
- **status.py** Checks RPI3 status, logging data on time, IP address, and update RPI time if internet is corrected
- **/DHT** DHT  Sensors libary by Adafuit
- **DHT.py** DHT scripts to be called in **start.py** to log data to csv
- **GPS.py** edits of python GPS scripts by [Dan Mandle](https://github.com/ggtd/independend-python-gps-logger-for-airodump-ng/blob/master/log_position.py) to be called in **start.py** to log data to csv
- **AQ/MulOPCData.py** script to read the csv output, accounting for multiple OPC attaced to one RPI3


### Bascis Function list:
- **initOPC():** , initionate SPI connection with OPCN3
- **fanOn()** , turn on fan
- **fanOff():** , turns fan off
- **LazOn():** , turns lazer on
- **LazOff():**, turns lazer off
- **RHcon():** , converts RH bytes into RH by RH=100*(bytes/(2^16-1)) 
- **Tempcon():** , converts OPC Temperature bytes to Temprature (C) by Temp=-45+175*(bytes/(2^16+1))
- **combine_bytes(LSB,MSB):** combines upper and lower bytes for bin data 
- **getHist():** , gest hist data from OPC
- **getdata():** , gets just PM data from OPC
- **Hisdtdata():** , get outbut from gethist and convert it into the varaible information



### AQ repositroy structure:
- **/AQ**
- **/AQ/OPCData** Directory for log data to be stored
- **/AQ/OPCscripts** Scripts to run OPCN3, OPCN2 with options for DHT11 or DHT22 Temprature and RH sensors and GPS attachment. 
- **/AQ/teamviewer-host_14.1.18533_armhf.deb** RPI3 installer package for [teamviewer](https://www.teamviewer.com/en/buy-now/?pid=google.tv_ex_repeat.s.gb&gclid=Cj0KCQjwn8_mBRCLARIsAKxi0GJuys2-XjuxDuTIxFylKvXF4VzWCYLQhYoHMkoMawyTfyEpjDdK40YaAuQ9EALw_wcB) allowing romote over a WIFI connection. 
 


# AQ set up
Once RPI3 is set up and connected to wifi
</br>
default set up packages

'sudo apt-get update'   

'sudo pip install psutil'   used to check wifi in **status.py**

'sudo pip install ntplib'   used to check time RPI3 and update it in **status.py**



**Optional Installs** 

**DHT install**
'sudo python3 AQ/OPCscripts/DHT/setup.py install'

**GPS install**
GPS used is [G-mouse USB Gps Dongle](https://www.amazon.co.uk/Diymall-G-mouse-Glonass-Raspberry-Aviation/dp/B015E2XSSO/ref=sr_1_3_sspa?crid=K5C3JJ0ZYQHH&keywords=gps+dongle+usb&qid=1557393883&s=gateway&sprefix=GPS+dongle%2Caps%2C131&sr=8-3-spons&psc=1), GPS set up on RPI3 follows those found on this youtube vid by [KM4ACK](https://www.youtube.com/watch?v=Oag9qYuhMGg), setting the GPS up as the RPI3 clock as well. 

Plotter scipts in **"AQ/AQplotter"**
![GPSWALK](https://github.com/JarvisSan22/OPC-N3_python/blob/master/AQ/AQplotter/STATICMAP.gif)

**RPI3 external clock**
if the GPS is not attached to the [Adafruit PiRTC](https://www.amazon.co.uk/Adafruit-PiRTC-PCF8523-Raspberry-ADA3386/dp/B072DWKDW9/ref=sr_1_2?keywords=adafruit+real+time+clock&qid=1557395250&s=gateway&sr=8-2) is recommended to be attached to the RPI3 to stop the RPI3 time drifting when the internet is lost. [Setup instructions](https://www.amazon.co.uk/Adafruit-PiRTC-PCF8523-Raspberry-ADA3386/dp/B072DWKDW9/ref=sr_1_2?keywords=adafruit+real+time+clock&qid=1557395250&s=gateway&sr=8-2)

# Getting the kit running 
in OPCscripts
'cd/OPCscripts'


**update *varaibles.py***
'nano variables.py'

Update the RPI3 name (RPINAME)

operation location (LOC), desired MODE: "LOG" or "GPS". "LOG" is for static site recording to csv, "GPS" added the lat, lon and altitude to csv allowing for mobile usage. 

RUNNING sensors (RUNSEN) (Note: multiple OPC sensors can be added)
The connection ports (RUNPORTS), if your not sure what port it is 'cd /dev/' then unplug and replug the OPC cable
DHT setting, if DHT is connected set "DHTON" to "ON", and insert the DHT name in (DHTNAMES) and connected RPI pin in (DHTPINS)

![variables](https://github.com/JarvisSan22/OPC-N3_python/blob/master/variables.png)

With all variables now set up hopefully correctly by just running start.py the attached OPC sensors will start logging

'python3 start.py'

This command can be added to crontab to get the sensors running on startup.
'sudo nano crontab -e'
 
'@reboot python3 AQ/OPCscripts/start.py'

![Runtest](https://github.com/JarvisSan22/OPC-N3_python/blob/master/Runexample.gif)

### SDS011 support

With an plugged in SDS011, in 'variables.py' add "/dev/ttyUSB0" as the first variable in RUNPORTS and do the same for the name (i.e DSO11_1) in RUNSEN. Instead of running start.py, run 'python start-SDS.py' (for some currently unknown reason python3 does not work with the SDS, will fix soon). This will add a columns for the SDSO11s; pm2.5, pm10 and the other unkownvalue (assumed to be TSP) reading. 



# Error log:
- 30/05/2019 Added failed attemt varaible for OPCN3 scripts. Found on Summit by Heather Guy, OPN3 was sending enoguh data using a 5m wire, by increasing the failed attemts in OPCN3_rec.py from 20 to 40 the OPC send the data. 

# To do:
- add OPCN3 live data viewer
- add functions to change default bin weighting
- Implement new PM10, PM2.5 and PM1 calculation

