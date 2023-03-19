import time
import sys, os
from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np
import sys
import RPi.GPIO as GPIO
from time import sleep
import serial
import math
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
class Main(QtGui.QMainWindow): 
    def __init__(self): 
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,start_time
        start_time = time.time()
        flag=1
        centralwidget = QtGui.QWidget(self) 

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        #Initial Page
        self.databutton = QtGui.QPushButton("Database Management",self)
        self.databutton.clicked.connect(self.databasepage)
        self.databutton.move(80,50)
        self.databutton.resize(150,25)
        self.reportbutton = QtGui.QPushButton("Report Generation",self)
        self.reportbutton.clicked.connect(self.reportpage)
        self.reportbutton.move(80,100)
        self.reportbutton.resize(150,25)
        #
        #Database Page
        self.addrecordbutton = QtGui.QPushButton("Add Record",self)
        self.addrecordbutton.clicked.connect(self.addpage)
        self.addrecordbutton.move(80,50)
        self.addrecordbutton.resize(150,25)
        self.deleterecordbutton = QtGui.QPushButton("Delete Record",self)
        self.deleterecordbutton.clicked.connect(self.deletepage)
        self.deleterecordbutton.move(80,100)
        self.deleterecordbutton.resize(150,25)
        #
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(150,225)

        self.deletebutton = QtGui.QPushButton("Delete",self)
        self.deletebutton.clicked.connect(self.delete)
        self.deletebutton.move(150,175)

        self.readbutton = QtGui.QPushButton("Read",self)
        self.readbutton.clicked.connect(self.read)
        self.readbutton.move(40,150)

        self.enrollbutton = QtGui.QPushButton("Register",self)
        self.enrollbutton.clicked.connect(self.enroll)
        self.enrollbutton.move(260,350)
        
        font10 = QtGui.QFont("Helvetica", 10)
        self.l1=QtGui.QLabel("ID",self)
        self.l1.move(40,30)
        self.l1.setFont(font10)
        self.l2=QtGui.QLineEdit(self)
        self.l2.move(120,35)
        self.l2.resize(40,20)
        #Information
        self.r1=QtGui.QLabel("First Name",self)
        self.r1.move(40,60)
        self.r1.resize(100,20)
        self.r1.setFont(font10)
        self.r2=QtGui.QLineEdit(self)
        self.r2.move(120,65)
        self.r2.resize(200,20)
        self.r3=QtGui.QLabel("Last Name",self)
        self.r3.move(40,90)
        self.r3.resize(100,20)
        self.r3.setFont(font10)
        self.r4=QtGui.QLineEdit(self)
        self.r4.move(120,95)
        self.r4.resize(200,20)
        self.r5=QtGui.QLabel("Cell No.",self)
        self.r5.move(40,120)
        self.r5.resize(100,20)
        self.r5.setFont(font10)
        self.r6=QtGui.QLineEdit(self)
        self.r6.move(120,125)
        self.r6.resize(200,20)
        self.r7=QtGui.QLabel("Address",self)
        self.r7.move(40,150)
        self.r7.resize(100,20)
        self.r7.setFont(font10)
        self.r8=QtGui.QLineEdit(self)
        self.r8.move(120,155)
        self.r8.resize(200,20)
        self.r9=QtGui.QLabel("Email Add",self)
        self.r9.move(40,180)
        self.r9.resize(100,20)
        self.r9.setFont(font10)
        self.r10=QtGui.QLineEdit(self)
        self.r10.move(120,185)
        self.r10.resize(200,20)
        self.r11=QtGui.QLabel("Age",self)
        self.r11.move(40,210)
        self.r11.resize(40,20)
        self.r11.setFont(font10)
        self.r12=QtGui.QLineEdit(self)
        self.r12.move(120,215)
        self.r12.resize(40,20)
        self.r13=QtGui.QLabel("Full Name",self)
        self.r13.move(370,60)
        self.r13.resize(100,20)
        self.r13.setFont(font10)
        self.r14=QtGui.QLineEdit(self)
        self.r14.move(450,65)
        self.r14.resize(200,20)
        self.r15=QtGui.QLabel("Relationship",self)
        self.r15.move(370,90)
        self.r15.resize(100,20)
        self.r15.setFont(font10)
        self.r16=QtGui.QLineEdit(self)
        self.r16.move(450,95)
        self.r16.resize(200,20)
        self.r17=QtGui.QLabel("Cell No.",self)
        self.r17.move(370,120)
        self.r17.resize(100,20)
        self.r17.setFont(font10)
        self.r18=QtGui.QLineEdit(self)
        self.r18.move(450,125)
        self.r18.resize(200,20)
        self.r19=QtGui.QLabel("Address",self)
        self.r19.move(370,150)
        self.r19.resize(100,20)
        self.r19.setFont(font10)
        self.r20=QtGui.QLineEdit(self)
        self.r20.move(450,155)
        self.r20.resize(200,20)


        
        self.addrecordbutton.setVisible(0)
        self.deleterecordbutton.setVisible(0)
        self.stopbutton.setVisible(1)
        self.deletebutton.setVisible(1)
        self.readbutton.setVisible(0)
        self.enrollbutton.setVisible(0)
        self.l1.setVisible(0)
        self.l2.setVisible(0)
        
        self.r1.setVisible(0)
        self.r2.setVisible(0)
        self.r3.setVisible(0)
        self.r4.setVisible(0)
        self.r5.setVisible(0)
        self.r6.setVisible(0)
        self.r7.setVisible(0)
        self.r8.setVisible(0)
        self.r9.setVisible(0)
        self.r10.setVisible(0)
        self.r11.setVisible(0)
        self.r12.setVisible(0)
        self.r13.setVisible(0)
        self.r14.setVisible(0)
        self.r15.setVisible(0)
        self.r16.setVisible(0)
        self.r17.setVisible(0)
        self.r18.setVisible(0)
        self.r19.setVisible(0)
        self.r20.setVisible(0)
        
        #self.setGeometry(0,15,660,480)
        self.setGeometry(150,150,300,150)
    def addpage(self):
        self.addrecordbutton.setVisible(0)
        self.deleterecordbutton.setVisible(0)
        self.enrollbutton.setVisible(1)
        self.l1.setVisible(1)
        self.l2.setVisible(1)
        self.r1.setVisible(1)
        self.r2.setVisible(1)
        self.r3.setVisible(1)
        self.r4.setVisible(1)
        self.r5.setVisible(1)
        self.r6.setVisible(1)
        self.r7.setVisible(1)
        self.r8.setVisible(1)
        self.r9.setVisible(1)
        self.r10.setVisible(1)
        self.r11.setVisible(1)
        self.r12.setVisible(1)
        self.r13.setVisible(1)
        self.r14.setVisible(1)
        self.r15.setVisible(1)
        self.r16.setVisible(1)
        self.r17.setVisible(1)
        self.r18.setVisible(1)
        self.r19.setVisible(1)
        self.r20.setVisible(1)
        
        self.setGeometry(0,15,660,480)
    def databasepage(self):
        self.addrecordbutton.setVisible(1)
        self.deleterecordbutton.setVisible(1)
        
        self.databutton.setVisible(0)
        self.reportbutton.setVisible(0)
    def deletepage(self):
        x=0
        
    def reportpage(self):
        x=0
    def read(self):
        global flag
        flag=1
        
    def enroll(self):
        global flag
        self.databutton.setVisible(1)
        self.reportbutton.setVisible(1)
        self.l1.setVisible(0)
        self.l2.setVisible(0)
        
        self.r1.setVisible(0)
        self.r2.setVisible(0)
        self.r3.setVisible(0)
        self.r4.setVisible(0)
        self.r5.setVisible(0)
        self.r6.setVisible(0)
        self.r7.setVisible(0)
        self.r8.setVisible(0)
        self.r9.setVisible(0)
        self.r10.setVisible(0)
        self.r11.setVisible(0)
        self.r12.setVisible(0)
        self.r13.setVisible(0)
        self.r14.setVisible(0)
        self.r15.setVisible(0)
        self.r16.setVisible(0)
        self.r17.setVisible(0)
        self.r18.setVisible(0)
        self.r19.setVisible(0)
        self.r20.setVisible(0)
        idvar=str(self.l2.text())
        firstname=str(self.r2.text())
        lastname=str(self.r4.text())
        dcell=str(self.r6.text())
        daddress=str(self.r8.text())
        email=str(self.r10.text())
        age=str(self.r12.text())
        fullname=str(self.r14.text())
        relationship=str(self.r16.text())
        gcell=str(self.r18.text())
        gaddress=str(self.r20.text())
        pathmain="/home/pi/Desktop/studentdatabase.csv"
        if os.path.exists(pathmain):
                 
                 df=pd.read_csv(pathmain,names=['ID','First Name','Last Name','Cell No.','Address','Email Address','Age','Guardian Name','Relationship','Guardian Cell No.','Guardian Address'],skiprows=1)
                 np_df = df.as_matrix()
                 df = df.append({'ID':idvar,'First Name':firstname,'Last Name':lastname,'Cell No.':dcell,'Address':daddress,'Email Address':email,
                             'Age':age,'Guardian Name':fullname,'Relationship':relationship,'Guardian Cell No.':gcell,'Guardian Address':gaddress}, ignore_index=True)   
                 df.to_csv(pathmain,  index = False)
                 print df
        else:
             columns = ['ID','First Name','Last Name','Cell No.','Address','Email Address','Age','Guardian Name','Relationship','Guardian Cell No.','Guardian Address']
             df = pd.DataFrame(columns=columns)
             np_df = df.as_matrix()
             df = df.append({'ID':idvar,'First Name':firstname,'Last Name':lastname,'Cell No.':dcell,'Address':daddress,'Email Address':email,
                             'Age':age,'Guardian Name':fullname,'Relationship':relationship,'Guardian Cell No.':gcell,'Guardian Address':gaddress}, ignore_index=True)
             df.to_csv(pathmain,  index = False)
             print df

        flag=2
        idvar="A,"+idvar+","
        print idvar
        ser.write(idvar)
        self.setGeometry(150,150,300,150)
    def delete(self):
        #idvar=str(self.l2.text())
        idvar=str(5)    
        idvar="C,"+idvar+","
        print idvar
        ser.write(idvar)
        
    def stop(self):
        global flag
        flag=0
        ser.write("D,")
        print "Terminated."
    def Loop(self):
        global flag,start_time,j
        elapsed_time = time.time() - start_time
        #print "flag="+str(flag)
        if flag==2:
            try:
                data= ser.readline()
                print data
                reference=data.split(",")[1]
                if reference=="Done":
                    flag=1
                    
                
            except:
                print
        elif flag==1:
            
            ser.write("B,")
            
            try:
                
                data = ser.readline()
                #print data
                if data.find("Found ID #")==0:
                    studentid = data.split("#")[1]
                    studentid = studentid.split(" ")[0]
                    
                    #print "ID: "+str(studentid)
                    pathmain="/home/pi/Desktop/studentdatabase.csv"
                    if os.path.exists(pathmain):
                             
                             df=pd.read_csv(pathmain,names=['ID','First Name','Last Name','Cell No.','Address','Email Address','Age','Guardian Name','Relationship','Guardian Cell No.','Guardian Address'],skiprows=1)
                             np_df = df.as_matrix()
                             
                             targetdata=np.where(df["ID"] == int(studentid))
                             targetdata=targetdata[0][0]
                             print np_df[targetdata][1].split(" ")[0]
                             idvar=""
                             idvar=np_df[targetdata][1].split(" ")[0]
                             idvar="E,"+idvar+","
                             print idvar
                             ser.write(idvar)
        
                
                      
            except:
                print "No Data"
            
            
            
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
