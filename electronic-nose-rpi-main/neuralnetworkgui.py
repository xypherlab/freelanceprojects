import wx
import serial
import numpy as np
import os.path
import time
import Adafruit_CharLCD as LCD
from sklearn.neural_network import MLPClassifier
from collections import Counter
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

class MyForm(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self,None,wx.ID_ANY,"Food Spoilage Neural Network Classifier",size=(150,360))

        panel=wx.Panel(self,wx.ID_ANY)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer=wx.GridSizer(5,1)
        button1=wx.Button(panel,id=wx.ID_ANY,label="Analyze")
        button2=wx.Button(panel,id=wx.ID_ANY,label="Add Not Spoiled")
        button3=wx.Button(panel,id=wx.ID_ANY,label="Add Spoiled")
        button4=wx.Button(panel,id=wx.ID_ANY,label="Delete Not Spoiled")
        button5=wx.Button(panel,id=wx.ID_ANY,label="Delete Spoiled")
        button6=wx.Button(panel,id=wx.ID_ANY,label="Reading")
        button7=wx.Button(panel,id=wx.ID_ANY,label="Training")
        buttons = [button1,button2,button3,button4,button5,button6, button7]

        for button in buttons:
            self.buildButtons(button,sizer)

        panel.SetSizer(sizer)
    def buildButtons(self,btn,sizer):
        btn.Bind(wx.EVT_BUTTON,self.onButton)
        sizer.Add(btn,0,wx.ALL,6)

    
    def onButton(self,event):
        button=event.GetEventObject()
        choices=button.GetLabel()
        if choices=='Analyze':
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
                    print rdata

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
        elif choices=='Reading':
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
            print mdatai
            
        elif choices=='Training':
            mdataa=np.load('/home/pi/Desktop/notspoiled.npy')
            ldataa=np.load('/home/pi/Desktop/notspoiledlabel.npy')
            mdatab=np.load('/home/pi/Desktop/spoiled.npy')
            ldatab=np.load('/home/pi/Desktop/spoiledlabel.npy')
            mdata=np.vstack([mdataa,mdatab])
            ldata=np.hstack([ldataa,ldatab])
            print mdata
            print ldata
            np.save('/home/pi/Desktop/neuralnetworkdata',mdata)
            np.save('/home/pi/Desktop/neuralnetworklabel',ldata)
            
        elif choices=='Add Not Spoiled':
            if os.path.isfile('/home/pi/Desktop/notspoiled.npy'):
                mdatai=np.load('/home/pi/Desktop/notspoiled.npy')
                ldatai=np.load('/home/pi/Desktop/notspoiledlabel.npy')
                ldata=np.hstack([ldatai,0])
                ser.write("A,")
                time.sleep(1)
                pdata=ser.readline()
                print "Not Spoiled added to database."
                s0=int(pdata.split(",")[0])
                s1=int(pdata.split(",")[1])
                s2=int(pdata.split(",")[2])
                s3=int(pdata.split(",")[3])
                s4=int(pdata.split(",")[4])
                s5=int(pdata.split(",")[5])
                s6=int(pdata.split(",")[6])
                s7=float(pdata.split(",")[7])
                s8=float(pdata.split(",")[8])

                mdata=np.array([s0,s1,s2,s3,s4,s5,s6,s7,s8])
                mdatai=np.vstack([mdatai,mdata])
                np.save('/home/pi/Desktop/notspoiled',mdatai)
                np.save('/home/pi/Desktop/notspoiledlabel',ldata)
                print mdatai
                print ldata
            else:
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

                mdata=np.array([s0,s1,s2,s3,s4,s5,s6,s7,s8])
                ldata=np.array([0])
                np.save('/home/pi/Desktop/notspoiled',mdata)
                np.save('/home/pi/Desktop/notspoiledlabel',ldata)
                print mdata
                print ldata
        elif choices=='Add Spoiled':
            if os.path.isfile('/home/pi/Desktop/spoiled.npy'):
                mdatai=np.load('/home/pi/Desktop/spoiled.npy')
                ldatai=np.load('/home/pi/Desktop/spoiledlabel.npy')
                ldata=np.hstack([ldatai,1])
                ser.write("A,")
                time.sleep(1)
                pdata=ser.readline()
                print "Spoiled added to database."
                s0=int(pdata.split(",")[0])
                s1=int(pdata.split(",")[1])
                s2=int(pdata.split(",")[2])
                s3=int(pdata.split(",")[3])
                s4=int(pdata.split(",")[4])
                s5=int(pdata.split(",")[5])
                s6=int(pdata.split(",")[6])
                s7=float(pdata.split(",")[7])
                s8=float(pdata.split(",")[8])

                mdata=np.array([s0,s1,s2,s3,s4,s5,s6,s7,s8])
                mdatai=np.vstack([mdatai,mdata])
                np.save('/home/pi/Desktop/spoiled',mdatai)
                np.save('/home/pi/Desktop/spoiledlabel',ldata)
                print mdatai
                print ldata
            else:
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

                mdata=np.array([s0,s1,s2,s3,s4,s5,s6,s7,s8])
                ldata=np.array([1])
                np.save('/home/pi/Desktop/spoiled',mdata)
                np.save('/home/pi/Desktop/spoiledlabel',ldata)
                print mdata
                print ldata  
        elif choices=='Delete Not Spoiled':
            if os.path.isfile('/home/pi/Desktop/notspoiled.npy'):
                mdatai=np.load('/home/pi/Desktop/notspoiled.npy')
                ldatai=np.load('/home/pi/Desktop/notspoiledlabel.npy')
                x=len(mdatai)-1
                y=len(ldatai)-1
                mdatai=np.delete(mdatai,x,0)
                ldatai=np.delete(ldatai,x,0)
                np.save('/home/pi/Desktop/notspoiled',mdatai)
                np.save('/home/pi/Desktop/notspoiledlabel',ldatai)
                print "Not Spoiled data deleted."
                print mdatai
                print ldatai
            else:
                print "File doesn't exist"
        elif choices=='Delete Spoiled':
            if os.path.isfile('/home/pi/Desktop/spoiled.npy'):
                mdatai=np.load('/home/pi/Desktop/spoiled.npy')
                ldatai=np.load('/home/pi/Desktop/spoiledlabel.npy')
                x=len(mdatai)-1
                y=len(ldatai)-1
                mdatai=np.delete(mdatai,x,0)
                ldatai=np.delete(ldatai,x,0)
                np.save('/home/pi/Desktop/spoiled',mdatai)
                np.save('/home/pi/Desktop/spoiledlabel',ldatai)
                print "Spoiled data deleted."
                print mdatai
                print ldatai
            else:
                print "File doesn't exist"
       
                
            
if __name__ == "__main__":
    app = wx.App(False)
    frame=MyForm()
    frame.Show()
    app.MainLoop()
