import cv2
import numpy as np
from PyQt4 import QtGui, QtCore
import sys
import time
import os
import pymeanshift as pms
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
        self.process = QtGui.QPushButton("Process",self)
        self.process.clicked.connect(self.processstool)
        self.process.move(150,100)
        self.setGeometry(0,20,400,200)
    def processstool(self):
        stoolimage = cv2.imread("stool1.jpg")
        cv2.imshow('Original Image',stoolimage)
        #Threshold
        threshold=220 #Up to 255
        ##########
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) 
        stoolimage = cv2.filter2D(stoolimage, -1, kernel) 
        grayimage=cv2.cvtColor(stoolimage,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Gray Image',grayimage)
        bimg=cv2.threshold(grayimage, threshold, 255, cv2.THRESH_BINARY)[1]
        bimg= cv2.bitwise_not(bimg)
        #cv2.imshow('Binary Image',bimg)
        output =  cv2.connectedComponentsWithStats(bimg)
        num_labels = output[0]-1
        labels = output[1]
        stats = output[2]
        centroids = output[3]	    
        sizes = stats[1:, -1]
        min_size = 20000 #Change
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
        print "Total Area: "+str(totalarea)
        print "# of Cell Detected: "+str(z)
        mask = cv2.convertScaleAbs(mask)
        cv2.imshow('Filtered',mask)
        outputimage = cv2.bitwise_and(stoolimage,stoolimage,mask = mask)
        cv2.imshow('Segmented',outputimage)
        grayimage=cv2.cvtColor(outputimage,cv2.COLOR_BGR2GRAY)
        cv2.imshow('Gray Image',grayimage)
        threshold=170
        bimg=cv2.threshold(grayimage, threshold, 255, cv2.THRESH_BINARY)[1]
        bimg= cv2.bitwise_not(bimg)
        cv2.imshow('Binary Image',bimg)
        cv2.waitKey(0) 
    def Loop(self):
        stoolimage = cv2.imread("sample8.jpg")
        #Sample 1 and 2 failed
        cv2.imshow('Original Image',stoolimage)
        #Threshold
        threshold=200 #Up to 255
        ##########
        #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) 
        #stoolimage = cv2.filter2D(stoolimage, -1, kernel) 
        grayimage=cv2.cvtColor(stoolimage,cv2.COLOR_BGR2GRAY)
        cv2.imshow('Gray Image',grayimage)
        bimg=cv2.threshold(grayimage, threshold, 255, cv2.THRESH_BINARY)[1]
        
        #ret, thresh = cv2.threshold(grayimage,220,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        
        bimg= cv2.bitwise_not(bimg)
        
        cv2.imshow('Binary Image',bimg)
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
        print "Total Area: "+str(totalarea)
        print "# of Cell Detected: "+str(z)
        cellmask = cv2.convertScaleAbs(mask)
        cv2.imshow('Binary Mask',cellmask)
        im_floodfill = cellmask.copy()
        h, w = cellmask.shape[:2]
        maskzero = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(im_floodfill, maskzero, (0,0), 255);
        fillmask=cv2.bitwise_not(im_floodfill)
        mask=fillmask+cellmask
        cv2.imshow('Filled Mask',mask)
        
        mask = cv2.convertScaleAbs(mask)
        
        outputimage = cv2.bitwise_and(stoolimage,stoolimage,mask = mask)
        cv2.imshow('Segmented',outputimage)
        (segmented_image, labels_image, number_regions) = pms.segment(outputimage, spatial_radius=3, 
                                                              range_radius=3, min_density=20)
        cv2.imshow('Mean Shift',segmented_image)
        threshold=100
        grayimage=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
        bimg=cv2.threshold(grayimage, threshold, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow('Binary 1', bimg)
        bilateral_filtered_image = cv2.bilateralFilter(outputimage, 5, 175, 175)
        edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
        cv2.imshow('Edge', edge_detected_image )
        extract=mask-edge_detected_image
        cv2.imshow('Extract', extract )
        #kernel = np.ones((1,20), np.uint8)  # note this is a horizontal kernel
        #d_im = cv2.dilate(edge_detected_image, kernel, iterations=1)
        #cv2.imshow('Edge', d_im )
        contours,hiearchy=cv2.findContours(edge_detected_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(outputimage,contours,-1,(0,255,0),3) 
        
        cv2.imshow('Objects Detected',outputimage)        
        cv2.waitKey(0) 
                
    
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
