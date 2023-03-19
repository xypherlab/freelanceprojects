from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
from picamera import PiCamera
import time
import cv2
import serial
import Adafruit_DHT
from datetime import datetime
import pandas as pd
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
os.system("sudo mount.cifs //192.168.0.10/RaspberryPiNAS /home/pi/ShareFile/ -o user=pi,password=raspberry")

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,x,cap,z,liveflag,start_time,camera,rawCapture
        start_time = time.time()
        liveflag=0
        z=0
        flag=0
        x=0
        cap=cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
         
        # allow the camera to warmup
        time.sleep(0.1)
       
        
        #Live Feed Button
        self.livefeedbutton = QtGui.QPushButton("Live Feed",self)
        self.livefeedbutton.clicked.connect(self.livefeed)
        self.livefeedbutton.move(210,300)
        #
        #Live Feed Button
        self.relaybutton = QtGui.QPushButton("Relay",self)
        self.relaybutton.clicked.connect(self.relaycom)
        self.relaybutton.move(410,300)
        #
        #Image Display Left
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(100,60,400,200)
        self.disp=QtGui.QPixmap("/home/pi/Share/blackscreen.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)
        #
        #Image Display Right
        self.i2=QtGui.QLabel(self)
        self.i2.setGeometry(400,60,400,200)
        self.dispa=QtGui.QPixmap("/home/pi/Share/blackscreen.png")
        self.dispa=self.disp.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
        #
        
        font10 = QtGui.QFont("Helvetica", 10)
        self.l1=QtGui.QLabel("Values: ",self)
        self.l1.move(260,270)
        self.l1.setFont(font10)
        self.l2=QtGui.QLabel(self)
        self.l2.move(350,270)
        self.l2.resize(200,30)
        self.l2.setFont(font10)
        self.setGeometry(50,20,640,360)
    
    
    def relaycom(self):
        sensor_name = Adafruit_DHT.DHT11 
        sensor_pin = 17
        humidity, temperature = Adafruit_DHT.read_retry(sensor_name, sensor_pin)
        #print(humidity)
        idvar="ZA,1000,"
        print(idvar)
        ser.write(idvar.encode())
        time.sleep(10)
        idvar="R,"
        ser.write(idvar.encode())
        time.sleep(0.5)
        data= str(ser.readline())
        #print(data)
        print("Data Length: "+str(len(data)))
        
        
        if len(data)>70:
            solar=data.split(",")[0]
            tempA=data.split(",")[2]
            soilA=data.split(",")[3]
            tempB=data.split(",")[5]
            soilB=data.split(",")[6]
            tempC=data.split(",")[8]
            soilC=data.split(",")[9]
            tempD=data.split(",")[11]
            soilD=data.split(",")[12]
            tempE=data.split(",")[14]
            soilE=data.split(",")[15]
            windspeed=data.split(",")[17]
            completedata=str(solar)+","+str(humidity)+","+str(tempA)+","+str(soilA)+","+str(tempB)+","+str(soilB)+","+str(tempC)+","+str(soilC)+","+str(tempD)+","+str(soilD)+","+str(tempE)+","+str(soilE)+","+str(windspeed)
            print(completedata)
            pathmain="/home/pi/Share/irrigationdatabase.csv"
            now = datetime.now()
            if os.path.exists(pathmain):
                 
                 df=pd.read_csv(pathmain,names=["Date Time","Solar","Humidity","Temperature A","Soil Moisture A","Temperature B","Soil Moisture B","Temperature C","Soil Moisture C","Temperature D","Soil Moisture D","Temperature E","Soil Moisture E","Wind Speed"],skiprows=1)
                 np_df = df.as_matrix()
                 df = df.append({"Date Time":now,"Solar":solar,"Humidity":humidity,"Temperature A":tempA,"Soil Moisture A":soilA,"Temperature B":tempB,"Soil Moisture B":soilB,"Temperature C":tempC,
                                 "Soil Moisture C":soilC,"Temperature D":tempD,"Soil Moisture D":soilD,"Temperature E":tempE,"Soil Moisture E":soilE,"Wind Speed":windspeed}, ignore_index=True)   
                 df.to_csv(pathmain,  index = False)
                 print(df)
            else:
                 columns = ["Date Time","Solar","Humidity","Temperature A","Soil Moisture A","Temperature B","Soil Moisture B","Temperature C","Soil Moisture C","Temperature D","Soil Moisture D","Temperature E","Soil Moisture E","Wind Speed"]
                 df = pd.DataFrame(columns=columns)
                 np_df = df.as_matrix()
                 df = df.append({"Date Time":now,"Solar":solar,"Humidity":humidity,"Temperature A":tempA,"Soil Moisture A":soilA,"Temperature B":tempB,"Soil Moisture B":soilB,"Temperature C":tempC,
                                 "Soil Moisture C":soilC,"Temperature D":tempD,"Soil Moisture D":soilD,"Temperature E":tempE,"Soil Moisture E":soilE,"Wind Speed":windspeed}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print(df)         
                     
        else:
            print(humidity)
            print("Sensor Data not Complete")
            print(data)
    def livefeed(self):
        global liveflag
        liveflag=1
    
    def Loop(self):
        global cap,liveflag,upper,lower,camera
      #try:
        if liveflag==1:
                #ret, frame = cap.read()
                now = datetime.now()
                
                timelog=str(now).split(" ")[1].split(".")[0]
                hour=timelog.split(":")[0]
                minute=timelog.split(":")[1]
                second=timelog.split(":")[2]
                timestamp=str(hour)+"-"+str(minute)+"-"+str(second)
                print(timestamp)
                GPIO.output(23, 1)
                time.sleep(1)
                GPIO.output(23, 0)
                time.sleep(3)
                frame=cv2.imread("/home/pi/ShareFile/livefeed.png")
                imagergb="/home/pi/Share/Image/rgb_"+str(timestamp)+".png"
                imagecopy="/home/pi/Share/livefeedA.png"
              
                cv2.imwrite(imagergb,frame)
                cv2.imwrite(imagecopy,frame)
                self.disp=QtGui.QPixmap("/home/pi/Share/livefeedA.png")
                self.disp=self.disp.scaledToHeight(180)
                self.i1.setPixmap(self.disp)
                
                camera.capture('/home/pi/Share/livefeed.png')
                time.sleep(0.5)
                imagenoir="/home/pi/Share/Image/noir_"+str(timestamp)+".png"
                
                saveimage = cv2.imread("/home/pi/Share/livefeed.png")
                cv2.imwrite(imagenoir,saveimage)
                
                self.disp=QtGui.QPixmap("/home/pi/Share/livefeed.png")
                self.disp=self.disp.scaledToHeight(180)
                self.i2.setPixmap(self.disp)
                time.sleep(1)
                noir_image=cv2.imread("/home/pi/ShareFile/livefeed.png")
                color_image=cv2.imread(imagergb)
                
                # Define the motion model  
                warp_mode = cv2.MOTION_TRANSLATION  
                #warp_mode = cv2.MOTION_AFFINE  
                #warp_mode = cv2.MOTION_HOMOGRAPHY  
                # Define 2x3 or 3x3 matrices and initialize the matrix to identity  
                if warp_mode == cv2.MOTION_HOMOGRAPHY :   
                  warp_matrix = np.eye(3, 3, dtype=np.float32)  
                else :  
                  warp_matrix = np.eye(2, 3, dtype=np.float32)  
                # Specify the number of iterations.  
                number_of_iterations = 5000;  
                # Specify the threshold of the increment  
                # in the correlation coefficient between two iterations   
                termination_eps = 1e-10;  
                # Define termination criteria  
                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)  
                  
                nir_channel = noir_image[:,:,0]/256.0  
                green_channel = noir_image[:,:,1]/256.0  
                blue_channel = noir_image[:,:,2]/256.0  
                red_channel = color_image[:,:,0]/256.0
                sz = color_image.shape  
                (cc, warp_matrix) = cv2.findTransformECC (color_image[:,:,1],noir_image[:,:,1],warp_matrix, warp_mode, criteria)  
                if warp_mode == cv2.MOTION_HOMOGRAPHY :  
                  # Use warpPerspective for Homography   
                  nir_aligned = cv2.warpPerspective (nir_channel, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)  
                else :  
                  # Use warpAffine for nit_channel, Euclidean and Affine  
                  nir_aligned = cv2.warpAffine(nir_channel, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP); 
                bottom = (nir_aligned + red_channel) 
                bottom[bottom == 0] = 0.00001
                ndvi_image = (nir_aligned - red_channel)/bottom  
                       
                ndvi_image = (ndvi_image+1)/2
                print("NDVI="+str(ndvi_image.mean())) 
                ndvi_image = cv2.convertScaleAbs(ndvi_image*255)  
                ndvi_image = cv2.applyColorMap(ndvi_image, cv2.COLORMAP_JET)
                
                gndvi_image = (nir_channel - green_channel)/(nir_channel + green_channel)  
                gndvi_image = (gndvi_image+1)/2  
                gndvi_image = cv2.convertScaleAbs(gndvi_image*255)  
                gndvi_image = cv2.applyColorMap(gndvi_image, cv2.COLORMAP_JET) 
                bndvi_image = (nir_channel - blue_channel)/(nir_channel + blue_channel)  
                bndvi_image = (bndvi_image+1)/2  
                bndvi_image = cv2.convertScaleAbs(bndvi_image*255)  
                bndvi_image = cv2.applyColorMap(bndvi_image, cv2.COLORMAP_JET)  
                liveflag=0
      #except:
          #liveflag=0
          #print("Error")
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
