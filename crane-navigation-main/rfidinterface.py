from PyQt4 import QtGui, QtCore

import sys
import time
import numpy as np
import pandas as pd
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import os,time
import serial
import datetime
ser=serial.Serial('COM3',9600,timeout=1)
class Main(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,tic,rfidflag
        flag=0
        rfidflag=0
        tic = time.clock()
        
        self.setWindowTitle("Crane Database")
        
        self.frame = QtGui.QFrame(self)
        self.frame.resize(720,480)
        self.frame.setStyleSheet("background-image: url(background.png);");
        self.frame1 = QtGui.QFrame(self)
        self.frame1.resize(350,300)
        self.frame1.setStyleSheet("background-color: rgb(255, 255, 0)")
        self.frame1.move(50,100)
        self.frame2 = QtGui.QFrame(self)
        self.frame2.resize(350,100)
        self.frame2.setStyleSheet("background-color: rgb(255, 255, 0)")
        self.frame2.move(50,550)
        self.frame3 = QtGui.QFrame(self)
        self.frame3.resize(500,250)
        self.frame3.setStyleSheet("background-color: rgb(255, 255, 0)")
        self.frame3.move(500,100)
        
        centralwidget = QtGui.QWidget(self)
        self.setGeometry(100,100,1024,700)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        
        self.startbutton = QtGui.QPushButton("Start",self)
        self.startbutton.clicked.connect(self.startfunc)
        self.startbutton.move(300,770)
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stopfunc)
        self.stopbutton.move(450,770)
        
        self.i0=QtGui.QLabel(self)#########
        self.i1=QtGui.QLabel(self)
        self.i2=QtGui.QLabel(self)
        self.i3=QtGui.QLabel(self)
        self.i4=QtGui.QLabel(self)
        self.i5=QtGui.QLabel(self)
        self.w1=QtGui.QLabel(self)
        self.w2=QtGui.QLabel(self)
        self.w3=QtGui.QLabel(self)
        self.s1=QtGui.QLabel("CONTAINER LABEL:",self)
        self.s2=QtGui.QLabel(self)
        self.s3=QtGui.QLabel("WEIGHT: ",self)
        self.s4=QtGui.QLabel(self)
        self.s5=QtGui.QLabel("CARGO: ",self)
        self.s6=QtGui.QLabel(self)
        
        font = QtGui.QFont("Times", 24)
        
        
        self.corpname=QtGui.QLabel("Name of Corporation",self)
        self.corpname.move(400,20)
        self.corpname.resize(300,50)
        self.corpname.setStyleSheet("color: white;background-color:blue;")
        self.corpname.setFont(font)
        self.corpname.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.i0.move(100,100)#########
        self.i1.move(100,150)
        self.i2.move(100,200)
        self.i3.move(100,250)
        self.i4.move(100,300)
        self.i5.move(100,350)
        self.w1.move(100,570)
        self.w2.move(100,620)
        self.w3.move(100,670)
        self.s1.move(530,150)
        self.s2.move(750,150)
        self.s3.move(530,250)
        self.s4.move(630,250)
        self.s5.move(530,350)
        self.s6.move(630,350)
        fontsensor = QtGui.QFont("Times", 16)
        self.i0.setStyleSheet("background-color:yellow;")#########
        self.i1.setStyleSheet("background-color:yellow;")
        self.i2.setStyleSheet("background-color:yellow;")
        self.i3.setStyleSheet("background-color:yellow;")
        self.i4.setStyleSheet("background-color:yellow;")
        self.i5.setStyleSheet("background-color:yellow;")
        self.w1.setStyleSheet("background-color:yellow;")
        self.w2.setStyleSheet("background-color:yellow;")
        self.w3.setStyleSheet("background-color:yellow;")
        self.s1.setStyleSheet("background-color:yellow;")
        self.s2.setStyleSheet("background-color:yellow;")
        self.s3.setStyleSheet("background-color:yellow;")
        self.s4.setStyleSheet("background-color:yellow;")
        self.s5.setStyleSheet("background-color:yellow;")
        self.s6.setStyleSheet("background-color:yellow;")
        self.i0.resize(300,50)#########
        self.i1.resize(300,50)
        self.i2.resize(300,50)
        self.i3.resize(300,50)
        self.i4.resize(300,50)
        self.i5.resize(300,50)
        self.w1.resize(300,50)
        self.w2.resize(300,50)
        self.w3.resize(300,50)
        self.s1.resize(300,50)
        self.s2.resize(250,50)
        self.s3.resize(300,50)
        self.s4.resize(300,50)
        self.s5.resize(300,50)
        self.s6.resize(300,50)
        self.i0.setFont(fontsensor)#########
        self.i1.setFont(fontsensor)
        self.i2.setFont(fontsensor)
        self.i3.setFont(fontsensor)
        self.i4.setFont(fontsensor)
        self.i5.setFont(fontsensor)
        self.w1.setFont(fontsensor)
        self.w2.setFont(fontsensor)
        self.w3.setFont(fontsensor)
        self.s1.setFont(fontsensor)
        self.s2.setFont(fontsensor)
        self.s3.setFont(fontsensor)
        self.s4.setFont(fontsensor)
        self.s5.setFont(fontsensor)
        self.s6.setFont(fontsensor)
        
        
       
        
    def startfunc(self):
        global flag,rfidflag
        flag=1
        rfidflag=1
    def stopfunc(self):
        global flag
        flag=0
        self.i1.setText("")
        self.i2.setText("")
        self.i3.setText("")
        self.i4.setText("")
        self.i5.setText("")
        self.w1.setText("")
        self.w2.setText("")
        self.w3.setText("")
        self.s2.setText("")
        self.s4.setText("")
        self.s6.setText("")
        rfidflag=0
    def Loop(self):
        global flag,rfidflag
        if flag==1:
            rfidcom=ser.readline()
            
            try:
                minimumdistance=40
                grabdistance=70
                dA=float(rfidcom.split(",")[0])
                dB=float(rfidcom.split(",")[1])
                dC=float(rfidcom.split(",")[2])
                dD=float(rfidcom.split(",")[3])
                dE=float(rfidcom.split(",")[4])
                dF=float(rfidcom.split(",")[5])
                cardid=str(rfidcom.split(",")[7])
                temperature=str(rfidcom.split(",")[8])#########
                print temperature#########
                self.i0.setText("Temperature: "+str(temperature)+" C")#########
                self.i1.setText("Range: "+str(dA)+" cm")
                self.i2.setText("Range: "+str(dB)+" cm")
                self.i3.setText("Range: "+str(dC)+" cm")
                self.i4.setText("Range: "+str(dD)+" cm")
                self.i5.setText("Range: "+str(dE)+" cm")
                print rfidcom
                print dF
                if dA<=minimumdistance or dB<=minimumdistance or dC<=minimumdistance or dD<=minimumdistance or dE<=minimumdistance:
                   self.w1.setText("CONTAINER ABOUT")
                   self.w2.setText("TO COLLIDE")
                   self.w3.setText("CRANE IS STOPPED")
                elif cardid!="" and dF<=grabdistance and dA>minimumdistance and dB>minimumdistance and dC>minimumdistance and dD>minimumdistance and dE>minimumdistance:
                   self.w1.setText("CONTAINER IS")
                   self.w2.setText("GRABBED")
                   self.w3.setText("")
                elif cardid=="" and dF>grabdistance and dA>minimumdistance and dB>minimumdistance and dC>minimumdistance and dD>minimumdistance and dE>minimumdistance:
                   self.w1.setText("CONTAINER IS")
                   self.w2.setText("PLACED/PICKED")
                   self.w3.setText("")
                   self.s2.setText("")
                   self.s4.setText("")
                   self.s6.setText("")
    
                
                else:
                   self.w1.setText("")
                   self.w2.setText("")
                   self.w3.setText("") 
                if rfidflag==1 and cardid!="":   
                    try:
                        dbconfig = read_db_config()
                        conn = MySQLConnection(**dbconfig)
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM cargodata")
                        rows = cursor.fetchall()
                        
                        for row in rows:
                            if row[0]==cardid:
                                self.s2.setText(row[0])
                                self.s4.setText(row[1])
                                self.s6.setText(row[2])
                              
                    except Error as e:
                        print(e)
                 
                    finally:
                        cursor.close()
                        conn.close()
                    rfidflag=0
                
            except:
                x=0
  
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
