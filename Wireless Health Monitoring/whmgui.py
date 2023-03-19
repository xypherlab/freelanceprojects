from PyQt4 import QtGui, QtCore
import sys
import time
import os
import socket
import pandas as pd
import numpy as np
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,start_time,data,conn,BUFFER_SIZE,initialflag,removeflag
        removeflag=1
        initialflag=0
        flag=0
        start_time = time.time()
        
        self.setWindowTitle("Wireless Health Monitoring")    
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        #Login Form
        self.m1=QtGui.QLabel("Username:",self)
        self.m1.move(140,90)
        self.m2=QtGui.QLineEdit(self)
        self.m2.move(200,95)
        self.m2.resize(100,20)
        
        self.m3=QtGui.QLabel("Password:",self)
        self.m3.move(140,120)
        self.m4=QtGui.QLineEdit(self)
        self.m4.move(200,125)
        self.m4.resize(100,20)
        
        self.login = QtGui.QPushButton("Login",self)
        self.login.clicked.connect(self.loginfunc)
        self.login.move(200,180)
        
        self.setGeometry(500,100,500,300)
        ######################

        #Status Form
        self.connect = QtGui.QPushButton("Connect",self)
        self.connect.clicked.connect(self.connectfunc)
        self.connect.move(350,410)
        
        self.logout = QtGui.QPushButton("Logout",self)
        self.logout.clicked.connect(self.logoutfunc)
        self.logout.move(550,410)
        
        font = QtGui.QFont("Times", 12)
        self.t1=QtGui.QLabel("St. Jude College Community-Based Rehabilitation Center",self)
        self.t1.setFont(font)
        self.t1.move(60,10)
        self.t1.resize(900,50)
        
        font = QtGui.QFont("Times", 10)
        self.l1=QtGui.QLabel("Current Status",self)
        self.l1.setFont(font)
        self.l1.move(350,50)
        self.l1.resize(900,50)
        
        
        
        font = QtGui.QFont("Times", 6)
        self.l2=QtGui.QLabel("Station:  ",self)
        self.l2.setFont(font)
        self.l2.move(350,100)
        self.l2.resize(900,50)
        
        font = QtGui.QFont("Times", 6)
        self.l3=QtGui.QLabel("Patient Name: ",self)
        self.l3.setFont(font)
        self.l3.move(150,150)
        self.l3.resize(900,50)
        
        font = QtGui.QFont("Times", 6)
        self.l4=QtGui.QLabel("Attending Doctor/Supervisor: ",self)
        self.l4.setFont(font)
        self.l4.move(150,200)
        self.l4.resize(900,50)
        
        font = QtGui.QFont("Times", 6)
        self.l5=QtGui.QLabel("Clinical Staff in-charge: ",self)
        self.l5.setFont(font)
        self.l5.move(470,150)
        self.l5.resize(900,50)
        
        
        font = QtGui.QFont("Times", 6)
        self.l6=QtGui.QLabel("Note to Clinical Staff in-charge: ",self)
        self.l6.setFont(font)
        self.l6.move(170,350)
        self.l6.resize(900,50)
        
        font = QtGui.QFont("Times", 6)
        self.t2=QtGui.QLabel("      Heart Rate\n(Beats per Minute)",self)
        self.t2.setFont(font)
        self.t2.move(150,250)
        self.t2.resize(350,50)
        
        font = QtGui.QFont("Times", 6)
        self.t3=QtGui.QLabel("      Respiratory Rate\nRespiration per Minute ",self)
        self.t3.setFont(font)
        self.t3.move(350,250)
        self.t3.resize(350,50)
        
        font = QtGui.QFont("Times",  6)
        self.t4=QtGui.QLabel("  Temperature\nDegree Celsius",self)
        self.t4.setFont(font)
        self.t4.move(600,250)
        self.t4.resize(350,50)
        
        font = QtGui.QFont("Times",  6)
        self.v1=QtGui.QLabel("----\n----",self)
        self.v1.setFont(font)
        self.v1.move(200,300)
        self.v1.resize(350,50)
        
        font = QtGui.QFont("Times",  6)
        self.v2=QtGui.QLabel("----\n----",self)
        self.v2.setFont(font)
        self.v2.move(400,300)
        self.v2.resize(350,50)
        
        font = QtGui.QFont("Times",  6)
        self.v3=QtGui.QLabel("----\n----",self)
        self.v3.setFont(font)
        self.v3.move(630,300)
        self.v3.resize(350,50)
        self.l1.setVisible(0)
        self.l2.setVisible(0)
        self.l3.setVisible(0)
        self.l4.setVisible(0)
        self.l5.setVisible(0)
        self.l6.setVisible(0)
        self.t1.setVisible(0)
        self.t2.setVisible(0)
        self.t3.setVisible(0)
        self.t4.setVisible(0)
        self.v1.setVisible(0)
        self.v2.setVisible(0)
        self.v3.setVisible(0)
        self.connect.setVisible(0)
        self.logout.setVisible(0)
        ################################

        #Modify Record
             
        self.resetdata = QtGui.QPushButton("Reset Data",self)
        self.resetdata.clicked.connect(self.resetdatafunc)
        self.resetdata.move(350,610)
        
        self.logoutsave = QtGui.QPushButton("Logout",self)
        self.logoutsave.clicked.connect(self.logoutsavefunc)
        self.logoutsave.move(550,610)

        self.n2=QtGui.QLineEdit(self)
        self.n2.move(550,200)
        self.n2.resize(50,20)
        self.n3=QtGui.QLineEdit(self)
        self.n3.move(250,150)
        self.n3.resize(100,20)
        self.n4=QtGui.QLineEdit(self)
        self.n4.move(350,200)
        self.n4.resize(100,20)
        self.n5=QtGui.QLineEdit(self)
        self.n5.move(620,150)
        self.n5.resize(100,20)

        
        #self.t1.move(60,10)
        #self.l1.move(350,50)
        #self.l2.move(470,200)
        #self.l3.move(150,150)
        #self.l4.move(150,200)
        #self.l5.move(470,150)
       
        #
        #
        font = QtGui.QFont("Times", 6)
        self.l6=QtGui.QLabel("Note to Clinical Staff in-charge: ",self)
        self.l6.setFont(font)
        self.l6.move(70,700)
        self.l6.resize(400,30)
        #
        self.n6=QtGui.QLineEdit(self)
        self.n6.move(270,700)
        self.n6.resize(300,30)
        #
        
        self.editnote = QtGui.QPushButton("Edit",self)
        self.editnote.clicked.connect(self.editnotefunc)
        self.editnote.move(600,700)
        self.editnote.resize(50,30)
        
        
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.move(50,350)
        self.table.setHorizontalHeaderLabels(['      Heart Rate\n(Beats per Minute)','  Temperature\nDegree Celsius','      Respiratory Rate\nRespiration per Minute '])
        self.table.resize(720,250)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        pathtarget="logrecord.csv"
        cnt=0
        if os.path.exists(pathtarget):
            df=pd.read_csv(pathtarget,names=['HeartRate','Temperature','RespiratoryRate'],skiprows=1)
            np_df = df.as_matrix()
            self.table.setRowCount(len(np_df))
            for i in xrange(len(np_df)):
                 
                 self.table.setItem(cnt, 0, QtGui.QTableWidgetItem("            "+str(np_df[cnt,0])+""))
                 self.table.setItem(cnt, 1, QtGui.QTableWidgetItem("            "+str(np_df[cnt,1])+""))
                 self.table.setItem(cnt, 2, QtGui.QTableWidgetItem("            "+str(np_df[cnt,2])+""))
                 
                 cnt=cnt+1
        self.table.setVisible(0)
        self.n2.setVisible(0)
        self.n3.setVisible(0)
        self.n4.setVisible(0)
        self.n5.setVisible(0)
        self.n6.setVisible(0)
        self.resetdata.setVisible(0)
        self.logoutsave.setVisible(0)
        self.editnote.setVisible(0)
        ################################

        #Doctor Interface
        self.current = QtGui.QPushButton("Current Status",self)
        self.current.clicked.connect(self.currentfunc)
        self.current.move(180,120)
        self.current.resize(150,50)
        self.logrecord = QtGui.QPushButton("Log Record",self)
        self.logrecord.clicked.connect(self.logrecordfunc)
        self.logrecord.move(180,180)
        self.logrecord.resize(150,50)
        self.current.setVisible(0)
        self.logrecord.setVisible(0)

        #Admin Interface
        self.modifylogrecord = QtGui.QPushButton("Modify Log Record",self)
        self.modifylogrecord.clicked.connect(self.modifylogrecordfunc)
        self.modifylogrecord.move(180,240)
        self.modifylogrecord.resize(200,50)
        self.modifylogrecord.setVisible(0)
    def  editnotefunc(self):
        
        note=str(self.n6.text())
        
        pathtarget="note.csv"
 
        if os.path.exists(pathtarget):
            os.remove("note.csv")
        columns = ['Note']
        df = pd.DataFrame(columns=columns)
        np_df = df.as_matrix()
         
        df = df.append({'Note':note}, ignore_index=True)
        df.to_csv(pathtarget,  index = False)
        print df
        stationname=str(self.n2.text())
        patientname=str(self.n3.text())
        doctorname=str(self.n4.text())
        clinicalname=str(self.n5.text())
        if stationname=="" or patientname=="" or doctorname=="" or clinicalname=="":
            dump=0
        else:
            pathtarget="information.csv"
     
            if os.path.exists(pathtarget):
                os.remove("information.csv")
            columns = ['Station','Patient','Doctor','Clinical']
            df = pd.DataFrame(columns=columns)
            np_df = df.as_matrix()
             
            df = df.append({'Station':stationname,'Patient':patientname,'Doctor':doctorname,'Clinical':clinicalname}, ignore_index=True)
            df.to_csv(pathtarget,  index = False)
            print df
        #
    def logoutsavefunc(self):
        
        self.login.setVisible(1)
        self.m1.setVisible(1)
        self.m2.setVisible(1)
        self.m3.setVisible(1)
        self.m4.setVisible(1)
        self.setGeometry(500,100,500,300)
        #
        self.l1.setVisible(0)
        self.l2.setVisible(0)
        self.l3.setVisible(0)
        self.l4.setVisible(0)
        self.l5.setVisible(0)
        self.l6.setVisible(0)
        self.t1.setVisible(0)
        self.t2.setVisible(0)
        self.t3.setVisible(0)
        self.t4.setVisible(0)
        self.v1.setVisible(0)
        self.v2.setVisible(0)
        self.v3.setVisible(0)
        self.connect.setVisible(0)
        self.logout.setVisible(0)
        self.table.setVisible(0)
        self.n2.setVisible(0)
        self.n3.setVisible(0)
        self.n4.setVisible(0)
        self.n5.setVisible(0)
        self.n6.setVisible(0)
        self.resetdata.setVisible(0)
        self.logoutsave.setVisible(0)
        self.editnote.setVisible(0)
        self.modifylogrecord.setVisible(0)
    def resetdatafunc(self):
        pathtarget="logrecord.csv"
        cnt=0
        if os.path.exists(pathtarget):
            df=pd.read_csv(pathtarget,names=['HeartRate','Temperature','RespiratoryRate'],skiprows=1)
            np_df = df.as_matrix()
            self.table.setRowCount(len(np_df))
            for i in xrange(len(np_df)):
                 
                 self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""))
                 self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""))
                 self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""))
                 
                 cnt=cnt+1
        os.remove("logrecord.csv")
  
  
        
    
    def connectfunc(self):
        global initialflag,flag
        initialflag=1
        flag=1
    def logoutfunc(self):
            self.setWindowTitle("Clinical")
            #
            self.login.setVisible(1)
            self.m1.setVisible(1)
            self.m2.setVisible(1)
            self.m3.setVisible(1)
            self.m4.setVisible(1)
            self.setGeometry(500,100,500,300)
            #
            self.l1.setVisible(0)
            self.l2.setVisible(0)
            self.l3.setVisible(0)
            self.l4.setVisible(0)
            self.l5.setVisible(0)
            self.l6.setVisible(0)
            self.t1.setVisible(0)
            self.t2.setVisible(0)
            self.t3.setVisible(0)
            self.t4.setVisible(0)
            self.v1.setVisible(0)
            self.v2.setVisible(0)
            self.v3.setVisible(0)
            self.connect.setVisible(0)
            self.logout.setVisible(0)

            
    def loginfunc(self):
        username=str(self.m2.text())
        password=str(self.m4.text())
        if username=="Clinical" and password=="1234":
            self.m2.setText("")
            self.m4.setText("")
            self.setWindowTitle("Clinical")
            #
            self.login.setVisible(0)
            self.m1.setVisible(0)
            self.m2.setVisible(0)
            self.m3.setVisible(0)
            self.m4.setVisible(0)
            #Status
            self.l1.setVisible(1)
            self.l2.setVisible(1)
            self.l2.move(350,100)
            self.l3.setVisible(1)
            self.l4.setVisible(1)
            self.l5.setVisible(1)
            self.l6.setVisible(1)
            self.t1.setVisible(1)
            self.t2.setVisible(1)
            self.t3.setVisible(1)
            self.t4.setVisible(1)
            self.v1.setVisible(1)
            self.v2.setVisible(1)
            self.v3.setVisible(1)
            self.connect.setVisible(1)
            self.logout.setVisible(1)
            self.setGeometry(490,70,800,500)
        elif username=="Doctor" and password=="1234":
            self.m2.setText("")
            self.m4.setText("")
            self.setWindowTitle("Doctor")
            #
            self.login.setVisible(0)
            self.m1.setVisible(0)
            self.m2.setVisible(0)
            self.m3.setVisible(0)
            self.m4.setVisible(0)
            #
            self.current.setVisible(1)
            self.logrecord.setVisible(1)
            self.setGeometry(500,100,500,300)
        elif username=="Admin" and password=="1234":
            self.m2.setText("")
            self.m4.setText("")
            #
            self.login.setVisible(0)
            self.m1.setVisible(0)
            self.m2.setVisible(0)
            self.m3.setVisible(0)
            self.m4.setVisible(0)
            #
            self.setWindowTitle("Admin")
            self.current.setVisible(1)
            self.logrecord.setVisible(1)
            self.modifylogrecord.setVisible(1)
            self.setGeometry(500,100,500,400)
        else:
            self.m2.setText("")
            self.m4.setText("")
            print "Wrong username or password"
    def currentfunc(self):
            self.current.setVisible(0)
            self.logrecord.setVisible(0)
            self.modifylogrecord.setVisible(0)
            self.l1.setVisible(1)
            self.l2.setVisible(1)
            self.l2.move(350,100)
            self.l3.setVisible(1)
            self.l4.setVisible(1)
            self.l5.setVisible(1)
            self.l6.setVisible(1)
            self.t1.setVisible(1)
            self.t2.setVisible(1)
            self.t3.setVisible(1)
            self.t4.setVisible(1)
            self.v1.setVisible(1)
            self.v2.setVisible(1)
            self.v3.setVisible(1)
            self.connect.setVisible(1)
            self.connect.move(350,410)
            self.logout.setVisible(1)
            self.setGeometry(490,70,800,500)
        #
    def logrecordfunc(self):
            self.modifylogrecord.setVisible(0)
            self.current.setVisible(0)
            self.logrecord.setVisible(0)
            self.setGeometry(490,70,800,800)
            self.l1.setVisible(1)
            self.l2.setVisible(1)
            self.l2.move(350,100)
            self.l3.setVisible(1)
            self.l4.setVisible(1)
            self.l5.setVisible(1)
            self.l6.setVisible(1)
            self.t1.setVisible(1)
            self.t2.setVisible(1)
            self.t3.setVisible(1)
            self.t4.setVisible(1)
            self.v1.setVisible(1)
            self.v2.setVisible(1)
            self.v3.setVisible(1)
            self.connect.setVisible(1)
            self.connect.move(150,610)
            self.logout.setVisible(1)
            self.logout.move(550,610)
            self.table.setVisible(1)
            
    def modifylogrecordfunc(self):
            self.modifylogrecord.setVisible(0)
            self.current.setVisible(0)
            self.logrecord.setVisible(0)
            self.setGeometry(490,70,800,800)
            self.l1.setVisible(1)
            self.l2.setVisible(1)
            self.l2.move(470,200)
            self.l3.setVisible(1)
            self.l4.setVisible(1)
            self.l5.setVisible(1)
            self.l6.setVisible(1)
            self.t1.setVisible(1)
            self.t2.setVisible(1)
            self.t3.setVisible(1)
            self.t4.setVisible(1)
            self.v1.setVisible(1)
            self.v2.setVisible(1)
            self.v3.setVisible(1)
            self.connect.setVisible(1)
            self.connect.move(150,610)
            self.logoutsave.setVisible(1)
            self.table.setVisible(1)
            self.n2.setVisible(1)
            self.n3.setVisible(1)
            self.n4.setVisible(1)
            self.n5.setVisible(1)
            self.n6.setVisible(1)
            self.resetdata.setVisible(1)
            self.editnote.setVisible(1)
    def Loop(self):
        global start_time,data,conn,BUFFER_SIZE,initialflag,flag,removeflag
        elapsed_time=time.time()-start_time
        
        
        if initialflag==1:
            initialflag=0
            print "Initializing"
            TCP_IP = '192.168.43.214'
            TCP_PORT = 80
            BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.bind((TCP_IP, TCP_PORT))
            s.listen(1)
        
            conn, addr = s.accept()
            print 'Connection address:', addr
            pathtarget="information.csv"
            df=pd.read_csv(pathtarget,names=['Station','Patient','Doctor','Clinical'],skiprows=1)             
            np_df = df.as_matrix()
            stationname=str(np_df[0,0])
            patientname=str(np_df[0,1])
            doctorname=str(np_df[0,2])
            clinicalname=str(np_df[0,3])
            pathtarget="note.csv"
            df=pd.read_csv(pathtarget,names=['Note'],skiprows=1)             
            np_df = df.as_matrix()
            note=str(np_df[0,0])
           
            self.l2.setText("Station:  "+stationname)
            self.l3.setText("Patient Name: "+patientname)
            self.l4.setText("Attending Doctor/Supervisor: "+doctorname)
            self.l5.setText("Clinical Staff in-charge: "+clinicalname)
            self.l6.setText("Note to Clinical Staff in-charge: "+note)
            
        if elapsed_time>=20 and flag==1:
            start_time = time.time()
            try:
                data = conn.recv(BUFFER_SIZE)
                
                print "received data:", data
                val1=int(data.split(",")[1])
                val2=float(data.split(",")[2])
                val3=int(data.split(",")[3])
                
                if removeflag==0:
                    self.v1.setText(str(val3))
                    self.v2.setText(str(val1))
                    self.v3.setText(str(val2))   
                    print "Heart Rate: "+str(val3)
                    print "Respiratory Rate: "+str(val1)
                    print "Temperature: "+str(val2)
                    conn.send(data)  # echo
                    pathtarget="logrecord.csv"
                    cnt=0
                    if os.path.exists(pathtarget):
                                     
                         df=pd.read_csv(pathtarget,names=['HeartRate','Temperature','RespiratoryRate'],skiprows=1)
                         np_df = df.as_matrix()
                         df = df.append({'HeartRate':val3,'Temperature':val2,'RespiratoryRate':val1}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         print df
                    else:
                         
                         columns = ['HeartRate','Temperature','RespiratoryRate']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         
                         df = df.append({'HeartRate':val3,'Temperature':val2,'RespiratoryRate':val1}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         print df
                    cnt=0
                    self.table.setRowCount(len(np_df))
                    for i in xrange(len(np_df)):
                         
                         self.table.setItem(cnt, 0, QtGui.QTableWidgetItem("            "+str(np_df[cnt,0])+""))
                         self.table.setItem(cnt, 1, QtGui.QTableWidgetItem("            "+str(np_df[cnt,1])+""))
                         self.table.setItem(cnt, 2, QtGui.QTableWidgetItem("            "+str(np_df[cnt,2])+""))
                         
                         cnt=cnt+1
                if removeflag==1:
                    removeflag=0
            except:
                dump=0

def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
