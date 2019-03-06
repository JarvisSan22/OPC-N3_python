# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:41:45 2019

@author: Jarvi
OPCN3 test code 
"""


from __future__ import print_function
import serial
import time
import struct
import datetime
import sys
import os.path
#IMport the file names, you dont want to type them out in all the code 

import variables as V
# SAMPLING VARIABLES
#integration time (seconds)
integration=10

# NAMING VARIABLES
OPCNAME = "TestOPC"
OPCPORT= "COM8"
LOCATION = "Lab2"
#FOLDER = "C:\Users\Jarvi\Documents\MRES!!!!!!! 勝とう\Project\Pi\26-2-2019 pi code\AQ\OPCData"

# Init

def initOPC(ser):
        #print("Init:")
        time.sleep(1)
        ser.write(bytearray([0x5A,0x01]))
        nl = ser.read(3)
        print(nl)
        time.sleep(.1)
        ser.write(bytearray([0x5A,0x03]))
        nl=ser.read(9)
        print(nl)
        time.sleep(.1)
		
		 #SPI conncetion
        ser.write(bytearray([0x5A,0x02,0x92,0x07]))
        nl=ser.read(2)
        print(nl)
        time.sleep(.1)
        
       
# Turn fan 
        
def fanOff(ser):
         #start the flow chart the flow chart
        ser.write(bytearray([0x61,0x03]))
        time.sleep(.1)
        ser.write(bytearray([0x61,0x03]))
        time.sleep(.1)
        #fan off
        ser.write(bytearray([0x61,0x02]))
        #nl = ser.read(2)
        #print(nl)
        time.sleep(0.1)
        #lazer off
       # ser.write(bytearray([0x61,0x62]))
       # time.sleep(20)
# Turn fan and laser on
def fanOn(ser):
    
        ser.write(bytearray([0x61,0x03]))
        nl = ser.read(2)
        print(nl)
        time.sleep(.1)
        ser.write(bytearray([0x61,0x03]))
        nl = ser.read(2)
        print(nl)
        time.sleep(.1)

#Lazer on   0x07 is SPI byte following 0x03 to turn laser ON.
def LazOn(ser):
        ser.write(bytearray([0x61,0x03]))
        nl = ser.read(2)
        print(nl)
        time.sleep(.1)
        ser.write(bytearray([0x61,0x07])) #ON
        nl = ser.read(2)
        print(nl)
        time.sleep(.1)
#Lazer off 0x06 is SPI byte following 0x03 to turn laser off.
def LazOff(ser):
        ser.write(bytearray([0x61,0x03]))
        nl = ser.read(2)
        print(nl)
        time.sleep(.1)
        ser.write(bytearray([0x61,0x06])) #ON
        nl = ser.read(2)
        print(nl)
        time.sleep(.1)
        
        
def combine_bytes(LSB, MSB):
        return (MSB << 8) | LSB       
 

def getHist(ser):
        ser.write(bytearray([0x61,0x30]))
        nl=ser.read(2)
        #print(nl)
        time.sleep(.1)
        br = bytearray([0x61])
        for i in range(0,86):
                br.append(0x30)
        print(br)
        ser.write(br)
        ans=bytearray(ser.read(1))
        ans=bytearray(ser.read(86))
        print(ans)
        data={}
        data['Bin 0'] = combine_bytes(ans[0],ans[1])
        data['Bin 1'] = combine_bytes(ans[2],ans[3])
        data['Bin 2'] = combine_bytes(ans[4],ans[5])
        data['Bin 3'] = combine_bytes(ans[6],ans[7])
        data['Bin 4'] = combine_bytes(ans[8],ans[9])
        data['Bin 5'] = combine_bytes(ans[10],ans[11])
        data['Bin 6'] = combine_bytes(ans[12],ans[13])
        data['Bin 7'] = combine_bytes(ans[14],ans[15])
        data['Bin 8'] = combine_bytes(ans[16],ans[17])
        data['Bin 9'] = combine_bytes(ans[18],ans[19])
        data['Bin 10'] = combine_bytes(ans[20],ans[21])
        data['Bin 11'] = combine_bytes(ans[22],ans[23])
        data['Bin 12'] = combine_bytes(ans[24],ans[25])
        data['Bin 13'] = combine_bytes(ans[26],ans[27])
        data['Bin 14'] = combine_bytes(ans[28],ans[29])
        data['Bin 15'] = combine_bytes(ans[30],ans[31])
        data['Bin 16'] = combine_bytes(ans[32],ans[33])
        data['Bin 17'] = combine_bytes(ans[34],ans[35])
        data['Bin 18'] = combine_bytes(ans[36],ans[37])
        data['Bin 19'] = combine_bytes(ans[38],ans[39])
        data['Bin 20'] = combine_bytes(ans[40],ans[41])
        data['Bin 21'] = combine_bytes(ans[42],ans[43])
        data['Bin 22'] = combine_bytes(ans[44],ans[45])
        data['Bin 23'] = combine_bytes(ans[46],ans[47])
        data['Bin 24'] = combine_bytes(ans[48],ans[49])
        data['period'] = combine_bytes(ans[52],ans[53])
        data['FlowRate'] = combine_bytes(ans[54],ans[55])
        data['Temp']=combine_bytes(ans[56],ans[57])
        data['RH'] = combine_bytes(ans[52],ans[53])
        print(data)
        data['pm1'] = struct.unpack('f',bytes(ans[60:64]))[0]
        data['pm2.5'] = struct.unpack('f',bytes(ans[64:68]))[0]
        data['pm10'] = struct.unpack('f',bytes(ans[68:73]))[0]
       # data['Check']= combine_bytes(ans[84],ans[85])
        return(data)
	
# Retrieve data
def getData(ser):
        ser.write(bytearray([0x61,0x32]))
        nl=ser.read(2)
        time.sleep(.1)
        ser.write(bytearray([0x61,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32]))
        ans=bytearray(ser.read(14))
        b1 = ans[0:4]
        b2 = ans[4:8]
        b3 = ans[8:12]
        print(b1,b2,b3)
        #get vales in micro grams per cubic meter 
        c1=struct.unpack('f',bytes(b1))[0]
        c2=struct.unpack('f',bytes(b2))[0]
        c3=struct.unpack('f',bytes(b3))[0]
        return([c1,c2,c3])
        
def initFile(date):
        ofile= FOLDER + LOCATION + '_' + OPCNAME + '_' + str(date).replace('-','') + ".csv"
        print("Opening Output File:")
        if(not os.path.isfile(ofile)):
                f=open(ofile,'w+')
                print("time,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,period,pm1,pm2,pm10",file=f)
        else:
                f=open(ofile,'a')
        return f





       
if __name__ == "__main__":
    
     
        serial_opts = {
        # built-in serial port is "COM1"
        # USB serial port is "COM4"
        "port": OPCPORT,
        "baudrate": 9600,
        "parity": serial.PARITY_NONE,
        "bytesize": serial.EIGHTBITS,
        "stopbits": serial.STOPBITS_ONE,
         "xonxoff": False,
        "timeout": 1
        }
	
	# wait for opc to boot
#time.sleep(10)
        
        ser = serial.Serial(**serial_opts)
        #ser.open()
	
        print("**************************************************")
        print("DID YOU CHECK THE DATE/TIME ????????")
        print("**************************************************")
        print("integration time (seconds)",integration)
        print("**************************************************")
        print("Init:")
        initOPC(ser)
        time.sleep(1)

        print("Fan & Lazer Off:")
        fanOff(ser)
        LazOff(ser)
        time.sleep(1)
        print("Fan & Lazer on:")
        fanOn(ser)
        LazOn(ser)
        time.sleep(2)
       # PM data
        print(getData(ser))
        #get Hist
        print(getHist(ser))
        ser.close()
print(OPCNAME,"Ready")