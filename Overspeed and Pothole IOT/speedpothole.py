import time
import sys, os
from PyQt4 import QtGui, QtCore
import Adafruit_ADXL345
import pandas as pd
import numpy as np
import sys
import RPi.GPIO as GPIO
from time import sleep
import urllib2
import serial
import string
import pynmea2
import math
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)    
GPIO.setup(17, GPIO.IN)    
class Main(QtGui.QMainWindow): 
    def __init__(self): 
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,gpsflag,start_time,acceflag
        acceflag=1
        start_time = time.time()
        flag=0
        gpsflag=0
        centralwidget = QtGui.QWidget(self) 

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.startbutton = QtGui.QPushButton("Start",self)
        self.startbutton.clicked.connect(self.start)
        self.startbutton.move(40,100)
        
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(150,100)
        self.setGeometry(50,50,300,160)
    def start(self):
        global flag
        flag=1
    def stop(self):
        global flag
        flag=0
    def Loop(self):
        global flag,gpsflag,start_time,acceflag,lat1,lat2,lon1,lon2
        
        if flag==1:
            elapsed_time = time.time() - start_time
                #print "elapse_time="+str(elapsed_time)
            try:
                ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
                data = ser.readline()
                #print data
                if data[0:6] == '$GPGGA':
                    
                  msg = pynmea2.parse(data)
  
                  latval = msg.latitude
                  concatlat = "lat:" + str(latval)
                  print concatlat

                  longval = msg.longitude
                  concatlong = "long:"+ str(longval)
                  print concatlong
                  x1 = latval
                  x2 = longval
                  if GPIO.input(17)==True:
                      x6=1
                  else:
                      x6=0
                  #print "gpsflag: "+str(gpsflag)
                  if gpsflag==0:
                        gpsflag=1
                        print "gpsflag: "+str(gpsflag)
                        lat1=latval
                        lon1=longval
                        #print lat1
                        print "##############################"
                  elif gpsflag==1 and elapsed_time>=5:
                        start_time = time.time()
                        lat2=latval
                        lon2=longval
                        radius = 6371 #km
                        print "gpsflag: "+str(gpsflag)
                        #print lat1
                        #print lat2
                        #print "##############################"
                        dlat = math.radians(lat2-lat1)
                        dlon = math.radians(lon2-lon1)
                        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                        d = radius * c
                        v=(float(d)*3600)/float(elapsed_time)
                        print "Speed: "+str(v)+" km/h"
                        gpsflag=0
                        #print "gpsflag: "+str(gpsflag)
                        #v=50 #Dummy Data
                    
                        if v>=11 and v<=20: #km/h
                                for i in range(3000):
                                    print "Loop: "+str(i)
                                    for i in range(3):
                                        
                                        accel = Adafruit_ADXL345.ADXL345()
                                        x, y, z = accel.read()
                                        if acceflag==1:
                                           pointA=x
                                           acceflag=2
                                        elif acceflag==2:
                                           pointB=x
                                           acceflag=3
                                        elif acceflag==3:
                                           pointC=x
                                           acceflag=1
                                    cycleA=pointA-pointB #+
                                    cycleB=pointB-pointC #-
                                    print "cycleA="+str(cycleA)
                                    print "cycleB="+str(cycleB)
                                    difference=abs(cycleB)
                                    differenceA=abs(cycleA)
                                    if cycleA<0 and cycleB>=0 and difference>=30 or differenceA>=30:
                                       print "Pothole Moderate Level"
                                       x3=1
                                       break
                                    elif cycleA<0 and cycleB>=0 and difference>=30 or differenceA>=30:
                                       print "Pothole High Level"
                                       x3=2
                                       break
                                    else:
                                       
                                       x3=3
                                #print('X={0}, Y={1}, Z={2}'.format(x, y, z))
                                pathtarget="/home/pi/Share/accedata.csv"
                                if os.path.exists(pathtarget):
                                         
                                         df=pd.read_csv(pathtarget,names=['X','Y','Z'],skiprows=1)
                                         np_df = df.as_matrix()
                                         df = df.append({'X':x, 'Y':y, 'Z':z}, ignore_index=True)
                                         df.to_csv(pathtarget,  index = False)
                                         #print df
                                else:
                                     
                                     columns = ['X','Y','Z']
                                     df = pd.DataFrame(columns=columns)
                                     np_df = df.as_matrix()
                                     
                                     df = df.append({'X':x, 'Y':y, 'Z':z}, ignore_index=True)
                                     df.to_csv(pathtarget,  index = False)
                                     #print df
                                x1=lat2
                                x2=lon2
                                
                                x4=v #Velocity
                                x5=10000 #Vehicle ID
                     
                                f = urllib2.urlopen("https://api.thingspeak.com/update?api_key=7FV28MU6PT4ESS4I&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s" % (x1,x2,x3,x4,x5,x6))  
                                f.close()
                        elif v<11: #km/h
                                for i in range(3000):
                                    print "Loop: "+str(i)
                                    for i in range(3):
                                        
                                        accel = Adafruit_ADXL345.ADXL345()
                                        x, y, z = accel.read()
                                        if acceflag==1:
                                           pointA=x
                                           acceflag=2
                                        elif acceflag==2:
                                           pointB=x
                                           acceflag=3
                                        elif acceflag==3:
                                           pointC=x
                                           acceflag=1
                                    cycleA=pointA-pointB #+
                                    cycleB=pointB-pointC #-
                                    print "cycleA="+str(cycleA)
                                    print "cycleB="+str(cycleB)
                                    difference=abs(cycleB)
                                    differenceA=abs(cycleA)
                                    if cycleA<0 and cycleB>=0 and difference>=50 or differenceA>=50:
                                       print "Pothole Moderate Level"
                                       x3=1
                                       break
                                    elif cycleA<0 and cycleB>=0 and difference>=50 or differenceA>=50:
                                       print "Pothole High Level"
                                       x3=2
                                       break
                                    else:
                                       
                                       x3=3
                                #print('X={0}, Y={1}, Z={2}'.format(x, y, z))
                                pathtarget="/home/pi/Share/accedata.csv"
                                if os.path.exists(pathtarget):
                                         
                                         df=pd.read_csv(pathtarget,names=['X','Y','Z'],skiprows=1)
                                         np_df = df.as_matrix()
                                         df = df.append({'X':x, 'Y':y, 'Z':z}, ignore_index=True)
                                         df.to_csv(pathtarget,  index = False)
                                         #print df
                                else:
                                     
                                     columns = ['X','Y','Z']
                                     df = pd.DataFrame(columns=columns)
                                     np_df = df.as_matrix()
                                     
                                     df = df.append({'X':x, 'Y':y, 'Z':z}, ignore_index=True)
                                     df.to_csv(pathtarget,  index = False)
                                     #print df
                                x1=lat2
                                x2=lon2
                                
                                x4=v #Velocity
                                x5=10000 #Vehicle ID
                         
                                f = urllib2.urlopen("https://api.thingspeak.com/update?api_key=7FV28MU6PT4ESS4I&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s" % (x1,x2,x3,x4,x5,x6))  
                                f.close()
                                print "################## Pothole Speed #################"
                        else:
                                x1=lat2
                                x2=lon2
                                x3=0
                                x4=v #Velocity
                                x5=10000 #Vehicle ID
                         
                                f = urllib2.urlopen("https://api.thingspeak.com/update?api_key=7FV28MU6PT4ESS4I&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s" % (x1,x2,x3,x4,x5,x6))  
                                f.close()

                               
            except:
                print "No Signal"
            
            
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
