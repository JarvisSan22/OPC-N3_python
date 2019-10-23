from flask import Flask, render_template, send_file, make_response, request
import datetime
import os
import sys
import pandas as pd
import glob
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import matplotlib.dates as mdates
import psutil # to check the sensors are running 


# run SDS011 scripts


  
     
def dateparse(timestamp):  # read the data time properly
    time = pd.to_datetime(timestamp, yearfirst=True, dayfirst=False)
 #   print(time)
  #  time.strftime(time, '%Y-%m-%d %H:%M:%S')
    return time


def readrpi3data():
	DataFolder = "/home/pi/AQ/OPCData/"
	today = datetime.datetime.now().strftime("%Y%m%d")
	todayfiles = []
	for file in glob.glob(DataFolder+'****.csv'):
		if today in file:
			todayfiles.append(file)
	data = pd.DataFrame()
	for file in todayfiles:
	#	print(file)
		dataloop = pd.read_csv(file, header=4, error_bad_lines=False, engine='python',index_col=False)
	
		data = pd.concat([data, dataloop], ignore_index=False, axis=0, sort=True)
        
		sensors=pd.read_csv(file,header=None, skiprows=1,nrows=1)
	  	sensors=sensors.values.tolist()[0]

	#print(data.index)
#	print(data["time"])
	#print(data.iloc[0]["sds-pm2.5"])
  	# pd.to_datetime(data.time,yearfirst=True, dayfirst=False)

        data["time"] = dateparse(data["time"])
 	data.set_index('time', inplace=True)

	return data, sensors

def sensorsmean(data,sensors):
	DHT=0
	SDS=0
	OPC=0
  	Meandata={}
	for sen in sensors:
		if "DHT" in sen.upper():
			DHT=DHT+1
		elif "SDS" in sen.upper():
			SDS=SDS+1
		elif "OPC" in sen.upper():
				OPC=OPC+1
	print(DHT)
	if DHT>1:
 
    		DHTMeandata=pd.DataFrame(columns=["RH","Temp"])
		print("There are "+ str(DHT)+" DHT22 in Data")
		DHTColumns=["DHT-RH","DHT-T"]
		for i in range(0,DHT):
			if i>0:
				DHTColumns.append("DHT-RH."+str(i))
				DHTColumns.append("DHT-T."+str(i))
    		DHTMeandata["RH"]=data[DHTColumns[::2]].mean(axis=1)
	  	DHTMeandata["Temp"]=data[DHTColumns[1::2]].mean(axis=1)
	  	print(DHTMeandata.describe())
    		Meandata["DHT22"]=DHTMeandata
		
 	if SDS>1:
		print("There are "+ str(SDS)+"SDS011 in Data")
    		SDSMeandate=pd.DataFrame(columns=["sds-pm2.5","sds-pm10"])
		SDSColumns=["sds-pm2.5","sds-pm10"]
		for i in range(0,SDS):
			if i>0:
				SDSColumns.append("sds-pm2.5."+str(i))
				SDSColumns.append("sds-pm10."+str(i)) 
    		SDSMeandata["sds-pm2.5"]=data[SDSColumns[::2]].mean(axis=1)
	  	SDSMeandata["sds-pm10"]=data[SDSColumns[1::2]].mean(axis=1)
	  	print(SDSMeandata.describe())
    		Meandata["SDS011"]=SDSMeandata    
  	if OPC>1:
		print("There are "+ str(OPC)+"OPC in Data")
                OPCMeandate=pd.DataFrame(columns=["pm1","pm2.5","pm10"])
                OPCColumns=["pm1","pm2.5","pm10"]
                for i in range(0,OPC):
                        if i>0:
				OPCColums.append("pm1."+str(i))
                                OPCColumns.append("pm2.5."+str(i))
                                OPCColumns.append("pm10."+str(i)) 
                OPCMeandata["pm1"]=data[OPCColumns[::3]].mean(axis=1)
                OPCMeandata["pm2.5"]=data[OPCColumns[1::3]].mean(axis=1)
                OPCMeandata["pm10"]=date[OPCColumns[2::3]].mean(axis=1)
		print(OPCMeandata.describe())
                Meandata["OPC"]=OPCMeandata
	if "OPC" in Meandata.keys():
		OPCdata=Meandata["OPC"]
	else:
		OPCdata=data[["pm1","pm2.5","pm10"]]   
	if "SDS011" in Meandata.keys():
      		sdsdata=Meandata["SDS011"]
  	else:
        	sdsdata=data[["sds-pm2.5","sds-pm10"]]
  	if "DHT22" in Meandata.keys():
        	dhtdata=Meandata["DHT22"]
	elif "DHT22" notin Meandata.keys(): #if no DHT22 attched make error data to not cause errors in the python script
		dhtdata=pd.DataFrame(columns=["RH","Temp"],index=data.index)
		dhtdata["RH"]="NaN"
		dhtdata["Temp"]="NaN"
  	else:
      		dhtdata=Meandata[["DHT-RH","DHT-T"]]
      		dhtdata.rename(columns={"DHT-RH":"RH","DHT-T":"Temp"},inplace=True)
  	return opcdata,dhtdata
	


