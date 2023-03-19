import sys
from PyQt4 import QtGui, QtCore
import subprocess
#import serial
import numpy as np
import os.path
import time
import pyqtgraph as pg
#ser=serial.Serial('COM4',9600,timeout=1)
import bluetooth 
class Main(QtGui.QMainWindow):
 
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()
 
    def initUI(self):
        global blueflag,start_time,x,y,z,tic
        tic = time.clock()
        x=0
        y=0
        z=0
        start_time = time.time()
        blueflag=0
        centralwidget = QtGui.QWidget(self)
        print "Searching for devices..."
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.eeglabelA= QtGui.QLabel("EEG A: ",self)
        self.eeggradeA = QtGui.QLabel("----",self)
        self.eeglabelA.resize(135,35)
        self.eeggradeA.resize(135,35)
        self.eeggradeA.move(260,15)
        self.eeglabelA.move(150,15)
        
        self.eeglabelB= QtGui.QLabel("EEG B: ",self)
        self.eeggradeB = QtGui.QLabel("----",self)
        self.eeglabelB.resize(135,35)
        self.eeggradeB.resize(135,35)
        self.eeggradeB.move(260,220)
        self.eeglabelB.move(150,220)
        
        self.eeglabelC= QtGui.QLabel("EEG C: ",self)
        self.eeggradeC = QtGui.QLabel("----",self)
        self.eeglabelC.resize(135,35)
        self.eeggradeC.resize(135,35)
        self.eeggradeC.move(260,420)
        self.eeglabelC.move(150,420)
        
        self.readingbutton = QtGui.QPushButton("Reading",self)
        self.readingbutton.clicked.connect(self.reading)
        self.readingbutton.move(400,650)
        #
        self.plotA = pg.PlotWidget(self)
        self.plotA.resize(700,150)
        self.plotA.move(100,50)
        self.plotA.setXRange(0, 9, padding=0)
        self.plotB = pg.PlotWidget(self)
        self.plotB.resize(700,150)
        self.plotB.move(100,250)
        self.plotB.setXRange(0, 9, padding=0)
        self.plotC = pg.PlotWidget(self)
        self.plotC.resize(700,150)
        self.plotC.move(100,450)
        self.plotC.setXRange(0, 9, padding=0)
        self.dataA =[]
        self.curveA = self.plotA.getPlotItem().plot()
        self.dataB =[]
        self.curveB = self.plotB.getPlotItem().plot()
        self.dataC =[]    
        self.curveC = self.plotC.getPlotItem().plot()
        #
        self.setGeometry(50,50, 960,760) #Size of Screen
        print ""
        nearby_devices = bluetooth.discover_devices()
        num = 0
        print "Select your device by entering its coresponding number..."
        for i in nearby_devices:
                num+=1
                print num , ": " , bluetooth.lookup_name( i )


        selection = input("> ") - 1
        print "You have selected", bluetooth.lookup_name(nearby_devices[selection])
        bd_addr = nearby_devices[selection]

        port = 1 
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((bd_addr, port))
        s.settimeout(1)

   
            
    def reading(self):
            global blueflag
            blueflag=1
            #ser.write("T,")
            #time.sleep(1)
            #eegval=ser.readline()
            #e0=float(eegval.split(",")[0])
            #e1=float(eegval.split(",")[1])
            #e2=float(eegval.split(",")[2])
            #print str(e0)+","+str(e1)+","+str(e2)
            #self.eeggradeA.setText(str(e0))
            #self.eeggradeB.setText(str(e1))
            #self.eeggradeC.setText(str(e2))
    def Loop(self):
        global blueflag,x,y,z,tic,start_time
        toc = time.clock()
        timer=toc-tic
        tref=2
        
        data=""
        if blueflag==1:
            x=0
            
            try:
                elapsed_time=time.time()-start_time
                while x==0 and elapsed_time>=1:
                    print elapsed_time    
                    start_time = time.time()
                    newdata = s.recv(8096)
                    data=data+newdata
                    substring = "&"
                    
                    if substring in data:
                        #print "Data: "+str(data)
                        dA=float(data.split(",")[0])
                        dB=float(data.split(",")[1])*float(4.888)
                        dC=float(data.split(",")[2])*float(4.888)
                        x=x+1
                        z=z+1
                        if x>10 and z<10:
                            y=y+10
                            self.plotA.setXRange(0+y, 10+y, padding=0)
                            self.plotB.setXRange(0+y, 10+y, padding=0)
                            self.plotC.setXRange(0+y, 10+y, padding=0)
                            
                            x=0
                        if z==10:
                            self.dataA =[]
                            self.dataB =[]
                            self.dataC =[]
                            self.plotA.setXRange(0, 9, padding=0)
                            self.plotB.setXRange(0, 9, padding=0)
                            self.plotC.setXRange(0, 9, padding=0)
                            
                            z=0
                            y=0
                        
                        self.dataA.append(dA)
                        self.curveA.setData(self.dataA)
                        self.dataB.append(dB)
                        self.curveB.setData(self.dataB)
                        self.dataC.append(dC)
                        self.curveC.setData(self.dataC)
                        self.eeggradeA.setText(str(dA)+" mV")
                        self.eeggradeB.setText(str(dB)+" mV")
                        self.eeggradeC.setText(str(dC)+" mV")
                        print dA
                        print dB
                        print dC
                        data=""
                        x=1
                        
            except:
                 dump=0
        

def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

        
