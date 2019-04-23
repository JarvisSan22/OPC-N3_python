import requests
import sys
import glob
import datetime
#IMport the file names, you dont want to type them out 
import variables as V 

run=V.RUNSEN
url = 'https://cemac.leeds.ac.uk/living-lab/staticdata'



FOLDER = V.FOLDER




#post all data 
def postalldata(FOLDER,RUN):
        #loop through all csv
         for file in glob.glob(FOLDER):
             #loop tthrough all running sensors "Or sensors data you want to upload"
            for sen in RUN:
                #if that sensors is in the file then upload the data 
                if sen in file:
                    with open(file, 'rb') as f:
                        r = requests.post(url, files={'file': file});
                        datenow = datetime.date.today()
                        print("Upladed:",file," at ",datenow)
                    
postalldata(FOLDER,run)



