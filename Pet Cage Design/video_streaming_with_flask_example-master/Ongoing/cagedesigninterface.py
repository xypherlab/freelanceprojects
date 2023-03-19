from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import serial
import pymeanshift as pms
import urllib2
import socket
import datetime
#ser=serial.Serial('COM4',9600,timeout=1)

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,start_time,datedata
        flag=0
        datedata=""
        os.system('start cmd /D /C "python main.py && pause"')
        start_time = time.time()
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
       
        #Head Title
        font = QtGui.QFont("Times", 24)
        self.t1=QtGui.QLabel("Cage Cleaning System",self)
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
        self.d10=QtGui.QLabel("Left Conveyor",self)
        self.d10.move(120,45)
        self.d11=QtGui.QLabel("Right Conveyor",self)
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
        global flag,datedata
        flag=0
        datedata=""
    def scan(self):
        
       
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
        min_size = 1000
        max_size = 50000 
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
        lowerrange = np.array([0,0,0]) #Color
        upperrange = np.array([0,0,0])
        mask = cv2.inRange(segmented_image, lowerrange, upperrange)
        
        mask = cv2.bitwise_not(mask)
        mask = cv2.convertScaleAbs(mask)
        segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
        #cv2.imshow('1st Level',segmented_image)
        self.dispa=QtGui.QPixmap("binaryB.png")
        self.dispa=self.dispa.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
        #Conveyor
        if totalarea>=100:
            #A- Forward B- Stop C- Reverse
            ##############
            #ser.write("A,")
            print "Conveyor Activated: Right Side"
            time.sleep(1)
            #sensordata=ser.readline()
            #print sensordata
            time.sleep(5)
            ###############
            #ser.write("B,")
            print "Conveyor Activated: Right Side"
            time.sleep(1)
            #sensordata=ser.readline()
            #print sensordata
            ##############
            #ser.write("C,")
            print "Conveyor Activated: Right Side"
            time.sleep(1)
            #sensordata=ser.readline()
            #print sensordata
            time.sleep(5)
            ###############
            #ser.write("B,")
            print "Conveyor Activated: Right Side"
            time.sleep(1)
            #sensordata=ser.readline()
            #print sensordata
        
 
    def Loop(self):
        global flag,elapsed_time,start_time,datedata
        elapsed_time=time.time()-start_time
        #flag=1 #Infinite Loop
        if elapsed_time>=1 and flag==1:
            
            #if os.path.exists("imageB.png"):
            #    dump=0
            #    print "Accessed from another host." 
            #else:
            #    webUrl = urllib2.urlopen("http://192.168.43.214:5000/video_feed")
            #    print "Web URL is being used."  
            #Image Left
            yl=0
            xl=0
            hl=480
            wl=320
            yr=0
            xr=320
            hr=480
            wr=640
            original_image = cv2.imread("imageB2.png")
            partL=original_image[yl:yl+hl, xl:xl+wl]
            partR=original_image[yr:yr+hr, xr:xr+wr]
            partL=partL[70:0+430,70:270]
            partR=partR[130:0+450,0:240]
            cv2.imwrite("partL.png",partL)
            cv2.imwrite("partR.png",partR)
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            ######Left Side
            original_image = cv2.filter2D(partL, -1, kernel) 
            #Waste Detection BGR
            (segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=3, 
                                                                  range_radius=3, min_density=25)
            
            
            
            lowerrange = np.array([10,10,10]) #Color
            upperrange = np.array([50,50,50])
            mask = cv2.inRange(segmented_image, lowerrange, upperrange)
            
            mask = cv2.bitwise_not(mask)
            mask = cv2.convertScaleAbs(mask)
            segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
            
            grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
            
            bimg=cv2.threshold(grayimg, 105, 255, cv2.THRESH_BINARY)[1]
            bimg = cv2.bitwise_not(bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            #Size
            min_size = 1000
            max_size = 30000 
            mask = np.zeros((labels.shape))
            z=0
            
            totalarea=0
            for i in range(0, num_labels):
                       if sizes[i] >= min_size and sizes[i] <= max_size:
                            mask[labels == i + 1] = 255

                            totalarea=totalarea+sizes[i]
                            z=z+1
            print "Area Left: "+str(totalarea)
            totalarealeft=totalarea
            bimg = cv2.convertScaleAbs(mask)
            
            mask =bimg
            
            cv2.imwrite("binaryB.png",mask)



            original_image = cv2.filter2D(partR, -1, kernel)
            #######Right Side
            (segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=3, 
                                                                  range_radius=3, min_density=25)
            
            
            
            lowerrange = np.array([10,10,10]) #Color
            upperrange = np.array([50,50,50])
            mask = cv2.inRange(segmented_image, lowerrange, upperrange)
            
            mask = cv2.bitwise_not(mask)
            mask = cv2.convertScaleAbs(mask)
            segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
            
            grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
            
            bimg=cv2.threshold(grayimg, 105, 255, cv2.THRESH_BINARY)[1]
            bimg = cv2.bitwise_not(bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            #Size
            min_size = 1000
            max_size =30000 
            mask = np.zeros((labels.shape))
            z=0
            
            totalarea=0
            for i in range(0, num_labels):
                       if sizes[i] >= min_size and sizes[i] <= max_size:
                            mask[labels == i + 1] = 255

                            totalarea=totalarea+sizes[i]
                            z=z+1
            print "Area Right: "+str(totalarea)
            totalarearight=totalarea
            
            
            cv2.imwrite("binaryA.png",mask)

            ######Display
            self.dispa=QtGui.QPixmap("binaryA.png")
            self.dispa=self.dispa.scaledToHeight(180)
            self.i2.setPixmap(self.dispa)
            self.disp=QtGui.QPixmap("binaryB.png")
            self.disp=self.disp.scaledToHeight(180)
            self.i1.setPixmap(self.disp)
            #Conveyor
            if totalarealeft>=1000 and totalarealeft<=100000:
                #A- Forward B- Stop C- Reverse
                ##############
                #ser.write("C,")
                
                print "Conveyor Activated: Left Side"
                ######################################
                #sensordata=ser.readline()
                #print sensordata
                ######################################
                ###############
                #ser.write("B,")
                now = "Conveyor Activated: Left Side "+str(datetime.datetime.now())+"\n"
                datedata+=now
                for i in xrange(10):
                   
                    try:
                            host = ''       
                            port = 80     

                            
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.settimeout(1)
                            s.bind((host, port))

                            print host , port
                            s.listen(1)
                            conn, addr = s.accept()
                            conn.sendall(datedata)
                            time.sleep(1)
                            conn.close()
                    except:
                        print "No data received"
                #sensordata=ser.readline()
                #print sensordata
                ###############
                
            if totalarearight>=1000 and totalarearight<=100000:
                #A- Forward B- Stop C- Reverse
                ##############
                #ser.write("A,")
                print "Conveyor Activated: Right Side"
                time.sleep(1)
                #sensordata=ser.readline()
                #print sensordata
                time.sleep(10)
                ###############
                #ser.write("B,")
                
                time.sleep(1)
                #sensordata=ser.readline()
                #print sensordata
                ###############
                
            #os.remove("imageB.png")
            
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
