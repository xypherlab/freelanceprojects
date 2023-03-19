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
        self.d1.move(50,20)
        self.d2=QtGui.QLabel("--",self)
        self.d2.move(30,50)
        self.d2.resize(150,50)
        self.d3=QtGui.QLabel("Blood(1): ",self)
        self.d3.move(50,150)
        self.d4=QtGui.QLabel("--",self)
        self.d4.move(120,150)
        self.d5=QtGui.QLabel("Blood(2): ",self)
        self.d5.move(50,220)
        self.d6=QtGui.QLabel("--",self)
        self.d6.move(120,220)
        self.d7=QtGui.QLabel("Blood(3): ",self)
        self.d7.move(50,290)
        self.d8=QtGui.QLabel("--",self)
        self.d8.move(120,290)
        #Analyze Button
        self.analyzebutton = QtGui.QPushButton("Change",self)
        self.analyzebutton.clicked.connect(self.start)
        self.analyzebutton.move(70,110)
        #
        #Stop Button
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(210,150)
        #
        #Recordbutton Button
        self.recordbutton = QtGui.QPushButton("Record",self)
        self.recordbutton.clicked.connect(self.record)
        self.recordbutton.move(210,110)
        #
        self.sl1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sl1.setMinimum(380)
        self.sl1.setMaximum(780)
        self.sl1.setValue(380)
        self.sl1.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl1.setTickInterval(1)
        self.sl1.valueChanged.connect(self.bloodBvalue)
        self.sl1.move(50,180)
        self.sl1.resize(220,30)
        self.sl2 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sl2.setMinimum(380)
        self.sl2.setMaximum(780)
        self.sl2.setValue(380)
        self.sl2.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl2.setTickInterval(1)
        self.sl2.valueChanged.connect(self.bloodAvalue)
        self.sl2.move(50,250)
        self.sl2.resize(220,30)
        self.sl3 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sl3.setMinimum(380)
        self.sl3.setMaximum(780)
        self.sl3.setValue(380)
        self.sl3.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl3.setTickInterval(1)
        self.sl3.valueChanged.connect(self.bloodCvalue)
        self.sl3.move(50,320)
        self.sl3.resize(220,30)

        self.setGeometry(0,20,320,400)
    def bloodAvalue(self):
       global bloodA
       bloodA = self.sl2.value()
    def bloodBvalue(self):
       global bloodB
       bloodB = self.sl1.value()
    def bloodCvalue(self):
       global bloodC
       bloodC= self.sl3.value()
       
    def start(self):
        global flag,start_time
        #flag=1
        #start_time = time.time()
        print bloodA
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
        print bloodB
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
        print bloodC
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
           
        colorout= "B,"+str(RA)+","+str(GA)+","+str(BA)+","+str(RB)+","+str(GB)+","+str(BB)+","+str(RC)+","+str(GC)+","+str(BC)
        ser.write(colorout)
        print colorout
    def stop(self):
        global flag
        flag=0
	
    def record(self):     
        global flag,bloodA,bloodB,bloodC,val1,val2,val3
        flag=1
        bloodA=380
        bloodB=380
        bloodC=380
        val1=0
        val2=0
        val3=0
    def Loop(self):
        global flag,start_time,bloodA,bloodB,bloodC,val1,val2,val3
        delay=1
        self.d6.setText(str(bloodA))
        self.d4.setText(str(bloodB))
        self.d8.setText(str(bloodC))
        elapsed_time=time.time()-start_time
        if flag==1:
            ser.write("A,")
	    
            try:
                
                sensordata=ser.readline()
                s0=float(sensordata.split(",")[0])
                s1=float(sensordata.split(",")[1])
                s2=float(sensordata.split(",")[2])
                s3=float(sensordata.split(",")[3])
                s4=float(sensordata.split(",")[4])
                s5=float(sensordata.split(",")[5])       
                
                print str(s0)+","+str(s1)+","+str(s2)+","+str(s3)+","+str(s4)+","+str(s5)
                sensordata= str(s0)+","+str(s1)+","+str(s2)+",\n"+str(s3)+","+str(s4)+","+str(s5)+","
                    
                self.d2.setText(sensordata)
                if bloodA<=780:
                    print "Wavelength: "+str(bloodA)
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
                    print bloodB
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
                    print bloodC
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
                    print colorout
                else:
                    flag=0
                try:    
                    val1=math.log10(s1/s0)
                    
                except:
                    val1="Error"
                try:
                    val2=math.log10(s3/s2)
                except:
                    val2="Error"
                try:
                    val3=math.log10(s5/s4)
                except:
                    val3="Error"
                    
		print str(val1)+" - "+str(val2)+" - "+str(val3)
                pathtarget="/home/pi/Desktop/logrecord.csv"
                
                if os.path.exists(pathtarget):
                                 
                     df=pd.read_csv(pathtarget,names=['WAV','ABS1','ABS2','ABS3'],skiprows=1)
                     np_df = df.as_matrix()
                     df = df.append({'WAV':bloodA,'ABS1':val1,'ABS2':val2,'ABS3':val3}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                else:
                     
                     columns = ['WAV','ABS1','ABS2','ABS3']
                     df = pd.DataFrame(columns=columns)
                     np_df = df.as_matrix()
                     
                     df = df.append({'WAV':bloodA,'ABS1':val1,'ABS2':val2,'ABS3':val3}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                bloodA=bloodA+1
                bloodB=bloodB+1
                bloodC=bloodC+1
                #Voting Algorithm
                #data=""
                #proc=Counter(data)
                #result = proc.most_common(1)[0][0]
                #if result==0:
                #    print "Type A"
                #    self.v2.setText("Type A+")
                #elif result==1:
                #    print "Type B"
                #    self.v2.setText("Type B+")
                #elif result==2:
                #    print "Type O"
                #    self.v2.setText("Type O+")
                #elif result==3:
                #    print "Type AB"
                #      self.v2.setText("Type AB+")
                #elif result==4:
                #    print "Type A"
                #    self.v2.setText("Type A-")
                #elif result==5:
                #    print "Type B"
                #    self.v2.setText("Type B-")
                #elif result==6:
                #    print "Type O"
                #    self.v2.setText("Type O-")
                #elif result==7:
                #    print "Type AB"
                #      self.v2.setText("Type AB-")
            except:
                    dump=0    
        #if flag==1 and elapsed_time>=delay:
           
            #start_time = time.time()
      
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
