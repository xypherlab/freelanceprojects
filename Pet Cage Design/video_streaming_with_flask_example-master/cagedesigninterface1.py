from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import serial
import pymeanshift as pms
##ser=#serial.#serial('/dev/ttyAMA0',9600,timeout=1)
import urllib2
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,start_time
        #os.system('python main.py')
        os.system('start cmd /D /C "python main.py && pause"')
        #os.system('open -a Terminal python main.py')
        flag=0
        start_time = time.time()
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
       
        #Head Title
        font = QtGui.QFont("Times", 24)
        self.t1=QtGui.QLabel("` Cleaning System",self)
        self.t1.setFont(font)
        self.t1.move(160,10)
        self.t1.resize(350,50)
        #
        
        #scan Button
        self.scanbutton = QtGui.QPushButton("Scan",self)
        self.scanbutton.clicked.connect(self.scan)
        self.scanbutton.move(150,280)
        #
        
        self.startbutton = QtGui.QPushButton("Start",self)
        self.startbutton.clicked.connect(self.start)
        self.startbutton.move(260,280)
        #
        
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(370,280)
        #
        
        #Side Title
        self.d10=QtGui.QLabel("Camera A",self)
        self.d10.move(120,45)
        self.d11=QtGui.QLabel("Camera B",self)
        self.d11.move(400,45)
        #
        #Image Display Left
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(50,60,230,200)
        self.disp=QtGui.QPixmap("blackscreen.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)
        #
        #Image Display Right
        self.i2=QtGui.QLabel(self)
        self.i2.setGeometry(310,60,400,200)
        self.dispa=QtGui.QPixmap("blackscreen.png")
        self.dispa=self.disp.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
        #
        self.setGeometry(0,20,600,380)
        
    
    def start(self):
        global flag
        flag=1
    def stop(self):
        global flag
        flag=0
    def scan(self):
        #i=0
        #while i<5:
        #    try:
        #            sensordata=#ser.readline()
        #            s0=float(sensordata.split(",")[0]) 
        #            #print s0          
        #            i=i+1            
        #    except:
        #        dump=0
        
        #cap=cv2.VideoCapture(1)
        #cap.set(3,640)
        #cap.set(4,480)
        #cap1=cv2.VideoCapture(0)
        #cap1.set(3,640)
        #cap1.set(4,480)
        #i=0
        #while i<30:
            #ret, frame = cap.read()
            #ret1, frame1 = cap1.read()
            #i=i+1
        
        #cv2.imwrite("imageA.jpg",frame)
        #cv2.imwrite("imageB.jpg",frame1)
        
        #cap.release()
        #cap1.release()
        
        #Image Left
       
        original_image = cv2.imread("imageB.jpg")
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        original_image = cv2.filter2D(original_image, -1, kernel) 
       
        (segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
        grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
        
        bimg=cv2.threshold(grayimg, 105, 255, cv2.THRESH_BINARY)[1]
        bimg = cv2.bitwise_not(bimg)
        #cv2.imshow('1st Level',bimg)
        output =  cv2.connectedComponentsWithStats(bimg)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        #Size
        min_size = 0 
        max_size = 100000 
        mask = np.zeros((labels.shape))
        z=0
        
        totalarea=0
        for i in range(0, num_labels):
                   if sizes[i] >= min_size and sizes[i] <= max_size:
                        mask[labels == i + 1] = 255
                        #print "Area("+str(z)+"):"+str(sizes[i])
                        totalarea=totalarea+sizes[i]
                        z=z+1
        print "Area: "+str(totalarea)
        bimg = cv2.convertScaleAbs(mask)
        
        mask =bimg
        #cv2.imshow('Binary',bimg)
        res = cv2.bitwise_and(original_image,original_image,mask = mask)
        (segmented_image, labels_image, number_regions) = pms.segment(res, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
        
        cv2.imwrite("binaryB.png",segmented_image)
        
               
        #Waste Detection BGR
        lowerrange = np.array([20,20,20]) #Color
        upperrange = np.array([90,90,90])
        mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        
        mask = cv2.bitwise_not(mask)
        mask = cv2.convertScaleAbs(mask)
        segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
        #cv2.imshow('1st Level',segmented_image)
        self.dispa=QtGui.QPixmap("binaryB.png")
        self.dispa=self.dispa.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
        #Conveyor
        if totalarea>100:
            #A- Forward B- Stop C- Reverse
            ##############
            #ser.write("A,")
            print "Conveyor Activated: Right Side"
            time.sleep(1)
            #sensordata=#ser.readline()
            #print sensordata
            time.sleep(5)
            ###############
            #ser.write("B,")
            print "Conveyor Activated: Right Side"
            time.sleep(1)
            #sensordata=#ser.readline()
            #print sensordata
            
        ##Image Right
        #original_image = cv2.imread("imageA.jpg")
        #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        #original_image = cv2.filter2D(original_image, -1, kernel) 
       
        #(segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=3, 
        #                                                      range_radius=3, min_density=25)
        #grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
        
        #bimg=cv2.threshold(grayimg, 105, 255, cv2.THRESH_BINARY)[1]
        #bimg = cv2.bitwise_not(bimg)
        
        #output =  cv2.connectedComponentsWithStats(bimg)
        #num_labels = output[0]-1
        #labels = output[1]
        #stats = output[2]
        #centroids = output[3]	    
        ##sizes = stats[1:, -1]
        #min_size = 5000 
        #max_size = 100000 
        #mask = np.zeros((labels.shape))
        #z=0
        
        #totalarea=0
        #for i in range(0, num_labels):
        #           if sizes[i] >= min_size and sizes[i] <= max_size:
        #                mask[labels == i + 1] = 255
        #                #print "Area("+str(z)+"):"+str(sizes[i])
        #                totalarea=totalarea+sizes[i]
        #                z=z+1

        #bimg = cv2.convertScaleAbs(mask)
        
        #mask =bimg
        #cv2.imshow('Binary',bimg)
        #res = cv2.bitwise_and(crop_img,crop_img,mask = mask)
        #(segmented_image, labels_image, number_regions) = pms.segment(res, spatial_radius=3, 
        #                                                      range_radius=3, min_density=25)
        
        #cv2.imwrite("binaryA.png",segmented_image)
        
               
        #Waste Detection
        #lowerrange = np.array([20,20,20])
        #upperrange = np.array([90,90,90])
        #mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        
        #mask = cv2.bitwise_not(mask)
        #mask = cv2.convertScaleAbs(mask)
        #segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
        #cv2.imshow('1st Level',segmented_image)
        
 
    def Loop(self):
        
        global flag,elapsed_time,start_time
        elapsed_time=time.time()-start_time
        
        if elapsed_time>=5 and flag==1:
           
            if os.path.exists("imageB.png"):
                dump=0
                print "Accessed from another host." 
            else:
                webUrl = urllib2.urlopen("http://192.168.43.214:5000/video_feed")
                print "Web URL is being used."   
            #Image Left
            
            original_image = cv2.imread("imageB.png")
            #cv2.imwrite("imageB.png",original_image)
            
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            original_image = cv2.filter2D(original_image, -1, kernel) 
           
            (segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=3, 
                                                                  range_radius=3, min_density=25)
            grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
            
            bimg=cv2.threshold(grayimg, 105, 255, cv2.THRESH_BINARY)[1]
            bimg = cv2.bitwise_not(bimg)
            #cv2.imshow('1st Level',bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            #Size
            min_size = 0 
            max_size = 100000 
            mask = np.zeros((labels.shape))
            z=0
            
            totalarea=0
            for i in range(0, num_labels):
                       if sizes[i] >= min_size and sizes[i] <= max_size:
                            mask[labels == i + 1] = 255
                            #print "Area("+str(z)+"):"+str(sizes[i])
                            totalarea=totalarea+sizes[i]
                            z=z+1
            print "Area: "+str(totalarea)
            
            bimg = cv2.convertScaleAbs(mask)
            
            mask =bimg
            #cv2.imshow('Binary',bimg)
            res = cv2.bitwise_and(original_image,original_image,mask = mask)
            (segmented_image, labels_image, number_regions) = pms.segment(res, spatial_radius=3, 
                                                                  range_radius=3, min_density=25)
            
            cv2.imwrite("binaryB.png",segmented_image)
            
                   
            #Waste Detection BGR
            lowerrange = np.array([20,20,20]) #Color
            upperrange = np.array([90,90,90])
            mask = cv2.inRange(segmented_image, lowerrange, upperrange)
            
            mask = cv2.bitwise_not(mask)
            mask = cv2.convertScaleAbs(mask)
            segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
            #cv2.imshow('1st Level',segmented_image)
            self.dispa=QtGui.QPixmap("binaryB.png")
            self.dispa=self.dispa.scaledToHeight(180)
            self.i2.setPixmap(self.dispa)
            #Conveyor
            if totalarea>100:
                #A- Forward B- Stop C- Reverse
                ##############
                #ser.write("A,")
                print "Conveyor Activated: Right Side"
                time.sleep(1)
                #sensordata=#ser.readline()
                #print sensordata
                time.sleep(10)
                ###############
                #ser.write("B,")
                print "Conveyor Activated: Right Side"
                time.sleep(1)
                #sensordata=#ser.readline()
                #print sensordata
                ###############
            os.remove("imageB.png")    
                     
            
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
    
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
