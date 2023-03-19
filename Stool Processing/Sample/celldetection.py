import cv2
import numpy as np
from PyQt4 import QtGui, QtCore
import sys
import time
import os
import pymeanshift as pms
import math
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
        self.setGeometry(0,20,400,200)
    
    
    def Loop(self):
        def adjust_gamma(image, gamma=1.0):
            # build a lookup table mapping the pixel values [0, 255] to
            # their adjusted gamma values
            invGamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** invGamma) * 255
                    for i in np.arange(0, 256)]).astype("uint8")
     
            # apply gamma correction using the lookup table
            return cv2.LUT(image, table)
        stoolimage = cv2.imread("Sample1.2.jpg")
        stoolimage = adjust_gamma(stoolimage, gamma=0.5)
        #Sample 1 and 2 failed
        cv2.imshow('Original Image',stoolimage)
        #Threshold
        threshold=190 #Up to 255
        ##########
        #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) 
        #stoolimage = cv2.filter2D(stoolimage, -1, kernel) 
        grayimage=cv2.cvtColor(stoolimage,cv2.COLOR_BGR2GRAY)
        cv2.imshow('Gray Image',grayimage)
            
        bilateral_filtered_image = cv2.bilateralFilter(grayimage, 5, 175, 175)
        edge_detected_image = cv2.Canny(bilateral_filtered_image, 105, 200)
        cv2.imshow('Edge', edge_detected_image)
        
        bimg=edge_detected_image
        output =  cv2.connectedComponentsWithStats(bimg)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 200 #Change
        max_size = 1000000 #Change
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
        print "Total Area: "+str(totalarea)
        print "# of Cell Detected: "+str(z)
        cellmask = cv2.convertScaleAbs(mask)
        cv2.imshow('Cell', cellmask)
        circles = cv2.HoughCircles(cellmask,cv2.HOUGH_GRADIENT,1,170,
                            param1=30,param2=15,minRadius=50,maxRadius=120)
        circles = np.uint16(np.around(circles))
        print circles
        val=0
        inval=0
        copyimg=stoolimage.copy()
        for i in circles[0,:]:
            
            cv2.circle(copyimg,(i[0],i[1]),i[2],(0,255,0),-1)
        cv2.imshow('Outer',copyimg)
        lowerrange = np.array([0,255,0])
        upperrange = np.array([0,255,0])
        mask = cv2.inRange(copyimg, lowerrange, upperrange)
        mask = cv2.convertScaleAbs(mask)  
        maskinv=cv2.bitwise_not(mask)
        
        cv2.imshow('Mask',mask)
        outputimage = cv2.bitwise_and(stoolimage,stoolimage,mask = mask)
        maskref=outputimage.copy()
        cv2.imshow('Segmented',outputimage)
        
        bilateral_filtered_image = cv2.bilateralFilter(outputimage, 5, 175, 175)
        edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
        cv2.imshow('Edge', edge_detected_image)
        
        #adjusted = adjust_gamma(outputimage, gamma=0.1)
        #cv2.imshow('Gamma Correction',adjusted)

        
        
        #outputimage=adjusted
        threshold=100
        grayimage=cv2.cvtColor(outputimage,cv2.COLOR_BGR2GRAY)
        
        bimg=cv2.threshold(grayimage, threshold, 255, cv2.THRESH_BINARY)[1]
        bimg=cv2.bitwise_not(bimg)
        bimg=bimg-maskinv
        
        cv2.imshow('Binary 1', bimg)
        
        circles = cv2.HoughCircles(bimg,cv2.HOUGH_GRADIENT,1,30,
                            param1=30,param2=15,minRadius=15,maxRadius=40)
        circles = np.uint16(np.around(circles))
        print circles
        val=0
        inval=0
        for i in circles[0,:]:
            
            cv2.circle(outputimage,(i[0],i[1]),i[2],(0,255,0),2)
            print i
            maskimg=maskref
            img=np.zeros((1024,1280,3),np.uint8)
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),-1)
            cirarea=math.pow(i[2],2)*math.pi
            print cirarea
            convarea=(float(cirarea)/float(3800))*15
            print "Circle Area: "+str(convarea)+" u"
            #cv2.putText(outputimage, str(convarea)+" u", (i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
            
            cgrayimage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            mask=cv2.threshold(cgrayimage, threshold, 255, cv2.THRESH_BINARY)[1]
            typeimg = cv2.bitwise_and(maskimg,maskimg,mask = mask)
            cgrayimage=cv2.cvtColor(typeimg,cv2.COLOR_BGR2GRAY)
            bimg=cv2.threshold(cgrayimage, threshold, 255, cv2.THRESH_BINARY)[1]
            #cv2.imshow('Mask Circle'+str(i), bimg)
            output =  cv2.connectedComponentsWithStats(bimg)
            num_labels = output[0]-1
            labels = output[1]
            stats = output[2]
            centroids = output[3]	    
            sizes = stats[1:, -1]
            min_size = 50 #Change
            max_size = 1200 #Change
            mask = np.zeros((labels.shape))
            z=0
            totalarea=0
            j=i
            for i in range(0, num_labels):
                       if sizes[i] >= min_size and sizes[i] <= max_size:
                            mask[labels == i + 1] = 255
                            #print "Area("+str(z)+"):"+str(sizes[i])
                            totalarea=totalarea+sizes[i]
                            z=z+1
            #print "Total Area: "+str(totalarea)
            #print "# of Cell Detected: "+str(z)
            mask = cv2.convertScaleAbs(mask)
            
            cv2.imshow('Mask Bound'+str(j), mask)
            if totalarea<1000:
                val=val+1
            else:
                inval=inval+1
        print "Valid: "+str(val)
        print "Invalid: "+str(inval)
        cv2.imshow('Watershed Transform', outputimage)
        cv2.waitKey(0) 
                
    
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
