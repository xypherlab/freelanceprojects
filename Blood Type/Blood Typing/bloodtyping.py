from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import serial
from collections import Counter
import pandas as pd
import math
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,start_time,bloodA,bloodB,bloodC
        #380 to 420
        #600 to 610
        #Change Light>Read Lux>Binary Result from Sensor 1 to Sensor 3
        self.frame = QtGui.QFrame(self)
        self.frame.resize(500,400)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255)");
        
        self.frame1 = QtGui.QFrame(self)
        self.frame1.resize(100,100)
        self.frame1.setStyleSheet("background-image: url(/home/pi/Desktop/logo.png);")
        self.frame1.move(200,50)
        #Enter Button
        self.enterbutton = QtGui.QPushButton("Enter",self)
        self.enterbutton.clicked.connect(self.enter)
        self.enterbutton.move(210,200)
        #
        #Shutdown Button
        self.shutdownbutton = QtGui.QPushButton("Shutdown",self)
        self.shutdownbutton.clicked.connect(self.shutdown)
        self.shutdownbutton.move(210,260)
        #
        self.d5=QtGui.QLabel("(MAM JSFR VHCS JCD)",self)
        self.d5.move(320,360)
        self.d5.resize(200,30)
        #(MAM JSFR VHCS JCD)

        #Image Display Main
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(150,20,300,200)
        self.disp=QtGui.QPixmap("/home/pi/Desktop/whitescreen.png")
        self.disp=self.disp.scaledToHeight(120)
        self.i1.setPixmap(self.disp)
        #
        
        
        bloodA=380
        bloodB=380
        bloodC=380
        start_time = time.time()
        flag=0
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.v1=QtGui.QLabel("Blood Type: ",self)
        self.v1.move(200,20)
        self.v2=QtGui.QLabel("--",self)
        self.v2.move(230,50)
        self.d1=QtGui.QLabel("Sensor: ",self)
        self.d1.move(150,220)
        self.d1.resize(80,20)
        self.d2=QtGui.QLabel("--",self)
        self.d2.move(220,220)
        self.d2.resize(150,20)
        self.d3=QtGui.QLabel("Wavelength: ",self)
        self.d3.move(150,250)
        self.d4=QtGui.QLabel("--",self)
        self.d4.move(250,250)
        
       
        
        #Stop Button
        self.stopbutton = QtGui.QPushButton("Cancel",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(270,310)
        #
        #Recordbutton Button
        self.recordbutton = QtGui.QPushButton("Start",self)
        self.recordbutton.clicked.connect(self.record)
        self.recordbutton.move(120,310)
        #

        #Back Button
        self.backbutton = QtGui.QPushButton("Back",self)
        self.backbutton.clicked.connect(self.back)
        self.backbutton.move(200,360)
        #
        self.d6=QtGui.QLabel("ABO Test/RH Test",self)
        self.d6.move(180,40)
        self.d6.resize(150,30)

        

        
        self.stopbutton.setVisible(0)
        self.recordbutton.setVisible(0)
        self.v1.setVisible(0)
        self.v2.setVisible(0)
        self.d1.setVisible(0)
        self.d2.setVisible(0)
        self.d3.setVisible(0)
        self.d4.setVisible(0)
        self.i1.setVisible(0)
        self.d6.setVisible(0)
        self.d5.setVisible(1)
        self.backbutton.setVisible(0)
        self.frame1.setVisible(1)
        self.enterbutton.setVisible(1)
        self.shutdownbutton.setVisible(1)
        self.setGeometry(0,20,500,400)
    def back(self):
        self.stopbutton.setVisible(0)
        self.recordbutton.setVisible(0)
        #self.v1.setVisible(1)
        #self.v2.setVisible(1)
        self.i1.setVisible(0)
        self.d1.setVisible(0)
        self.d2.setVisible(0)
        self.d3.setVisible(0)
        self.d4.setVisible(0)
        self.d6.setVisible(0)
        self.backbutton.setVisible(0)
        self.d5.setVisible(1)
        self.frame1.setVisible(1)
        self.enterbutton.setVisible(1)
        self.shutdownbutton.setVisible(1)
    def shutdown(self):
        os.system("sudo shutdown -h now")
    def enter(self):
        self.backbutton.setVisible(1)
        self.stopbutton.setVisible(1)
        self.recordbutton.setVisible(1)
        #self.v1.setVisible(1)
        #self.v2.setVisible(1)
        self.i1.setVisible(1)
        self.d1.setVisible(1)
        self.d2.setVisible(1)
        self.d3.setVisible(1)
        self.d4.setVisible(1)
        self.d5.setVisible(0)
        self.d6.setVisible(1)
        self.frame1.setVisible(0)
        self.enterbutton.setVisible(0)
        self.shutdownbutton.setVisible(0)
    def stop(self):
        global flag
        flag=0
        self.v2.setText("----")
        self.d4.setText("----")
        self.d2.setText("----")
        self.disp=QtGui.QPixmap("/home/pi/Desktop/whitescreen.png")
        self.disp=self.disp.scaledToHeight(120)
        self.i1.setPixmap(self.disp)
    def record(self):     
        global flag,bloodA,bloodB,bloodC,val1,val2,val3,data,start_time
        self.v2.setText("----")
        data=np.array([])
        flag=-1
        bloodA=380
        bloodB=380
        bloodC=380
        val1=0
        val2=0
        val3=0
        start_time = time.time()
    def Loop(self):
        global flag,start_time,bloodA,bloodB,bloodC,val1,val2,val3,data
        delay=1
        
        elapsed_time=time.time()-start_time
        if flag==-1:
            timedelay=120
            self.d2.setText("Starting in "+str(timedelay-int(elapsed_time)))  
            if elapsed_time>=timedelay:
                start_time = time.time()
                flag=1
        elif flag==1: #380 to 420
                ser.write("A,")
	    
                sensordata=ser.readline()
                s0=float(sensordata.split(",")[0])
                s1=float(sensordata.split(",")[1])
                s2=float(sensordata.split(",")[2])
                s3=float(sensordata.split(",")[3])
                s4=float(sensordata.split(",")[4])
                s5=float(sensordata.split(",")[5])       
               
                #print str(s0)+","+str(s1)+","+str(s2)+","+str(s3)+","+str(s4)+","+str(s5)
                sensordata= str(s0)+" | "+str(s1)+" | "+str(s2)+" | "+str(s3)+" | "+str(s4)+" | "+str(s5)
                    
                self.d2.setText(sensordata)
                if bloodA<=610:
                    #print "Wavelength: "+str(bloodA)
                    MaxIntensity=255
                    
                    Wavelength=bloodA
                    def Adjust_and_Scale(Color, Factor, Highest=100):
                        
                        Gamma = 0.80
                    
                        if Color == 0.0:
                            result = 0
                        else:
                            result = int( round(pow(Color * Factor, Gamma) * round(Highest)) )
                            if result < 0:        result = 0
                            if result > Highest:  result = Highest
                    
                        return result
                    
                    
                    if (Wavelength >= 380.0) and (Wavelength < 440.0):
                        Red   = -(Wavelength - 440.) / (440. - 380.)
                        Green = 0.0
                        Blue  = 1.0
                    
                    elif (Wavelength >= 440.0) and (Wavelength < 490.0):
                        Red   = 0.0
                        Green = (Wavelength - 440.) / (490. - 440.)
                        Blue  = 1.0
                    
                    elif (Wavelength >= 490.0) and (Wavelength < 510.0):
                        Red   = 0.0
                        Green = 1.0
                        Blue  = -(Wavelength - 510.) / (510. - 490.)
                    
                    elif (Wavelength >= 510.0) and (Wavelength < 580.0):
                        Red   = (Wavelength - 510.) / (580. - 510.)
                        Green = 1.0
                        Blue  = 0.0
                    
                    elif (Wavelength >= 580.0) and (Wavelength < 645.0):
                        Red   = 1.0
                        Green = -(Wavelength - 645.) / (645. - 580.)
                        Blue  = 0.0
                    
                    elif (Wavelength >= 645.0) and (Wavelength <= 780.0):
                        Red   = 1.0
                        Green = 0.0
                        Blue  = 0.0
                    
                    else:
                        Red   = 0.0
                        Green = 0.0
                        Blue  = 0.0
                    
                    
                    
                    if (Wavelength >= 380.0) and (Wavelength < 420.0):
                        Factor = 0.3 + 0.7*(Wavelength - 380.) / (420. - 380.)
                    elif (Wavelength >= 420.0) and (Wavelength < 701.0):
                        Factor = 1.0
                    elif (Wavelength >= 701.0) and (Wavelength <= 780.0):
                        Factor = 0.3 + 0.7*(780. - Wavelength) / (780. - 700.)
                    else:
                        Factor = 0.0
                    
                    
                    RA = Adjust_and_Scale(Red,   Factor, MaxIntensity)
                    GA = Adjust_and_Scale(Green, Factor, MaxIntensity)
                    BA = Adjust_and_Scale(Blue,  Factor, MaxIntensity)
                    #print bloodB
                    MaxIntensity=255
                    Wavelength=bloodB
                    def Adjust_and_Scale(Color, Factor, Highest=100):
                        
                        Gamma = 0.80
                    
                        if Color == 0.0:
                            result = 0
                        else:
                            result = int( round(pow(Color * Factor, Gamma) * round(Highest)) )
                            if result < 0:        result = 0
                            if result > Highest:  result = Highest
                    
                        return result
                    
                    
                    if (Wavelength >= 380.0) and (Wavelength < 440.0):
                        Red   = -(Wavelength - 440.) / (440. - 380.)
                        Green = 0.0
                        Blue  = 1.0
                    
                    elif (Wavelength >= 440.0) and (Wavelength < 490.0):
                        Red   = 0.0
                        Green = (Wavelength - 440.) / (490. - 440.)
                        Blue  = 1.0
                    
                    elif (Wavelength >= 490.0) and (Wavelength < 510.0):
                        Red   = 0.0
                        Green = 1.0
                        Blue  = -(Wavelength - 510.) / (510. - 490.)
                    
                    elif (Wavelength >= 510.0) and (Wavelength < 580.0):
                        Red   = (Wavelength - 510.) / (580. - 510.)
                        Green = 1.0
                        Blue  = 0.0
                    
                    elif (Wavelength >= 580.0) and (Wavelength < 645.0):
                        Red   = 1.0
                        Green = -(Wavelength - 645.) / (645. - 580.)
                        Blue  = 0.0
                    
                    elif (Wavelength >= 645.0) and (Wavelength <= 780.0):
                        Red   = 1.0
                        Green = 0.0
                        Blue  = 0.0
                    
                    else:
                        Red   = 0.0
                        Green = 0.0
                        Blue  = 0.0
                    
                    
                    
                    if (Wavelength >= 380.0) and (Wavelength < 420.0):
                        Factor = 0.3 + 0.7*(Wavelength - 380.) / (420. - 380.)
                    elif (Wavelength >= 420.0) and (Wavelength < 701.0):
                        Factor = 1.0
                    elif (Wavelength >= 701.0) and (Wavelength <= 780.0):
                        Factor = 0.3 + 0.7*(780. - Wavelength) / (780. - 700.)
                    else:
                        Factor = 0.0
                    
                    
                    RB = Adjust_and_Scale(Red,   Factor, MaxIntensity)
                    GB = Adjust_and_Scale(Green, Factor, MaxIntensity)
                    BB = Adjust_and_Scale(Blue,  Factor, MaxIntensity)
                    #print bloodC
                    MaxIntensity=255
                    Wavelength=bloodC
                    def Adjust_and_Scale(Color, Factor, Highest=100):
                        
                        Gamma = 0.80
                    
                        if Color == 0.0:
                            result = 0
                        else:
                            result = int( round(pow(Color * Factor, Gamma) * round(Highest)) )
                            if result < 0:        result = 0
                            if result > Highest:  result = Highest
                    
                        return result
                    
                    
                    if (Wavelength >= 380.0) and (Wavelength < 440.0):
                        Red   = -(Wavelength - 440.) / (440. - 380.)
                        Green = 0.0
                        Blue  = 1.0
                    
                    elif (Wavelength >= 440.0) and (Wavelength < 490.0):
                        Red   = 0.0
                        Green = (Wavelength - 440.) / (490. - 440.)
                        Blue  = 1.0
                    
                    elif (Wavelength >= 490.0) and (Wavelength < 510.0):
                        Red   = 0.0
                        Green = 1.0
                        Blue  = -(Wavelength - 510.) / (510. - 490.)
                    
                    elif (Wavelength >= 510.0) and (Wavelength < 580.0):
                        Red   = (Wavelength - 510.) / (580. - 510.)
                        Green = 1.0
                        Blue  = 0.0
                    
                    elif (Wavelength >= 580.0) and (Wavelength < 645.0):
                        Red   = 1.0
                        Green = -(Wavelength - 645.) / (645. - 580.)
                        Blue  = 0.0
                    
                    elif (Wavelength >= 645.0) and (Wavelength <= 780.0):
                        Red   = 1.0
                        Green = 0.0
                        Blue  = 0.0
                    
                    else:
                        Red   = 0.0
                        Green = 0.0
                        Blue  = 0.0
                    
                    
                    
                    if (Wavelength >= 380.0) and (Wavelength < 420.0):
                        Factor = 0.3 + 0.7*(Wavelength - 380.) / (420. - 380.)
                    elif (Wavelength >= 420.0) and (Wavelength < 701.0):
                        Factor = 1.0
                    elif (Wavelength >= 701.0) and (Wavelength <= 780.0):
                        Factor = 0.3 + 0.7*(780. - Wavelength) / (780. - 700.)
                    else:
                        Factor = 0.0
                    
                    
                    RC = Adjust_and_Scale(Red,   Factor, MaxIntensity)
                    GC = Adjust_and_Scale(Green, Factor, MaxIntensity)
                    BC = Adjust_and_Scale(Blue,  Factor, MaxIntensity)
                       
                    colorout= str(RA)+","+str(GA)+","+str(BA)+","+str(RB)+","+str(GB)+","+str(BB)+","+str(RC)+","+str(GC)+","+str(BC)
                    ser.write(colorout)
                    #print colorout
                    try:    
                        val1=math.log10(s1/s0)
                        data1=1
                    except:
                        val1="Error"
                        data1=0
                    try:
                        val2=math.log10(s3/s2)
                        data2=1
                    except:
                        val2="Error"
                        data2=0
                    try:
                        val3=math.log10(s5/s4)
                        data3=1
                    except:
                        val3="Error"
                        data3=0
                    #A- 1 0 0
                    #A+ 1 0 1
                    #B- 0 1 0
                    #B+ 0 1 1
                    #AB- Else
                    #AB+ 1 1 1
                    #O-  0 0 0
                    #O+ 0 0 1
                    
                    if data1==1 and data2==0 and data3==0: #A-
                        bloodtype=0
                    elif data1==1 and data2==0 and data3==1: #A+
                        bloodtype=1
                    elif data1==0 and data2==1 and data3==0: #B-
                        bloodtype=2
                    elif data1==0 and data2==1 and data3==1: #B+
                        bloodtype=3
                    elif data1==0 and data2==0 and data3==0: #O-
                        bloodtype=4
                    elif data1==0 and data2==0 and data3==1: #O+
                        bloodtype=5
                    elif data1==1 and data2==1 and data3==1: #AB+
                        bloodtype=6
                    else:
                        bloodtype=7 #AB-
                    data=np.hstack([data,bloodtype])
                    
                    #print str(val1)+" - "+str(val2)+" - "+str(val3)
                    pathtarget="/home/pi/Desktop/logrecord.csv"
                    
                    if os.path.exists(pathtarget):
                                     
                         df=pd.read_csv(pathtarget,names=['WAV','ABS1','ABS2','ABS3'],skiprows=1)
                         np_df = df.as_matrix()
                         df = df.append({'WAV':bloodA,'ABS1':val1,'ABS2':val2,'ABS3':val3}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         #print(df)
                    else:
                         
                         columns = ['WAV','ABS1','ABS2','ABS3']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         
                         df = df.append({'WAV':bloodA,'ABS1':val1,'ABS2':val2,'ABS3':val3}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         #print(df)
                    self.d4.setText(str(bloodA))
                    
                    bloodA=bloodA+1
                    bloodB=bloodB+1
                    bloodC=bloodC+1
                   
                    if bloodA>420 and bloodA<600:
                        bloodA=600
                        bloodB=600
                        bloodC=600
                    elif bloodA>610:
                        flag=0
                        
                        #print("Done")
                

                    
                
        
                
                #Voting Algorithm
                #print(len(data))
                if len(data)>=52:
                    print data
                    proc=Counter(data)
                    result = proc.most_common(1)[0][0]
                    
                    if result==1:
                        #print "Type A"
                        self.v2.setText("Type A+")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/A+.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
                    elif result==3:
                        #print "Type B"
                        self.v2.setText("Type B+")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/B+.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
                    elif result==5:
                        #print "Type O"
                        self.v2.setText("Type O+")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/O+.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
                    elif result==6:
                        #print "Type AB"
                        self.v2.setText("Type AB+")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/AB+.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
                    elif result==0:
                        #print "Type A"
                        self.v2.setText("Type A-")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/A-.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
                    elif result==2:
                        #print "Type B"
                        self.v2.setText("Type B-")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/B-.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
                    elif result==4:
                        #print "Type O"
                        self.v2.setText("Type O-")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/O-.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
                    elif result==7:
                        #print "Type AB"
                        self.v2.setText("Type AB-")
                        self.disp=QtGui.QPixmap("/home/pi/Desktop/AB-.png")
                        self.disp=self.disp.scaledToHeight(100)
                        self.i1.setPixmap(self.disp)
                        
       
            
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
