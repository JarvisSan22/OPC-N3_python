
from __future__ import print_function
import requests
import sys
import datetime
import time
import urllib #to check wifi
import socket as SOCK #to check ip
import ntplib #to check the time to a internet serva
import os #to chage system setting
import psutil # to check the sensors are running 
import variables as V #IMport the file names, you dont want to type them out

url=V.URL
run="start.py"
FOLDER=V.FOLDER
LOCATION = V.LOCATION
RPI=V.RPINAME
#Test for WIFI status is working
def wificheck(url):
#check wifif by checking if the upload url can be accessed 

    
    try:
        urllib.urlopen(url)
        status="connceted"
    except:
        status="No"
    print("WIFI conncetion: ",status)
    return status

def ipcheck():
#get IP adress of the rpi3 
    
    s=SOCK.socket(SOCK.AF_INET,SOCK.SOCK_DGRAM)
    s.connect(('8.8.8.8',1))
    ip=s.getsockname()[0]
    print("ip: ",ip)
    return ip

def gettime(status):
    #function get the rpi3 time and checks it agians a online clock.
    #If there is no wifi conncetion is will just return the current rpi3 time
    #IF it does have a conncetion then it will check the time diffrece
    #If it diffrent it will be updated, and the diffrence will be locked
    #Fuction also returns updaed if the rpi3 clock was chaged, NoNeed if there is no diffrece, and NAN if there no wifi 

    
    timenow=datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #time time if wifi is connceted
    if status=="connceted":
        client=ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        wifitime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(response.tx_time))
        print(wifitime)
        print(timenow)
        if timenow !=wifitime:
            print("updating time")
            diff=timenow-wifitime
            update="updated"
            os.system('date '+wifitime)
            timenow=datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif timenow ==wifitime:
            print("Time synced")
            diff="NAN"
            update="NoNeed"
        
    elif status=="No":
        print("No conncetion, cant check time")
        diff="NAN"
        update="NAN"
    return timenow, update,diff


def checkrun(run):
    #fuction checks the run varaible from the varaible.py and sees if these code are running or not
    #it returns there stats with code name with Running or NotRunning in an array 
    
    check=""
    for R in run: #for loop for each code
        print(R) #check the code
        #Create a large array with all the prosses currenlty running
        Process=[]
        for process in psutil.process_iter():
            Process=Process+process.cmdline()
            # print(Process)                        

        # check if the code is in the processes,
        if any(R in s for s in Process):
                sys.exit(':Process found.')
                status="_Running"
        else:
                print('Process not found: starting.')
                status=":NotRunning"
        sp=R.split(".") #cut out the .py in the run code 
        sencheck=sp[0]+status
        print(sencheck)
        check=check+sencheck+"_"
        
    return check


def initFile():
    #open the file to be added to or create it if needed
        ofile= FOLDER + RPI + "_statuscheck.csv"
        print("Opening Output File:")
        if(not os.path.isfile(ofile)):
                f=open(ofile,'w+')
                print("wifi,ip,Loc,updated,time,diff,running",file=f)
        else:
                f=open(ofile,'a')
                
        return f


if __name__ == "__main__":

    
    #1st WIFI check
    wifis=wificheck(url)
    #2nd get IP
    if wifis=="connceted":
        ip=ipcheck()
    elif wifis=="No":
        ip="nan"
    #3rd check time if not update 
    time,updated,diff =gettime(wifis)
    #4th check running code
    running=checkrun(run)
    #5th add them to a file
    f=initFile()
    print(wifis+","+ip+","+LOCATION+","+updated+","+time+","+diff+","+running , file=f)
    print("Status-Checked")
    f.flush()
