import sys

from PyQt5 import QtWebEngineWidgets, QtWidgets, QtCore, QtWebChannel,QtGui
import os
import random
import serial
import time
ser=serial.Serial('COM4',9600,timeout=1)
from math import sin, cos, sqrt, atan2
from datetime import datetime
import pandas as pd
import numpy as np
import math
class Backend(QtCore.QObject):
    pointChanged = QtCore.pyqtSignal(float, float)

    @QtCore.pyqtSlot(float,float)
    def pointClicked(self, x, y):
        self.pointChanged.emit(x, y)
        
class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        global servoangle,start_time
        global robotcommand,ccounter,flag,robotlocation,vialcnt
        vialcnt=0
        robotlocation="Robot A"
        flag=0
        ccounter=0
        start_time = time.time()
        robotcommand=""
        servoangle=0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        
        self.i1=QtWidgets.QLabel(self)
        self.i1.setGeometry(400,100,500,500)
        self.disp=QtGui.QPixmap("blackscreen.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)
        self.i2=QtWidgets.QLabel("----------------------------------",self)
        self.u1=QtWidgets.QLineEdit(self)
        
        self.u1.setVisible(0)
        self.frame = QtWidgets.QFrame(self)
        self.frame.resize(220,200)
        self.frame.setStyleSheet("background-image: url(logo.png);");
        self.frame.move(10,10)
        self.Resetbutton = QtWidgets.QPushButton("Reset",self)
        self.Resetbutton.clicked.connect(self.Reset)

        self.startbutton = QtWidgets.QPushButton("Start",self)
        self.startbutton.clicked.connect(self.startcommand)

        self.forcebutton = QtWidgets.QPushButton("Forced Stop",self)
        self.forcebutton.clicked.connect(self.stop)

        self.locationbutton = QtWidgets.QPushButton("Get Location",self)
        self.locationbutton.clicked.connect(self.location)
        
        self.waypointgpsbutton = QtWidgets.QPushButton("Save Waypoint",self)
        self.waypointgpsbutton.clicked.connect(self.waypointgps)

        self.waypointloadbutton = QtWidgets.QPushButton("Load Waypoint",self)
        self.waypointloadbutton.clicked.connect(self.waypointload)

        self.waypointverifybutton = QtWidgets.QPushButton("Verify",self)
        self.waypointverifybutton.clicked.connect(self.waypointverify)

        self.manualbutton = QtWidgets.QPushButton("Manual",self)
        self.manualbutton.clicked.connect(self.manualcon)
        #self.waypointgpsBbutton = QtWidgets.QPushButton("Save Waypoint B",self)
        #self.waypointgpsBbutton.clicked.connect(self.waypointgpsA)

        #self.waypointgpsCbutton = QtWidgets.QPushButton("Save Waypoint C",self)
        #self.waypointgpsCbutton.clicked.connect(self.waypointgpsA)
       
        font10 = QtGui.QFont("Helvetica", 10)
        self.l1=QtWidgets.QLabel("\n",self)
        
        self.l1.setFont(font10)
        self.l2=QtWidgets.QLabel("\n\n\n\n\n\n",self)
        self.vialselectlist = QtWidgets.QComboBox(self)
        self.vialselectlist.addItems(["Vial A","Vial B","Vial C","Vial D","Vial E","Vial F"])
        self.vialselectlist.currentIndexChanged.connect(self.vialselect)
        self.vialselectlist.setCurrentIndex(0)
        self.vialselectlist.setVisible(0)
        self.robotselectlist = QtWidgets.QComboBox(self)
        self.robotselectlist.addItems(["Robot A","Robot B","Robot C"])
        self.robotselectlist.currentIndexChanged.connect(self.robotselect)
        self.robotselectlist.setCurrentIndex(0)
        
        ######################################
        self.map_view = map_view = QtWebEngineWidgets.QWebEngineView()

        backend = Backend(self)
        backend.pointChanged.connect(self.onPointChanged)
        channel = QtWebChannel.QWebChannel(self)
        channel.registerObject('backend', backend)
        map_view.page().setWebChannel(channel)

        file = QtCore.QDir.current().absoluteFilePath("index.html")
        map_view.load(QtCore.QUrl.fromLocalFile(file))
       
        ######################################


        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContentsMargins(50, 50, 50, 50)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QHBoxLayout(central_widget)

        button_container = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(button_container)
        vlay.setSpacing(20)
        vlay.addStretch()
        vlay.addWidget(self.l2)
        vlay.addWidget(self.l1)
        vlay.addWidget(self.vialselectlist)
        vlay.addWidget(self.startbutton)
        vlay.addWidget(self.Resetbutton)
        vlay.addWidget(self.forcebutton)
        vlay.addWidget(self.robotselectlist)
        vlay.addWidget(self.locationbutton)
        vlay.addWidget(self.waypointgpsbutton)
        vlay.addWidget(self.waypointloadbutton)
        vlay.addWidget(self.waypointverifybutton)
        vlay.addWidget(self.i2)
        vlay.addWidget(self.u1)
        vlay.addWidget(self.manualbutton)
        vlay.addStretch()
        lay.addWidget(button_container)
        lay.addWidget(self.map_view, stretch=1)

        
        
        
        self.manualbutton.setVisible(0)
        self.setGeometry(300, 300, 1200, 800)
        self.show()
    @QtCore.pyqtSlot(float,float)
    
    def onPointChanged(self, x, y):
        global robotlocation,ccounter,vialcnt
        
        global servoangle,robotcommand,ccounter,lat,lng,heading
        if vialcnt==0:
            servoangle=0
        elif vialcnt==1:
            servoangle=60
        elif vialcnt==2:
            servoangle=90
        elif vialcnt==3:
            servoangle=120
        elif vialcnt==4:
            servoangle=150
        elif vialcnt==5:
            servoangle=180
        vialcnt=vialcnt+1
        if vialcnt<7:
            print(x, y)
            print(servoangle)
            ccounter=ccounter+15
            print(ccounter)
            R = 6373.0
            lon1=float(lng)
            lat1=float(lat)
            #lon1=0
            #lat1=0
            heading=300
            lon2=float(y)
            lat2=float(x)
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            print(distance)
            robotforward=int(500*distance)

            dLon = (lon2 - lon1)
            xang = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
            yang = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
            brng = atan2(xang,yang)
            brng = math.degrees(brng)
            anglediff=float(heading)-float(brng)
            print(anglediff)
            
            if robotlocation=="Robot A":
                if anglediff<0:
                    robotrotation="YA2,"+str(int(anglediff*10))
                elif anglediff>=0:
                    robotrotation="YA3,"+str(int(anglediff*10))
                robotcommand=robotcommand+str(robotrotation)+","+"YA1,"+str(robotforward)+","+"YE,"+str(servoangle)+","+"YB1,1500,YC,3000,YD,30000,YB2,1500,YF,"
                print(robotcommand)
            elif robotlocation=="Robot B":
                if anglediff<0:
                    robotrotation="A2,"+str(int(anglediff*10))
                elif anglediff>=0:
                    robotrotation="A3,"+str(int(anglediff*10))
                robotcommand=robotcommand+str(robotrotation)+","+"A1,"+str(robotforward)+","+"E,"+str(servoangle)+","+"B1,1500,D,3000,C,30000,B2,1500,F,"
                print(robotcommand)
            elif robotlocation=="Robot C":
                if anglediff<0:
                    robotrotation="XA2,"+str(int(anglediff*10))
                elif anglediff>=0:
                    robotrotation="XA3,"+str(int(anglediff*10))
                robotcommand=robotcommand+str(robotrotation)+","+"XA1,"+str(robotforward)+","+"XE,"+str(servoangle)+","+"XB2,1500,XC,3000,XD,30000,XB1,1500,XF,"
                    
                print(robotcommand)
            lat=lat1
            lon1=lon1
        else:
            print("Waypoint Exceed")
    def manualcon(self):
        print("Transmitting Data..")
        inpdata=str(self.u1.text())
        cmd=inpdata.split(",")[0]+","
        ang=inpdata.split(",")[1]
        ser.write("Clear,".encode())
        time.sleep(2)
        
        datasent="S1,15,"+cmd+str(ang)+","+cmd+str(ang)+","+cmd+str(ang)+","+cmd+str(ang)+","+cmd+str(ang)+","+cmd+str(ang)+",YD,3000"+","+"N,"
        print(str(datasent))
        ser.write(datasent.encode())
        time.sleep(2)
        
        for i in range(1):
            ser.write("Display,".encode())
            time.sleep(1)
            sensordata=ser.readline()
            lensensor=len(sensordata)
            print(sensordata)
            time.sleep(1)
        for i in range(40):
                sensordata=ser.readline()
                if len(sensordata)<3:
                    break
                print("-")
        print("Serial Data Cleared.")
        
        datasend="End,15,"+str("1")+","
        ser.write(datasend.encode())
        time.sleep(2)
    def location(self):
        global robotlocation,lat,lng,heading
        page = self.map_view.page()
        if robotlocation=="Robot A":
            try:
                ser.write("Location,YF,".encode())
                time.sleep(1)
                sensordata=ser.readline()
                print(sensordata)
                sensordata=str(sensordata)
                robottarget=sensordata.split(",")[0]
                robottarget=robottarget.split("'")[1]
                lat=sensordata.split(",")[1]
                lng=sensordata.split(",")[2]
                heading=sensordata.split(",")[3]
                #lat=14.685148884554879
                #lng=120.54684162139894
                print(robottarget)
                print(lat)
                print(lat)
                print(lng)
                print(heading)
                page.runJavaScript("robotgpsA("+str(lat)+","+str(lng)+")")
                time.sleep(1)
            except:
                print("A not detected.")
        elif robotlocation=="Robot B":
            try:
                ser.write("LocationB,F,".encode())
                time.sleep(1)
                sensordata=ser.readline()
                print(sensordata)
                sensordata=str(sensordata)
                lat=sensordata.split(",")[1]
                lng=sensordata.split(",")[2]
                heading=sensordata.split(",")[3]
                #lat=14.685148884554879
                #lng=120.54684162139894
                #heading=0
                print(lat)
                print(lng)
                print(heading)
                page.runJavaScript("robotgpsB("+str(lat)+","+str(lng)+")")
                time.sleep(1)
            except:
                print("B not detected.")
        elif robotlocation=="Robot C":
            try:
                ser.write("LocationC,XF,".encode())
                time.sleep(1)
                sensordata=ser.readline()
                print(sensordata)
                sensordata=str(sensordata)
                
                lat=sensordata.split(",")[1]
                lng=sensordata.split(",")[2]
                heading=sensordata.split(",")[3]
                #heading=0
                #lat=14.685148884554879
                #lng=120.54684162139894
                print(lat)
                print(lng)
                print(heading)
                page.runJavaScript("robotgpsC("+str(lat)+","+str(lng)+")")
                time.sleep(1)
            except:
                print("C not detected.")
        
    def startcommand(self):
        global flag
        flag=1
        
        f = open("robotAcommand.txt", "r")
        datatransmit=str(f.read())
        datalength=int(datatransmit.split(",")[0])
        print(datalength)
        f.close()
        time.sleep(1)
        datasend="End,15,"+str(datalength)+","
        ser.write(datasend.encode())
        time.sleep(2)

        f = open("robotBcommand.txt", "r")
        datatransmit=str(f.read())
        datalength=int(datatransmit.split(",")[0])
        print(datalength)
        f.close()
        time.sleep(2)
        datasend="EndB,15,"+str(datalength)+","
        ser.write(datasend.encode())
        time.sleep(1)
        
        f = open("robotCcommand.txt", "r")
        datatransmit=str(f.read())
        datalength=int(datatransmit.split(",")[0])
        print(datalength)
        f.close()
        time.sleep(2)
        datasend="EndC,15,"+str(datalength)+","
        ser.write(datasend.encode())
        time.sleep(1)

        for i in range(120):
            sensordata=ser.readline()
            if len(sensordata)<3:
                break
            print("-")
    def stop(self):
        global flag
        flag=0
    def Reset(self):
        global robotcommand,flag,ccounter,robotlocation
        ccounter=0
        flag=0
        robotcommand=""
        page = self.map_view.page()
        page.runJavaScript("Reset()")
        if robotlocation=="Robot A":
            ser.write("Clear,".encode())
        elif robotlocation=="Robot B":
            ser.write("ClearB,".encode())
        elif robotlocation=="Robot C":
            ser.write("ClearC,".encode())
        
    def waypointverify(self):
        global robotlocation
        self.i2.setText("Verifying Data..")    
        QtCore.QCoreApplication.processEvents()
        verflag=0
        if robotlocation=="Robot A":
            f = open("robotAcommand.txt", "r")
            datatransmit=str(f.read())
            datalength=int(datatransmit.split(",")[0])/15
            print(datalength)
            for i in range(int(datalength)):
                ser.write("Display,".encode())
                time.sleep(1)
                sensordata=ser.readline()
                lensensor=len(sensordata)
                print(sensordata)
                time.sleep(1)
                if len(sensordata)<50:
                     self.i2.setText("Verification failed. Please retry.")    
                     QtCore.QCoreApplication.processEvents()
                     verflag=1
        elif robotlocation=="Robot B":
            f = open("robotBcommand.txt", "r")
            datatransmit=str(f.read())
            datalength=int(datatransmit.split(",")[0])/15
            print(datalength)
            for i in range(int(datalength)):
                ser.write("DisplayB,".encode())
                time.sleep(1)
                sensordata=ser.readline()
                lensensor=len(sensordata)
                print(sensordata)
                time.sleep(1)
                if len(sensordata)<50:
                    self.i2.setText("Verification failed. Please retry.")    
                    QtCore.QCoreApplication.processEvents()
                    verflag=1
        elif robotlocation=="Robot C":
            f = open("robotCcommand.txt", "r")
            datatransmit=str(f.read())
            datalength=int(datatransmit.split(",")[0])/15
            print(datalength)
            for i in range(int(datalength)):
                ser.write("DisplayC,".encode())
                time.sleep(1)
                sensordata=ser.readline()
                lensensor=len(sensordata)
                print(sensordata)
                time.sleep(1)
                if len(sensordata)<50:
                    self.i2.setText("Verification failed. Please retry.")    
                    QtCore.QCoreApplication.processEvents()
                    verflag=1
        if verflag==0:
             self.i2.setText("Verification successful.")    
             QtCore.QCoreApplication.processEvents()
        for i in range(40):
                sensordata=ser.readline()
                if len(sensordata)<3:
                    break
                print("-")
        print("Serial Data Cleared.")
    def waypointload(self):
        global robotlocation
        
        print("Transmitting Data..")
        self.i2.setText("Transmitting Data..")    
        QtCore.QCoreApplication.processEvents()
        if robotlocation=="Robot A":
            ser.write("Clear,".encode())
            time.sleep(2)
            f = open("robotAcommand.txt", "r")
            datatransmit=str(f.read())
            datalength=int(datatransmit.split(",")[0])/15
            print(datalength)
            print(datatransmit)
            f.close()
            #f = open("robotAcommand.txt", "w")
            #f.write("")
            #f.close()
            #ser.write(str(datalength).encode())
            
            j=0    
            for i in range(int(datalength)):
                cdata1=str(datatransmit.split(",")[j+1]+",")
                cdata2=str(datatransmit.split(",")[j+2]+",")
                cdata3=str(datatransmit.split(",")[j+3]+",")
                cdata4=str(datatransmit.split(",")[j+4]+",")
                cdata5=str(datatransmit.split(",")[j+5]+",")
                cdata6=str(datatransmit.split(",")[j+6]+",")
                cdata7=str(datatransmit.split(",")[j+7]+",")
                cdata8=str(datatransmit.split(",")[j+8]+",")
                cdata9=str(datatransmit.split(",")[j+9]+",")
                cdata10=str(datatransmit.split(",")[j+10]+",")
                cdata11=str(datatransmit.split(",")[j+11]+",")
                cdata12=str(datatransmit.split(",")[j+12]+",")
                cdata13=str(datatransmit.split(",")[j+13]+",")
                cdata14=str(datatransmit.split(",")[j+14]+",")
                cdata15=str(datatransmit.split(",")[j+15]+",")
                j=j+15
                if i==0:
                    datasent="S1,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==1:
                    datasent="S2,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==2:
                    datasent="S3,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==3:
                    datasent="S4,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==4:
                    datasent="S5,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==5:
                    datasent="S6,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                print(str(datasent))
                ser.write(datasent.encode())
                time.sleep(1)

            
            
            ser.write(datatransmit.encode())
            time.sleep(2)

            
            #if lensensor<5:
            #    print("Retry. Data not loaded")
            #else:
            #    print("Robot A data loaded successfully.")
            #print(sensordata)
        elif robotlocation=="Robot B":
            ser.write("ClearB,".encode())
            time.sleep(2)
            f = open("robotBcommand.txt", "r")
            datatransmit=str(f.read())
            datalength=int(datatransmit.split(",")[0])/15
            print(datalength)
            print(datatransmit)
            f.close()
            #f = open("robotAcommand.txt", "w")
            #f.write("")
            #f.close()
            #ser.write(str(datalength).encode())
            j=0    
            for i in range(int(datalength)):
                cdata1=str(datatransmit.split(",")[j+1]+",")
                cdata2=str(datatransmit.split(",")[j+2]+",")
                cdata3=str(datatransmit.split(",")[j+3]+",")
                cdata4=str(datatransmit.split(",")[j+4]+",")
                cdata5=str(datatransmit.split(",")[j+5]+",")
                cdata6=str(datatransmit.split(",")[j+6]+",")
                cdata7=str(datatransmit.split(",")[j+7]+",")
                cdata8=str(datatransmit.split(",")[j+8]+",")
                cdata9=str(datatransmit.split(",")[j+9]+",")
                cdata10=str(datatransmit.split(",")[j+10]+",")
                cdata11=str(datatransmit.split(",")[j+11]+",")
                cdata12=str(datatransmit.split(",")[j+12]+",")
                cdata13=str(datatransmit.split(",")[j+13]+",")
                cdata14=str(datatransmit.split(",")[j+14]+",")
                cdata15=str(datatransmit.split(",")[j+15]+",")
                j=j+15
                if i==0:
                    datasent="S1B,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==1:
                    datasent="S2B,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==2:
                    datasent="S3B,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==3:
                    datasent="S4B,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==4:
                    datasent="S5B,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==5:
                    datasent="S6B,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                print(str(datasent))
                ser.write(datasent.encode())
                time.sleep(1)


            
            
            ser.write(datatransmit.encode())
            time.sleep(2)
        elif robotlocation=="Robot C":
            ser.write("ClearC,".encode())
            time.sleep(2)
            f = open("robotCcommand.txt", "r")
            datatransmit=str(f.read())
            datalength=int(datatransmit.split(",")[0])/15
            print(datalength)
            print(datatransmit)
            f.close()
            #f = open("robotAcommand.txt", "w")
            #f.write("")
            #f.close()
            #ser.write(str(datalength).encode())
            j=0    
            for i in range(int(datalength)):
                cdata1=str(datatransmit.split(",")[j+1]+",")
                cdata2=str(datatransmit.split(",")[j+2]+",")
                cdata3=str(datatransmit.split(",")[j+3]+",")
                cdata4=str(datatransmit.split(",")[j+4]+",")
                cdata5=str(datatransmit.split(",")[j+5]+",")
                cdata6=str(datatransmit.split(",")[j+6]+",")
                cdata7=str(datatransmit.split(",")[j+7]+",")
                cdata8=str(datatransmit.split(",")[j+8]+",")
                cdata9=str(datatransmit.split(",")[j+9]+",")
                cdata10=str(datatransmit.split(",")[j+10]+",")
                cdata11=str(datatransmit.split(",")[j+11]+",")
                cdata12=str(datatransmit.split(",")[j+12]+",")
                cdata13=str(datatransmit.split(",")[j+13]+",")
                cdata14=str(datatransmit.split(",")[j+14]+",")
                cdata15=str(datatransmit.split(",")[j+15]+",")
                j=j+15
                if i==0:
                    datasent="S1C,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==1:
                    datasent="S2C,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==2:
                    datasent="S3C,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==3:
                    datasent="S4C,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==4:
                    datasent="S5C,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                elif i==5:
                    datasent="S6C,15,"+cdata1+cdata2+cdata3+cdata4+cdata5+cdata6+cdata7+cdata8+cdata9+cdata10+cdata11+cdata12+cdata13+cdata14+cdata15
                print(str(datasent))
                ser.write(datasent.encode())
                time.sleep(1)


            
            
            ser.write(datatransmit.encode())
            time.sleep(2)    
        self.i2.setText("Done.")
    def waypointgps(self):
        global robotlocation,robotcommand,ccounter,vialcnt
        
        if robotlocation=="Robot A":
           commandtransmission=str(ccounter)+","+(robotcommand)         
           print(commandtransmission)
           f = open("robotAcommand.txt", "w")
           f.write(commandtransmission)
           f.close()
           
           page = self.map_view.page()
           page.runJavaScript("Reset()")
        elif robotlocation=="Robot B":
           commandtransmission=str(ccounter)+","+(robotcommand)         
           print(commandtransmission)
           f = open("robotBcommand.txt", "w")
           f.write(commandtransmission)
           f.close()
           
           page = self.map_view.page()
           page.runJavaScript("Reset()")
        elif robotlocation=="Robot C":
           commandtransmission=str(ccounter)+","+(robotcommand)         
           print(commandtransmission)
           f = open("robotCcommand.txt", "w")
           f.write(commandtransmission)
           f.close()
           
           page = self.map_view.page()
           page.runJavaScript("Reset()") 
        robotcommand=""
        ccounter=0
        vialcnt=0

        
    def vialselect(self,vialselectflag):
        global vialselectsel,servoangle
        vialselectsel=self.vialselectlist.itemText(vialselectflag)
        #print(vialselectsel)
        if vialselectsel=="Vial A":
            servoangle=30
            print("Servo: 30")
        elif vialselectsel=="Vial B":
            servoangle=60
            print("Servo: 60")
        elif vialselectsel=="Vial C":
            servoangle=90
            print("Servo: 90")
        elif vialselectsel=="Vial D":
            servoangle=120
            print("Servo: 120")
        elif vialselectsel=="Vial E":
            servoangle=150
            print("Servo: 150")
        elif vialselectsel=="Vial F":
            servoangle=180
            print("Servo: 180")

    def robotselect(self,robotselectflag):
        global robotselectsel,robotlocation
        robotselectsel=self.robotselectlist.itemText(robotselectflag)

        if robotselectsel=="Robot A":
            robotlocation="Robot A"
        elif robotselectsel=="Robot B":
            robotlocation="Robot B"
        elif robotselectsel=="Robot C":
            robotlocation="Robot C"
    def Loop(self):
        global elapsed_time,start_time,flag
        elapsed_time=time.time()-start_time
        
        if elapsed_time>=2 and flag==1:
            
            start_time=time.time()
            try:
                
                page = self.map_view.page()
                sensordata=ser.readline()
                sensordata=str(sensordata)
                robottarget=sensordata.split(",")[0]
                robottarget=robottarget.split("'")[1]
                print(sensordata)
                print(robottarget) 
                lat=sensordata.split(",")[1]
                lng=sensordata.split(",")[2]
                heading=sensordata.split(",")[3]
                #lat=14.685148884554879
                #lng=120.54684162139894
                print(lat)
                print(lng)
                print(heading)
                if robottarget=="ZA":
                    page.runJavaScript("robotgpsA("+str(lat)+","+str(lng)+")")
                    pathtarget="robotAlog.csv"
                    now = datetime.now()
                    logdatetime=now.strftime("%d/%m/%Y %H:%M:%S")
                    if os.path.exists(pathtarget):
                     
                         df=pd.read_csv(pathtarget,names=['DateTime','Latitude','Longitude'],skiprows=1)
                         np_df = df.as_matrix()
                         df = df.append({'DateTime':logdatetime, 'Latitude':str(lat), 'Longitude':str(lng)}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                    else:
                         
                         columns = ['DateTime','Latitude','Longitude']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         
                         df = df.append({'DateTime':logdatetime, 'Latitude':str(lat), 'Longitude':str(lng)}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         
                elif robottarget=="ZB":
                    page.runJavaScript("robotgpsB("+str(lat)+","+str(lng)+")")
                    pathtarget="robotBlog.csv"
                    now = datetime.now()
                    logdatetime=now.strftime("%d/%m/%Y %H:%M:%S")
                    if os.path.exists(pathtarget):
                     
                         df=pd.read_csv(pathtarget,names=['DateTime','Latitude','Longitude'],skiprows=1)
                         np_df = df.as_matrix()
                         df = df.append({'DateTime':logdatetime, 'Latitude':str(lat), 'Longitude':str(lng)}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                    else:
                         
                         columns = ['DateTime','Latitude','Longitude']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         
                         df = df.append({'DateTime':logdatetime, 'Latitude':str(lat), 'Longitude':str(lng)}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                elif robottarget=="ZC":
                    page.runJavaScript("robotgpsC("+str(lat)+","+str(lng)+")")
                    pathtarget="robotClog.csv"
                    now = datetime.now()
                    logdatetime=now.strftime("%d/%m/%Y %H:%M:%S")
                    if os.path.exists(pathtarget):
                     
                         df=pd.read_csv(pathtarget,names=['DateTime','Latitude','Longitude'],skiprows=1)
                         np_df = df.as_matrix()
                         df = df.append({'DateTime':logdatetime, 'Latitude':str(lat), 'Longitude':str(lng)}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                    else:
                         
                         columns = ['DateTime','Latitude','Longitude']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         
                         df = df.append({'DateTime':logdatetime, 'Latitude':str(lat), 'Longitude':str(lng)}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                    
                
                    
                    
                    
            except:
                print("No data received.")
        QtCore.QCoreApplication.processEvents()
def main():

    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
