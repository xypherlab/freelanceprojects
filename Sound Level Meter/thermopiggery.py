import numpy as np
from scipy.fftpack import fft
from scipy import signal
from scipy.signal import argrelextrema, fftconvolve
from scipy.io import wavfile
from time import time
import sys, os, wave
from PyQt4 import QtGui, QtCore
from Adafruit_AMG88xx import Adafruit_AMG88xx
import pygame
import math
from scipy.interpolate import griddata
from colour import Color
from time import sleep
import time
import RPi.GPIO as GPIO
import pandas as pd
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

import spl_lib as spl
from scipy.signal import lfilter


class Main(QtGui.QMainWindow): 
    def __init__(self): 
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,NUMERATOR,DENOMINATOR,old,min_decibel,max_decibel
        flag=0
        NUMERATOR, DENOMINATOR = spl.A_weighting(48000)
        old=0
        min_decibel=100
        max_decibel=0
        centralwidget = QtGui.QWidget(self) 

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        
        font = QtGui.QFont("Times", 24)
        self.t1=QtGui.QLabel("Piggery Monitoring",self)
        self.t1.setFont(font)
        self.t1.move(80,10)
        self.t1.resize(350,50)
        
        self.l1=QtGui.QLabel("Temperature: ",self)
        self.l1.move(70,120) 
        self.l2=QtGui.QLabel("-----",self)
        self.l2.move(175,120)
        
        self.l3=QtGui.QLabel("Pitch Frequency: ",self)
        self.l3.move(70,150)
        self.l4=QtGui.QLabel("-----",self)
        self.l4.move(195,150)

        self.l5=QtGui.QLabel("Status: ",self)
        self.l5.move(70,210)
        self.l6=QtGui.QLabel("-----",self)
        self.l6.move(125,210)
        self.l6.resize(150,30)

        self.l7=QtGui.QLabel("Loudness: ",self)
        self.l7.move(70,180)
        self.l8=QtGui.QLabel("-----",self)
        self.l8.move(175,180)
        
        self.startbutton = QtGui.QPushButton("Start",self)
        self.startbutton.clicked.connect(self.initiate)
        self.startbutton.move(80,250)
        
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.terminate)
        self.stopbutton.move(190,250)

        self.viewbutton = QtGui.QPushButton("View",self)
        self.viewbutton.clicked.connect(self.display)
        self.viewbutton.move(300,250)
        
        
        self.setGeometry(230,20,430,360)
    def display(self):
        #low range of the sensor (this will be blue on the screen)
        MINTEMP = 26

        #high range of the sensor (this will be red on the screen)
        MAXTEMP = 32

        #how many color values we can have
        COLORDEPTH = 1024

        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.init()

        #initialize the sensor
        sensor = Adafruit_AMG88xx()

        points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
        grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

        #sensor is an 8x8 grid so lets do a square
        height = 240
        width = 240

        #the list of colors we can choose from
        blue = Color("indigo")
        colors = list(blue.range_to(Color("red"), COLORDEPTH))

        #create the array of colors
        colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

        displayPixelWidth = width / 30
        displayPixelHeight = height / 30

        lcd = pygame.display.set_mode((width, height))

        lcd.fill((255,0,0))

        pygame.display.update()
        pygame.mouse.set_visible(False)

        lcd.fill((0,0,0))
        pygame.display.update()

        #some utility functions
        def constrain(val, min_val, max_val):
            return min(max_val, max(min_val, val))

        def map(x, in_min, in_max, out_min, out_max):
          return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        #let the sensor initialize
        time.sleep(.1)
                
        while(1):
            #read the pixels
            pixels = sensor.readPixels()
            print pixels
            
            pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
            print p
            #perdorm interpolation
            bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
            print(sensor.readPixels())
            #draw everything
            for ix, row in enumerate(bicubic):
                    for jx, pixel in enumerate(row):
                            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
            
            pygame.display.update()
    def initiate(self):
        global flag
        flag=1
        
        
    def terminate(self):
        global flag
        flag=0
        pygame.quit()
        self.l2.setText("-----")
        self.l4.setText("-----")
        GPIO.output(24, 0) 
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))

    def map(x, in_min, in_max, out_min, out_max):
      return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
    def Loop(self):
        global flag,NUMERATOR,DENOMINATOR,old,min_decibel,max_decibel
        #Fan Relay Test
        #GPIO.output(23, 1)
        #time.sleep(5)
        #GPIO.output(23, 0)
        #time.sleep(5)
        #GPIO.output(23, 1)
        #time.sleep(5)
        #GPIO.output(23, 0)
        #time.sleep(5)
        try:
            x=0
        except KeyboardInterrupt:         
            GPIO.cleanup()                 
        if flag==1:
            #Mist
            os.system("arecord --device=hw:1,0 --format S16_LE --duration=5 --rate 48000 /home/pi/Desktop/input.wav")
            #flag=0 #One Time Record    
            wf = wave.open('/home/pi/Desktop/input.wav','r')
            rate = wf.getframerate()
            swidth = wf.getsampwidth()
            chunk = 2048
            values=[]
            timestep = 1.0/rate
            minFr=1000 #Minimum Frequency
            maxFr=2000 #Maximum Frequency
            while True:
                    

                    
                    signal = wf.readframes(chunk)
                    if len(signal) < chunk*swidth:
                        break
                    else:
                        signal = np.fromstring(signal, 'Int16')
                        n = signal.size
                        #Apply the FFT, extract the frequencies and take their absolute value
                        freqs = fft(signal)
                        freq = np.fft.fftfreq(n, d=timestep) 
                        data = np.abs(freqs)
                        #Frequency with maximum intensity 
                        max = [x for x in argrelextrema(data, np.greater)[0] if x<10000]
                        maxInt = data[max]
                        absMaxInt=np.max(maxInt)
                        absMax=np.where(maxInt==absMaxInt)[0][0]
                        number=max[absMax]*rate/chunk
                        if number>=minFr and number<=maxFr:
                            values.append(number)
                        y = lfilter(NUMERATOR, DENOMINATOR, signal)
                        new_decibel = 20*numpy.log10(spl.rms_flat(y))
                        if abs(old - new_decibel) > 3:
                            old = new_decibel
                            print 'A-weighted: {:+.2f} dBA'.format(new_decibel)
            l=int(len(values)/3)
            print "Pitch Frequency: "+str(np.mean(values))
            self.l4.setText(str(np.mean(values))+" Hz")
            
            loudness=new_decibel
            print "Loudness: "+str(loudness)+" dBA"
            self.l8.setText(str(loudness)+" dBA")
            sensor = Adafruit_AMG88xx()
            sleep(.1)
            data=str(sensor.readPixels())
            data =data.replace("[", "")
            data =data.replace("]", "")
            data=data.split(",")
            length=len(data)
            print length
            tempdata=np.array([])
            for i in range(length):
                tempdata=np.hstack((tempdata,float(data[i])))
            print tempdata
            print len(tempdata)
            self.l2.setText(str(np.amax(tempdata))+" C")
            sleep(1)
            pathmain="/home/pi/Desktop/tempdata.csv"
            if os.path.exists(pathmain):
                 
                 df=pd.read_csv(pathmain,names=['Temperature','Frequency','Amplitude'],skiprows=1)
                 np_df = df.as_matrix()
                 df = df.append({'Temperature':np.amax(tempdata),'Frequency':np.mean(values),'Amplitude':loudness}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print df
            else:
                 columns = ['Temperature','Frequency','Amplitude']
                 df = pd.DataFrame(columns=columns)
                 np_df = df.as_matrix()
                 
                 df = df.append({'Temperature':np.amax(tempdata),'Frequency':np.mean(values),'Amplitude':loudness}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print df
            if loudness>80.18 and np.amax(tempdata)>=31 and np.amax(tempdata)<=35 and np.mean(values)>276.71:     
                
                GPIO.output(24, 1)
                self.l6.setText("Misting is On")
                print "Status: Misting is On"
                time.sleep(60) #Mist duration
            else:
                GPIO.output(23, 0)
                GPIO.output(24, 0)
                self.l6.setText("Normal")
                print "Status: Normal"
            
            #Fan
            os.system("arecord --device=hw:1,0 --format S16_LE --duration=5 --rate 48000 /home/pi/Desktop/input.wav")
            #flag=0 #One Time Record    
            wf = wave.open('/home/pi/Desktop/input.wav','r')
            rate = wf.getframerate()
            swidth = wf.getsampwidth()
            chunk = 2048
            values=[]
            timestep = 1.0/rate
            minFr=1000 #Minimum Frequency
            maxFr=2000 #Maximum Frequency
            while True:
                    signal = wf.readframes(chunk)
                    if len(signal) < chunk*swidth:
                        break
                    else:
                        signal = np.fromstring(signal, 'Int16')
                        n = signal.size
                        #Apply the FFT, extract the frequencies and take their absolute value
                        freqs = fft(signal)
                        freq = np.fft.fftfreq(n, d=timestep) 
                        data = np.abs(freqs)
                        #Frequency with maximum intensity 
                        max = [x for x in argrelextrema(data, np.greater)[0] if x<10000]
                        maxInt = data[max]
                        absMaxInt=np.max(maxInt)
                        absMax=np.where(maxInt==absMaxInt)[0][0]
                        number=max[absMax]*rate/chunk
                        if number>=minFr and number<=maxFr:
                            values.append(number)
                        y = lfilter(NUMERATOR, DENOMINATOR, signal)
                        new_decibel = 20*numpy.log10(spl.rms_flat(y))
                        if abs(old - new_decibel) > 3:
                            old = new_decibel
                            print 'A-weighted: {:+.2f} dBA'.format(new_decibel)
            l=int(len(values)/3)
            print "Pitch Frequency: "+str(np.mean(values))
            self.l4.setText(str(np.mean(values))+" Hz")
            loudness=new_decibel
            print "Loudness: "+str(loudness)+" dBA"
            self.l8.setText(str(loudness)+" dBA")
            sensor = Adafruit_AMG88xx()
            sleep(.1)
            data=str(sensor.readPixels())
            data =data.replace("[", "")
            data =data.replace("]", "")
            data=data.split(",")
            length=len(data)
            print length
            tempdata=np.array([])
            for i in range(length):
                tempdata=np.hstack((tempdata,float(data[i])))
            print tempdata
            print len(tempdata)
            self.l2.setText(str(np.amax(tempdata))+" C")
            sleep(1)
            pathmain="/home/pi/Desktop/tempdata.csv"
            if os.path.exists(pathmain):
                 
                 df=pd.read_csv(pathmain,names=['Temperature','Frequency','Amplitude'],skiprows=1)
                 np_df = df.as_matrix()
                 df = df.append({'Temperature':np.amax(tempdata),'Frequency':np.mean(values),'Amplitude':loudness}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print df
            else:
                 columns = ['Temperature','Frequency','Amplitude']
                 df = pd.DataFrame(columns=columns)
                 np_df = df.as_matrix()
                 
                 df = df.append({'Temperature':np.amax(tempdata),'Frequency':np.mean(values),'Amplitude':loudness}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print df
            if loudness>80.18 and np.amax(tempdata)>=31 and np.amax(tempdata)<=35 and np.mean(values)>276.71:     
                GPIO.output(23, 1)
                GPIO.output(24, 0)
                self.l6.setText("Fan is On")
                print "Status: Fan is On"
                time.sleep(120) #Fan duration
            else:
                GPIO.output(23, 0)
                GPIO.output(24, 0)
                self.l6.setText("Normal")
                print "Status: Normal"
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
