#!/usr/bin/env python

#9600, 8, none, stop1, noflow

from __future__ import print_function
import serial
import time
import struct
import datetime
import sys
import os.path
#import panda as pd


# Init
class Opcn2:
        def initOPC(self,ser):
                #print("Init:")
                time.sleep(1)
                ser.write(bytearray([0x5A,0x01]))
                nl = ser.read(3)
                #print(nl)
                time.sleep(.1)
                ser.write(bytearray([0x5A,0x03]))
                nl=ser.read(9)
                #print(nl)
                time.sleep(.1)
                        
                        #The usb SPI conncetion  code 
                ser.write(bytearray([0x5A,0x02,0x92,0x07]))
                nl=ser.read(2)
                #print(nl)
                time.sleep(.1)

        # Turn fan and laser off
        def fanOff(self,ser):
                ser.write(bytearray([0x61,0x03]))
                nl = ser.read(2) #Fan and lazer off
#                print(nl)
                time.sleep(.1) 
                ser.write(bytearray([0x61,0x01]))
                nl = ser.read(2)
 #               print(nl)
                time.sleep(.1)

        # Turn fan and laser on
        def fanOn(self,ser):
                ser.write(bytearray([0x61,0x03]))
                nl = ser.read(2)
                #print(nl)
                time.sleep(.1)
                ser.write(bytearray([0x61,0x00]))
                nl = ser.read(2)
                #print(nl)
                time.sleep(.1)

        def combine_bytes(self,LSB, MSB):
                return (MSB << 8) | LSB

        def getHist(self,ser):
                ser.write(bytearray([0x61,0x30]))
                nl=ser.read(2)
                #print(nl)
                time.sleep(.1)
                br = bytearray([0x61])
     #           print("br",br)
                for i in range(0,62):
                        br.append(0x30)
    #            print("br",br)
                ser.write(br)
                ans=bytearray(ser.read(1))
   #             print("ans=",ans,"len",len(ans))
                ans=bytearray(ser.read(62))
  #              print("ans=",ans,"len",len(ans))
                data={}
                data['Bin 0'] =self.combine_bytes(ans[0],ans[1])
                data['Bin 1'] = self.combine_bytes(ans[2],ans[3])
                data['Bin 2'] = self.combine_bytes(ans[4],ans[5])
                data['Bin 3'] = self.combine_bytes(ans[6],ans[7])
                data['Bin 4'] = self.combine_bytes(ans[8],ans[9])
                data['Bin 5'] = self.combine_bytes(ans[10],ans[11])
                data['Bin 6'] = self.combine_bytes(ans[12],ans[13])
                data['Bin 7'] = self.combine_bytes(ans[14],ans[15])
                data['Bin 8'] = self.combine_bytes(ans[16],ans[17])
                data['Bin 9'] = self.combine_bytes(ans[18],ans[19])
                data['Bin 10'] = self.combine_bytes(ans[20],ans[21])
                data['Bin 11'] = self.combine_bytes(ans[22],ans[23])
                data['Bin 12'] = self.combine_bytes(ans[24],ans[25])
                data['Bin 13'] = self.combine_bytes(ans[26],ans[27])
                data['Bin 14'] = self.combine_bytes(ans[28],ans[29])
                data['Bin 15'] = self.combine_bytes(ans[30],ans[31])
                data['cross time']=struct.unpack('f',bytes(ans[32:36]))[0]
                data['flow_rate']=struct.unpack('f',bytes(ans[36:40]))[0]
                data['temp_pressure']=struct.unpack('f',bytes(ans[40:44]))[0]  #W temp and pressure are on the same bytes, and no controls to slect one or the other 
                data['period'] = struct.unpack('f',bytes(ans[44:48]))[0]
                data['checksum']=self.combine_bytes(ans[49],ans[50])
                data['pm1'] = struct.unpack('f',bytes(ans[50:54]))[0]
                data['pm2.5'] = struct.unpack('f',bytes(ans[54:58]))[0]
                data['pm10'] = struct.unpack('f',bytes(ans[58:62]))[0]
                return(data)
                
        # Retrieve data
        def getData(self,ser):
                ser.write(bytearray([0x61,0x32]))
                nl=ser.read(2)
                time.sleep(.1)
                ser.write(bytearray([0x61,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32]))
                ans=bytearray(ser.read(13))
                b1 = ans[1:5]
                b2 = ans[5:9]
                b3 = ans[9:13]
                c1=struct.unpack('f',bytes(b1))[0]
                c2=struct.unpack('f',bytes(b2))[0]
                c3=struct.unpack('f',bytes(b3))[0]
                return([c1,c2,c3])

        def initFile(self,date,FOLDER,LOCATION,OPCNAME):
                ofile= FOLDER + LOCATION + '_' + OPCNAME + '_' + str(date).replace('-','') + ".csv"
                print("Opening Output File:")
                if(not os.path.isfile(ofile)):
                        f=open(ofile,'w+')
                        print("time,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,ct,flowrate,temp_pressure,period,checksum,pm1,pm2,pm10",file=f)
                else:
                        f=open(ofile,'a')
                return f
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
                     
                t=self.getHist(ser)
                ts = time.time()
                tnow = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                data=t
                print(OPCNAME," Time",tnow , " PM1:", str(round(data['pm1'],2)) ,"PM2:", str(round(data['pm2.5'],2)) ,"PM10:", str(round(data['pm10'],2)))
                data= str(data['Bin 0']) + ","  + str(data['Bin 1']) + ","  + str(data['Bin 2']) + ","  + str(data['Bin 3']) + ","  + str(data['Bin 4']) + ","  + str(data['Bin 5']) + ","  + str(data['Bin 6']) + ","  + str(data['Bin 7']) + ","  + str(data['Bin 8']) + ","  + str(data['Bin 9']) + ","  + str(data['Bin 10']) + ","  + str(data['Bin 11']) + ","  + str(data['Bin 12']) + ","  + str(data['Bin 13']) + ","  + str(data['Bin 14']) + ","  + str(data['Bin 15']) + ","+str(data['cross time'])+","+str(data['flow_rate'])+","+str(data['temp_pressure'])+","+ str(data['period']) + ","+str(data['checksum'])+","  + str(data['pm1']) + ","  + str(data['pm2.5']) + ","  + str(data['pm10'])
               # data=[data['Bin 0'],data['Bin 1'],data['Bin 2'],data['Bin 3'],data['Bin 4'],data['Bin 5'],data['Bin 6'],data['Bin 7'],data['Bin 8'],data['Bin 9'],data['Bin 10'],data['Bin 11'],data['Bin 12'],data['Bin 13'],data['Bin 14'],data['Bin 15'],data['period'],data['pm1'],data['pm2.5'],data['pm10']]
                return data                      

                print("Closing:")

        def TurnOff(self,ser):
                f.close()
                self.fanOff(ser)
                ser.close()


                
        def __init__(self,OPCPORT,OPCNAME):
                serial_opts = {
                "port": OPCPORT,
                "baudrate": 9600,
                "parity": serial.PARITY_NONE,
                "bytesize": serial.EIGHTBITS,
                "stopbits": serial.STOPBITS_ONE,
                 "xonxoff": False,
                "timeout": 1
                }
                # wait for opc to boot
                time.sleep(10)
                ser = serial.Serial(**serial_opts)
                #ser.open()
                print("**************************************************")
                print("DID YOU CHECK THE DATE/TIME ????????")
                print("**************************************************")
                
                print("Init:",OPCNAME)
                self.initOPC(ser)
                time.sleep(1)

                print("Fan Off:")
                self.fanOff(ser)
                time.sleep(5)

                print("Fan on:")
                self.fanOn(ser)
                time.sleep(5)	
                print(OPCNAME,"Ready")
                #return serial_opts
                
               


