# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:52:30 2019

@author: Daniel Jarvis
OPC N3 record data to a CSV. 
"""
from __future__ import print_function
import serial
import time
import struct
import datetime
import sys
import os.path
import varaibles as V
AT=V.AT

wait=1e-06


class Opcn3:
        def initOPC(self,ser):
                #print("Init:")
                time.sleep(1)
                ser.write(bytearray([0x5A,0x01]))
                nl = ser.read(3)
                print(nl)
                time.sleep(wait)
                ser.write(bytearray([0x5A,0x03]))
                nl=ser.read(9)
                print(nl)
                time.sleep(wait)
                
                 #SPI conncetion
                ser.write(bytearray([0x5A,0x02,0x92,0x07]))
                nl=ser.read(2)
                print(nl)
                time.sleep(wait)
                
               
        # Turn fan 
                
        def fanOff(self,ser):
                print("Fan turn off")
                
                 #start the flow chart the flow chart
                T=0 #Triese counter
                while True:
                    
                    ser.write(bytearray([0x61,0x03]))
                    nl = ser.read(2)
                   # print(nl)
                    T=T+1 
                    if nl== (b"\xff\xf3" or b"xf3\xff"):
                        time.sleep(wait)
                        #fan off
                        ser.write(bytearray([0x61,0x02]))
                        nl = ser.read(2)
                  #      print(nl)
                        time.sleep(2)
                        fan="OFF"
                        print("Fan off")
                        return fan
                    elif T > AT:
                        
                        print("Reset SPI")
                        time.sleep(3) #time for spi buffer to reset
                        #reset SPI  conncetion 
                        self.initOPC(ser)
                        T=0
                    else:
                        time.sleep(wait*10) #wait 1e-05 before next commnad 
                                    
                     
        # Turn fan and laser on
        def fanOn(self,ser):
                print("Fan turn on")
                #start the flow chart the flow chart
                T=0 #Triese counter
                while True:   
                    ser.write(bytearray([0x61,0x03]))
                    nl = ser.read(2)
                 #   print(nl)
                    T=T+1 
                    if nl== (b"\xff\xf3" or b"xf3\xff"):
                        time.sleep(wait)
                        #fan on
                        ser.write(bytearray([0x61,0x03]))
                        nl = ser.read(2)
                #        print(nl)
                        time.sleep(2)
                        fan="ON"
                        print("Fan On")
                        return fan
                    elif T > AT:
                        print("Reset SPI")
                        time.sleep(3) #time for spi buffer to reset
                        #reset SPI  conncetion 
                        self.initOPC(ser)
                        T=0
                    else:
                        time.sleep(wait*10) #wait 1e-05 before next commnad 
                                
        #Lazer on   0x07 is SPI byte following 0x03 to turn laser ON.
        def LazOn(self,ser):
                print("Lazer turn On")
                T=0 #Triese counter
                while True:   
                    ser.write(bytearray([0x61,0x03]))
                    nl = ser.read(2)
               #     print(nl)
                   
                    T=T+1 
                    if nl== (b"\xff\xf3" or b"xf3\xff"):
                        time.sleep(wait)
                        #Lazer on
                        ser.write(bytearray([0x61,0x07]))
                        nl = ser.read(2)
              #          print(nl)
                        time.sleep(wait)
                        Laz="ON"
                        print("Fan On")
                        return Laz
                    elif T > AT:
                        print("Reset SPI")
                        time.sleep(3) #time for spi buffer to reset
                        #reset SPI  conncetion 
                        self.initOPC(ser)
                        T=0
                    else:
                        time.sleep(wait*10) #wait 1e-05 before next commnad 
                                    

                        
        #Lazer off 0x06 is SPI byte following 0x03 to turn laser off.
        def LazOff(self,ser):
                print("Lazer Off")
                
                T=0 #Triese counter
                while True:   
                    ser.write(bytearray([0x61,0x03]))
                    nl = ser.read(2)
             #       print(nl)
                    T=T+1 
                    if nl== (b"\xff\xf3" or b"xf3\xff"):
                        time.sleep(wait)
                        #Lazer off
                        ser.write(bytearray([0x61,0x06]))
                        nl = ser.read(2)
            #            print(nl)
                        time.sleep(wait)
                        Laz="Off"
                        print("Lazer Off")
                        return Laz
                    elif T > AT:
                        print("Reset SPI")
                        time.sleep(3) #time for spi buffer to reset
                        #reset SPI  conncetion 
                        self.initOPC(ser)
                        T=0
                    else:
                        time.sleep(wait*10) #wait 1e-05 before next commnad 
              

        #add the singal to temp and RH value convertion   from the SPI data sheet
                        
        def RHcon(self,ans):
            #ans is  combine_bytes(ans[52],ans[53])
            RH=100*(ans/(2**16-1))
            return RH
        def Tempcon(self,ans):
              #ans is  combine_bytes(ans[52],ans[53])
            Temp=-45+175*(ans/(2**16-1))
            return Temp
        def combine_bytes(self,LSB, MSB):
                return (MSB << 8) | LSB       
        def Histdata(self,ans):
        #function for all the hist data, to break up the getHist
             #time.sleep(wait)  
           
            data={}
            data['Bin 0'] = self.combine_bytes(ans[0],ans[1])
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
            data['Bin 16'] = self.combine_bytes(ans[32],ans[33])
            data['Bin 17'] = self.combine_bytes(ans[34],ans[35])
            data['Bin 18'] = self.combine_bytes(ans[36],ans[37])
            data['Bin 19'] = self.combine_bytes(ans[38],ans[39])
            data['Bin 20'] = self.combine_bytes(ans[40],ans[41])
            data['Bin 21'] = self.combine_bytes(ans[42],ans[43])
            data['Bin 22'] = self.combine_bytes(ans[44],ans[45])
            data['Bin 23'] = self.combine_bytes(ans[46],ans[47])
            data['MToF'] = struct.unpack('f',bytes(ans[48:52]))[0] #MTof is in 1/3 us, value of 10=3.33us
            data['period'] = self.combine_bytes(ans[52],ans[53]) 
            data['FlowRate'] = self.combine_bytes(ans[54],ans[55])
            data['OPC-T']=self.Tempcon(self.combine_bytes(ans[56],ans[57]))
            data['OPC-RH'] = self.RHcon(self.combine_bytes(ans[58],ans[59]))
            data['pm1'] = struct.unpack('f',bytes(ans[60:64]))[0]
            data['pm2.5'] = struct.unpack('f',bytes(ans[64:68]))[0]
            data['pm10'] = struct.unpack('f',bytes(ans[68:72]))[0]
            data['Check']= self.combine_bytes(ans[84],ans[85])
            
              #  print(data)
            return(data)

        def read_all(self,port, chunk_size=86):
            """Read all characters on the serial port and return them."""
            if not port.timeout:
                raise TypeError('Port needs to have a timeout set!')

            read_buffer = b''

            while True:
                # Read in chunks. Each chunk will wait as long as specified by
                # timeout. Increase chunk_size to fail quicker
                byte_chunk = port.read(size=chunk_size)
                read_buffer += byte_chunk
                if not len(byte_chunk) == chunk_size:
                    break

            return read_buffer

        def initFile(self,date):
                ofile=   FOLDER + LOCATION + '_' + OPCNAME + '_' + str(date).replace('-','') + ".csv"
                print("Opening Output File:")
                if(not os.path.isfile(ofile)):
                        f=open(ofile,'w+')
                        print("time,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,MToF,period,FlowRate,OPC-T,OPC-RH,pm1,pm2.5,pm10","Check",file=f)
                else:
                        f=open(ofile,'a')
                return f


        def rightbytes(self,response):
            '''
            Get ride of the 0x61 byeste responce from the hist data, returning just the wanted data
            '''
            hist_response=[]
            for j, k in enumerate(response):            # Each of the 86 bytes we expect to be returned is prefixed by 0xFF.
                if ((j + 1) % 2) == 0:                  # Throw away 0th, 2nd, 4th, 6th bytes, etc.
                    hist_response.append(k)     
            return hist_response
        def getData(self,ser):
                print("Get PM data")
                T=0
                
                while True:
                    #initsiate getData commnad
                    ser.write([0x61,0x32])
                    nl=ser.read(2)
                  #  time.sleep(1e-05)
                    T=T+1
                    print(nl)
                    if nl== (b'\xff\xf3' or b'\xf3\xff' ):
                        #write to the OPC 
                        for i in range(14):        # Send the whole stream of bytes at once.
                            ser.write([0x61, 0x01])
                            time.sleep(0.00001)    
                        #time.sleep(.1)
                        #read the data
                        ans=bytearray(ser.readall())
                       # print("ans=",ans)
                        ans=self.rightbytes(ans)
                       # print("ans=",ans)
                        b1 = ans[0:4]
                        b2 = ans[4:8]
                        b3 = ans[8:12]
                        c1=struct.unpack('f',bytes(b1))[0]
                        c2=struct.unpack('f',bytes(b2))[0]
                        c3=struct.unpack('f',bytes(b3))[0]
                        check=self.combine_bytes(ans[12],ans[13])
                        print("Check=",check)
                        return([c1,c2,c3])
                    elif T > AT:
                        print("Reset SPI")
                        time.sleep(3) #time for spi buffer to reset
                        #reset SPI  conncetion 
                        self.initOPC(ser)
                        T=0 
                        return
                    else:
                        time.sleep(wait*10) #wait 1e-05 before next commnad     
        #get hist data 
        def getHist(self,ser):
            
                #OPC N2 method 
                T=0 #attemt varaible 
                while True:   
                #    print("get hist attempt ",T)
                
                    #reques the hist data set 
                    ser.write([0x61,0x30])
                   # time.sleep(wait*10)
                    nl = ser.read(2)
                  #  print(nl)
                    T=T+1  
                  #  print("Reading Hist data")
                 #  # print(nl)
                    if nl== (b'\xff\xf3' or b'\xf3\xff' ):
                        for i in range(86):        # Send bytes one at a time 
                                ser.write([0x61, 0x01])
                                time.sleep(0.000001)   
                        
                       # ans=bytearray(ser.read(1))
                    #    print("ans=",ans,"len",len(ans))
                        time.sleep(wait) #delay
                        ans=bytearray(ser.readall())
                   #     print("ans=",ans,"len",len(ans))
                        ans=self.rightbytes(ans) #get the wanted data bytes 
                       # ans=bytearray(test)
                    #    print("ans=",ans,"len",len(ans))
                        #print("test=",test,'len',len(test))
                        data=self.Histdata(ans)
                        return data 
                    if T > AT:
                     #   print("Reset SPI")
                        time.sleep(wait) #time for spi buffer to reset
                        #reset SPI  conncetion 
                        self.initOPC(ser)
                        print("ERROR")
                        data="ERROR"
                        return data
                    else:
                        time.sleep(wait*10) #wait 1e-05 before next commn
                                
                      
                        
                        
                       
        
        def TurnOff(self,OPCPORT,OPCNAME):
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
                print(OPCNAME,"Shutting down, おやすみなさい")
                ser = serial.Serial(**serial_opts)
                self.fanOff(ser)
                self.LazOff(ser)
                ser.close()
				
				
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
                if data!="ERROR":
                    print(OPCNAME," Time",tnow , " PM1:", str(round(data['pm1'],2)) ,"PM2.5:", str(round(data['pm2.5'],2)) ,"PM10:", str(round(data['pm10'],2)))
                    data=str(data['Bin 0']) + ","  + str(data['Bin 1']) + ","  + str(data['Bin 2']) + ","  + str(data['Bin 3']) + ","  + str(data['Bin 4']) + ","  + str(data['Bin 5']) + ","  + str(data['Bin 6']) + ","  + str(data['Bin 7']) + ","  + str(data['Bin 8']) + ","  + str(data['Bin 9']) + ","  + str(data['Bin 10']) + ","  + str(data['Bin 11']) + ","  + str(data['Bin 12']) + ","  + str(data['Bin 13']) + ","  + str(data['Bin 14']) + ","  + str(data['Bin 15']) + ","  + str(data['Bin 16']) + "," + str(data['Bin 17']) + ","+ str(data['Bin 18']) + ","+ str(data['Bin 19']) + ","+ str(data['Bin 20']) + ","+ str(data['Bin 21']) + "," + str(data['Bin 22']) + ","+ str(data['Bin 23']) + ","+ str(data['MToF']) + ","+str(data['period']) + ","+ str(data['FlowRate']) + ","+ str(data['OPC-T']) + ","+ str(data['OPC-RH']) + ","  + str(data['pm1']) + ","  + str(data['pm2.5']) + ","  + str(data['pm10']) +"," + str(data['Check'])
                else:
                    print("OPC data capture error at "+tnow)
                    data="nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan"+ ","  + "nan" + ","  + "nan "+ ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + ","  + "nan" + "," + "nan" + ","+ "nan"+ ","+ "nan"+","+ "nan" + ","+ "nan" + "," + "nan" + ","+ "nan" + ","+ "nan" + ","+"nan" + ","+ "nan"+ ","+ "nan"+ ","+ "nan"+ ","  + "nan" + ","  + "nan" + ","  + "nan" +"," + "nan" 
                return data                      

               

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
                time.sleep(2)

                ser = serial.Serial(**serial_opts)
                #ser.open()
            
                print("**************************************************")
                print("Init:",OPCNAME)
                self.initOPC(ser)
                time.sleep(1)
                print("Turn Off:")
                self.fanOff(ser)
                self.LazOff(ser)
                time.sleep(5)
                print("Turn on:")
                self.fanOn(ser)
                self.LazOn(ser)
                print(OPCNAME,"Ready")
               

             
