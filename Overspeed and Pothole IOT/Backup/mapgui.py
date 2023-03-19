from PyQt4 import QtGui, QtCore
import sys
from mapsplotlib import mapsplot as mplt
import pandas as pd
import time
import os
import numpy as np
import urllib, json
import cv2
import datetime
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global start_time,reportflag
        reportflag=1
        start_time = time.time()
        
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
       
        #Head Title
        font = QtGui.QFont("Times", 18)
        self.t1=QtGui.QLabel("OVERSPEED AND POTHOLE DETECTION",self)
        self.t1.setFont(font)
        self.t1.move(50,10)
        self.t1.resize(600,50)
        #
        #Map Title
        fonta = QtGui.QFont("Times", 16)
        self.t2=QtGui.QLabel("Map View",self)
        self.t2.setFont(fonta)
        self.t2.move(700,10)
        self.t2.resize(600,50)
        #
        #Overspeed Title
        self.t3=QtGui.QLabel("Overspeed Report:",self)
        self.t3.setFont(fonta)
        self.t3.move(50,450)
        self.t3.resize(600,50)
        #
        #Pothole Title
        self.t4=QtGui.QLabel("Pothole Report:",self)
        self.t4.setFont(fonta)
        self.t4.move(700,450)
        self.t4.resize(600,50)
        #
        #Power Status Title
        self.t5=QtGui.QLabel("Power Status:",self)
        self.t5.setFont(fonta)
        self.t5.move(50,150)
        self.t5.resize(600,50)
        #
        #Image Map Display
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(700,60,800,400)
        self.disp=QtGui.QPixmap("blackscreen.png")
        self.disp=self.disp.scaledToHeight(550)
        self.i1.setPixmap(self.disp)
                
        #

        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.move(50,200)
        self.table.setHorizontalHeaderLabels(['           Vehicle ID             ','           Device Power            ','           Date            ','           Time            '])
        self.table.resize(510,200)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)

        self.tableA = QtGui.QTableWidget(self)
        self.tableA.setColumnCount(7)
        self.tableA.move(50,500)
        self.tableA.setHorizontalHeaderLabels(['     Vehicle ID       ','     Latitude      ','     Longitude      ','     Speed Limit      ','     Speed     ','     Date     ','     Time     '])
        self.tableA.resize(600,200)
        self.tableA.resizeColumnsToContents()
        self.tableA.verticalHeader().setVisible(0)

        self.tableB = QtGui.QTableWidget(self)
        self.tableB.setColumnCount(5)
        self.tableB.move(700,500)
        self.tableB.setHorizontalHeaderLabels(['         Latitude           ','         Longitude          ','         Pothole Level          ','         Date         ','          Time         '])
        self.tableB.resize(550,400)
        self.tableB.resizeColumnsToContents()
        self.tableB.verticalHeader().setVisible(0)

        pathtarget="potholedata.csv"
        if os.path.exists(pathtarget):
                     
            df=pd.read_csv(pathtarget,names=['latitude','longitude','potholelevel','date','time'],skiprows=1)
            np_df = df.as_matrix()
            idnumber=len(df.index)
             
            cnt=0
                
            self.tableB.setRowCount(len(np_df))
            print np_df
            for i in xrange(len(np_df)):
                 self.tableB.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(np_df[cnt][0])+""))
                 self.tableB.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])+""))
                 self.tableB.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))
                 self.tableB.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))
                 self.tableB.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][4])+""))
                 
                 cnt=cnt+1
                 
        pathtarget="overspeeddata.csv"
        if os.path.exists(pathtarget):
                     
            df=pd.read_csv(pathtarget,names=['vehicleid','latitude','longitude','speedlimit','speed','date','time'],skiprows=1)
            np_df = df.as_matrix()
            idnumber=len(df.index)
                
            cnt=0
                
            self.tableA.setRowCount(len(np_df))
            print np_df
            for i in xrange(len(np_df)):
                 self.tableA.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(np_df[cnt][0])+""))
                 self.tableA.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])+""))
                 self.tableA.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))
                 self.tableA.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))
                 self.tableA.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][4])+""))
                 self.tableA.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(np_df[cnt][5])+""))
                 self.tableA.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(np_df[cnt][6])+""))
                 
                 cnt=cnt+1 
        self.setGeometry(0,20,1400,700)
        
   
        
 
    def Loop(self):
        global start_time,reportflag
        elapsed_time = time.time() - start_time
        x=1
        url = "https://api.thingspeak.com/channels/540947/feeds/last"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        latitude=float(data["field1"])
        longitude=float(data["field2"])
        detectedtype=int(data["field3"])
        speed=float(data["field4"])
        vehicleid=float(data["field5"])
        powerstatus=float(data["field6"])
        entryid=data["entry_id"]
        if detectedtype==1 or detectedtype==2:
            label="P"
            labelname="Pothole-"
        elif detectedtype==0:
            label="S"
            labelname="Speed-"
        print "Latitude: "+str(data["field1"])
        print "Longitude: "+str(data["field2"])
        print "Type: "+str(data["field3"])
        print "Speed: "+str(data["field4"])
        print "Entry ID: "+str(data["entry_id"])
        print "Vehicle ID: "+str(data["field5"])
        print "Power Status: "+str(data["field6"])
        timenow=datetime.datetime.now().strftime("%H:%M")
        datenow=datetime.datetime.now().strftime("%Y-%m-%d")
        print "reportflag="+str(reportflag)
        if powerstatus==0 and reportflag==1:
                print "Battery Mode"
                
                pathtarget="powerdata.csv"
                if os.path.exists(pathtarget):
                             
                     df=pd.read_csv(pathtarget,names=['vehicleid','status','date','time'],skiprows=1)
                     np_df = df.as_matrix()
                     idnumber=len(df.index)
                     df = df.append({'vehicleid':vehicleid,'status':"Battery Mode",'date':datenow,'time':timenow}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                  
                     
                else:
                     
                     columns = ['vehicleid','status','date','time']
                     df = pd.DataFrame(columns=columns)
                     np_df = df.as_matrix()
                     idnumber=0
                     df = df.append({'vehicleid':vehicleid,'status':"Battery Mode",'date':datenow,'time':timenow}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                cnt=0
                df=pd.read_csv(pathtarget,names=['vehicleid','status','date','time'],skiprows=1)
                np_df = df.as_matrix()    
                self.table.setRowCount(len(np_df))
                
                print np_df
                for i in xrange(len(np_df)):
                     self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(np_df[cnt][0])+""))
                     self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])+""))
                     self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))
                     self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))
                     
                     cnt=cnt+1
                reportflag=0
        elif powerstatus==1 and reportflag==0:
                print "Power Mode"
                reportflag=1
                
                pathtarget="powerdata.csv"
                if os.path.exists(pathtarget):
                             
                     df=pd.read_csv(pathtarget,names=['vehicleid','status','date','time'],skiprows=1)
                     np_df = df.as_matrix()
                     idnumber=len(df.index)
                     df = df.append({'vehicleid':vehicleid,'status':"Power Mode",'date':datenow,'time':timenow}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                  
                     
                else:
                     
                     columns = ['vehicleid','status','date','time']
                     df = pd.DataFrame(columns=columns)
                     np_df = df.as_matrix()
                     idnumber=0
                     df = df.append({'vehicleid':vehicleid,'status':"Power Mode",'date':datenow,'time':timenow}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                cnt=0
                df=pd.read_csv(pathtarget,names=['vehicleid','status','date','time'],skiprows=1)
                np_df = df.as_matrix()    
                self.table.setRowCount(len(np_df))
                print np_df
                for i in xrange(len(np_df)):
                     self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(np_df[cnt][0])+""))
                     self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])+""))
                     self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))
                     self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))
                     
                     cnt=cnt+1    
        if latitude>=14.537119 and latitude<=14.554740 and longitude>=120.990020 and longitude<=120.992274:
            speedlimit=50
            print "Speed Limit: 50"
        elif latitude>=14.536111 and latitude<=14.553022 and longitude>=120.989538 and longitude<=120.989844:
            speedlimit=60
            print "Speed Limit: 60"    
        else:
            speedlimit=1000
            print "Speed Limit: None"
        if speed>speedlimit and detectedtype==0:
            print "Speed --------------------------------------"
    
            pathtarget="gpsmaptable.csv"
            if os.path.exists(pathtarget):
                         
                 df=pd.read_csv(pathtarget,names=['id','latitude','longitude','color','size','label','entryid'],skiprows=1)
                 np_df = df.as_matrix()
                 idnumber=len(df.index)
                 if entryid!=np_df[idnumber-1][6]:
                     df = df.append({'id':idnumber,'latitude':latitude,'longitude':longitude,'color':"red",'size':"big",'label':label,'entryid':entryid}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                     
                     if x==1:
                            #start_time = time.time()
                            mplt.register_api_key('AIzaSyCLdI8H_cWNMw-PuQ9RtZrG2GHG--KjSYE')
                            pathtarget="gpsmaptable.csv"
                            df=pd.read_csv(pathtarget,names=['id','latitude','longitude','color','size','label','entryid'],skiprows=1)
                            df=df.iloc[[-1]]
                            print df
                            mplt.plot_markers(df)
                            self.disp=QtGui.QPixmap("temp.png")
                            self.disp=self.disp.scaledToHeight(550)
                            self.i1.setPixmap(self.disp)
                            mapimage = cv2.imread("temp.png")
                            imagename=labelname+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))+".jpg"
                            print imagename
                            cv2.imwrite("imagedatabase/"+imagename,mapimage)
                            
                            
                            
                        
                            pathtarget="overspeeddata.csv"
                            if os.path.exists(pathtarget):
                                         
                                 df=pd.read_csv(pathtarget,names=['vehicleid','latitude','longitude','speedlimit','speed','date','time'],skiprows=1)
                                 np_df = df.as_matrix()
                                 idnumber=len(df.index)
                                 df = df.append({'vehicleid':vehicleid,'latitude':latitude,'longitude':longitude,'speedlimit':speedlimit,'speed':speed,'date':datenow,'time':timenow}, ignore_index=True)
                                 df.to_csv(pathtarget,  index = False)
                                 print df
        
                                 
                            else:
                                 
                                 columns = ['vehicleid','latitude','longitude','speedlimit','speed','date','time']
                                 df = pd.DataFrame(columns=columns)
                                 np_df = df.as_matrix()
                                 idnumber=0
                                 df = df.append({'vehicleid':vehicleid,'latitude':latitude,'longitude':longitude,'speedlimit':speedlimit,'speed':speed,'date':datenow,'time':timenow}, ignore_index=True)
                                 df.to_csv(pathtarget,  index = False)
                                 print df
                            cnt=0
                            df=pd.read_csv(pathtarget,names=['vehicleid','latitude','longitude','speedlimit','speed','date','time'],skiprows=1)
                            np_df = df.as_matrix()      
                            self.tableA.setRowCount(len(np_df))
                            print np_df
                            for i in xrange(len(np_df)):
                                 self.tableA.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(np_df[cnt][0])+""))
                                 self.tableA.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])+""))
                                 self.tableA.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))
                                 self.tableA.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))
                                 self.tableA.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][4])+""))
                                 self.tableA.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(np_df[cnt][5])+""))
                                 self.tableA.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(np_df[cnt][6])+""))
                                 
                                 cnt=cnt+1 
                            

            else:
                             
                         columns = ['id','latitude','longitude','color','size','label','entryid']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         idnumber=0
                         df = df.append({'id':0,'latitude':latitude,'longitude':longitude,'color':"red",'size':"big",'label':label,'entryid':entryid}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         print df                 
                                 
        elif detectedtype==2 or detectedtype==1:
                print "Pothole --------------------------------------"
                if detectedtype==1:
                    potholelevel="Moderate"
                elif detectedtype==2:
                    potholelevel="High"

                pathtarget="gpsmaptable.csv"
                if os.path.exists(pathtarget):
                             
                     df=pd.read_csv(pathtarget,names=['id','latitude','longitude','color','size','label','entryid'],skiprows=1)
                     np_df = df.as_matrix()
                     idnumber=len(df.index)
                     if entryid!=np_df[idnumber-1][6]:
                         df = df.append({'id':idnumber,'latitude':latitude,'longitude':longitude,'color':"red",'size':"big",'label':label,'entryid':entryid}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         print df
                         
                         if x==1:
                                #start_time = time.time()
                                mplt.register_api_key('AIzaSyCLdI8H_cWNMw-PuQ9RtZrG2GHG--KjSYE')
                                pathtarget="gpsmaptable.csv"
                                df=pd.read_csv(pathtarget,names=['id','latitude','longitude','color','size','label','entryid'],skiprows=1)
                                df=df.iloc[[-1]]
                                print df
                                mplt.plot_markers(df)
                                self.disp=QtGui.QPixmap("temp.png")
                                self.disp=self.disp.scaledToHeight(550)
                                self.i1.setPixmap(self.disp)
                                mapimage = cv2.imread("temp.png")
                                imagename=labelname+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))+".jpg"
                                print imagename
                                cv2.imwrite("imagedatabase/"+imagename,mapimage)
                                pathtarget="potholedata.csv"
                                if os.path.exists(pathtarget):
                                             
                                     df=pd.read_csv(pathtarget,names=['latitude','longitude','potholelevel','date','time'],skiprows=1)
                                     np_df = df.as_matrix()
                                     idnumber=len(df.index)
                                     df = df.append({'latitude':latitude,'longitude':longitude,'potholelevel':potholelevel,'date':datenow,'time':timenow}, ignore_index=True)
                                     df.to_csv(pathtarget,  index = False)
                                     print df

                                     
                                else:
                                     
                                     columns = ['latitude','longitude','potholelevel','date','time']
                                     df = pd.DataFrame(columns=columns)
                                     np_df = df.as_matrix()
                                     idnumber=0
                                     df = df.append({'latitude':latitude,'longitude':longitude,'potholelevel':potholelevel,'date':datenow,'time':timenow}, ignore_index=True)
                                     df.to_csv(pathtarget,  index = False)
                                     print df
                                cnt=0
                                df=pd.read_csv(pathtarget,names=['latitude','longitude','potholelevel','date','time'],skiprows=1)
                                np_df = df.as_matrix()    
                                self.tableB.setRowCount(len(np_df))
                                print np_df
                                
                                for i in xrange(len(np_df)):
                                     self.tableB.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(np_df[cnt][0])+""))
                                     self.tableB.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])+""))
                                     self.tableB.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))
                                     self.tableB.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))
                                     self.tableB.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][4])+""))
                                     
                                     cnt=cnt+1
                else:
                             
                         columns = ['id','latitude','longitude','color','size','label','entryid']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         idnumber=0
                         df = df.append({'id':0,'latitude':latitude,'longitude':longitude,'color':"red",'size':"big",'label':label,'entryid':entryid}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         print df  


        
                 
            
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
