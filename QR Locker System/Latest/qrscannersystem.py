import zbar
import cv2
from PyQt4 import QtGui, QtCore
import sys
from time import time, sleep
import os
import serial
import qrcode
from picamera.array import PiRGBArray
from picamera import PiCamera
import mysql.connector
from mysql.connector import Error
import datetime
import time
import numpy as np
import pandas as pd
import random
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global camera,flag,lockertype,start_time,contact,flagcontact,addtypeflag
        addtypeflag=0
        flagcontact=0
        contact=""
        start_time = time.time()
        
        lockertype=0
        flag=0
        camera = PiCamera()
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.setGeometry(0,0,800,500)
        #self.d1=QtGui.QLabel("Status: ",self)
        #self.d1.move(350,290)
        self.d2=QtGui.QLabel("",self)
        self.d2.move(230,290)
        self.d2.resize(400,50)
        self.d3=QtGui.QLabel("Credits: ",self)
        self.d3.move(350,340)
        self.d4=QtGui.QLabel("-----",self)
        self.d4.move(400,340)
        self.d3.setVisible(0)
        self.d4.setVisible(0)
        self.d5=QtGui.QLabel("Phone Number: ",self)
        self.d5.move(250,290)
        
        self.d6=QtGui.QLabel("",self)
        self.d6.move(350,290)
        self.d5.setVisible(0)
        self.d6.setVisible(0)
        
        self.unlockbutton = QtGui.QPushButton("Unlock",self)
        self.unlockbutton.clicked.connect(self.unlock)
        self.unlockbutton.move(500,410)
        self.unlockbutton.setVisible(0)

        self.capturebutton = QtGui.QPushButton("Capture",self)
        self.capturebutton.clicked.connect(self.captureimg)
        self.capturebutton.move(500,410)
        self.capturebutton.setVisible(0)

        self.capturechangebutton = QtGui.QPushButton("Capture",self)
        self.capturechangebutton.clicked.connect(self.capturechange)
        self.capturechangebutton.move(500,410)
        self.capturechangebutton.setVisible(0)
        
        self.claimbutton = QtGui.QPushButton("Claim",self)
        self.claimbutton.clicked.connect(self.claim)
        self.claimbutton.move(420,320)
        
        self.generatebutton = QtGui.QPushButton("Use Locker",self)
        self.generatebutton.clicked.connect(self.generate)
        self.generatebutton.move(290,320)
        
        self.extendbutton = QtGui.QPushButton("Extend",self)
        self.extendbutton.clicked.connect(self.extend)
        self.extendbutton.move(290,370)
        self.changebutton = QtGui.QPushButton("Change Locker",self)
        self.changebutton.clicked.connect(self.change)
        self.changebutton.move(420,370)

        self.cancelbutton = QtGui.QPushButton("Cancel",self)
        self.cancelbutton.clicked.connect(self.cancelfunction)
        self.cancelbutton.move(200,410)

        self.change1button = QtGui.QPushButton("Locker 1",self)
        self.change1button.clicked.connect(self.change1)
        self.change1button.move(350,340)
        self.change2button = QtGui.QPushButton("Locker 2",self)
        self.change2button.clicked.connect(self.change2)
        self.change2button.move(350,370)
        self.change1button.setVisible(0)
        self.change2button.setVisible(0)

        self.newrent1button = QtGui.QPushButton("Locker 1",self)
        self.newrent1button.clicked.connect(self.newrent1)
        self.newrent1button.move(350,340)
        self.newrent2button = QtGui.QPushButton("Locker 2",self)
        self.newrent2button.clicked.connect(self.newrent2)
        self.newrent2button.move(350,370)
        self.newrent1button.setVisible(0)
        self.newrent2button.setVisible(0)
        
        self.rent1button = QtGui.QPushButton("3 Hours = P5",self)
        self.rent1button.clicked.connect(self.rent1)
        self.rent1button.move(180,360)
        self.rent2button = QtGui.QPushButton("6 Hours = P10",self)
        self.rent2button.clicked.connect(self.rent2)
        self.rent2button.move(300,360)
        self.rent3button = QtGui.QPushButton("12 Hours = P15",self)
        self.rent3button.clicked.connect(self.rent3)
        self.rent3button.move(420,360)
        self.rent4button = QtGui.QPushButton("18 Hours = P20",self)
        self.rent4button.clicked.connect(self.rent4)
        self.rent4button.move(540,360)
        self.rent1button.setVisible(0)
        self.rent2button.setVisible(0)
        self.rent3button.setVisible(0)
        self.rent4button.setVisible(0)
        
        self.next1button = QtGui.QPushButton("Next",self)
        self.next1button.clicked.connect(self.next1)
        self.next1button.move(500,410)
        self.cancelbutton.setVisible(0)
        self.next1button.setVisible(0)
        #self.debugbutton = QtGui.QPushButton("Debug",self)
        #self.debugbutton.clicked.connect(self.debug)
        #self.debugbutton.move(100,400)
        #self.debugbutton.resize(200,30)
        xcor=-270
        ycor=20
        self.zerobutton = QtGui.QPushButton("0",self)
        self.zerobutton.clicked.connect(self.zero)
        self.zerobutton.move(650+xcor,390+ycor)
        self.zerobutton.resize(50,30)
        
        self.onebutton = QtGui.QPushButton("1",self)
        self.onebutton.clicked.connect(self.one)
        self.onebutton.move(600+xcor,300+ycor)
        self.onebutton.resize(50,30)
        
        self.twobutton = QtGui.QPushButton("2",self)
        self.twobutton.clicked.connect(self.two)
        self.twobutton.move(650+xcor,300+ycor)
        self.twobutton.resize(50,30)
        
        self.threebutton = QtGui.QPushButton("3",self)
        self.threebutton.clicked.connect(self.three)
        self.threebutton.move(700+xcor,300+ycor)
        self.threebutton.resize(50,30)
        
        self.fourbutton = QtGui.QPushButton("4",self)
        self.fourbutton.clicked.connect(self.four)
        self.fourbutton.move(600+xcor,330+ycor)
        self.fourbutton.resize(50,30)
        
        self.fivebutton = QtGui.QPushButton("5",self)
        self.fivebutton.clicked.connect(self.five)
        self.fivebutton.move(650+xcor,330+ycor)
        self.fivebutton.resize(50,30)
        
        self.sixbutton = QtGui.QPushButton("6",self)
        self.sixbutton.clicked.connect(self.six)
        self.sixbutton.move(700+xcor,330+ycor)
        self.sixbutton.resize(50,30)
        
        self.sevenbutton = QtGui.QPushButton("7",self)
        self.sevenbutton.clicked.connect(self.seven)
        self.sevenbutton.move(600+xcor,360+ycor)
        self.sevenbutton.resize(50,30)
        
        self.eightbutton = QtGui.QPushButton("8",self)
        self.eightbutton.clicked.connect(self.eight)
        self.eightbutton.move(650+xcor,360+ycor)
        self.eightbutton.resize(50,30)
        
        self.ninebutton = QtGui.QPushButton("9",self)
        self.ninebutton.clicked.connect(self.nine)
        self.ninebutton.move(700+xcor,360+ycor)
        self.ninebutton.resize(50,30)

        self.backbutton = QtGui.QPushButton("<<",self)
        self.backbutton.clicked.connect(self.back)
        self.backbutton.move(750+xcor,270+ycor)
        self.backbutton.resize(40,25)
        
        self.backbutton.setVisible(0)
        self.zerobutton.setVisible(0)
        self.onebutton.setVisible(0)
        self.twobutton.setVisible(0)
        self.threebutton.setVisible(0)
        self.fourbutton.setVisible(0)
        self.fivebutton.setVisible(0)
        self.sixbutton.setVisible(0)
        self.sevenbutton.setVisible(0)
        self.eightbutton.setVisible(0)
        self.ninebutton.setVisible(0)


        
        self.exitbutton = QtGui.QPushButton("Close",self)
        self.exitbutton.clicked.connect(self.exit)
        self.exitbutton.move(330,370)
        self.exitbutton.setVisible(0)

        self.exit1button = QtGui.QPushButton("Close",self)
        self.exit1button.clicked.connect(self.exit1)
        self.exit1button.move(330,370)
        self.exit1button.setVisible(0)

        self.exit2button = QtGui.QPushButton("Close",self)
        self.exit2button.clicked.connect(self.exit2)
        self.exit2button.move(330,370)
        self.exit2button.setVisible(0)

        self.exit3button = QtGui.QPushButton("Close",self)
        self.exit3button.clicked.connect(self.exit3)
        self.exit3button.move(330,370)
        self.exit3button.setVisible(0)
        
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(210,30,720,250)
        self.disp=QtGui.QPixmap("/home/pi/Desktop/blackscreen.png")
        self.disp=self.disp.scaledToHeight(280)
        self.i1.setPixmap(self.disp)

        
    def change(self):
        self.claimbutton.setVisible(0)
        self.generatebutton.setVisible(0)
        self.extendbutton.setVisible(0)
        self.changebutton.setVisible(0)
        self.cancelbutton.setVisible(1)
        self.capturechangebutton.setVisible(1)
    def capturechange(self):
        global camera,idrep
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imwrite("/home/pi/Desktop/qrlocker.png",image)
        image = cv2.imread("/home/pi/Desktop/qrlocker.png")
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        self.dispa=QtGui.QPixmap("/home/pi/Desktop/qrlocker.png")
        self.dispa=self.dispa.scaledToHeight(280)
        self.i1.setGeometry(180,30,720,250)
        self.i1.setPixmap(self.dispa)
        
        scanner = zbar.Scanner()
        results = scanner.scan(image)
        for result in results:
            print result.type
            print result.data
            print result.quality
            print result.position
            changeid=result.data
            

            pathtarget="/home/pi/Desktop/statusdatabase.csv"
            if os.path.exists(pathtarget):
                         
                 df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                 np_df = df.as_matrix()
                 z=0
                 for i in xrange(len(np_df)):
                     
                     lockid = np_df[z][2]
                     
                     
                     if str(result.data)==lockid:
                         lockid = lockid.split("-")[0] 
                         if lockid=="Locker A":
                             
                             self.d2.setText("           Your locker number is 1.\n Choose which available locker to change.")
                             self.capturechangebutton.setVisible(0)
                             
                             pathtarget="/home/pi/Desktop/statusdatabase.csv"
                             if os.path.exists(pathtarget):
                                         
                                 df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                                 np_df = df.as_matrix()
                                 z=0
                                 for i in xrange(len(np_df)):
                                     
                                     if np_df[z][2]==changeid:
                                         self.change2button.setVisible(1)
                                         idrep=z
                                     z=z+1
                          
                         elif lockid=="Locker B":
                             
                             self.d2.setText("           Your locker number is 2.\n Choose which available locker to change.")
                             self.capturechangebutton.setVisible(0)
                             pathtarget="/home/pi/Desktop/statusdatabase.csv"
                             if os.path.exists(pathtarget):
                                         
                                 df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                                 np_df = df.as_matrix()
                                 z=0
                                 for i in xrange(len(np_df)):
                                     
                                     if np_df[z][2]==changeid:
                                         self.change1button.setVisible(1)
                                         idrep=z
                                     z=z+1
                            
                         
                     else:
                             self.d2.setText("                            Invalid Key.")
                             
                             self.cancelbutton.setVisible(0)
                             self.capturechangebutton.setVisible(0)
                             self.exit3button.setVisible(1)
                     z=z+1
    def change1(self):
        global idrep
        self.d2.setText("           Changed to Locker 1.\n           Take a picture of the new qr image \n          of your assigned locker.")
        self.change1button.setVisible(0)
        self.cancelbutton.setVisible(0)
        self.exit3button.setVisible(1)
        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = 10,
            border = 4,
        )
        
        lockdata = "Locker A-"+str(random.randint(1,10))
            
        qr.add_data(lockdata)
        qr.make(fit=True)


        img = qr.make_image()


        img.save("/home/pi/Desktop/qrlocker.png")
        
        self.dispa=QtGui.QPixmap("/home/pi/Desktop/qrlocker.png")
        self.dispa=self.dispa.scaledToHeight(280)
        self.i1.setGeometry(250,30,720,250)
        self.i1.setPixmap(self.dispa)
        pathtarget="/home/pi/Desktop/statusdatabase.csv"
        if os.path.exists(pathtarget):
                     
             df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
             df.iloc[idrep,2]=lockdata
             df.to_csv(pathtarget,  index = False)
             
        ser.write("B,")
        time.sleep(5)
        ser.write("A,")   
    def change2(self):
        global idrep
        self.d2.setText("           Changed to Locker 2.\n           Take a picture of the new qr image \n          of your assigned locker.")
        
        self.change2button.setVisible(0)
        self.cancelbutton.setVisible(0)
        self.exit3button.setVisible(1)
        
        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = 10,
            border = 4,
        )
        
        lockdata = "Locker B-"+str(random.randint(1,10))
            
        qr.add_data(lockdata)
        qr.make(fit=True)


        img = qr.make_image()


        img.save("/home/pi/Desktop/qrlocker.png")
        
        self.dispa=QtGui.QPixmap("/home/pi/Desktop/qrlocker.png")
        self.dispa=self.dispa.scaledToHeight(280)
        self.i1.setGeometry(250,30,720,250)
        self.i1.setPixmap(self.dispa)
        pathtarget="/home/pi/Desktop/statusdatabase.csv"
        if os.path.exists(pathtarget):
                     
             df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
             df.iloc[idrep,2]=lockdata
             df.to_csv(pathtarget,  index = False)
        ser.write("A,")
        time.sleep(5)
        ser.write("B,")
    def exit1(self):
         self.d2.setText("")
         
         self.exit1button.setVisible(0)
         self.claimbutton.setVisible(1)
         self.generatebutton.setVisible(1)
         self.extendbutton.setVisible(1)
         self.changebutton.setVisible(1)
    def exit2(self):
         self.d2.setText("")
         self.cancelbutton.setVisible(0)
         self.exit2button.setVisible(0)
         self.claimbutton.setVisible(1)
         self.generatebutton.setVisible(1)
         self.extendbutton.setVisible(1)
         self.changebutton.setVisible(1)
         
    def exit3(self):
         self.d2.setText("")
         self.cancelbutton.setVisible(0)
         self.exit3button.setVisible(0)
         self.claimbutton.setVisible(1)
         self.generatebutton.setVisible(1)
         self.extendbutton.setVisible(1)
         self.changebutton.setVisible(1)
         self.disp=QtGui.QPixmap("/home/pi/Desktop/blackscreen.png")
         self.disp=self.disp.scaledToHeight(280)
         self.i1.setPixmap(self.disp)
    def rent1(self):
        global flag,creditacceptor,renttype
        renttype=1
        flag=1
        self.d3.setVisible(1)
        self.d4.setVisible(1)
        #ser.write("C,")
        #data=ser.readline()
        #creditacceptor=int(data.split(",")[0])
        #self.d4.setText(str(creditacceptor))
        self.rent1button.setVisible(0)
        self.rent2button.setVisible(0)
        self.rent3button.setVisible(0)
        self.rent4button.setVisible(0)
    def claim(self):
        self.cancelbutton.setVisible(1)
        self.unlockbutton.setVisible(1)
        self.claimbutton.setVisible(0)
        self.generatebutton.setVisible(0)
        self.extendbutton.setVisible(0)
        self.changebutton.setVisible(0)
    def rent2(self):
        global flag,creditacceptor,renttype
        renttype=2
        flag=1
        self.d3.setVisible(1)
        self.d4.setVisible(1)
        #ser.write("C,")
        #data=ser.readline()
        #creditacceptor=int(data.split(",")[0])
        #self.d4.setText(str(creditacceptor))
        self.rent1button.setVisible(0)
        self.rent2button.setVisible(0)
        self.rent3button.setVisible(0)
        self.rent4button.setVisible(0)
    def rent3(self):
        global flag,creditacceptor,renttype
        renttype=3
        flag=1
        self.d3.setVisible(1)
        self.d4.setVisible(1)
        #ser.write("C,")
        #data=ser.readline()
        #creditacceptor=int(data.split(",")[0])
        #self.d4.setText(str(creditacceptor))
        self.rent1button.setVisible(0)
        self.rent2button.setVisible(0)
        self.rent3button.setVisible(0)
        self.rent4button.setVisible(0)
    def rent4(self):
        global flag,creditacceptor,renttype
        renttype=4
        flag=1
        self.d3.setVisible(1)
        self.d4.setVisible(1)
        #ser.write("C,")
        #data=ser.readline()
        #creditacceptor=int(data.split(",")[0])
        #self.d4.setText(str(creditacceptor))
        self.rent1button.setVisible(0)
        self.rent2button.setVisible(0)
        self.rent3button.setVisible(0)
        self.rent4button.setVisible(0)
        
    def cancelfunction(self):
        global creditacceptor,flag,contact
        self.disp=QtGui.QPixmap("/home/pi/Desktop/blackscreen.png")
        self.disp=self.disp.scaledToHeight(280)
        self.i1.setPixmap(self.disp)
        contact=""
        creditacceptor=0
        flag=0
        self.d2.setText("")
        self.d4.setText("")
        self.change1button.setVisible(0)
        self.change2button.setVisible(0)
        self.capturebutton.setVisible(0)
        self.newrent1button.setVisible(0)
        self.newrent2button.setVisible(0)
        
        self.unlockbutton.setVisible(0)
        self.next1button.setVisible(0)
        self.rent1button.setVisible(0)
        self.rent2button.setVisible(0)
        self.rent3button.setVisible(0)
        self.rent4button.setVisible(0)
        self.exitbutton.setVisible(0)
        self.exit1button.setVisible(0)
        self.claimbutton.setVisible(1)
        self.generatebutton.setVisible(1)
        self.extendbutton.setVisible(1)
        self.changebutton.setVisible(1)
        self.cancelbutton.setVisible(0)
        self.d5.setVisible(0)
        self.d6.setVisible(0)
        self.zerobutton.setVisible(0)
        self.onebutton.setVisible(0)
        self.twobutton.setVisible(0)
        self.threebutton.setVisible(0)
        self.fourbutton.setVisible(0)
        self.fivebutton.setVisible(0)
        self.sixbutton.setVisible(0)
        self.sevenbutton.setVisible(0)
        self.eightbutton.setVisible(0)
        self.ninebutton.setVisible(0)
        self.backbutton.setVisible(0)
        
    
    def newrent1(self):
        global lockertype
        lockertype=1
        self.d2.setText("")
        self.newrent1button.setVisible(0)
        self.newrent2button.setVisible(0)
        self.d5.setVisible(1)
        self.d6.setVisible(1)
        self.zerobutton.setVisible(1)
        self.onebutton.setVisible(1)
        self.twobutton.setVisible(1)
        self.threebutton.setVisible(1)
        self.fourbutton.setVisible(1)
        self.fivebutton.setVisible(1)
        self.sixbutton.setVisible(1)
        self.sevenbutton.setVisible(1)
        self.eightbutton.setVisible(1)
        self.ninebutton.setVisible(1)
        self.backbutton.setVisible(1)
        self.next1button.setVisible(1)
    def newrent2(self):
        self.d2.setText("")
        global lockertype
        lockertype=2
        self.newrent1button.setVisible(0)
        self.newrent2button.setVisible(0)
        self.d5.setVisible(1)
        self.d6.setVisible(1)
        self.zerobutton.setVisible(1)
        self.onebutton.setVisible(1)
        self.twobutton.setVisible(1)
        self.threebutton.setVisible(1)
        self.fourbutton.setVisible(1)
        self.fivebutton.setVisible(1)
        self.sixbutton.setVisible(1)
        self.sevenbutton.setVisible(1)
        self.eightbutton.setVisible(1)
        self.ninebutton.setVisible(1)
        self.backbutton.setVisible(1)
        self.next1button.setVisible(1)
    def next1(self):
        
        self.d5.setVisible(0)
        self.d6.setVisible(0)
        self.zerobutton.setVisible(0)
        self.onebutton.setVisible(0)
        self.twobutton.setVisible(0)
        self.threebutton.setVisible(0)
        self.fourbutton.setVisible(0)
        self.fivebutton.setVisible(0)
        self.sixbutton.setVisible(0)
        self.sevenbutton.setVisible(0)
        self.eightbutton.setVisible(0)
        self.ninebutton.setVisible(0)
        self.backbutton.setVisible(0)
        self.rent1button.setVisible(1)
        self.rent2button.setVisible(1)
        self.rent3button.setVisible(1)
        self.rent4button.setVisible(1)
        self.next1button.setVisible(0)
        self.d2.setText("           Choose how long would you like to rent.")
    #def debug(self):
    #        ser.write("F,09062795780,Locker A-7,09174794242,")
    #        print "SMS Sent"
    
    def extend(self):
        global addtypeflag,creditacceptor
        addtypeflag=1
        self.claimbutton.setVisible(0)
        self.generatebutton.setVisible(0)
        self.extendbutton.setVisible(0)
        self.changebutton.setVisible(0)
        self.cancelbutton.setVisible(1)
        ser.write("C,")
        data=ser.readline()
        creditacceptor=int(data.split(",")[0])
        print "Debug: "+str(data)
        self.capturebutton.setVisible(1)
    def captureimg(self):
        global camera,extendid
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imwrite("/home/pi/Desktop/qrlocker.png",image)
        image = cv2.imread("/home/pi/Desktop/qrlocker.png")
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        self.dispa=QtGui.QPixmap("/home/pi/Desktop/qrlocker.png")
        self.dispa=self.dispa.scaledToHeight(280)
        self.i1.setGeometry(180,30,720,250)
        self.i1.setPixmap(self.dispa)
        
        scanner = zbar.Scanner()
        results = scanner.scan(image)
        for result in results:
            print result.type
            print result.data
            print result.quality
            print result.position
            extendid=result.data
            

            pathtarget="/home/pi/Desktop/statusdatabase.csv"
            if os.path.exists(pathtarget):
                         
                 df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                 np_df = df.as_matrix()
                 z=0
                 for i in xrange(len(np_df)):
                     
                     lockid = np_df[z][2]
                     
                     
                     if str(result.data)==lockid:
                         lockid = lockid.split("-")[0] 
                         if lockid=="Locker A":
                             
                             self.d2.setText("           Your locker number is 1.\n Choose how much would you like to extend.")
                             self.capturebutton.setVisible(0)
                             self.rent1button.setVisible(1)
                             self.rent2button.setVisible(1)
                             self.rent3button.setVisible(1)
                             self.rent4button.setVisible(1)
                             self.exit2button.setVisible(0)
                         elif lockid=="Locker B":
                             
                             self.d2.setText("           Your locker number is 2.\n Choose how much would you like to extend.")
                             self.capturebutton.setVisible(0)
                             self.rent1button.setVisible(1)
                             self.rent2button.setVisible(1)
                             self.rent3button.setVisible(1)
                             self.rent4button.setVisible(1)
                             self.exit2button.setVisible(0)
                         
                     else:
                             self.d2.setText("                            Invalid Key.")
                             self.exit2button.setVisible(1)
                             self.capturebutton.setVisible(0)
                             self.cancelbutton.setVisible(0)
                             self.rent1button.setVisible(0)
                             self.rent2button.setVisible(0)
                             self.rent3button.setVisible(0)
                             self.rent4button.setVisible(0)
                     z=z+1
        
    def back(self):
        global contact
        contact=contact[:-1]                  
    def zero(self):
        global contact
        contact+="0"
    def one(self):
        global contact
        contact+="1"
    def two(self):
        global contact
        contact+="2"
    def three(self):
        global contact
        contact+="3"
    def four(self):
        global contact
        contact+="4"
    def five(self):
        global contact
        contact+="5"
    def six(self):
        global contact
        contact+="6"
    def seven(self):
        global contact
        contact+="7"
    def eight(self):
        global contact
        contact+="8"
    def nine(self):
        global contact
        contact+="9"
    
    def exit(self):
        global creditacceptor,lockertype,contact
        print lockertype
        
        
        
        self.i1.setGeometry(180,30,720,250)
        self.disp=QtGui.QPixmap("/home/pi/Desktop/blackscreen.png")
        self.disp=self.disp.scaledToHeight(280)
        self.i1.setPixmap(self.disp)
        self.exitbutton.setVisible(0)
        self.newrent1button.setVisible(0)
        self.newrent2button.setVisible(0)
        self.d2.setText("")
        self.claimbutton.setVisible(1)
        self.generatebutton.setVisible(1)
        self.extendbutton.setVisible(1)
        self.changebutton.setVisible(1)
        self.d5.setVisible(0)
        self.d6.setVisible(0)
        self.zerobutton.setVisible(0)
        self.onebutton.setVisible(0)
        self.twobutton.setVisible(0)
        self.threebutton.setVisible(0)
        self.fourbutton.setVisible(0)
        self.fivebutton.setVisible(0)
        self.sixbutton.setVisible(0)
        self.sevenbutton.setVisible(0)
        self.eightbutton.setVisible(0)
        self.ninebutton.setVisible(0)
        self.backbutton.setVisible(0)
        if lockertype==1:
            lockdata = "Locker A"
            msg="G,"+str(contact)+","
            print "Message: "+str(msg)
            ser.write(msg)
        elif lockertype==2:
            lockdata = "Locker B"
            msg="H,"+str(contact)+","
            print "Message: "+str(msg)
            ser.write(msg)
        contact=""
    def unlock(self):
        global camera
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imwrite("/home/pi/Desktop/qrlocker.png",image)
        image = cv2.imread("/home/pi/Desktop/qrlocker.png")
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        self.dispa=QtGui.QPixmap("/home/pi/Desktop/qrlocker.png")
        self.dispa=self.dispa.scaledToHeight(280)
        self.i1.setGeometry(180,30,720,250)
        self.i1.setPixmap(self.dispa)
        
        scanner = zbar.Scanner()
        results = scanner.scan(image)
        for result in results:
            print result.type
            print result.data
            print result.quality
            print result.position
            
            
            self.disp=QtGui.QPixmap("/home/pi/Desktop/blackscreen.png")
            self.disp=self.disp.scaledToHeight(280)
            self.i1.setPixmap(self.disp)

            pathtarget="/home/pi/Desktop/statusdatabase.csv"
            if os.path.exists(pathtarget):
                         
                 df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                 np_df = df.as_matrix()
                 z=0
                 for i in xrange(len(np_df)):
                     
                     lockid = np_df[z][2]
                     
                     
                     if str(result.data)==lockid:
                         lockid = lockid.split("-")[0] 
                         if lockid=="Locker A":
                             ser.write("A,")
                             self.d2.setText("           You have unlock locker number 1.\n           Thank you for using our locker.")
                         elif lockid=="Locker B":
                             ser.write("B,")
                             self.d2.setText("           You have unlock locker number 2.\n           Thank you for using our locker.")
                         
                         df=df.drop([z], axis=0)
                         df.to_csv(pathtarget,  index = False)
                         self.exit1button.setVisible(1)
                         self.unlockbutton.setVisible(0)
                         self.cancelbutton.setVisible(0)
                     else:
                             self.d2.setText("                            Invalid Key.")
                             self.exit1button.setVisible(1)
                             self.unlockbutton.setVisible(0)
                             self.cancelbutton.setVisible(0)
                     z=z+1
    def generate(self):
        global flagcontact,addtypeflag,creditacceptor
        addtypeflag=0
        flagcontact=1
        ser.write("C,")
        data=ser.readline()
        creditacceptor=int(data.split(",")[0])
        print "creditacceptor="+str(creditacceptor)
        
        self.claimbutton.setVisible(0)
        self.generatebutton.setVisible(0)
        self.extendbutton.setVisible(0)
        self.changebutton.setVisible(0)
        self.cancelbutton.setVisible(1)
        pathtarget="/home/pi/Desktop/statusdatabase.csv"
        if os.path.exists(pathtarget):
                     
             df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
             np_df = df.as_matrix()
             z=0
             a=0
             b=0
             for i in xrange(len(np_df)):
                 lockid = np_df[z][2]
                 lockid = lockid.split("-")[0] 
                 if lockid=="Locker A":
                       a=1
                       self.newrent1button.setVisible(0)
                 if lockid=="Locker B":
                       b=1
                       self.newrent2button.setVisible(0)
                 z=z+1
             if a==1 and b==1:
                 self.d2.setText("                      No locker available.")
                 self.cancelbutton.setVisible(0)
                 self.exitbutton.setVisible(1)
             
             else:
                 self.d2.setText("                   Choose among available lockers .")   
                 if a==0:
                     self.newrent1button.setVisible(1)
                 if b==0:
                     self.newrent2button.setVisible(1)
        else:
            self.d2.setText("                   Choose among available lockers .")   
            self.newrent1button.setVisible(1)
            self.newrent2button.setVisible(1)
    def Loop(self):
        global flag,creditacceptor,lockertype,start_time,contact,flagcontact,renttype,addtypeflag,extendid
        
        elapsed_time=time.time()-start_time
        if elapsed_time>=5:
            start_time = time.time()
            pathtarget="/home/pi/Desktop/statusdatabase.csv"
            if os.path.exists(pathtarget):
                         
                 df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                 np_df = df.as_matrix()
                 z=0
                 for i in xrange(len(np_df)):
                     
                     targetnumber = np_df[z][0]
                     targetduration=np_df[z][3]
                     targetexceed=np_df[z][4]
                     print targetnumber
                     now = datetime.datetime.now()
                     data=str(now)
                     date=data.split(" ")[0]
                     timepost=data.split(" ")[1]
                     nowhour=int(timepost.split(":")[0])*60
                     timepost=timepost.split(".")[0]
                     nowminute=int(timepost.split(":")[1])
                    
                     hourtominute= int(np_df[z][1].split(":")[0])*60
                     minute= int(np_df[z][1].split(":")[1])
                     
                     duration=nowhour-hourtominute+nowminute-minute
                     print "Duration: "+str(duration)
                     print "Type: "+str(targetduration)+" Minutes"
                     if duration>=targetduration and duration<=targetexceed: #In Minutes - 1380
                         msg="D,"+str(targetnumber)+","
                         print "Message: "+str(msg)
                         ser.write(msg)
                        
                         
                     elif duration>=targetexceed and np_df[z][5]=="0":
                         msg="F,09267171976,"+str(np_df[z][2])+","+str(np_df[z][0])+","
                         print "Message: "+str(msg)
                         ser.write(msg)
                         df.iloc[z,5]="1"
                         df.to_csv(pathtarget,  index = False)
                         #df=df.drop([z], axis=0)
                         #df.to_csv(pathtarget,  index = False)
                     z=z+1
                 #duration=hourtominute+minute
                 #if duration<=60
                 #
                 
        #print elapsed_time
        #serdata=ser.readline()
        #print "data="+str(serdata)
        if flagcontact==1:
            self.d6.setText(contact)
        if flag==1:
            
            self.d2.setText("                   Please insert enough credits.")
           
            
            
            try:
                    serdata=ser.readline()
                    print "data="+str(serdata)
                    creditacceptor=int(serdata.split(",")[0])
                    
                    
                    
                    self.d4.setText(str(creditacceptor))
                    if renttype==1:
                        credittarget=5
                        notifduration=120
                        exceedduration=180
                    elif renttype==2:
                        credittarget=10
                        notifduration=300
                        exceedduration=360
                    elif renttype==3:
                        credittarget=15
                        notifduration=660
                        exceedduration=720
                    elif renttype==4:
                        credittarget=20
                        notifduration=1020
                        exceedduration=1080
                    if creditacceptor>=credittarget and lockertype!=0 and addtypeflag==0:
                        print "Credit Detected: "+str(creditacceptor)
                        self.cancelbutton.setVisible(0)
                        flag=0
                        qr = qrcode.QRCode(
                            version = 1,
                            error_correction = qrcode.constants.ERROR_CORRECT_H,
                            box_size = 10,
                            border = 4,
                        )
                        if lockertype==1:
                            lockdata = "Locker A-"+str(random.randint(1,10))
                            
                        elif lockertype==2:
                            lockdata = "Locker B-"+str(random.randint(1,10))
                            
                        qr.add_data(lockdata)
                        qr.make(fit=True)


                        img = qr.make_image()


                        img.save("/home/pi/Desktop/qrlocker.png")
                        
                        self.dispa=QtGui.QPixmap("/home/pi/Desktop/qrlocker.png")
                        self.dispa=self.dispa.scaledToHeight(280)
                        self.i1.setGeometry(250,30,720,250)
                        self.i1.setPixmap(self.dispa)
                        ser.write("C,")
                        data=ser.readline()
                        creditacceptor=int(data.split(",")[0])
                        print "Debug: "+str(data)
                        self.d4.setText(str(creditacceptor))
                        self.d2.setText("                         Process Completed. \n     Take a picture of the QR Code and press close after.")
                        
                        self.exitbutton.setVisible(1)
                        self.d3.setVisible(0)
                        self.d4.setVisible(0)
                        #lockertype=0
                        self.newrent1button.setVisible(0)
                        self.newrent2button.setVisible(0)
        
                        print "Database"
                        def insertdata(lockerid, number,time,date,credittarget):
                                query = "INSERT INTO qrlockerdata(Lockerid, Number,Time,Date,Credit) " \
                                        "VALUES(%s,%s,%s,%s)"
                                args = (lockerid, number,time,date,credittarget)
                                print "Inserting data." 
                                try:
                                    conn = mysql.connector.connect(host='sql12.freemysqlhosting.net',
                                                                   database='sql12273787',
                                                                   user='sql12273787',
                                                                   password='KdIxjNH8TK')
                                    cursor = conn.cursor()
                                    cursor.execute(query, args)
                                    conn.commit()
                                    print "mySQL database updated."
                                except Error as error:
                                    print(error)
                             
                                finally:
                                    cursor.close()
                                    conn.close() 
                        now = datetime.datetime.now()
                        data=str(now)
                        date=data.split(" ")[0]
                        timepost=data.split(" ")[1]
                        timepost=timepost.split(".")[0]
                        insertdata(lockdata,contact,timepost,date,credittarget)
                        
                        
                        pathtarget="/home/pi/Desktop/statusdatabase.csv"
                        if os.path.exists(pathtarget):
                                     
                             df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                             np_df = df.as_matrix()
                             idnumber=len(df.index)
                             df = df.append({'Number':contact,'Time':timepost,'ID':lockdata,'Notification':str(notifduration),'Exceed':str(exceedduration),'Textflag':str(exceedduration),'Textflag':"0"}, ignore_index=True)
                             df.to_csv(pathtarget,  index = False)
                             print df
                        else:
                             
                             columns = ['Number','Time','ID','Notification','Exceed','Textflag']
                             df = pd.DataFrame(columns=columns)
                             np_df = df.as_matrix()
                             idnumber=0
                             df = df.append({'Number':contact,'Time':timepost,'ID':lockdata,'Notification':str(notifduration),'Exceed':str(exceedduration),'Textflag':"0"}, ignore_index=True)
                             df.to_csv(pathtarget,  index = False)
                             print df
                        
                    elif creditacceptor>=credittarget and addtypeflag==1:
                        self.cancelbutton.setVisible(0)
                        flag=0
                        ser.write("C,")
                        data=ser.readline()
                        print "Debug: "+str(data)
                        self.d3.setVisible(0)
                        self.d4.setVisible(0)
                        self.d2.setText("                   "+extendid+" is extended.")
                        pathtarget="/home/pi/Desktop/statusdatabase.csv"
                        if os.path.exists(pathtarget):
                                     
                             df=pd.read_csv(pathtarget,names=['Number','Time','ID','Notification','Exceed','Textflag'],skiprows=1)
                             np_df = df.as_matrix()
                             z=0
                             for i in xrange(len(np_df)):
                                 
                                 if np_df[z][2]==extendid:
                                     print "Found"
                                     timeextend=int(np_df[z][3])+notifduration+60
                                     print timeextend
                                     df.iloc[z,3]=timeextend
                                     df.to_csv(pathtarget,  index = False)
                                 z=z+1
                        extendid=""
                        self.exitbutton.setVisible(1)
            except:
                    dump=0

                 
            
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
