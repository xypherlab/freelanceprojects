from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag
        flag=0
        
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
       
        #Head Title
        font = QtGui.QFont("Times", 24)
        self.t1=QtGui.QLabel("QR Locker System",self)
        self.t1.setFont(font)
        self.t1.move(160,10)
        self.t1.resize(350,50)
        #
        #Head Title
        font = QtGui.QFont("Times", 16)
        self.t2=QtGui.QLabel("Cost: ",self)
        self.t2.setFont(font)
        self.t2.move(560,60)
        self.t2.resize(350,50)
        #
        #Head Title
        font = QtGui.QFont("Times", 16)
        self.t3=QtGui.QLabel("Duration: ",self)
        self.t3.setFont(font)
        self.t3.move(560,110)
        self.t3.resize(350,50)
        #
        
        #Scan Button
        self.scanbutton = QtGui.QPushButton("Scan",self)
        self.scanbutton.clicked.connect(self.scan)
        self.scanbutton.move(150,280)
        #
        #Generate Button
        self.generatebutton = QtGui.QPushButton("Generate QR Code",self)
        self.generatebutton.clicked.connect(self.generate)
        self.generatebutton.move(300,280)
        #
        
        #Image Display Left
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(200,60,230,200)
        self.disp=QtGui.QPixmap("QR.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)
        #
        

        self.setGeometry(0,20,840,480)

    def scan(self):
        print "Scan"
    def generate(self):
        print "Generate"    
    def Loop(self):
        x=0

                 
            
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
