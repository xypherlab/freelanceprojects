import serial
import numpy as np
import os.path
import time
import Adafruit_CharLCD as LCD
from sklearn.neural_network import MLPClassifier
from collections import Counter
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN,GPIO.PUD_UP)
lcd_rs        = 21
lcd_en        = 20
lcd_d4        = 16
lcd_d5        = 26
lcd_d6        = 19
lcd_d7        = 13
lcd_backlight = 4
lcd_columns = 20
lcd_rows    = 4
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
ser.open()
lcd.message('TEMP: '+'\nHUM: '+'\nResult: ')
counttime=20
while True:
    if (GPIO.input(24)==0):
            time.sleep(1)
            os.system("sudo shutdown -h now")
    elif (GPIO.input(23)==0):
            time.sleep(1)
            ser.write("A,")
            time.sleep(1)
            pdata=ser.readline()
            s0=int(pdata.split(",")[0])
            s1=int(pdata.split(",")[1])
            s2=int(pdata.split(",")[2])
            s3=int(pdata.split(",")[3])
            s4=int(pdata.split(",")[4])
            s5=int(pdata.split(",")[5])
            s6=int(pdata.split(",")[6])
            s7=float(pdata.split(",")[7])
            s8=float(pdata.split(",")[8])
            mdatai=np.array([s0,s1,s2,s3,s4,s5,s6,s7,s8])
            for x in range(20):
                    ser.write("A,")
                    time.sleep(1)
                    pdata=ser.readline()
                    
                    s0=int(pdata.split(",")[0])
                    s1=int(pdata.split(",")[1])
                    s2=int(pdata.split(",")[2])
                    s3=int(pdata.split(",")[3])
                    s4=int(pdata.split(",")[4])
                    s5=int(pdata.split(",")[5])
                    s6=int(pdata.split(",")[6])
                    s7=float(pdata.split(",")[7])
                    s8=float(pdata.split(",")[8])
                    rdata=np.array([s0,s1,s2,s3,s4,s5,s6,s7,s8])
                    mdatai=np.vstack([mdatai,rdata])
                    counttime=counttime-1
                    lcd.clear()
                    lcd.message('TEMP: '+'\nHUM: '+'\nResult: '+'\nProcessing in '+str(counttime))
                    print rdata
            counttime=20
            mdata=np.load('/home/pi/Desktop/neuralnetworkdata.npy')
            ldata=np.load('/home/pi/Desktop/neuralnetworklabel.npy')
            print mdatai
            print mdata
            print ldata
            print "Data Length: "+str(len(mdata))
            print "Label Length: "+str(len(ldata))
            clf=MLPClassifier(solver='sgd',alpha=1e-5,hidden_layer_sizes=(10,10),learning_rate_init=0.01,max_iter=500)
            clf.fit(mdata,ldata)
            nndata=clf.predict(mdatai)
            nnproc=Counter(nndata)
            nnresult = nnproc.most_common(1)[0][0]
            print "Data: "+str(nndata)
            print "Result: "+str(nnresult)
            nndecision=int(nnresult)
            if nndecision==0:
                nntxt="NOT SPOILED"
            elif nndecision==1:
                nntxt="SPOILED"
            print nntxt
            lcd.clear()
            lcd.message('TEMP: '+str(s8)+' C'+'\nHUM: '+str(s7)+' g/m^3'+'\nResult: '+nntxt)
