from PyQt4 import QtGui, QtCore
import pymysql
import sys
import time
import numpy as np
import os
import pandas as pd

class Main(QtGui.QMainWindow):
   
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Student Registration")
        
       
        
        centralwidget = QtGui.QWidget(self)
        self.setGeometry(100,100,800,600)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()

        self.q1=QtGui.QLabel("Username:",self)
        self.q1.move(100,50)
        self.q1.resize(200,40)
        self.q2=QtGui.QLineEdit(self)
        self.q2.move(250,50)
        self.q2.resize(400,40)

        self.q3=QtGui.QLabel("Password:",self)
        self.q3.move(100,120)
        self.q3.resize(200,40)
        self.q4=QtGui.QLineEdit(self)
        self.q4.move(250,120)
        self.q4.resize(400,40)

        self.q5=QtGui.QLabel("Device ID:",self)
        self.q5.move(100,190)
        self.q5.resize(200,40)
        self.q6=QtGui.QLineEdit(self)
        self.q6.move(250,190)
        self.q6.resize(400,40)

        
        #self.q7=QtGui.QLabel("MAC Address:",self)
        #self.q7.move(100,260)
        #self.q7.resize(200,40)
        #self.q8=QtGui.QLineEdit(self)
        #self.q8.move(250,260)
        #self.q8.resize(50,40)

        #self.q9=QtGui.QLineEdit(self)
        #self.q9.move(310,260)
        #self.q9.resize(50,40)

        #self.q10=QtGui.QLineEdit(self)
        #self.q10.move(370,260)
        #self.q10.resize(50,40)

        #self.q11=QtGui.QLineEdit(self)
        #self.q11.move(430,260)
        #self.q11.resize(50,40)

        #self.q12=QtGui.QLineEdit(self)
        #self.q12.move(490,260)
        #self.q12.resize(50,40)

        #self.q13=QtGui.QLineEdit(self)
        #self.q13.move(550,260)
        #self.q13.resize(50,40)

        self.q14=QtGui.QLabel("Student Name:",self)
        self.q14.move(100,260)
        self.q14.resize(200,40)
        self.q15=QtGui.QLineEdit(self)
        self.q15.move(250,260)
        self.q15.resize(400,40)

  
        
        #Buttons
        
        
        self.registerbutton = QtGui.QPushButton("Register",self)
        self.registerbutton.clicked.connect(self.registerfunc)
        self.registerbutton.move(300,330)
        self.registerbutton.resize(150,50)

        self.systemlist = QtGui.QComboBox(self)
        self.systemlist.currentIndexChanged.connect(self.systemselect)
        self.systemlist.move(220,450)
        self.systemlist.resize(200,48)

        
        
        self.deletebutton = QtGui.QPushButton("Delete",self)
        self.deletebutton.clicked.connect(self.deletefunc)
        self.deletebutton.move(450,450)
        self.deletebutton.resize(150,50)
        try:
                self.systemlist.clear()
                self.systemlist.addItems(["User Select"])
                examf="studentinfo"
                conn = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examf,
                                      )
                
                
                try:
                    with conn.cursor() as cursor:
                        
                        sql = "SELECT `username`,`password`,`deviceid`,`studentname` FROM `"+"credentials"+"`"
                        
                        curs = conn.cursor()
                        #try:
                        if True:
                            curs.execute(sql)
                            result = curs.fetchall()
                            
                            cnt=0
                            
                            for row in result:
                                 self.systemlist.addItems([row[0]])
                                 
                                 cnt=cnt+1
                            
                
                except:
                    print("Error")
                    
                    
        except:
                x=0
               
    def deletefunc(self):
        global userselect
        print(userselect)
        try:
               examf="studentinfo"
               conn = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examf,
                                      ) 
               with conn.cursor() as cursor:
                   cur=conn.cursor()
                   curtext = "DELETE FROM `"+"credentials"+"` where username='"+str(userselect)+"'"
                   print(curtext)
                   cur.execute(curtext)
                   conn.commit()
        except:
           x=0
        try:
                self.systemlist.clear()
                self.systemlist.addItems(["User Select"])
                examf="studentinfo"
                conn = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examf,
                                      )
                
                
                try:
                    with conn.cursor() as cursor:
                        
                        sql = "SELECT `username`,`password`,`deviceid`,`studentname` FROM `"+"credentials"+"`"
                        
                        curs = conn.cursor()
                        #try:
                        if True:
                            curs.execute(sql)
                            result = curs.fetchall()
                            
                            cnt=0
                            
                            for row in result:
                                 self.systemlist.addItems([row[0]])
                                 
                                 cnt=cnt+1
                            
                
                except:
                    print("Error")
                    
                    
        except:
                x=0
    def registerfunc(self):
        iusername=str(self.q2.text())
        ipassword = str(self.q4.text())
        ideviceid = str(self.q6.text())
        #m1 = str(self.q8.text())
        #m2 = str(self.q9.text())
        #m3 = str(self.q10.text())
        #m4 = str(self.q11.text())
        #m5 = str(self.q12.text())
        #m6 = str(self.q13.text())
        #imacaddress=m1+":"+m2+":"+m3+":"+m4+":"+m5+":"+m6
        istudentname=str(self.q15.text())
        exam="studentinfo"
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=exam,
                                  )
        #Check Table
        flagreg=-1
        if flagreg==-1:
            try:
                with conn.cursor() as cursor:
                   
                    try:
                      
                        cursor.execute("SELECT * FROM credentials WHERE username=%s",(iusername,))
                        data="True"
                        
                        for i in cursor:
                            data=i
                        if data=="True":
                            
                            flagreg=0
                        else:
                            print("Username already exist!")
                            
                    except:
                        print("Oops! Something wrong")
             
                conn.commit()
            finally:
                print("")
        if flagreg==0:
            try:
                with conn.cursor() as cursor:
                   
                    try:
                        
                        cursor.execute("SELECT * FROM credentials WHERE deviceid=%s",(ideviceid,))
                        data="True"
                        
                        for i in cursor:
                            data=i
                        if data=="True":
                            
                            flagreg=1
                        else:
                            print("Device ID already exist!")
                            
                    except:
                        print("Oops! Something wrong")
             
                conn.commit()
            finally:
                print("")
            
       

        if flagreg==1:
            try:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO `"+"credentials"+"`(`username`,`password`, `deviceid`,  `studentname`) VALUES (%s, %s,  %s, %s)"
                    try:
                        cursor.execute(sql, (iusername,ipassword,ideviceid,istudentname))
                        print("Task added successfully")
                    except:
                        print("Oops! Something wrong")
            
                conn.commit()
            finally:
                print("")
            flagreg=-1
        try:
                self.systemlist.clear()
                self.systemlist.addItems(["User Select"])
                examf="studentinfo"
                conn = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examf,
                                      )
                
                
                try:
                    with conn.cursor() as cursor:
                        
                        sql = "SELECT `username`,`password`,`deviceid`,`studentname` FROM `"+"credentials"+"`"
                        
                        curs = conn.cursor()
                        #try:
                        if True:
                            curs.execute(sql)
                            result = curs.fetchall()
                            
                            cnt=0
                            
                            for row in result:
                                 self.systemlist.addItems([row[0]])
                                 
                                 cnt=cnt+1
                            
                
                except:
                    print("Error")
                    
                    
        except:
                x=0
    def systemselect(self,systemflag):
        global userselect
        self.systemlist.setCurrentIndex(systemflag)
        userselect=self.systemlist.itemText(systemflag)
        
    def Loop(self):
        x=0
            
                    
                
           
  
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
