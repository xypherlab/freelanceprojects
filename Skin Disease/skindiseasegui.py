from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import pymeanshift as pms
from skimage import measure
import wx
from skimage.feature import blob_doh
from skimage.measure import label
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
        cap.set(3,320)
        cap.set(4,240)
	time.sleep(1)
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
	self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(20,60,600,200)
	self.disp=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/blackscreen.png")
        self.disp=self.disp.scaledToHeight(120)
        self.i1.setPixmap(self.disp)
	self.i2=QtGui.QLabel(self)
        self.i2.setGeometry(220,60,400,200)
	self.dispa=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/blackscreen.png")
        self.dispa=self.disp.scaledToHeight(120)
        self.i2.setPixmap(self.dispa)

        self.i3=QtGui.QLabel(self)
        self.i3.setGeometry(420,60,400,200)
	self.dispb=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/blackscreen.png")
        self.dispb=self.disp.scaledToHeight(120)
        self.i3.setPixmap(self.dispb)

        self.i4=QtGui.QLabel(self)
        self.i4.setGeometry(620,60,400,200)
	self.dispb=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/blackscreen.png")
        self.dispb=self.disp.scaledToHeight(120)
        self.i4.setPixmap(self.dispb)

        
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

        self.t3=QtGui.QLabel("Match %: ",self)
        self.t3.move(290,340)
        self.t4=QtGui.QLabel("-----",self)
        self.t4.move(400,340)
        self.t4.resize(130,30)

        self.t5=QtGui.QLabel("Area: ",self)
        self.t5.move(290,310)
        self.t6=QtGui.QLabel("-----",self)
        self.t6.move(370,310)
        self.t6.resize(130,30)

        #self.t7=QtGui.QLabel("RGB: ",self)
        #self.t7.move(290,280)
        #self.t8=QtGui.QLabel("-----",self)
        #self.t8.move(370,280)
        #self.t8.resize(130,30)

        self.a1=QtGui.QLabel("Original",self)
        self.a1.move(20,50)
        self.a1.resize(130,30)
        self.a3=QtGui.QLabel("Binary",self)
        self.a3.move(220,50)
        self.a3.resize(130,30)
        self.a2=QtGui.QLabel("Segmented",self)
        self.a2.move(420,50)
        self.a2.resize(130,30)

        self.a4=QtGui.QLabel("Extracted",self)
        self.a4.move(620,50)
        self.a4.resize(130,30)
        
        
	self.setGeometry(0,20,820,480)
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
            
            dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.FD_OPEN)
            if dialog.ShowModal() == wx.ID_OK:
                
                openflag=0
                pathfile=dialog.GetPath()
                print pathfile
                liveflag=3
                		
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
        elif liveflag==3:
                
               
                

                inputimg=cv2.imread(pathfile)
                #inputimg = cv2.cvtColor(inputimg, cv2.COLOR_BGR2YUV)
                #inputimg[:, :, 0] = cv2.equalizeHist(inputimg[:, :, 0])
                #inputimg = cv2.cvtColor(inputimg, cv2.COLOR_YUV2RGB)
                #inputimg= cv2.cvtColor(inputimg, cv2.COLOR_BGR2RGB)
                image=inputimg.copy()
                #################
                #inputimg=cv2.resize(inputimg,(320,240))
                imagedata=os.listdir("C:/Users/Xypher/Desktop/Skin Disease Simulation/Database")
                print(imagedata)
                score=[]
                store=[]
                xloc=[]
                yloc=[]
                for i in range(len(imagedata)):
                    try:
                        tmp=cv2.imread("C:/Users/Xypher/Desktop/Skin Disease Simulation/Database/"+imagedata[i])
                       
                        result = cv2.matchTemplate(image, tmp, cv2.TM_SQDIFF)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                        confidence = (9999999999 - min_val) / 100000000
                       
                        altconfidence = 100 - ((min_val / max_val)*100)
                        #print(altconfidence)
                        score.append(altconfidence)
                        store.append(altconfidence)
                        xloc.append(min_loc[0])
                        yloc.append(min_loc[1])
                    except:
                        xloc.append(0)
                        yloc.append(0)
                        score.append(0)
                        store.append(0)
                        dump=0
                
                
                
                print xloc
                print yloc
                score.sort()
                #print score
                pos=score[-1]
                #print pos
                output=imagedata[store.index(pos)].split("_")[0]
                xcoor=xloc[store.index(pos)]
                ycoor=yloc[store.index(pos)]
                start_point = (xcoor, ycoor)
                print imagedata[store.index(pos)]
                selimg=cv2.imread("C:/Users/Xypher/Desktop/Skin Disease Simulation/Database/"+imagedata[store.index(pos)])
                
                # Ending coordinate, here (220, 220) 
                # represents the bottom right corner of rectangle 
                end_point = (xcoor+selimg.shape[1], ycoor+selimg.shape[0])
                
                roi=inputimg[ycoor:ycoor+selimg.shape[0], xcoor:xcoor+selimg.shape[1]]

                #
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/roi.png",inputimg)
                
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/inputimage.png",inputimg)
                

                #
                # Blue color in BGR 
                color = (255, 0, 0) 
                  
                # Line thickness of 2 px 
                thickness = 2
                  
                # Using cv2.rectangle() method 
                # Draw a rectangle with blue line borders of thickness of 2 px 
                image = cv2.rectangle(image, start_point, end_point, color, thickness) 
                
                inputimg=roi

                testimg=inputimg.copy()
                testimg = cv2.fastNlMeansDenoisingColored(testimg,None,20,10,7,21)
                
               
                testimg=cv2.cvtColor(testimg,cv2.COLOR_BGR2GRAY)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/test1.jpg",testimg)
                #testimg = cv2.threshold(testimg,10,255,cv2.THRESH_BINARY)
                testimg = cv2.adaptiveThreshold(testimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 151, 2)
                

                con=measure.label(testimg,background=0)
                propsa=measure.regionprops(con)
                totalarea=0
                for region in measure.regionprops(con):
                    totalarea=totalarea+region.area
                print totalarea
                areacrop=selimg.shape[0]*selimg.shape[1]
                refarea= float(totalarea)/float(areacrop)
                print refarea
                if refarea<0.40:
                    testimg = cv2.bitwise_not(testimg)
                maskern=testimg
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/test.png",testimg)
                ######
                
                (segmented_image, labels_image, number_regions) = pms.segment(inputimg, spatial_radius=1, 
                                                                      range_radius=1, min_density=1)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/segmented.png",segmented_image)
                
                
                frame = cv2.bitwise_and(inputimg,inputimg,mask = maskern)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/extract.png",frame)
                r, g, b = 0, 0, 0
                count = 0
                for x in range(frame.shape[0]):
                      for y in range(frame.shape[1]):
                          tempr,tempg,tempb = frame[x,y]
                          r += tempr
                          g += tempg
                          b += tempb
                          count += 1
                count=np.count_nonzero(frame)
                red=int(r/count)
                green=int(g/count)
                blue=int(b/count)
               
                
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/binary.png",maskern)
                im=cv2.imread("C:/Users/Xypher/Desktop/Skin Disease Simulation/binary.png")
                grayimg=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/output.png",grayimg)
                
                grayimg[grayimg>0]=1
                
                con=grayimg.astype('int')
                
                con=measure.label(con,background=0)
                
                propsa=measure.regionprops(con)
                totalarea=0
                for region in measure.regionprops(con):
                    totalarea=totalarea+region.area
                    #print region.area
                #self.t4.setText(str(len(propsa)))
                
                self.t2.setText(output)
                self.t4.setText(str(pos))
                if pos<97:
                    self.t2.setText("Unknown")
                    
                self.t6.setText(str(totalarea))

                #self.t8.setText(str(len(propsa)))

                #cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/segmented.png",frame)
                self.dispa=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/test.png")
                self.dispa=self.dispa.scaledToHeight(120)
                self.i2.setPixmap(self.dispa)
                
                
                self.dispa=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/roi.png")
                self.dispa=self.dispa.scaledToHeight(120)
                self.i1.setPixmap(self.dispa)

                self.dispb=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/segmented.png")
                self.dispb=self.dispb.scaledToHeight(120)
                self.i3.setPixmap(self.dispb)

                self.dispb=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/extract.png")
                self.dispb=self.dispb.scaledToHeight(120)
                self.i4.setPixmap(self.dispb)
                liveflag=0


                
        elif liveflag==2:
                
                
                
                ret, inputimg = cap.read()
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/inputimage.png",inputimg)
                pathfile="C:/Users/Xypher/Desktop/Skin Disease Simulation/inputimage.png"
                image = cv2.imread(pathfile)
                image=inputimg.copy()
                #################
                #inputimg=cv2.resize(inputimg,(320,240))
                imagedata=os.listdir("C:/Users/Xypher/Desktop/Skin Disease Simulation/Database")
                print(imagedata)
                score=[]
                store=[]
                xloc=[]
                yloc=[]
                for i in range(len(imagedata)):
                    try:
                        tmp=cv2.imread("C:/Users/Xypher/Desktop/Skin Disease Simulation/Database/"+imagedata[i])
                       
                        result = cv2.matchTemplate(image, tmp, cv2.TM_SQDIFF)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                        confidence = (9999999999 - min_val) / 100000000
                       
                        altconfidence = 100 - ((min_val / max_val)*100)
                        #print(altconfidence)
                        score.append(altconfidence)
                        store.append(altconfidence)
                        xloc.append(min_loc[0])
                        yloc.append(min_loc[1])
                    except:
                        xloc.append(0)
                        yloc.append(0)
                        score.append(0)
                        store.append(0)
                        dump=0
                
                
                
                print xloc
                print yloc
                score.sort()
                #print score
                pos=score[-1]
                #print pos
                output=imagedata[store.index(pos)].split("_")[0]
                xcoor=xloc[store.index(pos)]
                ycoor=yloc[store.index(pos)]
                start_point = (xcoor, ycoor)
                print imagedata[store.index(pos)]
                selimg=cv2.imread("C:/Users/Xypher/Desktop/Skin Disease Simulation/Database/"+imagedata[store.index(pos)])
                
                # Ending coordinate, here (220, 220) 
                # represents the bottom right corner of rectangle 
                end_point = (xcoor+selimg.shape[1], ycoor+selimg.shape[0])
                
                roi=inputimg[ycoor:ycoor+selimg.shape[0], xcoor:xcoor+selimg.shape[1]]

                #
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/roi.png",inputimg)
                
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/inputimage.png",inputimg)
                

                #
                # Blue color in BGR 
                color = (255, 0, 0) 
                  
                # Line thickness of 2 px 
                thickness = 2
                  
                # Using cv2.rectangle() method 
                # Draw a rectangle with blue line borders of thickness of 2 px 
                image = cv2.rectangle(image, start_point, end_point, color, thickness) 
               
                inputimg=roi

                testimg=inputimg.copy()
                testimg = cv2.fastNlMeansDenoisingColored(testimg,None,20,10,7,21)
                
               
                testimg=cv2.cvtColor(testimg,cv2.COLOR_BGR2GRAY)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/test1.jpg",testimg)
                #testimg = cv2.threshold(testimg,10,255,cv2.THRESH_BINARY)
                testimg = cv2.adaptiveThreshold(testimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 151, 2)
                

                con=measure.label(testimg,background=0)
                propsa=measure.regionprops(con)
                totalarea=0
                for region in measure.regionprops(con):
                    totalarea=totalarea+region.area
                print totalarea
                areacrop=selimg.shape[0]*selimg.shape[1]
                refarea= float(totalarea)/float(areacrop)
                print refarea
                if refarea<0.40:
                    testimg = cv2.bitwise_not(testimg)
                maskern=testimg
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/test.png",testimg)
                ######
                
                (segmented_image, labels_image, number_regions) = pms.segment(inputimg, spatial_radius=3, 
                                                                      range_radius=3, min_density=10)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/segmented.png",segmented_image)
                
                
                frame = cv2.bitwise_and(inputimg,inputimg,mask = maskern)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/extract.png",frame)
                r, g, b = 0, 0, 0
                count = 0
                for x in range(frame.shape[0]):
                      for y in range(frame.shape[1]):
                          tempr,tempg,tempb = frame[x,y]
                          r += tempr
                          g += tempg
                          b += tempb
                          count += 1
                count=np.count_nonzero(frame)
                red=int(r/count)
                green=int(g/count)
                blue=int(b/count)
               
                
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/binary.png",maskern)
                im=cv2.imread("C:/Users/Xypher/Desktop/Skin Disease Simulation/binary.png")
                grayimg=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/output.png",grayimg)
                
                grayimg[grayimg>0]=1
                
                con=grayimg.astype('int')
                
                con=measure.label(con,background=0)
                
                propsa=measure.regionprops(con)
                totalarea=0
                for region in measure.regionprops(con):
                    totalarea=totalarea+region.area
                    #print region.area
                #self.t4.setText(str(len(propsa)))
                
                self.t2.setText(output)
                self.t4.setText(str(pos))
                if pos<97:
                    self.t2.setText("Unknown")
                    
                self.t6.setText(str(totalarea))

                #self.t8.setText(str(len(propsa)))

                #cv2.imwrite("C:/Users/Xypher/Desktop/Skin Disease Simulation/segmented.png",frame)
                self.dispa=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/test.png")
                self.dispa=self.dispa.scaledToHeight(120)
                self.i2.setPixmap(self.dispa)
                
                
                self.dispa=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/roi.png")
                self.dispa=self.dispa.scaledToHeight(120)
                self.i1.setPixmap(self.dispa)

                self.dispb=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/segmented.png")
                self.dispb=self.dispb.scaledToHeight(120)
                self.i3.setPixmap(self.dispb)

                self.dispb=QtGui.QPixmap("C:/Users/Xypher/Desktop/Skin Disease Simulation/extract.png")
                self.dispb=self.dispb.scaledToHeight(120)
                self.i4.setPixmap(self.dispb)
                liveflag=0
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()


