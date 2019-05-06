#! /usr/bin/python
# Daniel Jarvis
# Eddit of GPS code by Dan Mandle http://dan.mandle.me September 2012

import os
from gps import *
from time import *
import time
import threading
 
gpsd = None #seting the global variable
 
#os.system('clear') #clear the terminal (optional)
def main(gpsp):
 # gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
        lat=gpsd.fix.latitude
        lon=gpsd.fix.longitude
        alt=gpsd.fix.altitude
        utctime=gpsd.utc,' + ', gpsd.fix.time
      #  gpsd.next()
        
        #print (gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc)
        if gpsd.utc is not '' :
            return lat,lon,alt,utctime
        else:
           time.sleep(1)
        #time.sleep(1) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing

def Work():
  gpsp = GpsPoller() # create the thread
  global gpsp
  lat,lon,alt,utctime=main(gpsp)
  print("Time:" ,utctime,"Lat",lat,"Lon",lon,"Alt",alt)
  return lat, lon, alt



class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
     gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


#Work()