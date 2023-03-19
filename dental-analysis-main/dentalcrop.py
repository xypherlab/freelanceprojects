from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import pymeanshift as pms
from sklearn.svm import SVC
import pandas as pd
from collections import Counter
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,x,cap,z,liveflagA,liveflagB,start_time
        start_time = time.time()
        liveflagA=1
        liveflagB=0
        z=0
        flag=0
        x=0
        cap=cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        #
        self.newbutton = QtGui.QPushButton("New User",self)
        self.newbutton.clicked.connect(self.newuser)
        self.newbutton.move(120,50)
        
        #
        #
        self.matchingbutton = QtGui.QPushButton("Matching",self)
        self.matchingbutton.clicked.connect(self.matching)
        self.matchingbutton.move(120,100)
        
        #
        
        #Analyze Button
        self.analyzebutton = QtGui.QPushButton("Analyze",self)
        self.analyzebutton.clicked.connect(self.analyze)
        self.analyzebutton.move(320,390)
        
        #
        #Upper Jaw Button
        self.upperjawbutton = QtGui.QPushButton("Upper Jaw",self)
        self.upperjawbutton.clicked.connect(self.upperjaw)
        self.upperjawbutton.move(560,170)
        #
        #Lower Jaw Button
        self.lowerjawbutton = QtGui.QPushButton("Lower Jaw",self)
        self.lowerjawbutton.clicked.connect(self.lowerjaw)
        self.lowerjawbutton.move(560,200)
        #
        #Live Feed Button
        self.livefeedAbutton = QtGui.QPushButton("Live Upper",self)
        self.livefeedAbutton.clicked.connect(self.livefeedA)
        self.livefeedAbutton.move(560,230)
        #
        #Live Feed Button
        self.livefeedBbutton = QtGui.QPushButton("Live Lower",self)
        self.livefeedBbutton.clicked.connect(self.livefeedB)
        self.livefeedBbutton.move(560,260)
        #
        #Side Title
        self.d10=QtGui.QLabel("Upper",self)
        self.d10.move(200,45)
        self.d11=QtGui.QLabel("Lower",self)
        self.d11.move(200,245)
        #
        #Image Display Left
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(100,60,400,200)
        self.disp=QtGui.QPixmap("blackscreen.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)
        #
        #Image Display Right
        self.i2=QtGui.QLabel(self)
        self.i2.setGeometry(100,260,400,200)
        self.dispa=QtGui.QPixmap("blackscreen.png")
        self.dispa=self.disp.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
        #
        #Edit
        self.l1=QtGui.QLabel("Name:",self)
        self.l1.move(130,100)
        self.l2=QtGui.QLineEdit(self)
        self.l2.move(130,130)
        self.l2.resize(450,40)
        self.r1=QtGui.QLabel("----",self)
        self.r1.move(200,100)
        self.r1.resize(450,40)
        #
        #Edit
        self.l5=QtGui.QLabel("Age:",self)
        self.l5.move(130,180)
        self.r5=QtGui.QLabel("----",self)
        self.r5.move(200,180)
        
        self.l6=QtGui.QLineEdit(self)
        self.l6.move(190,180)
        self.l6.resize(50,40)
        #
        #Edit
        self.l7=QtGui.QLabel("Gender:",self)
        self.l7.move(310,180)
        self.r7=QtGui.QLabel("----",self)
        self.r7.move(410,180)
        self.l8=QtGui.QLineEdit(self)
        self.l8.move(400,180)
        self.l8.resize(50,40)
        #
        #Edit
        self.l9=QtGui.QLabel("Contact Number:",self)
        self.l9.move(130,230)
        self.r9=QtGui.QLabel("----",self)
        self.r9.move(320,230)
        self.r9.resize(450,40)
        self.l9.resize(230,30)
        self.l10=QtGui.QLineEdit(self)
        self.l10.move(130,260)
        self.l10.resize(450,40)
        #

        #Edit
        self.l11=QtGui.QLabel("Email:",self)
        self.l11.move(130,300)
        self.l12=QtGui.QLineEdit(self)
        self.l12.move(130,330)
        self.l12.resize(450,40)
        #
        #Register Button
        self.registerbutton = QtGui.QPushButton("Register",self)
        self.registerbutton.clicked.connect(self.register)
        self.registerbutton.move(320,390)
        #
        #Delete Button
        self.deletebutton = QtGui.QPushButton("Delete",self)
        self.deletebutton.clicked.connect(self.delete)
        self.deletebutton.move(320,420)
        #
        #Save Button
        self.savebutton = QtGui.QPushButton("Save",self)
        self.savebutton.clicked.connect(self.save)
        self.savebutton.move(320,450)
        #
        #Exit Button
        self.exitbutton = QtGui.QPushButton("Exit",self)
        self.exitbutton.clicked.connect(self.exitgui)
        self.exitbutton.move(320,430)
        #
        #Result Button
        self.resultbutton = QtGui.QPushButton("Proceed",self)
        self.resultbutton.clicked.connect(self.result)
        self.resultbutton.move(560,300)
        #
        #Result
        self.l3=QtGui.QLabel("Result:",self)
        self.l3.move(530,430)
        self.l4=QtGui.QLabel(self)
        self.l4.move(600,430)
        
        #
        #Info
        self.infobutton = QtGui.QPushButton("Proceed",self)
        self.infobutton.clicked.connect(self.info)
        self.infobutton.move(560,300)
        #
        
        #GUI
        self.exitbutton.setVisible(0)
        self.infobutton.setVisible(0)
        self.resultbutton.setVisible(0)
        self.analyzebutton.setVisible(0)
        self.upperjawbutton.setVisible(0)
        self.lowerjawbutton.setVisible(0)
        self.livefeedAbutton.setVisible(0)
        self.livefeedBbutton.setVisible(0)
        self.d10.setVisible(0)
        self.d11.setVisible(0)
        self.i1.setVisible(0)
        self.i2.setVisible(0)
        self.registerbutton.setVisible(0)
        self.deletebutton.setVisible(0)
        self.savebutton.setVisible(0)
        self.l1.setVisible(0)
        self.r1.setVisible(0)
        self.l2.setVisible(0)
        self.l3.setVisible(0)
        self.l4.setVisible(0)
        self.l5.setVisible(0)
        self.r5.setVisible(0)
        self.l6.setVisible(0)
        self.l7.setVisible(0)
        self.r7.setVisible(0)
        self.l8.setVisible(0)
        self.l9.setVisible(0)
        self.r9.setVisible(0)
        self.l10.setVisible(0)
        self.l11.setVisible(0)
        self.l12.setVisible(0)
        self.setGeometry(0,20,360,240)
    def exitgui(self):
        self.exitbutton.setVisible(0)
        self.l1.setVisible(0)
        self.r1.setVisible(0)
        self.l5.setVisible(0)
        self.r5.setVisible(0)
        self.l7.setVisible(0)
        self.r7.setVisible(0)
        self.l9.setVisible(0)
        self.r9.setVisible(0)
        self.analyzebutton.setVisible(0)
        self.newbutton.setVisible(1)
        self.matchingbutton.setVisible(1)
        self.setGeometry(0,20,360,240)
    def save(self):
        self.l1.setVisible(0)
        self.l2.setVisible(0)
        self.l5.setVisible(0)
        self.l6.setVisible(0)
        self.l7.setVisible(0)
        self.l8.setVisible(0)
        self.l9.setVisible(0)
        self.l10.setVisible(0)
        self.l11.setVisible(0)
        self.l12.setVisible(0)
        self.registerbutton.setVisible(0)
        self.deletebutton.setVisible(0)
        self.savebutton.setVisible(0)
        self.newbutton.setVisible(1)
        self.matchingbutton.setVisible(1)
        self.setGeometry(0,20,360,240)
        name=str(self.l2.text())
        age=str(self.l6.text())
        gender=str(self.l8.text())
        contact=str(self.l10.text())
        email=str(self.l12.text())
        pathmain="/home/pi/Desktop/dentaldatabase.csv"
        if os.path.exists(pathmain):
                 
                 df=pd.read_csv(pathmain,names=['Name','Age','Gender','Contact','Email'],skiprows=1)
                 np_df = df.as_matrix()
                 df = df.append({'Name':name,'Age':age,'Gender':gender,'Contact':contact,'Email':email}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print df
        else:
             columns = ['Name','Age','Gender','Contact','Email']
             df = pd.DataFrame(columns=columns)
             np_df = df.as_matrix()
             
             df = df.append({'Name':name,'Age':age,'Gender':gender,'Contact':contact,'Email':email}, ignore_index=True)
             df.to_csv(pathmain,  index = False)
             print df
    def info(self):
        self.l1.setVisible(1)
        self.l2.setVisible(1)
        self.l5.setVisible(1)
        self.l6.setVisible(1)
        self.l7.setVisible(1)
        self.l8.setVisible(1)
        self.l9.setVisible(1)
        self.l10.setVisible(1)
        self.l11.setVisible(1)
        self.l12.setVisible(1)
        self.registerbutton.setVisible(1)
        self.deletebutton.setVisible(1)
        self.savebutton.setVisible(1)
        self.infobutton.setVisible(0)
        self.upperjawbutton.setVisible(0)
        self.lowerjawbutton.setVisible(0)
        self.livefeedAbutton.setVisible(0)
        self.livefeedBbutton.setVisible(0)
        self.d10.setVisible(0)
        self.d11.setVisible(0)
        self.i1.setVisible(0)
        self.i2.setVisible(0)
        
    def newuser(self):
        #Capture GUI
        
        self.infobutton.setVisible(1)
        self.upperjawbutton.setVisible(1)
        self.lowerjawbutton.setVisible(1)
        self.livefeedAbutton.setVisible(1)
        self.livefeedBbutton.setVisible(1)
        self.d10.setVisible(1)
        self.d11.setVisible(1)
        self.i1.setVisible(1)
        self.i2.setVisible(1)
        
        
        self.newbutton.setVisible(0)
        self.matchingbutton.setVisible(0)
        self.setGeometry(0,20,750,480)
    def result(self):
        self.resultbutton.setVisible(0)
        self.upperjawbutton.setVisible(0)
        self.lowerjawbutton.setVisible(0)
        self.livefeedAbutton.setVisible(0)
        self.livefeedBbutton.setVisible(0)
        self.d10.setVisible(0)
        self.d11.setVisible(0)
        self.i1.setVisible(0)
        self.i2.setVisible(0)
        self.l1.setVisible(1)
        self.r1.setVisible(1)
        self.l5.setVisible(1)
        self.r5.setVisible(1)
        self.l7.setVisible(1)
        self.r7.setVisible(1)
        self.l9.setVisible(1)
        self.r9.setVisible(1)
        self.exitbutton.setVisible(1)
        self.analyzebutton.setVisible(1)
    def matching(self):
        self.resultbutton.setVisible(1)
        self.upperjawbutton.setVisible(1)
        self.lowerjawbutton.setVisible(1)
        self.livefeedAbutton.setVisible(1)
        self.livefeedBbutton.setVisible(1)
        self.d10.setVisible(1)
        self.d11.setVisible(1)
        self.i1.setVisible(1)
        self.i2.setVisible(1)
        
        self.newbutton.setVisible(0)
        self.matchingbutton.setVisible(0)
        self.setGeometry(0,20,750,480)
    def livefeedA(self):
        global liveflagA,liveflagB
        liveflagA=1
        liveflagB=0
    def livefeedB(self):
        global liveflagA,liveflagB
        liveflagB=1
        liveflagA=0
    
    def delete(self):
        if os.path.isfile('/home/pi/Desktop/featurevec.npy'):
                bvali=np.load('/home/pi/Desktop/featurevec.npy')
                lvali=np.load('/home/pi/Desktop/featureveclabel.npy')
                x=len(bvali)-1
                y=len(lvali)-1
                bvali=np.delete(bvali,x,0)
                lvali=np.delete(lvali,x,0)
                np.save('/home/pi/Desktop/featurevec',bvali)
                np.save('/home/pi/Desktop/featureveclabel',lvali)
                print "Data deleted."
                print bvali
                print lvali
        else:
            print "File doesn't exist"  
    def register(self):
        global liveflagA,liveflagB
        liveflagA=0
        liveflagB=0
        img=cv2.imread("/home/pi/Desktop/C1.jpg")
        image=cv2.imread("/home/pi/Desktop/C1.jpg")
        #cv2.imshow('Original 1',img)
        #Position
        #   1    2   3   4   5   6   7   8   9  10  11  12  13
        yi=[120,160,200,260,320,380,390,370,320,260,200,160,120,80] #Vertical
        xi=[120,120,120,120,150,190,260,340,410,410,430,450,460,460] #Horizontal
        #Size
        #   1  2  3  4  5  6  7  8  9  10 11 12 13  
        yf=[40,40,60,60,60,60,60,60,60,60,60,40,40,40] #Width
        xf=[60,60,60,60,60,70,80,70,60,60,60,60,60,60] #Length
        cnt=len(xf)
        #Upper Jaw
        areaval=np.array([])
        for i in xrange(cnt):
            
            print i
            
            crop=img[yi[i]:yi[i]+yf[i], xi[i]:xi[i]+xf[i]]
            
            
            blur = cv2.GaussianBlur(crop,(5,5),0)
            smooth = cv2.addWeighted(blur,1.5,crop,-0.5,0)
            
            grayimg=cv2.cvtColor(smooth,cv2.COLOR_BGR2GRAY)
            bimg=cv2.threshold(grayimg,78, 255, cv2.THRESH_BINARY)[1]
            #if i==5:
                #cv2.imshow('Crop',crop)
                #cv2.imshow('smooth',smooth)
                #cv2.imshow('before',bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            min_size = 0
            max_size = 100000 
            mask = np.zeros((labels.shape))
            z=0
            
            totalarea=0
            for j in range(0, num_labels):
                       if sizes[j] >= min_size and sizes[j] <= max_size:
                            mask[labels == j + 1] = 255
                            #print "Area("+str(z)+"):"+str(sizes[j])
                            totalarea=totalarea+sizes[j]
                            z=z+1
            print "Teeth Area "+str(i+1)+" = "+str(totalarea)
            bimg = cv2.convertScaleAbs(mask)
            print yi[i]
            cv2.putText(image, str(i+1), (xi[i],yi[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
            cv2.rectangle(image,(xi[i],yi[i]),(xi[i]+xf[i],yi[i]+yf[i]),(0,255,0),3)
            areaval=np.hstack([areaval,totalarea])    
        
        #cv2.imshow('Processed',bimg)
        #cv2.imshow('Upper Jaw',img)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                   frame.strides[0], QtGui.QImage.Format_RGB888)
        image=image.scaledToHeight(180)
        self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
        img=cv2.imread("/home/pi/Desktop/C2.jpg")
        image=cv2.imread("/home/pi/Desktop/C2.jpg")
        #cv2.imshow('Original 2',img)
        
        #Position
        #   1    2   3   4   5   6   7   8   9  10  11  12  13
        yi=[390,340,300,240,180,120,90,110,160,220,280,320,360,400] #Vertical
        xi=[120,120,120,120,150,190,260,340,410,410,430,450,460,460] #Horizontal
        #Size
        #   1  2  3  4  5  6  7  8  9  10 11 12 13  
        yf=[40,40,60,60,60,60,60,60,60,60,60,40,40,40] #Width
        xf=[60,60,60,60,60,70,80,70,60,60,60,60,60,60] #Length
        cnt=len(xf)
        #Lower Jaw
        for i in xrange(cnt):
            
            print i
            
            crop=img[yi[i]:yi[i]+yf[i], xi[i]:xi[i]+xf[i]]
            #cv2.imshow('Crop',crop)
            
            blur = cv2.GaussianBlur(crop,(5,5),0)
            smooth = cv2.addWeighted(blur,1.5,crop,-0.5,0)
            #cv2.imshow('smooth',smooth)
            grayimg=cv2.cvtColor(smooth,cv2.COLOR_BGR2GRAY)
            bimg=cv2.threshold(grayimg,20, 255, cv2.THRESH_BINARY)[1]
            #cv2.imshow('before',bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            min_size = 0
            max_size = 100000 
            mask = np.zeros((labels.shape))
            z=0
            
            totalarea=0
            for j in range(0, num_labels):
                       if sizes[j] >= min_size and sizes[j] <= max_size:
                            mask[labels == j + 1] = 255
                            #print "Area("+str(z)+"):"+str(sizes[j])
                            totalarea=totalarea+sizes[j]
                            z=z+1
            print "Teeth Area "+str(i+14)+" = "+str(totalarea)
            bimg = cv2.convertScaleAbs(mask)
            print yi[i]
            cv2.putText(image, str(i+14), (xi[i],yi[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
            cv2.rectangle(image,(xi[i],yi[i]),(xi[i]+xf[i],yi[i]+yf[i]),(0,255,0),3)
            areaval=np.hstack([areaval,totalarea])    
        #print areaval
        nameval=str(self.l2.text())
        if os.path.isfile('/home/pi/Desktop/featurevec.npy'):
                areavali=np.load('/home/pi/Desktop/featurevec.npy')
                labeli=np.load('/home/pi/Desktop/featureveclabel.npy')
                label=np.hstack([labeli,nameval])

                areavali=np.vstack([areavali,areaval])
                np.save('/home/pi/Desktop/featurevec',areavali)
                np.save('/home/pi/Desktop/featureveclabel',label)
                print label
                print areavali
                print areavali.shape
                
        else:
            namelabel=np.array([nameval])
            np.save('/home/pi/Desktop/featurevec',areaval)
            np.save('/home/pi/Desktop/featureveclabel',namelabel)
            print namelabel
            print areaval
        #cv2.imshow('Processed',bimg)
        #cv2.imshow('Lower Jaw',img)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                   frame.strides[0], QtGui.QImage.Format_RGB888)
        image=image.scaledToHeight(180)
        self.i2.setPixmap(QtGui.QPixmap.fromImage(image))
    def analyze(self):
        global liveflagA,liveflagB
        liveflagA=0
        liveflagB=0
        img=cv2.imread("/home/pi/Desktop/C1.jpg")
        #cv2.imshow('Original 1',img)
        #Position
        #   1    2   3   4   5   6   7   8   9  10  11  12  13
        yi=[120,160,200,260,320,380,390,370,320,260,200,160,120,80] #Vertical
        xi=[120,120,120,120,150,190,260,340,410,410,430,450,460,460] #Horizontal
        #Size
        #   1  2  3  4  5  6  7  8  9  10 11 12 13  
        yf=[40,40,60,60,60,60,60,60,60,60,60,40,40,40] #Width
        xf=[60,60,60,60,60,70,80,70,60,60,60,60,60,60] #Length
        cnt=len(xf)
        areaval=np.array([])
        #Upper Jaw
        for i in xrange(cnt):
            
            print i
            
            crop=img[yi[i]:yi[i]+yf[i], xi[i]:xi[i]+xf[i]]
            #cv2.imshow('Crop',crop)
            
            blur = cv2.GaussianBlur(crop,(5,5),0)
            smooth = cv2.addWeighted(blur,1.5,crop,-0.5,0)
            #cv2.imshow('smooth',smooth)
            grayimg=cv2.cvtColor(smooth,cv2.COLOR_BGR2GRAY)
            bimg=cv2.threshold(grayimg,20, 255, cv2.THRESH_BINARY)[1]
            #cv2.imshow('before',bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            min_size = 0
            max_size = 100000 
            mask = np.zeros((labels.shape))
            z=0
            
            totalarea=0
            for j in range(0, num_labels):
                       if sizes[j] >= min_size and sizes[j] <= max_size:
                            mask[labels == j + 1] = 255
                            #print "Area("+str(z)+"):"+str(sizes[j])
                            totalarea=totalarea+sizes[j]
                            z=z+1
            print "Teeth Area "+str(i+1)+" = "+str(totalarea)
            bimg = cv2.convertScaleAbs(mask)
            print yi[i]
            cv2.putText(img, str(i+1), (xi[i],yi[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
            cv2.rectangle(img,(xi[i],yi[i]),(xi[i]+xf[i],yi[i]+yf[i]),(0,255,0),3)
            areaval=np.hstack([areaval,totalarea])    
            

        #cv2.imshow('Processed',bimg)
        #cv2.imshow('Upper Jaw',img)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                   frame.strides[0], QtGui.QImage.Format_RGB888)
        image=image.scaledToHeight(180)
        self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
        img=cv2.imread("/home/pi/Desktop/C2.jpg")
        #cv2.imshow('Original 2',img)
        
        #Position
        #   1    2   3   4   5   6   7   8   9  10  11  12  13
        yi=[390,340,300,240,180,120,90,110,160,220,280,320,360,400] #Vertical
        xi=[120,120,120,120,150,190,260,340,410,410,430,450,460,460] #Horizontal
        #Size
        #   1  2  3  4  5  6  7  8  9  10 11 12 13  
        yf=[40,40,60,60,60,60,60,60,60,60,60,40,40,40] #Width
        xf=[60,60,60,60,60,70,80,70,60,60,60,60,60,60] #Length
        cnt=len(xf)
        #Lower Jaw
        for i in xrange(cnt):
            
            print i
            
            crop=img[yi[i]:yi[i]+yf[i], xi[i]:xi[i]+xf[i]]
            #cv2.imshow('Crop',crop)
            
            blur = cv2.GaussianBlur(crop,(5,5),0)
            smooth = cv2.addWeighted(blur,1.5,crop,-0.5,0)
            #cv2.imshow('smooth',smooth)
            grayimg=cv2.cvtColor(smooth,cv2.COLOR_BGR2GRAY)
            bimg=cv2.threshold(grayimg,20, 255, cv2.THRESH_BINARY)[1]
            #cv2.imshow('before',bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            min_size = 0
            max_size = 100000 
            mask = np.zeros((labels.shape))
            z=0
            
            totalarea=0
            for j in range(0, num_labels):
                       if sizes[j] >= min_size and sizes[j] <= max_size:
                            mask[labels == j + 1] = 255
                            #print "Area("+str(z)+"):"+str(sizes[j])
                            totalarea=totalarea+sizes[j]
                            z=z+1
            print "Teeth Area "+str(i+14)+" = "+str(totalarea)
            bimg = cv2.convertScaleAbs(mask)
            print yi[i]
            cv2.putText(img, str(i+14), (xi[i],yi[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
            cv2.rectangle(img,(xi[i],yi[i]),(xi[i]+xf[i],yi[i]+yf[i]),(0,255,0),3)
            areaval=np.hstack([areaval,totalarea])    
            
        print areaval
        #cv2.imshow('Processed',bimg)
        #cv2.imshow('Lower Jaw',img)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                   frame.strides[0], QtGui.QImage.Format_RGB888)
        image=image.scaledToHeight(180)
        self.i2.setPixmap(QtGui.QPixmap.fromImage(image))
        areastack=np.array([areaval])
        for i in xrange(10):
            areastack=np.vstack([areastack,areaval]) 
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        bval=np.load('/home/pi/Desktop/featurevec.npy')
        lval=np.load('/home/pi/Desktop/featureveclabel.npy')
        scaler=StandardScaler()
        scaler.fit(bval)
        bval=scaler.transform(bval)
        areastack=scaler.transform(areastack)   
        print bval
        print lval
        clf=MLPClassifier(hidden_layer_sizes=(4,4))
        clf.fit(bval,lval)
	    
        nndata=clf.predict(areastack)
        nnproc=Counter(nndata)
        nnresult = nnproc.most_common(1)[0][0]
        print "Data: "+str(nndata)
        print "Result: "+str(nnresult)
        self.r1.setText(str(nnresult))
        afdata="/home/pi/Desktop/dentaldatabase.csv"
        dfaf=pd.read_csv(afdata,names=['Name','Age','Gender','Contact','Email'],skiprows=1)
        afout=np.where(dfaf["Name"] == str(nnresult))
        np_dfaf = dfaf.as_matrix()
         
        afout=afout[0][0]
        name=np_dfaf[afout][0]
        age=np_dfaf[afout][1]
        gender=np_dfaf[afout][2]
        contact=np_dfaf[afout][3]
        email=np_dfaf[afout][4]
        self.r1.setText(str(name))
        self.r5.setText(str(age))
        self.r7.setText(str(gender))
        self.r9.setText(str(contact))
        
    def upperjaw(self):
        global cap
        for i in xrange(30):
            ret, img = cap.read()
        imgname="/home/pi/Desktop/C1.jpg"
                
        
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                   frame.strides[0], QtGui.QImage.Format_RGB888)
        image=image.scaledToHeight(180)
        self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
        cv2.imwrite(imgname,frame)
    def lowerjaw(self):
        global cap
        for i in xrange(30):
            ret, img = cap.read()
        
        imgname="/home/pi/Desktop/C2.jpg"
        
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                   frame.strides[0], QtGui.QImage.Format_RGB888)
        image=image.scaledToHeight(180)
        self.i1.setPixmap(QtGui.QPixmap.fromImage(image))        
        cv2.imwrite(imgname,frame)
    def Loop(self):
        global cap,liveflagA,liveflagB
        
        if liveflagA==1:
            ret, frame = cap.read()
            #Position
            #   1    2   3   4   5   6   7   8   9  10  11  12  13
            yi=[120,160,200,260,320,380,390,370,320,260,200,160,120,80] #Vertical
            xi=[120,120,120,120,150,190,260,340,410,410,430,450,460,460] #Horizontal
            #Size
            #   1  2  3  4  5  6  7  8  9  10 11 12 13  
            yf=[40,40,60,60,60,60,60,60,60,60,60,40,40,40] #Width
            xf=[60,60,60,60,60,70,80,70,60,60,60,60,60,60] #Length
            cnt=len(xf)
            #Upper Jaw
            for i in xrange(cnt):
                cv2.putText(frame, str(i+1), (xi[i],yi[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
                cv2.rectangle(frame,(xi[i],yi[i]),(xi[i]+xf[i],yi[i]+yf[i]),(0,255,0),3)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QtGui.QImage.Format_RGB888)
            image=image.scaledToHeight(180)
            self.i2.setPixmap(QtGui.QPixmap.fromImage(image))
        elif liveflagB==1:
            ret, frame = cap.read()
            #Position
            #   1    2   3   4   5   6   7   8   9  10  11  12  13
            yi=[390,340,300,240,180,120,90,110,160,220,280,320,360,400] #Vertical
            xi=[120,120,120,120,150,190,260,340,410,410,430,450,460,460] #Horizontal
            #Size
            #   1  2  3  4  5  6  7  8  9  10 11 12 13  
            yf=[40,40,60,60,60,60,60,60,60,60,60,40,40,40] #Width
            xf=[60,60,60,60,60,70,80,70,60,60,60,60,60,60] #Length
            cnt=len(xf)
            #Upper Jaw
            for i in xrange(cnt):
                cv2.putText(frame, str(i+1), (xi[i],yi[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
                cv2.rectangle(frame,(xi[i],yi[i]),(xi[i]+xf[i],yi[i]+yf[i]),(0,255,0),3)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QtGui.QImage.Format_RGB888)
            image=image.scaledToHeight(180)
            self.i2.setPixmap(QtGui.QPixmap.fromImage(image))     
        
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
