
# OPC N3 Reposiotry Ploter scripts 
Author : Daniel Jarvis 
Contacts : ee18dj@leeds.ac.uk

### Currenrly not working on RPI3, due to issue will Folium maps, will fix soon

### Needed imports
1st updata
- sudo apt-get update
- sudo apt-get upgrade

2st get mpld, pandas and Scientific Python moduels
 - sudo apt-get install xsel xclip libxml2-dev libxslt-dev python-lxml python-h5py python-numexpr python-dateutil python-six python-tz python-bs4 python-html5lib python-openpyxl python-tables python-xlrd python-xlwt cython python-sqlalchemy python-xlsxwriter python-jinja2 python-boto python-gflags python-googleapi python-httplib2 python-zmq libspatialindex-dev
 - sudo pip install bottleneck rtree
 - sudo apt-get install python-numpy python-matplotlib python-mpltoolkits.basemap python-scipy python-sklearn python-statsmodels python-pandas
1nd get other import for map and plots
  -sudo pip install mpld3
  -sudo pip install folium 
 
 # "AQDataplot.py"
 Dashboard creatuer scripts, with many options based on data varaibles and addional maps (See plot OPTIONS). Base Dashboard works for multiple sensors as long as all the data is in the same folder. To run:
 - 1st check AQDataplot.py, nano AQDataplot.py
 - 2nd Updata "Sens" sensors you want to plot, "vals" the varaibles you want to lot, "ave" timestampe average ("RAW","1T","10T","60t" ...)
 ,"Dates" desired dates for the dashbord (deafult is today and yesterday), "filename" save file name, and "DataFolder" where is all the data stored 
 - 3rd "RUN" python AQDataplot.py 
 
 ![DASHBOARD](https://github.com/JarvisSan22/OPC-N3_python/blob/master/AQ/AQplotter/Dashbord.gif)
 
 # Plot OPTIONS 
  
 ### "STATICMAP"
![STATICMAP1](https://github.com/JarvisSan22/OPC-N3_python/blob/master/AQ/AQplotter/STATICMAP.gif)
 ### "GPSWALK"
 
