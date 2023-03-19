from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import pymeanshift as pms
from skimage import measure
import wx
np.set_printoptions(threshold=sys.maxsize)
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
	global liveflag,cap,openflag
	openflag=0
	liveflag=0
	cap=cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)
	time.sleep(1)
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
	self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(100,60,400,200)
	self.disp=QtGui.QPixmap("blackscreen.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)
	self.i2=QtGui.QLabel(self)
        self.i2.setGeometry(420,60,400,200)
	self.dispa=QtGui.QPixmap("blackscreen.png")
        self.dispa=self.disp.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
	self.livefeedbutton = QtGui.QPushButton("Live View",self)
        self.livefeedbutton.clicked.connect(self.livefeed)
        self.livefeedbutton.move(200,420)
	self.processbutton = QtGui.QPushButton("Process",self)
        self.processbutton.clicked.connect(self.process)
        self.processbutton.move(320,420)
	self.browse = QtGui.QPushButton("Open File",self)
        self.browse.clicked.connect(self.opendialog)
	self.browse.move(440,420)
	self.t1=QtGui.QLabel("Result: ",self)
        self.t1.move(290,370)
        self.t2=QtGui.QLabel("-----",self)
        self.t2.move(370,370)
        self.t2.resize(130,30)

        self.t3=QtGui.QLabel("Count: ",self)
        self.t3.move(290,340)
        self.t4=QtGui.QLabel("-----",self)
        self.t4.move(370,340)
        self.t4.resize(130,30)
        
	self.setGeometry(0,20,720,480)
    def process(self):
        global pathfile,liveflag
        liveflag=2
        
        

    def livefeed(self):
        global liveflag
	if liveflag==0:
        	liveflag=1
	elif liveflag==1:
		liveflag=0
    def opendialog(self):
        global pathfile,openflag,liveflag
        if openflag==0:
            openflag=1
            app = wx.PySimpleApp()
            wildcard = "Picture (*.png,*.jpg)|*.png*;*.jpg"
            #dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
            #dialog.SetDirectory("/root/Desktop")
            dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.FD_OPEN)
            if dialog.ShowModal() == wx.ID_OK:
                
                openflag=0
                pathfile=dialog.GetPath()
                print pathfile
                liveflag=2
                		
    def Loop(self):
	global liveflag,cap,pathfile
	global x_start, y_start, x_end, y_end, cropping,roi,breakflag
	if liveflag==1:
            ret, frame = cap.read()
	    

	    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QtGui.QImage.Format_RGB888)
            image=image.scaledToHeight(180)
            self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
        elif liveflag==2:
            
            #inputimg=cv2.imread(pathfile)
            cropping = False
     
            x_start, y_start, x_end, y_end = 0, 0, 0, 0
             
            
            def mouse_crop(event, x, y, flags, param):
                # grab references to the global variables
                global x_start, y_start, x_end, y_end, cropping,roi,breakflag
                breakflag=0
             
                # if the left mouse button was DOWN, start RECORDING
                # (x, y) coordinates and indicate that cropping is being
                if event == cv2.EVENT_LBUTTONDOWN:
                    x_start, y_start, x_end, y_end = x, y, x, y
                    cropping = True
             
                # Mouse is Moving
                elif event == cv2.EVENT_MOUSEMOVE:
                    if cropping == True:
                        x_end, y_end = x, y
             
                # if the left mouse button was released
                elif event == cv2.EVENT_LBUTTONUP:
                    # record the ending (x, y) coordinates
                    x_end, y_end = x, y
                    cropping = False # cropping is finished
             
                    refPoint = [(x_start, y_start), (x_end, y_end)]
             
                    if len(refPoint) == 2: #when two points were found
                        roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
                        #cv2.imshow("Cropped", roi)
                        breakflag=1
            image = cv2.imread(pathfile)
            oriImage = image.copy()
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", mouse_crop)
            breakflag=0
            while True:
     
                i = image.copy()
             
                if not cropping:
                    cv2.imshow("image", image)
             
                elif cropping:
                    cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
                    cv2.imshow("image", i)
                if breakflag==1:
                    breakflag=0
                    break;
                    
                cv2.waitKey(1)
            cv2.destroyAllWindows()
            # close all open windows    
            inputimg=roi    

            #################
            #inputimg=cv2.resize(inputimg,(320,240))
            (segmented_image, labels_image, number_regions) = pms.segment(inputimg, spatial_radius=3, 
                                                                  range_radius=3, min_density=50)
            cv2.imwrite("segmented.png",segmented_image)
            grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
            
            bimg=cv2.threshold(grayimg, 170, 255, cv2.THRESH_BINARY)[1]
            #bimg = cv2.bitwise_not(bimg)
            
            
            cv2.imwrite("binary.png",bimg)
            im=cv2.imread("binary.png")
            grayimg=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            cv2.imwrite("output.png",grayimg)
            
            grayimg[grayimg>0]=1
            
            con=grayimg.astype('int')
            
            con=measure.label(con,background=0)
            
            propsa=measure.regionprops(con)
            print len(propsa)
            self.t4.setText(str(len(propsa)))
            self.dispa=QtGui.QPixmap("binary.png")
            self.dispa=self.dispa.scaledToHeight(180)
            self.i2.setPixmap(self.dispa)
            self.dispa=QtGui.QPixmap("segmented.png")
            self.dispa=self.dispa.scaledToHeight(180)
            self.i1.setPixmap(self.dispa)
            liveflag=0
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()


