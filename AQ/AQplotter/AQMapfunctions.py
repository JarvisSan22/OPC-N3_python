# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 12:44:52 2019

@author: Jarvis
AQ Map fuctions libary for compter project
"""
#All the imports 
import folium 
from folium import plugins
#needed to get plot in popup
import vincent 
import json
import datetime
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#for random data generator
import random
import math
import codecs
#get AQ Fuctios 
import sys
from folium.plugins import TimestampedGeoJson
#color bars
import branca.colormap as cm
#import folium
from folium import IFrame
import mpld3
import csv



#set varables for all fuctions 
#colors used for the color bar and the data plots 
colors=["green","greenyellow","yellow","gold","orange","salmon","red","purple"]





#get data 
def Walkdata(loc):
    try:
        #read the data
        df=pd.read_csv(loc,header=4,error_bad_lines=False)
        #df=pd.DataFrame({'time':data['time'] 'PM2':data['pm2'],'PM10':data['pm10'],'PM1':data['pm2'], 'RH':data['RH'],'lat':data['lat'],'lon':data['lon']})
        print("Data check 1",df.head(3))
        #df.index=pd.to_datetime(df.index)
        df.set_index('time', inplace=True, drop=True)
        #print("Data check 2",df.head(3))
        #read in info  from csv
        with open(loc) as f:
            reader=csv.reader(f)
            info={}
            i=0
            for row in reader:
                i=i+1
                if i<5:
                    print(row)
                    rowinfo=rowinfo=list(filter(None,row[1:5]))
                    info[row[0]]=rowinfo
                    
                    
        return df, info
    except Exception as e:
             print("Error in reading file ",loc," /n please check file")
             print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
             print(type(e))
             print(e.args)
             

# vectorized haversine function
def gendist(data):
    """
    Genrate the distance between two point and add them as a new row called dist

    """ 
    earth_radius=6371
    
    diffs=[]
    #reset indec, to get the number not time 
    print("gendist")
    print(data["lat"].iloc[3])
    for ind in range(0,len(data)):
       # print(ind)
        #if not first point and last point
        try:
            if ind != 0 and ind != len(data)-1:
              #  print(data["lat"][ind])
                lat1=data["lat"].iloc[ind]
                lat2=data["lat"].iloc[ind+1]
                lon1=data["lon"].iloc[ind]
                lon2=data["lon"].iloc[ind+1]
            
                lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
                dlat=lat2-lat1
                dlon=lon2-lon1
                a = np.sin((dlat)/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin((dlon)/2.0)**2
                diff=earth_radius * 2 * np.arcsin(np.sqrt(a))*1000
            else:
                diff="nan"
            diffs.append(diff)
        except IndexError: 
            diff="nan"
            diffs.append(diff)
        except Exception as e:
             print("Error in GPS distance, check columns names")
             print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
             print(type(e))
             print(e.args)
             pass
    data.insert(len(data.columns),"dist",diffs,True) 
    
    return data

def Staticsitedate(df,val,location,m):
    """
    Plot static data, take in the data df, 
    located the data in Geolocation from the file name and plot it
    
    """
    #get date from name in the GPS data 

  #  print(df.head(5))
    #plot the data as popup
    Goefol="Data//GeoLocations.csv"
   # Geolocs=pd.read_csv(Goefol,header=0,encoding = 'unicode_escape',error_bad_lines=False)
    with codecs.open(Goefol, "br",encoding="utf8", errors='ignore') as file:
        Geolocs = pd.read_table(file, delimiter=",")
    #Geolocs.set_index("Site")
   # print(Geolocs)
    #find the site information in the Geolocsation
    for i,ind in enumerate(Geolocs["Site"]):
        if ind==location:
           
            try:
                Lat=Geolocs["Lat"][i]
                lon=Geolocs["lon"][i]
                info={}
                info["Site"]=Geolocs["Site"][i]
                info["Sensor"]=Geolocs["Sensor"][i]
                info["start date"]=Geolocs["start date"][i]
                info["end date"]=Geolocs["end date"][i]
                info["Link"]=Geolocs["Link"][i]
                print("siteinfo",Lat,lon)
            except:
                print("Site infromation error")
                pass
            
            try:
                popup=plotdataPopInfo(df,val,info)
            except:
                print("Popup error")
                popup=info["Site"]
            folium.Marker(location=[Lat,lon],
            popup=popup,
            #get icon and color based of mean value , of the first value
            icon=folium.Icon(color= genfill_color(df[val[0]].mean(),100))
            ).add_to(m)
            print("Markger Generated")



def Stationrydata(data):
    """
    Fuction: Run through GPS data files, find stationry data cuts its of the old data.
    Then it run though the Stationry data to find if there are multiple statiory spots,
    if so it splits the stationory data into dic elements.
    
    
    """
    
    
    #get dist data
    data=gendist(data)  #get the date
    print("Distance", data["dist"])
    Statdata=pd.DataFrame(index=data.index,columns=data.columns) #create a stationy data frame array
  #  Nanlatlon=pd.DataFrame(index=data.index,columns=data.columns) #create a GPS error dataframe array
    #pDataFrame(columns=data.columns)
    a=0 #set an index for the save
    #loop through the data
    try:
    
        for index,row in data.iterrows():
            
            diff=row["dist"]
           # print(diff)
            if diff != "nan":
                save=pd.DataFrame(index=data.index,columns=data.columns)
               # rec="on"
                if diff<1.5:
                    #dict1.update()
                    a=a+1
                    save.append(row)
                    if a>5: #if 5 stationry points in row
           
                        Statdata.loc[index]=row      
                else:
                    a=0 #reset index
    
        print("Stationary Data")
        print(Statdata.head(4))
        
        
        Newdata=Statdata[Statdata['dist'].notnull()]
        #cut the data from old array
        data=data[Statdata['dist'].isnull()]
     # checks 
      #  print("OldD",data.head(4))
       # print("NewD",Newdata.head(4))
        
  
     #of there is some still data 
          #chaeck if Still data is close to one another in time
        #If it is split the data into diffrenct section
        Stilldic={} #dic to add the splits
    
        Satname="Sat" #place holdername
        satnum=1 #set number to add to satname for diffrent station data sets 
        saveindex=0 #set a index to deal with multiple silld
        
        save=Newdata.index[0] #place holder to get the function working
        for index,row in Newdata.iterrows():
            if index != 0:
                timediff=divmod((index-save).total_seconds(),60)
                if timediff[1] >120: #if greater than 2 mins split
                    #add to still data to dic
                    Stilldic[Satname+str(satnum)]=pd.DataFrame(Newdata.ilox[saveindex:index])
                    satnum=satnum+1 #add to the satnum
            #save the index for next interval
            save=index
        if len(Stilldic) <1: # if there only 1 sill data, then add it to the dict. This is to make future code what loop through a dic easyer
            Stilldic[Satname]=Newdata
        print("Got GPS Stationy data")
           # print(Newdata.head(3))
    except Exception as e:
         print("No stationry GPS data ")
         print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
         print(type(e))
         print(e.args)
         pass
    return data, Newdata

#color map
def colormap(m,index,caption):
    """
    Def a color map, need the map m, an array of colors with a matching index and caption for the name.
    """

    
    CB= cm.StepColormap(colors, vmin=0,vmax=50,index=index,  caption=caption )
    m.add_child(CB)


def genfill_color(val,ref):
    """
    Generate colors for to fill cirles based on data values
    need a color lits and index defined before the use 
    
    """
    val=val/ref
    col=""
    try:
        if val <= 0.05:
            col=colors[0]
        elif (val >= 0.05 and val <0.1):
            col=colors[1]
        elif (val >0.1 and val <0.15):
            col=colors[2]    
        elif (val >0.15 and val <0.20):
            col=colors[3]
        elif (val >= 0.20 and val <0.25):
            col=colors[4]
        elif (val >= 0.25 and val <0.3):
            col=colors[5]    
        elif(val >=0.3 and val <0.4 ):
            col=colors[6]
        elif val>0.4:
            col=colors[7]
        return col
    except  Exception as e:
                    print("Error in  genfill_color")
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    print(type(e))
                    print(e.args)
                    pass


def GenPMCircles(data,val,group,outlinecolor):
    """
    Generate walk map data as circles data, need data, the varaibles and the map group i.e for diffrent dates 
    And an outlinecolor for 
    """
    data=data.dropna()
    try:
        for index,row in data.iterrows():   
            ref=100
            folium.Circle(location=[row['lat'],row['lon']],
            radius=8,
            popup=("Time <br>"+str(index)+" "+val+"+:"+str(round(row[val],2))+"ug/m^2"+" Temp:"+str(round(row['DHT-T'],2))+"C"+" RH:"+str(round(row['DHT-RH'],1))+"(%)"),
            fill_color=genfill_color(row[val],ref),
            color=genfill_color(row[val],ref),
            fill_opacity=0.8,
            opacity=0.9,
            ).add_to(group)
    except  Exception as e:
                    
                    print("-----------Error in GPS Data cirlce generation----------")
                    print(val)
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    print(type(e))
                    print(e.args)
                    pass    



def DataCircle(df,lat, lon,group,val):
    """
    Data circle fuction but this time iver with a data plot of mean data 
    
    
    """
    #generate data cirles with plots of the data or mean depending on length
    #print(df)
     
    try:
        if len(df)>1 and len(df)<10: #just plot mean data, too small for a time series 
            popup="Mean <br> Time <br>"+str(min(df.index))+"_"+str(max(df.index))+"PM2.5:"+str(round(df[val[0]],2))+"ug/m^2"+" PM10:"+str(round(df[val[1]],2))+"ug/m^2" +" Temp:"+str(round(df['DHT-T'],2))+"C"+" RH:"+str(round(df['DHT-RH'],1))+"(%)"
            if "BinCount" in df.colomns:
                ref=1000
                popup=popup+"Partical Count:"+str(round(df['BinCount'],2)) 
                fill_color=genfill_color(df[val[0]],ref)
            else:
                fill_color=genfill_color(df[val[0]],100)
            df=df.mean()
            folium.Circle(location=[df['lat'],df['lon']],
            radius=8,
            fill_color=fill_color,
            color="grey",
            fill_opacity=0.8,
            opacity=0.9,
            ).add_to(group)
        else:
            #if more than 10 data points, plot the time series of the data
           
            folium.Circle(location=[lat,lon],
            popup=plotdataPop(df,val),
            radius=10, fill=True,color='black'
        ).add_to(group)
    except  Exception as e:
                    print("Error in GPS Data cirlce generation")
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    print(type(e))
                    print(e.args)
                    pass
    
def DataMarker(df,val,lat, lon,group):
    
    folium.Marker(location=[lat,lon],
    popup=plotdataPop(df,val),
    icon=folium.Icon(color= genfill_color(df[val[0]].mean(),100))
).add_to(group)


def DataMarkerInfo(df,val,lat, lon,group,info):
    
    folium.Marker(location=[lat,lon],
    popup=plotdataPopInfo(df,val,info),
    icon=folium.Icon(color= genfill_color(df[val[0]].mean(),100))
).add_to(group)   


def GenCount(data):
    """
    Generate a total count from all bins for an OPC
    
    """
    counts=[]
    for index,row in data.iterrows(): 
        count=0
        for column in data.columns:
            if "b" in column:
                count=count+row[column]    
      #  print(count)
        counts.append(count)
    data.insert(len(data.columns),"BinCount",counts,True)
    return data


def plotdataPopInfo(df,vals,info):
    """
    Popup data ploter with information columns 
    Takes in the data desired to plot, 
    the  varaibles and the infomration about the location and sensor for the popup
    returned the popup
    """    
    #def data beased on values 
    figname=""
    df.index=pd.to_datetime(df.index)
    try:
        #df=df.copy()
        width=len(df.index)
        if width <500: #if there not much data, still make is big enoguh
            width=400
        #if more values are wanted to be plotted, add fadding 
        alpha=1 
        if len(vals) >1:
            alpha=0.8
        
        #define figure 
        fig, ax = plt.subplots(figsize=(6,6))
        if "GPS" in info["Site"]:  #if its a GPS file add the 1 min mean to the plot
            mindf=df.resample("1T").mean()
            for val in vals:
                minval=val+"(1 min-mean)" 
                ax.plot(mindf[val], label=minval,alpha=alpha) 
            
            ax.legend()
        else:       
            ax = df.plot(ax=ax, legend=True, alpha=alpha)
        ax.set_ylabel('Mass concentration (uu g/m^3)')
        ax.set_xlabel('')
        
      #  ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60*3))   #to get a tick every 6 hours 
        #ax.format_xdata = plt.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))     #optional formatting 
        ax.set_title(info["Site"])
        ax.grid()
        
       #create a htlmfile for the plot
        date=pd.to_datetime(df.index[0]).strftime("%Y%m%d")#get the date 
        figname = 'popplot_'+info["Site"]+"_"+date+'.html'
        #The location dic has to be added sepratly, as the HTML map will be created from pic inside the same output directory
        mpld3.save_html(fig,"Mapoutput//"+figname)
     
    
        #Generate some more plot information based on data   
        #Replace with error if error occures 
        try:
            MAX=df[vals[0]].max()
            MAXid=df[vals[0]].idxmax()
            MAXid=MAXid.strftime("%H:%M")
            MAX=str(round(MAX))+" ug/m^3 </br> at "+str(MAXid)
            
            MIN=df[vals[0]].min()
            MINid=df[vals[0]].idxmin()
            MINid=MINid.strftime("%H:%M")
            MIN=str(round(MIN,2))+" ug/m^3 </br> at "+str(MINid)
            print("Check min value ",MIN)
            mean=str(round(df[vals[0]].mean(),2))+" ug/m^3"
           # print(MAX,MIN,mean)
        except:
            MAX="ERROR"
            MIN="ERROR"
            mean="ERROR"
            
        try:
            sitename=info["Site"]
            sitesensor=info["Sensor"]
            sitedate=str(info["start date"])+"-"+str(info["end date"])
           
        except:
            sitename="ERROR"
            sitesensor="ERROR"
            sitedate="ERROR"
           

 
            
    #Set out the HTML for the popup
    #This take in the previous plot HTML just created and the sensor infrom for a info columns
        html="""
      <!DOCTYPE html>
    <html>
    
    <head>
        
         <style>
         
         .row {
           height: 350px;
           width:600px;
           }
        .column {
          float: left;
          width: 50%;
           
        }
        /* Clear floats after the columns */
        .row:after {
          content: "";
          display: table;
          clear: both;
        }
        
        iframe {
        display: block;
        border: none;
    
    }
        
       </style>
       
      </head>
      <body>
      
      <div class="row">
    	<div class="column">
        <iframe src= '"""+figname+"""' name="sample" width="300" height="350">
        </iframe>
    	</div>
        <br />
        <div class="column">
        </div>
    	<div class="column">
    		<table border="1! width="40" cellspacing="1" cellpadding="1" bordercolor="#333333">
    		<tr>
    		<th bgcolor="#EE0000"><font color="#FFFFFF">Location</font></th>
    		<th bgcolor="#EE0000" align="right" width="120"><font color="#FFFFFF">"""+sitename+"""</font></th></tr>
    		<tr>
    		<td bgcolor="#99CC00" align="center" nowrap>Operating Sensor</td>
    		<td bgcolor="#FFFFFF" align="center" valign="top" width="100">"""+sitesensor+"""</td>
    		</tr>
    		<tr>
    		<td bgcolor="#99CC00" align="center" nowrap>Operation date </td>
    		<td bgcolor="#FFFFFF" align="center" valign="top" width="100">"""+sitedate+"""</td>
    		</tr>
    		
    		<tr>
    		<td bgcolor="#99CC00" align="center" nowrap>Mean """+vals[0]+""" </td>
    		<td bgcolor="#FFFFFF" align="center" valign="top" width="100">"""+mean+"""</td>
    		</tr>
    	
    		<tr>
    		<td bgcolor="#99CC00" align="center" nowrap>Max  """+vals[0]+"""</td>
    		<td bgcolor="#FFFFFF" align="center" valign="top" width="100">"""+MAX+"""</td>
    		</tr>
    		
    		<tr>
    		<td bgcolor="#99CC00" align="center" nowrap>Min """+vals[0]+"""</td>
    		<td bgcolor="#FFFFFF" align="center" valign="top" width="100">"""+MIN+"""</td>
    		</tr>
    	
    
    		</table>
    	</div>
    </div>
      
      
      
      </body>
      </html>
        """
    
        #put the html into map usable format 
        pop = folium.Html(html, script=True)
        #Create the popup
        popup = folium.Popup(pop,  max_width=800) 
        return popup
    except  Exception as e:
                print("Error in GPS Data cirlce generation")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(type(e))
                print(e.args)
                pass


def plotdataPopVega(data,vals):
    '''
    Fuction to create a data popup, as a time servies.
    What then can be added to a marker
    
    '''
    df=data[vals]
    
    df.fillna(value='null', inplace=True)  # Does not handle missing values.
    line=vincent.Line(df)
    line.axis_titles(x="Time", y="Mass Concentration")
    line.legend(title="Values")
   
    #find the lenght of the data
    width=len(df.index)
    if width <500:
        width=400
    
    line.width=width
    line.height=200
    vega = folium.Vega(json.loads(line.to_json()), width="30%", height="10%")
    popup = folium.Popup(max_width=line.width+75).add_child(vega)
    return popup

def plotdataPop(data,vals):
    
    """
    simple data popup, take in data and values, plots it as a mpld3 plot allowing for interaction, 
    add it to an Iframe what then can be used in a folium map popup    
    
    returns a popup
    
    
    Last edit: 25/05/2019
    -added exceptions with line number 
    """
    try:
        df=data[vals]
      # print(df)
        width=300
        height=320
        #If more than one varable add fadding 
        alpha=1
        if len(vals) >1:
            alpha=0.8
        #define figure    
        fig, ax = plt.subplots(figsize=(4,4))
        #plot data
        for val in vals:
            ax.plot(df[val], alpha=alpha,label=val)
            
        ax.legend()    
        #Plot information
        ax.set_ylabel('Mass concentration (ug/m^3)')
        ax.set_xlabel('') #solving issue with x labes being cut in 1/2 
        #set tile based of time interval
        
        ax.set_title(df.index[0].strftime("%Y/%m/%d")+"-("+df.index[0].strftime("%H:%M")+" to "+df.index[len(df)-1].strftime("%H:%M"))
        ax.grid() #grid 
      
        #setppop up in mld3
        now=datetime.datetime.now()
        date=df.index[0].strftime("%Y%m%d")#get the date 
        #save=datetime.datetime.strptime(now,"%HH%MM%SS")
        figname = 'popup_plot'+date+str(now.microsecond)+'.html'
        mpld3.save_html(fig,'Mapoutput//'+figname)
        time.sleep(0.1)
        a=mpld3.fig_to_html(fig)
        #put pop up in iframe format ready to be put into the popup
        iframe = IFrame(a, width=(width), height=(height))
        popup = folium.Popup(iframe,  max_width=600) 
    
        return popup
    except  Exception as e:
                    print("Error in GPS Data cirlce generation")
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    print(type(e))
                    print(e.args)
                    pass
    
    




def generate_data(lat,lon,N):
    data=[]
    for x in range(N):
   
        dec_lat=random.random()/100
        dec_lon=random.random()/100
        con=round((math.sin(10*x))**2*50,2)
        print(con)
       
        data.append([lat+dec_lat,lon+dec_lon,con])
    return data





def Staticsitedatetime(df,info,val,m):
    """
    Generate style data for GeoJson time stamp in GenStaticTimemap 
    Takes in a df and location, get the wanted value
    Functional for static and GPS data
    
    Created:2019/05/31
    """
    features=[] #array to append Geojson features too
    
    #get locations from info
    loc=info["Location:"][0]
    sen=info["Sensors:"][0]
    print(loc)
    if "GPS" not in loc: #check if its static of GPS data
        Lat=info["Location:"][2]
        lon=info["Location:"][3]
                #print("siteinfo",Lat,lon)
               # PMstyle=pd.DataFrame()  
    #features=[]
    
    for index,row in df.iterrows():
        #print(index,row[val])
        pm=row[val] #get value
        row["color"]=genfill_color(pm,100) #generate color
        if "GPS" in loc: #if walk data get lat and lon
            lon=row["lon"]
            Lat=row["lat"]
        #freate GeoJson feature    
        feature = {
                'type': 'Feature',
                
                'geometry': {
                        'type':'Point', 
                        'coordinates':[lon,Lat]
                        },
        'properties': {
       # 'popup':location+" - "+sen+"<br>"+val+":"+str(round(pm,2)),
        'time': str(index),
        'style': {'color' : row['color']},
        'icon': 'circle',
        'iconstyle':{
            'fillColor': row['color'],
            'fillOpacity': 0.8,
            'stroke': 'true',
            'radius': 7
                    }
                     },
            }
         #append feature 
        
        features.append(feature)
        features.append(plugins.Terminator().to_json(str(index)))
    return  features,df


#generate standard map

def GenStaticTimemap(Datadic,val,ave,titlename,infos): 
    """
    Generate a static time series make for Date in a Datadirectory, the location come from the Datadic keys
    needed functions Staticsitedatetime, colormap
    Features:basics popups
    
    
    Created:08/06/2019
    #updated for RPI3 use
    """

    
    for k , info in infos.items():
            locs=infos[k]['Location:']
            Lat=float(locs[2])
            Lon=float(locs[3])
            print(Lat,Lon)
   
    #generate base map

    m=folium.Map([Lat,Lon],
             zoom_start=10,
             tiles='OpenStreetMap')
    
    #add colar bard
    if "pm" in val:
        index=[0,5,10,15,20,25,30,40,50]
        colormap(m,index,"Mass concentration ug/m^3")
    styledict=[] #Stlyed dict for the time stamped features to be added to map
    
    #loop through data dic, getting the location and putting the data as geojseon data under style
    for k, item in Datadic.items():
    #    print(item.head(4),loc)
        if val.upper()=="PM2.5" or val.upper()=="PM10" and "SDS" in k.upper():
            val="sds-"+val
        item=item.dropna()
        style,df=Staticsitedatetime(item,infos[k],val,m) #Add the time stamed geoJson
        styledict=styledict+style 
    #Read the styledict, puting the time onto the map  
    if ave.upper()=="RAW":
        interval="1T"
    else:
        i=ave.find("T")
        interval=ave[0:i]
        print(interval)
    TimestampedGeoJson(
                {
                        'type': 'FeatureCollection',
                        'features': styledict,
                        },
          period='PT'+interval+'M'
        , add_last_point=True
        , auto_play=False
        , loop=False
        , max_speed=10
        , loop_button=True
        , time_slider_drag_update=True).add_to(m)
       
    #save map     
    
    m.save(titlename+".html")
    print("完成")
    print(style)
   


def genmap(Datadic,val,titlename,infos):
    """
    Daniel Jarvis 
    Vertion generate a MAP based on one date, and returned the data into a dictionary 
   
    retrun a dictionary full of data, and a html map name
   
    last edit: 29/04/2019
   
    """
    #start
    print("Starting map generation, Values:"+str(val)+ "title:"+titlename)
    #plase holder to make code run
       
    #Lat=[]
    #Lon=[]
   
    for k , info in infos.items():
            locs=infos[k]['Location:']
            Lat=float(locs[2])
            Lon=float(locs[3])
            print(Lat,Lon)
    #CenLatlon=[Lat,Lon]
    
    #create base map
    print("Generating Base map, center :",[Lat,Lon])
    m=folium.Map([Lat,Lon],zoom_start=12,tiles='OpenStreetMap')
      #generate a color bar based on input value 
    if "PM" in val.upper():
        index=[0,5,10,15,20,25,30,40,50]
        colormap(m,index,"Mass concentration ug/m^3")
    elif val=="ParticleCount":
        index=[0,500,1000,1500,2000,2500,3000,4000,5000]
        colormap(m,index,"Mass concentration ug/m^3")
     
   
  
    print("Base map generated")
   
        
   

     #-------------------------------------    
    #Generate Walk GPS data  
     #---------------------
    for k, data in Datadic.items():
        print("Generating GPS walk data for ",k)
        #dont plot GPS data with erros 
        mask = ~np.isnan(data["lat"]) & ~np.isnan(data["lon"])
        df=data[mask]
        info=infos[k]
    
        try:
            #generate walkdata and still data, i.e if you sat for 20mins outside, or chatted for 5 mins
            print(info,df.head(4))
            #get walk data and still data 
            #print(walks)
            print(df.head(4))
            print("Plotting GPS walk data")
            #create group for GPS data
            walkg = folium.FeatureGroup(name=k)
            m.add_child(walkg)
            #add marker for walk start 
    
            
            #get start and end times
            start=df.index[0]
            end=df.index[len(df)-1]
            walkinfo={}
            #get location name
            #Sindex=W.index("Data\\")+5
            #Endindex=W.index("_GPS")+4
            locationname="Test" #W[Sindex:Endindex]
            print("Location name", locationname)
            walkinfo["Site"]=k.split(":")[0]
           # getting sensors name 
            walkinfo["Sensor"]=k.split(":")[1]
            walkinfo["start date"]=str(pd.to_datetime(start).strftime("%H:%M"))
            walkinfo["end date"]=str(pd.to_datetime(end).strftime("%H:%M"))
            walkinfo["Link"]=""
            
            #Plot infor marker with information
           # DataMarkerInfo(df,val,info["Location:"][2],info["Location:"][3],walkg,walkinfo)
            #print("Check",walkdf["pm2"]) 
            #Plot walk data   
            if "SDS" in k.upper(): #account for SDS data format
                val="sds-"+val
                
            #Create GPS Walk cirles 
        
            GenPMCircles(df,val,walkg,"green")
            
            
            #start plotting data on map
            print("-------------------------Ploted GPS walk data-----------------------------------")
        except Exception as e:
            print("-------------------------Error------------------------------------")
            print("GPS plot error")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            print(type(e))
            print(e.args)
            pass

    
    #add the layer control, for diffrent data sets 
    folium.LayerControl(collapsed=True).add_to(m)
    #save map
    m.save(titlename+".html")
    print("Map Created")