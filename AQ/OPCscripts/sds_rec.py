
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#Code just logs the data from the sds11, it does not print. As it aim is 
#to be a back grond code, allow the pi to do other thing and be accesed 
#with out damaged the data recording
from __future__ import print_function
import serial, struct, time, csv, datetime 
import sys 
import os

class SDS011:           
    # 0xAA, 0xB4, 0x06, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    # 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x06, 0xAB
    def sensor_wake(self,ser):
        bytes = ['\xaa', #head
        '\xb4', #command 1
        '\x06', #data byte 1
        '\x01', #data byte 2 (set mode)
        '\x01', #data byte 3 (sleep)
        '\x00', #data byte 4
        '\x00', #data byte 5
        '\x00', #data byte 6
        '\x00', #data byte 7
        '\x00', #data byte 8
        '\x00', #data byte 9
        '\x00', #data byte 10
        '\x00', #data byte 11
        '\x00', #data byte 12
        '\x00', #data byte 13
        '\xff', #data byte 14 (device id byte 1)
        '\xff', #data byte 15 (device id byte 2)
        '\x05', #checksum
        '\xab'] #tail
        for b in bytes:
            ser.write(b)
    # xAA, 0xB4, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    # 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x05, 0xAB
    def sensor_sleep(self,ser):
        bytes = ['\xaa', #head
        '\xb4', #command 1
        '\x06', #data byte 1
        '\x01', #data byte 2 (set mode)
        '\x00', #data byte 3 (sleep)
        '\x00', #data byte 4
        '\x00', #data byte 5
        '\x00', #data byte 6
        '\x00', #data byte 7
        '\x00', #data byte 8
        '\x00', #data byte 9
        '\x00', #data byte 10
        '\x00', #data byte 11
        '\x00', #data byte 12
        '\x00', #data byte 13
        '\xff', #data byte 14 (device id byte 1)
        '\xff', #data byte 15 (device id byte 2)
        '\x05', #checksum+","+
        '\xab'] #tail
        for b in bytes:
            ser.write(b)
            
    def process_frame (self,d):
    #Get and Print the wanted data, and put in into a usable data fromet
        
        r = struct.unpack('<HHxxBBB', d[2:])
        pm25 = r[0]/10.0
        pm10 = r[1]/10.0
        TSP= r[2]/10.0
       # print(r)
        #print(d)
        checksum = sum(ord(v) for v in d[2:8])%256
       # print(datetime.datetime.now())
        #add a varable for if the data is good or bad
        if (checksum==r[2] and r[3]==0xab):
          com=0 #good data
          data = {"pm2":pm25,"pm10":pm10,"TSP?":TSP,"Check":com}
        else:
          com=999 #bad data
          data ={"pm2":"nan","pm10":"nan" ,"TSP?":"nan","Check":com}
        return data
        
    def sensor_read(self,ser):
    # Read the data, by getting the the bytes and puttem them into the 
    # process frame to get the data
        byte = 0
        while byte != "\xaa":
            #try:
                byte = ser.read(size=1)
                d = ser.read(size=10)
           #     print(d,len(d))
                if d[0] == "\xc0":
                    data = self.process_frame(byte + d)
            #        print("Data reciveds")
                    return data
        #    except:
             #   print("Error")
            #    data ={"pm2":"nan","pm10":"nan" 
            #    ,"TSP?":"nan","Check":"nan"}
               # return data
                
            
    def getData(self,OPCPORT,OPCNAME):
        
          serial_opts = {
                "port": OPCPORT,
                "baudrate": 9600,
                "parity": serial.PARITY_NONE,
                "bytesize": serial.EIGHTBITS,
                "stopbits": serial.STOPBITS_ONE,
                 "xonxoff": False,
                "timeout": 1
                }
          ser = serial.Serial(**serial_opts)
           # now is in form YYYYMMDD print("Sensor OFF")
          try:
              ser.open()
          except:
              pass
            
         # ser.flushInput()
         # self.sensor_sleep(ser)
         # time.sleep(2)
          #print("Sensor ON")
         # self.sensor_wake(ser)
#          print(OPCNAME,"Ready")
          #ser.close()
          data=self.sensor_read(ser)
          ser.flushInput()
 #         print("Got data")
          #get time
          ts=time.time()
          tnow = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
          if data is not None:
              print(OPCNAME,"Time:",tnow,"PM2.5:",str(data['pm2']),"PM10:",str(data['pm10']),"TSP:",str(data['TSP?']))
              data=str(data['pm2'])+","+str(data['pm10'])+","+str(data['TSP?'])+","+str(data['Check'])
          
          else:
              print(OPCNAME," Data error")
              #return nan for errors so the code does not get stuck
              data="nan,nan,nana,nana" 
          return data
    def __init__(self,OPCPORT,OPCNAME):
          print(OPCNAME)
