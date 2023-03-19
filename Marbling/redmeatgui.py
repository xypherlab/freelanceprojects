from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np



class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,cap,fourcc,out,i,cameraid
        i=0
        flag=0
        
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.e1=QtGui.QLabel("Camera ID: ",self)
        self.e2=QtGui.QLineEdit("1",self)
        self.e1.move(550,60)
        self.e2.move(610,60)
        self.e2.resize(40,30)
        cameraid=int(self.e2.text())
        self.e3=QtGui.QLabel("Duration: ",self)
        self.e4=QtGui.QLineEdit(self)
        self.e3.move(550,100)
        self.e4.move(610,100)
        self.e4.resize(40,30)
        
        #Record Button
        self.recordbutton = QtGui.QPushButton("Start",self)
        self.recordbutton.clicked.connect(self.recording)
        self.recordbutton.move(560,140)
        #
        #Stop Button
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(560,180)
        #
        
        
        #Side Title
        self.d1=QtGui.QLabel("Side A",self)
        self.d1.move(200,45)
        self.d2=QtGui.QLabel("Side B",self)
        self.d2.move(200,245)
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
        cap = cv2.VideoCapture(cameraid)
        cap.set(3,640)
        cap.set(4,480)
        w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
        h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT); 
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (int(w),int(h)))
    def recording(self):
        global flag,cap,fourcc,out,cameraid
        cameraid=int(self.e2.text())
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
        global flag
        flag=0
        cap.release()
        out.release()
        cv2.destroyAllWindows()
    def Loop(self):
        global flag,cap,fourcc,out,i
        
            
        if flag==1:
            duration=self.e4.text()
            if duration!="":
                duration=int(self.e4.text())*30
                i=i+1
                ret, frame = cap.read()
             
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                           frame.strides[0], QtGui.QImage.Format_RGB888)
                image=image.scaledToHeight(180)
                self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
                if i>duration:
                    flag=0
                    i=0
            else:
                ret, frame = cap.read()
                out.write(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                           frame.strides[0], QtGui.QImage.Format_RGB888)
                image=image.scaledToHeight(180)
                self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
       
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
