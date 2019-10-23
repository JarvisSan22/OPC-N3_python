# rpiwebserver 
rpiwebserver for live viewing of reading, and plot of todays data.

Note: i Currently dont have a OPCN3 or OPCN2 to test this on, but this code should work and work for my [SDS011 repository](https://github.com/JarvisSan22/SDS-011-Python)

Please give feedback if you run into errors !!!!



## set up
1st install the needed packages, this get matplot, pandas working on the rpi3 and give you the needed software for the webserver flask

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install xsel xclip libxml2-dev libxslt-dev python-lxml python-h5py python-numexpr python-dateutil python-six python-tz python-bs4 python-html5lib python-openpyxl python-tables python-xlrd python-xlwt cython python-sqlalchemy python-xlsxwriter python-jinja2 python-boto python-gflags python-googleapi python-httplib2 python-zmq libspatialindex-dev
sudo pip install bottleneck rtree
sudo apt-get install python-numpy python-matplotlib python-mpltoolkits.basemap python-scipy python-sklearn python-statsmodels python-pandas
pip install flask
pip install codecs
```

2nd RUN interface.py 

```
sudo python OPC-N3-python-master/AQ/rpiWebServer/interface.py
```
If you have not changed any folder names it should all work fine and come up wtih the following
```
* Serving Flask app "interface" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 254-904-053
```

3rd Check the server

Put your RPI3 ip address in a webbrowser

SDS011 example, the this verstion will have PM1. PM2.5 and PM10

![RpiWeb](https://github.com/JarvisSan22/SDS-011-Python/blob/master/Screenshot_20191020-170102_Chrome.jpg)

If you dont now your RPI3 ip address, use an ip scanner or type the following in the terminal
```
ifconfig
```
It should in next to inet in the wlan0 settings.


