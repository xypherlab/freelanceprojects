from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import serial
import pymeanshift as pms
#ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)

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
        #Shape
        self.d3=QtGui.QLabel("Shape: ",self)
        self.d3.move(440,220)
        self.d4=QtGui.QLabel("-----",self)
        self.d4.move(425,240)
        #
        #Color
        self.d5=QtGui.QLabel("Color: ",self)
        self.d5.move(510,220)
        self.d6=QtGui.QLabel("-----",self)
        self.d6.move(505,240)
        #
        #Weight
        self.d1=QtGui.QLabel("Weight: ",self)
        self.d1.move(620,220)
        self.d2=QtGui.QLabel("-----",self)
        self.d2.move(595,240)
        #
        #Spots
        self.d7=QtGui.QLabel("Spots: ",self)
        self.d7.move(720,220)
        self.d8=QtGui.QLabel("-----",self)
        self.d8.move(720,240)
        #
        #Head Title
        font = QtGui.QFont("Times", 24)
        self.t1=QtGui.QLabel("Eggplant Classifier",self)
        self.t1.setFont(font)
        self.t1.move(270,10)
        self.t1.resize(350,50)
        #
        #Command Title
        font = QtGui.QFont("Times", 16)
        self.t2=QtGui.QLabel("Commands",self)
        self.t2.setFont(font)
        self.t2.move(570,80)
        self.t2.resize(350,50)
        #
        #Analyze Button
        self.analyzebutton = QtGui.QPushButton("Analyze",self)
        self.analyzebutton.clicked.connect(self.analyze)
        self.analyzebutton.move(560,140)
        #
        #Characteristic Title
        font = QtGui.QFont("Times", 16)
        self.t3=QtGui.QLabel("Characteristics",self)
        self.t3.setFont(font)
        self.t3.move(550,180)
        self.t3.resize(350,50)
        #
        #Classification Title
        font = QtGui.QFont("Times", 16)
        self.t4=QtGui.QLabel("Classification",self)
        self.t4.setFont(font)
        self.t4.move(550,280)
        self.t4.resize(350,50)
        #
        #Spots
        self.d9=QtGui.QLabel("-----------",self)
        self.d9.move(580,330)
        #
        #Side Title
        self.d10=QtGui.QLabel("Side A",self)
        self.d10.move(200,45)
        self.d11=QtGui.QLabel("Side B",self)
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
        self.setGeometry(0,20,800,480)
        
    def analyze(self):
        #i=0
        #while i<5:
        #    try:
        #            sensordata=ser.readline()
        #            s0=float(sensordata.split(",")[0]) #Weight Parameter
        #            print s0
        #            self.d2.setText(str(s0)+" grams")            
        #            i=i+1            
        #    except:
        #        dump=0
        #s0=s0+8 #Weight        
        #cap=cv2.VideoCapture(1)
        #cap.set(3,640)
        #cap.set(4,480)
        #cap1=cv2.VideoCapture(0)
        #cap1.set(3,640)
        #cap1.set(4,480)
        #i=0
        #while i<30:
        #    ret, frame = cap.read()
        #    ret1, frame1 = cap1.read()
        #    i=i+1
        
        #cv2.imwrite("imageA.jpg",frame)
        #cv2.imwrite("imageB.jpg",frame1)
        
        #cap.release()
        #cap1.release()
        s0=106 #Dummy Data
        #Image Left
        original_image = cv2.imread("imageB.jpg")
        y=0
        x=140
        h=350
        w=500
        crop_img = original_image[y:y+h, x:x+w]
        (segmented_image, labels_image, number_regions) = pms.segment(crop_img, spatial_radius=3, 
                                                              range_radius=3, min_density=50)
        grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
        
        bimg=cv2.threshold(grayimg, 125, 255, cv2.THRESH_BINARY)[1]
        bimg = cv2.bitwise_not(bimg)
        
        output =  cv2.connectedComponentsWithStats(bimg)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 5000 #Change
        max_size = 100000 #Change
        mask = np.zeros((labels.shape))
        z=0
        #print "Minimum Setting Area: "+str(min_size)
        #print "Maximum Setting Area: "+str(max_size)
        totalarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size and sizes[i] <= max_size:
                        mask[labels == i + 1] = 255
                        print "Area("+str(z)+"):"+str(sizes[i])
                        totalarea=totalarea+sizes[i]
                        z=z+1
        othertotalarea=totalarea
        print "Total Area A: "+str(othertotalarea)
        bimg = cv2.convertScaleAbs(mask)
        
        mask =bimg
    
        res = cv2.bitwise_and(crop_img,crop_img,mask = mask)
        (segmented_image, labels_image, number_regions) = pms.segment(res, spatial_radius=3, 
                                                              range_radius=3, min_density=50)
        cv2.imwrite("binaryB.png",segmented_image)
        #Skin Removal
        lowerrange = np.array([40,40,40])
        upperrange = np.array([90,90,90])
        mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        mask = cv2.bitwise_not(mask)
        mask = cv2.convertScaleAbs(mask)
        segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
        
        #Noise Removal
        lowerrange = np.array([80,80,80])
        upperrange = np.array([120,120,120])
        mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        mask = cv2.bitwise_not(mask)
        mask = cv2.convertScaleAbs(mask)
        segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
        
        
        output =  cv2.connectedComponentsWithStats(mask)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 0 
        max_size = 100000
        mask = np.zeros((labels.shape))
        z=0
        spotarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size and sizes[i] <= max_size:
                        mask[labels == i + 1] = 255
                        print "Area("+str(z)+"):"+str(sizes[i])
                        spotarea=spotarea+sizes[i]
                        z=z+1
        otherspotarea=spotarea
        print "Spot Area A: "+str(otherspotarea)
        self.disp=QtGui.QPixmap("binaryB.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)
        #


        
        #Image Right
        original_image = cv2.imread("imageA.jpg")
        y=0
        x=0
        h=390
        w=500
        crop_img = original_image[y:y+h, x:x+w]
        (segmented_image, labels_image, number_regions) = pms.segment(crop_img, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
        grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
        
        bimg=cv2.threshold(grayimg, 105, 255, cv2.THRESH_BINARY)[1]
        bimg = cv2.bitwise_not(bimg)
        
        output =  cv2.connectedComponentsWithStats(bimg)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 5000 #Change
        max_size = 100000 #Change
        mask = np.zeros((labels.shape))
        z=0
        print "Minimum Setting Area: "+str(min_size)
        print "Maximum Setting Area: "+str(max_size)
        totalarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size and sizes[i] <= max_size:
                        mask[labels == i + 1] = 255
                        print "Area("+str(z)+"):"+str(sizes[i])
                        totalarea=totalarea+sizes[i]
                        z=z+1
        ctotal=totalarea
        print "Total Area B: "+str(ctotal)
        bimg = cv2.convertScaleAbs(mask)
        
        mask =bimg
        #cv2.imshow('Binary',bimg)
        #bimg = cv2.convertScaleAbs(bimg)
        im,contours,hiearchy=cv2.findContours(bimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        print len(contours)
        for cnt in contours:

            leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
            rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
            topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
            bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

            

            print "Left: "+str(leftmost[0])
            #print "Right: "+str(rightmost[0])
            #print "Top: "+str(topmost[1])
            #toppointA=topmost[1]
            #midpoint=leftmost[0]+(rightmost[0]-leftmost[0])/2
            #print "Midpoint: "+str(midpoint)
            
            
        res = cv2.bitwise_and(crop_img,crop_img,mask = mask)
        (segmented_image, labels_image, number_regions) = pms.segment(res, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
        
        cv2.imwrite("binaryA.png",segmented_image)
        #Pixel Height and Curvature Measurement
        y=0
        x=midpoint
        h=390
        w=2
        happrox = segmented_image[y:y+h, x:x+w]
        grayimg=cv2.cvtColor(happrox,cv2.COLOR_BGR2GRAY)
        himg=cv2.threshold(grayimg, 5, 255, cv2.THRESH_BINARY)[1]
        output =  cv2.connectedComponentsWithStats(himg)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 0 #Change
        max_size = 100000 #Change
        mask = np.zeros((labels.shape))
        z=0
        #print "Minimum Setting Area: "+str(min_size)
        #print "Maximum Setting Area: "+str(max_size)
        totalarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size and sizes[i] <= max_size:
                        mask[labels == i + 1] = 255
                        print "Area("+str(z)+"):"+str(sizes[i])
                        totalarea=totalarea+sizes[i]
                        z=z+1
        
        himg = cv2.convertScaleAbs(mask)
        cv2.imwrite("height.png",himg)
        im,contours,hiearchy=cv2.findContours(himg,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        #print len(contours)
        for cnt in contours:

            leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
            rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
            topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
            bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

            print "Top: "+str(topmost[1])
            toppointB=topmost[1]
            print "Bottom: "+str(bottommost[1])
            curvature=toppointB-toppointA
            height=bottommost[1]-topmost[1]
            print "Curvature Distance: "+str(curvature)
            print "Thickness: "+str(height)
            
        ix=311
        iy=351
        cropimg=segmented_image[iy:iy+10,ix:ix+10]
        
        red = int(cropimg[5,5,2])
        print "Red: "+str(red)
        green = int(cropimg[5,5,1])
        print "Green: "+str(green)
        blue = int(cropimg[5,5,0])
        print "Blue: "+str(blue)
        
        #Skin Removal
        lowerrange = np.array([40,40,40])
        upperrange = np.array([90,90,90])
        mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        
        mask = cv2.bitwise_not(mask)
        mask = cv2.convertScaleAbs(mask)
        segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
        #cv2.imshow('1st Level',segmented_image)
        #Noise Removal
        lowerrange = np.array([80,80,80])
        upperrange = np.array([120,120,120])
        mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        
        mask = cv2.bitwise_not(mask)
        mask = cv2.convertScaleAbs(mask)
        segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
        grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
        mask=cv2.threshold(grayimg, 5, 255, cv2.THRESH_BINARY)[1]
        #cv2.imshow('2nd Level',mask)
        
        output =  cv2.connectedComponentsWithStats(mask)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 0 
        max_size = 100000
        mask = np.zeros((labels.shape))
        z=0
        spotarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size and sizes[i] <= max_size:
                        mask[labels == i + 1] = 255
                        print "Area("+str(z)+"):"+str(sizes[i])
                        spotarea=spotarea+sizes[i]
                        z=z+1
        print "Spot Area B: "+str(spotarea)
        spotpercent=(float(spotarea+otherspotarea)/float(ctotal+othertotalarea))*100
        print "Spot Percentage: "+str(spotpercent)
    
        
        self.dispa=QtGui.QPixmap("binaryA.png")
        self.dispa=self.dispa.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
   
        if s0>=0 and s0<101:
            self.d2.setText(str(s0)+" g - Small")
        elif s0>=101 and s0<200:
            self.d2.setText(str(s0)+" g - Medium")
        elif s0>=200:
            self.d2.setText(str(s0)+" g - Large")
            
        #
        if red>=80 and red<=100 and green>=90 and green<=110 and blue>=60 and blue<=80:
            self.d6.setText("Green") #Color
        else:
            self.d6.setText("Purple") #Color
            
        if curvature<20:
            curve=1
            print "Level 1 Curve"
        elif curvature>20 and curvature<=30:
            curve=2
            print "Level 2 Curve"
        elif curvature>30:
            curve=3
            print "Level 3 Curve"
        if height<90:
            self.d4.setText("Elongated") #Shape
        else:
            self.d4.setText("Round") #Shape
        
        #
        self.d8.setText(str("%.2f" % spotpercent)+" %") #Spots
        if spotpercent<10 and curve==1:
            self.d9.setText("Extra Class") #Classification
        elif spotpercent>=10 and spotpercent<20 and curve<3:
            self.d9.setText("Class 1") #Classification
        elif spotpercent>=20 and spotpercent<30 or curve==3:
            self.d9.setText("Class 2") #Classification
 
    def Loop(self):
        x=0

                 
            
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
