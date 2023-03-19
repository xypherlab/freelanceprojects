from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import serial
ser=serial.Serial('COM4',9600,timeout=1)
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,start_time,red,green,blue
        red=0
        green=0
        blue=0
        start_time = time.time()
        flag=0
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.d1=QtGui.QLabel("Sensor: ",self)
        self.d1.move(120,50)
        self.d2=QtGui.QLabel("--",self)
        self.d2.move(190,50)
        #Analyze Button
        self.analyzebutton = QtGui.QPushButton("Change",self)
        self.analyzebutton.clicked.connect(self.start)
        self.analyzebutton.move(70,110)
        #
        #Stop Button
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(210,110)
        #
        self.sl1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sl1.setMinimum(0)
        self.sl1.setMaximum(255)
        self.sl1.setValue(20)
        self.sl1.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl1.setTickInterval(1)
        self.sl1.valueChanged.connect(self.greenvalue)
        self.sl1.move(160,170)

        self.sl2 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sl2.setMinimum(0)
        self.sl2.setMaximum(255)
        self.sl2.setValue(20)
        self.sl2.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl2.setTickInterval(1)
        self.sl2.valueChanged.connect(self.redvalue)
        self.sl2.move(160,210)

        self.sl3 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sl3.setMinimum(0)
        self.sl3.setMaximum(255)
        self.sl3.setValue(20)
        self.sl3.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl3.setTickInterval(1)
        self.sl3.valueChanged.connect(self.bluevalue)
        self.sl3.move(160,250)
        
        self.setGeometry(0,20,320,400)
    def redvalue(self):
       global red,green,blue
       red = self.sl2.value()
    def greenvalue(self):
       global green
       green = self.sl1.value()
    def bluevalue(self):
       global blue
       blue= self.sl3.value()
       
    def start(self):
        global flag,start_time
        #flag=1
        #start_time = time.time()
        colorout=str(red)+","+str(green)+","+str(blue)
        ser.write(colorout)
        print colorout
    def stop(self):
        global flag
        flag=0
        
        
 
    def Loop(self):
        global flag,start_time,red,green,blue
        delay=1
        elapsed_time=time.time()-start_time
            
        #if flag==1 and elapsed_time>=delay:
        #if flag==1:   
            #colorout=str(red)+","+str(green)+","+str(blue)
            #ser.write(colorout)
            #print colorout
            #start_time = time.time()
      
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
