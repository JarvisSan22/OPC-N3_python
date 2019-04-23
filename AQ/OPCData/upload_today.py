import requests
import sys
import datetime
#IMport the file names, you dont want to type them out 
import variables as V 

run=V.RUNSEN
url = V.URL
RPI=V.RPINAME


LOCATION = V.LOCATION
FOLDER = V.FOLDER

datenow = datetime.date.today()
yesterday=datetime.date.today() - datetime.timedelta(days=1)


def postdata(date,NAME):
         datestring = str(date).replace('-','')
		 #create varaible for running OPCN3
         NAMES=""
    	 for r in run:
             NAMES=NAMES+","+r
             file= FOLDER + LOCATION +"_"+ RPI+'_' +  datestring + ".csv"
		#make hte request, to send the data
         with open(file, 'rb') as f:
                r = requests.post(url, files={'file': f});
                print("Uplaoded:", file, " at ",datenow)
                


for r in run:

    postdata(datenow,r)    