def runsen():
	os.system("sudo python /home/pi/AQ/OPCscripts/start.py &")
	return "yes"


# flask get serverworking
app = Flask(__name__)
@app.route("/")
def start():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   status,statuscol=check_opp()
   
  # on = runsen()
   data, sens = readrpi3data()
   opcdata,dhtdata=sensorsmean(data,sens)
   templateData = {
      'title': 'OPC Data',
      'time': timeString,
       'pm1':opcdata.iloc[~0]["pm1"],	
      'pm2': opcdata.iloc[~0]["pm2.5"],
      'pm10': opcdata.iloc[~0]["pm10"],
      'Maxpm10': max(opcdata["pm10"]),
      'Maxpm2': max(opcdata["pm2.5"]),
           'Minpm2': min(opcdata["pm2.5"]),
		      'Minpm10': min(opcdata["pm10"]), 
	 'Minpm1': min(opcdata["pm1"]),
                      'Maxpm1': min(opcdata["pm1"]), 
  
           'RH':round(dhtdata.iloc[~0]["RH"],1),
           'Temp':round(dhtdata.iloc[~0]["Temp"],1),
            'status':status,
       'statuscol':statuscol
      }
   return render_template('index.html', **templateData)
   
#plots scripts    
@app.route('/Plots/PM')
def plot_pm():
  data, sens = readrpi3data()
  opcdata,dhtdata=sensorsmean(data,sens)
  fig=Figure(facecolor='#f0f8ff')
  
  axis=fig.add_subplot(1,1,1)
  axis.set_title("OPC")
  axis.grid(True)
  axis.plot(opcdata["pm1"],label="PM1")
  axis.plot(opcdata["pm2.5"],label="PM2.5")
  axis.plot(opcdata["pm10"],label="PM10")
  axis.set_xlim(opcdata.index[0],opcdata.index[~0])
  myFmt = mdates.DateFormatter('%H:%M')
  axis.xaxis.set_major_formatter(myFmt)
  axis.legend()
  #the new plotty side of Flask
  canvas = FigureCanvas(fig)
  output = io.BytesIO()
  canvas.print_png(output)
  response = make_response(output.getvalue())
  response.mimetype = 'image/png'
  return response
  

@app.route('/Plots/DHT')
def plot_dht():
  data, sens = readrpi3data()
  sdsdata,dhtdata=sensorsmean(data,sens)
  fig=Figure(facecolor='#f0f8ff')
  axis=fig.add_subplot(1,1,1)
  axis.set_title("DHT22")
  axis.grid(True)
  #RH plot
  axis.plot(dhtdata["RH"],color="BLUE")
  axis.set_ylim(0,100)
  axis.set_xlim(dhtdata.index[0],dhtdata.index[~0])
  axis.set_ylabel("RH %")
  myFmt = mdates.DateFormatter('%H:%M')
  axis.xaxis.set_major_formatter(myFmt)
  
  #temp plot 
  axT=axis.twinx()
  axT.plot(dhtdata["Temp"],color="RED")
  axT.set_ylabel("Temp C")
  #axis colores 
  axT.tick_params('y', colors='RED')
  axT.xaxis.set_major_formatter(myFmt)
  axis.tick_params('y', colors='BLUE')
 
  #the new plotty side of Flask
  canvas = FigureCanvas(fig)
  output = io.BytesIO()
  canvas.print_png(output)
  response = make_response(output.getvalue())
  response.mimetype = 'image/png'
  return response

#check sensors operatin

