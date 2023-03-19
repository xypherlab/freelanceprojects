from PyQt4 import QtGui, QtCore
import sys 
import time 
import os 
import cv2 
import numpy as np 
import pymeanshift as pms

class Main(QtGui.QMainWindow): 
    def __init__(self): 
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self): 
        global flag,i
        i=0
        flag=0
       
        centralwidget = QtGui.QWidget(self) 

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()

        
      
        self.d3=QtGui.QLabel("Marble Area: ",self)
        self.d3.move(500,220) 
        self.d4=QtGui.QLabel("-----",self)
        self.d4.move(525,240)
        
        self.d5=QtGui.QLabel("Red Area: ",self)
        self.d5.move(590,220)
        self.d6=QtGui.QLabel("-----",self)
        self.d6.move(605,240)

        self.d7=QtGui.QLabel("Area Percentage: ",self)
        self.d7.move(670,220)
        self.d8=QtGui.QLabel("-----",self)
        self.d8.move(685,240)
        
        
        #Head Title
        font = QtGui.QFont("Times", 24)
        self.t1=QtGui.QLabel("Marbling",self)
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
        self.analyzebutton.move(460,140)
        #
        #Record Button
        self.recordbutton = QtGui.QPushButton("Start",self)
        self.recordbutton.clicked.connect(self.recording)
        self.recordbutton.move(560,140)
        #
        #Stop Button
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(660,140)
        #
        
        #Characteristic Title
        font = QtGui.QFont("Times", 16)
        self.t3=QtGui.QLabel("Characteristics",self)
        self.t3.setFont(font)
        self.t3.move(550,180)
        self.t3.resize(350,50)
        #
        #Classification Title
        #font = QtGui.QFont("Times", 16)
        #self.t4=QtGui.QLabel("Classification",self)
        #self.t4.setFont(font)
        #self.t4.move(550,280)
        #self.t4.resize(350,50)

        #self.d9=QtGui.QLabel("-----------",self)
        #self.d9.move(580,330)

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

        
    def recording(self):
        #Camera Start
        global flag,cap,fourcc,out,cameraid
        cameraid=0
        flag=1
        cap = cv2.VideoCapture(cameraid)
        cap.set(3,640)
        cap.set(4,480)
        w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
        h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT); 
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (int(w),int(h)))
        ret, frame = cap.read()
        cv2.imwrite("background.png",frame)
        
        
    def stop(self):
        #Camera Stop
        global flag
        flag=0
        cap.release()
        out.release()
        cv2.destroyAllWindows()  
    def analyze(self): 

        original_image = cv2.imread("imageB1.jpg") #Original Image
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) #Image Sharpening
        original_image = cv2.filter2D(original_image, -1, kernel) #Image Sharpening
        grayimage=cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY) #Grayscale Conversion
        cv2.imshow('Original',original_image)
        bimg=cv2.threshold(grayimage, 120, 255, cv2.THRESH_BINARY)[1] #Binary Threshold
        cv2.imshow('Binary',bimg)
        mask=bimg 
        notredmeat= cv2.bitwise_not(bimg) #Mask for Red Meat
        #Blob Detection with Properties
        output =  cv2.connectedComponentsWithStats(mask)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        #Marble Area
        min_size = 10 
        max_size = 1000
        mask = np.zeros((labels.shape))
        z=0
        
        totalarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size and sizes[i] <= max_size:
                        mask[labels == i + 1] = 255
                        print "Area("+str(z)+"):"+str(sizes[i])
                        totalarea=totalarea+sizes[i]
                        z=z+1
        cv2.imshow('Marble',mask)
        othertotalarea=totalarea #Marble Area
        ############
        bimg = cv2.convertScaleAbs(mask) #Image Property Conversion
        
        mask = notredmeat #Mask for Marbling and Fats
    
        res = cv2.bitwise_and(original_image,original_image,mask = mask) #Marbling and Fats is Removed from the Original Image
        cv2.imshow('Red Meat',res)
        #K-Means Shift
        (segmented_image, labels_image, number_regions) = pms.segment(res, spatial_radius=5, 
                                                              range_radius=5, min_density=100)
        #
        cv2.imshow('Red Segment',segmented_image)
        cv2.imwrite('redsegment.jpg',segmented_image)
        #Color Segmentation
        lowerrange = np.array([0,0,0])
        upperrange = np.array([30,30,30])
        #
        #Red Meat Isolation
        mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        redmeat= cv2.bitwise_not(mask)
        #
        cv2.imshow('Red Mask',redmeat)
        #Blob Detection for Red Meat
        output =  cv2.connectedComponentsWithStats(redmeat)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 0 
        mask = np.zeros((labels.shape))
        z=0
        
        totalarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size:
                        mask[labels == i + 1] = 255
                        print "Area("+str(z)+"):"+str(sizes[i])
                        totalarea=totalarea+sizes[i]
                        z=z+1
        ###################                
        print "Marble Area: "+str(othertotalarea)
        print "Red Meat Area: "+str(totalarea)
        meatgrade=float(othertotalarea)/float(totalarea)
        print "Grade Percentage: "+str(meatgrade*100)+" %"
        self.d4.setText(str(othertotalarea))
        self.d6.setText(str(totalarea))
        self.d8.setText(str(meatgrade*100)+" %") 
        #self.disp=QtGui.QPixmap("binaryB.png")
        #self.disp=self.disp.scaledToHeight(180)
        #self.i1.setPixmap(self.disp)
      

 
    def Loop(self):
        global flag,cap,fourcc,out,i
        
        #Live View    
        if flag==1:
            
                ret, frame = cap.read()
                out.write(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                           frame.strides[0], QtGui.QImage.Format_RGB888)
                image=image.scaledToHeight(180)
                self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
        #####
                 
            
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