def check_opp():
  run="start.py" #SDSoll opration code
  status=""
  print(run) #check the code
  #Create a large array with all the prosses currenlty running
  Process=[]
  for process in psutil.process_iter():
      Process=Process+process.cmdline()
      # print(Process)                        

  # check if the code is in the processes,
  if any(run in s for s in Process):
         # sys.exit('Sensors Running')
          status="RUNNING"
          statuscol="#00ff00"
  else:
        #  print('Sensors not Running')
          status="NOT RUNNING"
          statuscol="#ff0000"
  return status, statuscol
  


#buttons 
@app.route("/<deviceName>/<action>")  # get latest value
def newdata(deviceName, action):
	now = datetime.datetime.now()
 	timeString = now.strftime("%Y-%m-%d %H:%M")
	status,statuscol=check_opp()
	templateData = {
	'title': 'Sensors are running:?',
      'time': timeString,
      'pm2': "NAN",
	    'pm10': "NAN",
           'Maxpm2': "NAN",
		      'Maxpm10': "NAN",
           'Minpm2': "NAN",
		      'Minpm10': "NAN",   
       'RH':"NAN",
       'Temp':"NAN", 
       'status':status,
       'statuscol':statuscol
 
	}
  

	if deviceName == "newdata":
		data, sens = readrpi3data()
    		opcdata,dhtdata=sensorsmean(data,sens)
                templateData = {
      'title': 'OPC Data',
      'time': timeString,
       'pm1':opcdata.iloc[~0]["pm1"],	
      'pm2': opcdata.iloc[~0]["pm2.5"],
      'pm10': opcdata.iloc[~0]["pm10"],
      'Maxpm10': max(opcdata["pm10"]),
      'Maxpm2': max(opcdata["pm2.5"]),
           'Minpm2': min(opcdata["pm2.5"]),
		      'Minpm10': min(opcdata["pm10"]), 
	 'Minpm1': min(opcdata["pm1"]),
                      'Maxpm1': min(opcdata["pm1"]), 
  
           'RH':round(dhtdata.iloc[~0]["RH"],1),
           'Temp':round(dhtdata.iloc[~0]["Temp"],1),
            'status':status,
       'statuscol':statuscol
      }
    #dataplotter(data)
		
	if deviceName == "kill":
	   	os.system("sudo pkill -f /home/pi/SDS-011-Python-master/AQ/Scripts/start.py ")
    		data,sens=readrpi3data()
        	opcdata,dhtdata=sensorsmean(data,sens)
  
       
        
      		templateData = {
      'title': 'OPC Data',
      'time': timeString,
       'pm1':opcdata.iloc[~0]["pm1"],	
      'pm2': opcdata.iloc[~0]["pm2.5"],
      'pm10': opcdata.iloc[~0]["pm10"],
      'Maxpm10': max(opcdata["pm10"]),
      'Maxpm2': max(opcdata["pm2.5"]),
           'Minpm2': min(opcdata["pm2.5"]),
		      'Minpm10': min(opcdata["pm10"]), 
	 'Minpm1': min(opcdata["pm1"]),
                      'Maxpm1': min(opcdata["pm1"]), 
  
           'RH':round(dhtdata.iloc[~0]["RH"],1),
           'Temp':round(dhtdata.iloc[~0]["Temp"],1),
            'status':status,
       'statuscol':statuscol
      }
	if deviceName== "reset":
		on=runsen()
                data,sens=readrpi3data()
                opcdata,dhtdata=sensorsmean(data,sens)
    
                templateData = {
      'title': 'OPC Data',
      'time': timeString,
       'pm1':opcdata.iloc[~0]["pm1"],	
      'pm2': opcdata.iloc[~0]["pm2.5"],
      'pm10': opcdata.iloc[~0]["pm10"],
      'Maxpm10': max(opcdata["pm10"]),
      'Maxpm2': max(opcdata["pm2.5"]),
           'Minpm2': min(opcdata["pm2.5"]),
		      'Minpm10': min(opcdata["pm10"]), 
	 'Minpm1': min(opcdata["pm1"]),
                      'Maxpm1': min(opcdata["pm1"]), 
  
           'RH':round(dhtdata.iloc[~0]["RH"],1),
           'Temp':round(dhtdata.iloc[~0]["Temp"],1),
            'status':status,
       'statuscol':statuscol
      }
        if action =="yes":
                return render_template('index.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
