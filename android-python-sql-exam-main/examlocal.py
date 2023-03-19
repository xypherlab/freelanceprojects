from PyQt4 import QtGui, QtCore #GUI Library
import pymysql #Library for Database (MySQL)
import sys #Watchdog
import time #Delay or Timing
import numpy as np #Equivalent sa Matrix ng MATLAB
import os #Directory of Folders
import pandas as pd #CSV management or excel
import pyqtgraph as pg #Bar Graph
import socket #IP Address 
class Main(QtGui.QMainWindow):
   
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.initUI()
    
    def initUI(self):
        global conn,cur,examtable
        global subjecttable,safeflag,ipaddress
        safeflag=0
        subjecttable="Course"
        ipaddress=socket.gethostbyname(socket.gethostname())
        self.setWindowTitle("Exam Database - "+ipaddress)
        
       
        
        centralwidget = QtGui.QWidget(self)
        self.setGeometry(100,100,1580,780) #Properties of GUI Window (X Location,Y Location, Size Horizontal, Size Vertical)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()

        
        self.examlist = QtGui.QComboBox(self)
        self.examlist.currentIndexChanged.connect(self.examselect) #Function
        self.examlist.move(800,700) #Location
        self.examlist.resize(200,50) #Size

        #Objects
        #Pushbutton
        #Table
        #Frame
        #Bargraph
        #Dropdown Box
        #Label 
        #Edit/Fill Up Box


        #
        #1. SQL Commands
        #2. pyqt4 Objects





        #
        self.frame1 = QtGui.QFrame(self)
        self.frame1.resize(350,780)
        self.frame1.setStyleSheet("background-color: rgb(0,0,0)")
        self.frame1.move(0,0)

        self.frame2 = QtGui.QFrame(self)
        self.frame2.resize(600,700)
        
        self.frame2.move(550,50)
        #Plot
        self.plotbar = pg.PlotWidget(self)
        self.plotbar.resize(1000,550)
        self.plotbar.move(450,50)
        
      

        #Select Attendance Combobox
        
        self.attendancebutton = QtGui.QComboBox(self)
        self.attendancebutton.currentIndexChanged.connect(self.attendanceselect)
        self.attendancebutton.move(100,150)
        self.attendancebutton.resize(150,50)
        self.attendancebutton.clear()
        self.attendancebutton.addItems(["Attendance"])
        

        
        
        self.createbutton = QtGui.QPushButton("Create Quiz",self)
        self.createbutton.clicked.connect(self.createfunc)
        self.createbutton.move(100,250)
        self.createbutton.resize(150,50)


     
        #System Combobox
        
        self.systemlist = QtGui.QComboBox(self)
        self.systemlist.currentIndexChanged.connect(self.systemselect)
        self.systemlist.move(100,650)
        self.systemlist.resize(200,70)

        #System Table
        self.systemtable = QtGui.QTableWidget(self)
        self.systemtable.setColumnCount(3)
        self.systemtable.move(600,50)
        self.systemtable.setHorizontalHeaderLabels(['         Topic        ','    Current Time (Hours)    ','   Recommended Time (Hours)   '])
        self.systemtable.resize(700,400)
        self.systemtable.resizeColumnsToContents()

        self.systembutton = QtGui.QPushButton("Update",self)
        self.systembutton.clicked.connect(self.systemfunc)
        self.systembutton.move(850,550)
        self.systembutton.resize(150,50)
        #Subject Combobox
        
        
        self.subjectlist = QtGui.QComboBox(self)
        self.subjectlist.addItems(["Course"])
        df=pd.read_csv("Subject.csv",names=["Subject"],skiprows=1)
        np_df = df.values
        initflag=0
        for table in [tables[0] for tables in np_df]:
            
            self.subjectlist.addItems([str(table)])
            if initflag==0:
                subjecttable=str(table)
                initflag=1
        self.subjectlist.currentIndexChanged.connect(self.subjectselect)
        self.subjectlist.move(100,50)
        self.subjectlist.resize(150,50)
        self.subjectlist.setCurrentIndex(0)
        #Comparison Combobox
        
        self.comparisonlist = QtGui.QComboBox(self)
        self.comparisonlist.currentIndexChanged.connect(self.comparisonselect)
        self.comparisonlist.move(750,700)
        self.comparisonlist.resize(150,50)

        self.compareadd = QtGui.QPushButton("Add",self)
        self.compareadd.clicked.connect(self.compareaddfunc)
        self.compareadd.move(920,700)
        self.compareadd.resize(100,50)
        fontscore = QtGui.QFont("Times", 18)
        
        self.scoredisp=QtGui.QLabel("",self)
        self.scoredisp.setFont(fontscore)
        self.scoredisp.move(550,620)
        self.scoredisp.resize(1000,80)
        
        #Topic Combobox
        
        self.topiclist = QtGui.QComboBox(self)
        self.topiclist.currentIndexChanged.connect(self.topicselect)
        self.topiclist.move(1150,650)
        self.topiclist.resize(150,50)
        
     
        #Select Quiz Combobox
        
        self.selectlist = QtGui.QComboBox(self)
        self.selectlist.currentIndexChanged.connect(self.slistselect)
        self.selectlist.move(100,350)
        self.selectlist.resize(150,50)

        #Exam Analysis Combobox
        
        self.analysislist = QtGui.QComboBox(self)
        self.analysislist.currentIndexChanged.connect(self.analysisselect)
        self.analysislist.move(100,450)
        self.analysislist.resize(150,50)
       
        #Student Understanding Combobox
        
        self.itemlist = QtGui.QComboBox(self)
        self.itemlist.currentIndexChanged.connect(self.itemselect)
        self.itemlist.move(100,550)
        self.itemlist.resize(150,50)
        #Threshold
        self.a1=QtGui.QLabel("Lower - Upper",self)
        self.a1.move(850,450)
        self.a1.resize(200,40)

        self.a2=QtGui.QLabel("Filter",self)
        self.a2.move(1100,450)
        self.a2.resize(200,40)

        #Topic Filter Combobox
        
        self.filterlist = QtGui.QComboBox(self)
        self.filterlist.currentIndexChanged.connect(self.filterselect)
        self.filterlist.move(1050,500)
        self.filterlist.resize(150,50)

        
        
        self.i1=QtGui.QLabel("Poor:",self)
        self.i1.move(780,500)
        self.i1.resize(100,40)
        self.i2l=QtGui.QLineEdit(self)
        self.i2l.move(850,500)
        self.i2l.resize(60,40)
        self.i2u=QtGui.QLineEdit(self)
        self.i2u.move(920,500)
        self.i2u.resize(60,40)
        
        self.i3=QtGui.QLabel("Average:",self)
        self.i3.move(700,550)
        self.i3.resize(200,40)
        self.i4l=QtGui.QLineEdit(self)
        self.i4l.move(850,550)
        self.i4l.resize(60,40)
        self.i4u=QtGui.QLineEdit(self)
        self.i4u.move(920,550)
        self.i4u.resize(60,40)
        
        self.i5=QtGui.QLabel("Above Average:",self)
        self.i5.move(780,600)
        self.i5.resize(100,40)
        self.i6l=QtGui.QLineEdit(self)
        self.i6l.move(850,600)
        self.i6l.resize(60,40)
        self.i6u=QtGui.QLineEdit(self)
        self.i6u.move(920,600)
        self.i6u.resize(60,40)

        
        self.difficultyanalysis = QtGui.QPushButton("Analyze",self)
        self.difficultyanalysis.clicked.connect(self.analysisfunc)
        self.difficultyanalysis.move(920,670)
        self.difficultyanalysis.resize(150,50)
        #
        self.comparisonlist.clear()
        self.comparisonlist.addItems(["Select Quiz"])
        self.systemlist.clear()
        self.systemlist.addItems(["System Recommendation"])

        self.filterlist.clear()
        self.filterlist.addItems(["All"])
        
        
        self.selectlist.clear()
        self.selectlist.addItems(["Select Quiz"])

        self.analysislist.clear()
        self.analysislist.addItems(["Exam Analysis"])

        self.itemlist.clear()
        self.itemlist.addItems(["Student Understanding"])
        
        #Question Bank
        self.questionlist = QtGui.QTableWidget(self)
        self.questionlist.setColumnCount(9)
        self.questionlist.move(450,50)
        self.questionlist.setHorizontalHeaderLabels(['                Item              ','                Question              ','        Choice 1        ','        Choice 2        ','        Choice 3        ','        Choice 4        ','        Answer        ','        Topic        ','        Difficulty        '])
        self.questionlist.resize(1000,400)
        self.questionlist.resizeColumnsToContents()
        
        #Attendance List
        self.attendancelist = QtGui.QTableWidget(self)
        self.attendancelist.setColumnCount(2)
        self.attendancelist.move(450,50)
        self.attendancelist.setHorizontalHeaderLabels(['                     Name                          ','      Device    ID      '])
        self.attendancelist.resize(1000,600)
        self.attendancelist.resizeColumnsToContents()
        
        
        
        #Select Table -- Subject for Deletion
        self.selecttable = QtGui.QTableWidget(self)
        self.selecttable.setColumnCount(4)
        self.selecttable.move(450,50)
        self.selecttable.setHorizontalHeaderLabels(['                    Item                          ','           Question           ','           Choices          ','           Difficulty          '])
        self.selecttable.resize(1000,600)
        self.selecttable.resizeColumnsToContents()

        #Item Table
        self.itemtable = QtGui.QTableWidget(self)
        self.itemtable.setColumnCount(5)
        self.itemtable.move(450,50)
        self.itemtable.setHorizontalHeaderLabels(['        Item       ','        Question       ','        Topic       ','      Average      ','        Difficulty         '])
        self.itemtable.resize(1000,400)
        self.itemtable.resizeColumnsToContents()

        
        
        #Overview Table
        self.viewlist = QtGui.QTableWidget(self)
        self.viewlist.setColumnCount(9)
        self.viewlist.move(450,50)
        self.viewlist.setHorizontalHeaderLabels(['                Item              ','                Question              ','        Choice 1        ','        Choice 2        ','        Choice 3        ','        Choice 4        ','        Answer        ','        Topic        ','        Difficulty        '])
        self.viewlist.resize(1000,400)
        self.viewlist.resizeColumnsToContents()
        self.viewlist.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.viewlist.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #Topic Table
        self.tabletopic = QtGui.QTableWidget(self)
        self.tabletopic.setColumnCount(2)
        self.tabletopic.move(700,50)
        self.tabletopic.setHorizontalHeaderLabels(['              Topic             ','       Time (Hours) 		'])
        self.tabletopic.resize(450,400)
        self.tabletopic.resizeColumnsToContents()
        self.tabletopic.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tabletopic.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        font = QtGui.QFont("Times", 16)
        ###Insert Data###
        self.q1=QtGui.QLabel("Quiz Name:",self)
        self.q1.move(600,250)
        self.q1.resize(200,40)
        self.q2=QtGui.QLineEdit(self)
        self.q2.move(750,250)
        self.q2.resize(400,40)
        self.createquiz = QtGui.QPushButton("Next",self)
        self.createquiz.clicked.connect(self.quizfunc)
        self.createquiz.move(850,320)
        self.createquiz.resize(150,50)

        self.tablequiz = QtGui.QPushButton("Next",self)
        self.tablequiz.clicked.connect(self.tablequizfunc)
        self.tablequiz.move(850,550)
        self.tablequiz.resize(150,50)
        
        self.createtopic = QtGui.QPushButton("Add",self)
        self.createtopic.clicked.connect(self.topicfunc)
        self.createtopic.move(850,470)
        self.createtopic.resize(150,50)
        
        self.l1=QtGui.QLabel("Question:",self)
        self.l1.move(500,500)
        self.l2=QtGui.QLineEdit(self)
        self.l2.move(600,500)
        self.l2.resize(400,40)

        self.l3=QtGui.QLabel("Choice 1:",self)
        self.l3.move(500,550)
        self.l4=QtGui.QLineEdit(self)
        self.l4.move(600,550)
        self.l4.resize(300,40)

        self.l5=QtGui.QLabel("Choice 2:",self)
        self.l5.move(500,600)
        self.l6=QtGui.QLineEdit(self)
        self.l6.move(600,600)
        self.l6.resize(300,40)

        self.l7=QtGui.QLabel("Choice 3:",self)
        self.l7.move(1050,500)
        self.l8=QtGui.QLineEdit(self)
        self.l8.move(1150,500)
        self.l8.resize(300,40)

        self.l9=QtGui.QLabel("Choice 4:",self)
        self.l9.move(1050,550)
        self.l10=QtGui.QLineEdit(self)
        self.l10.move(1150,550)
        self.l10.resize(300,40)

        self.l11=QtGui.QLabel("Answer:",self)
        self.l11.move(1050,600)
        self.l12=QtGui.QLineEdit(self)
        self.l12.move(1150,600)
        self.l12.resize(300,40)
        
        self.l13=QtGui.QLabel("Total Time: -----",self)
        self.l13.move(780,480)
        self.l13.resize(300,30)
        self.l13.setFont(font)
        self.l13.setStyleSheet('color: red')
        #Add
        self.insertbutton = QtGui.QPushButton("Add",self)
        self.insertbutton.clicked.connect(self.insertfunc)
        self.insertbutton.move(800,650)
        self.insertbutton.resize(200,50)
        
        self.deletebutton = QtGui.QPushButton("Delete",self)
        self.deletebutton.clicked.connect(self.deletefunc)
        self.deletebutton.move(650,650)
        self.deletebutton.resize(200,50)
        
        self.editbutton = QtGui.QPushButton("Update",self)
        self.editbutton.clicked.connect(self.editfunc)
        self.editbutton.move(850,650)
        self.editbutton.resize(200,50)

        self.savebutton = QtGui.QPushButton("Save",self)
        self.savebutton.clicked.connect(self.savefunc)
        self.savebutton.move(800,550)
        self.savebutton.resize(200,50)
        
        self.activatebutton = QtGui.QPushButton("Activate Quiz",self)
        self.activatebutton.clicked.connect(self.activatefunc)
        self.activatebutton.move(1050,650)
        self.activatebutton.resize(200,50)
        #Visibility
        
        
        
        self.attendancelist.setVisible(0)
        self.itemtable.setVisible(0)
        self.selecttable.setVisible(0)
        self.questionlist.setVisible(0)
        self.viewlist.setVisible(0)
        self.insertbutton.setVisible(0)
        self.l1.setVisible(0)
        self.l2.setVisible(0)
        self.l3.setVisible(0)
        self.l4.setVisible(0)
        self.l5.setVisible(0)
        self.l6.setVisible(0)
        self.l7.setVisible(0)
        self.l8.setVisible(0)
        self.l9.setVisible(0)
        self.l10.setVisible(0)
        self.l11.setVisible(0)
        self.l12.setVisible(0)
        self.l13.setVisible(0)
        self.comparisonlist.setVisible(0)
        self.compareadd.setVisible(0)
        
        self.topiclist.setVisible(0)
        
        self.examlist.setVisible(0)
        self.createquiz.setVisible(0)
        self.plotbar.setVisible(0)
        self.q1.setVisible(0)
        self.q2.setVisible(0)
        self.tabletopic.setVisible(0)
        self.tablequiz.setVisible(0)
        self.createtopic.setVisible(0)
        self.frame2.setVisible(0)
        
        self.savebutton.setVisible(0)
        self.deletebutton.setVisible(0)
        self.editbutton.setVisible(0)
        self.activatebutton.setVisible(0)
        self.scoredisp.setVisible(0)
        
        self.a1.setVisible(0)
        self.i1.setVisible(0)
        self.i2l.setVisible(0)
        self.i2u.setVisible(0)
        self.i3.setVisible(0)
        self.i4l.setVisible(0)
        self.i4u.setVisible(0)
        self.i5.setVisible(0)
        self.i6l.setVisible(0)
        self.i6u.setVisible(0)
        self.systembutton.setVisible(0)
        self.difficultyanalysis.setVisible(0)
        self.systemtable.setVisible(0)

        self.filterlist.setVisible(0)
        self.a2.setVisible(0)
        
        self.frame = QtGui.QFrame(self)
        self.frame.resize(512,512)
        self.frame.setStyleSheet("background-image: url(logo.png);");
        self.frame.move(700,100)


        
    def filterselect(self,filterflag):
        filtertable=self.filterlist.itemText(filterflag)
        totalstudent=0
        examr=subjecttable+"attendance"
        connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        try:
            with connr.cursor() as cursor:
                sql = "SELECT `studentname`,`deviceid` FROM `"+examtable+"`"
                
                
                curs = connr.cursor()
                curs.execute(sql)
                result = curs.fetchall()
                totalstudent=len(result)
        except:
            print("Something Wrong!")
            
        examr=subjecttable+"results"
        connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        
        try:
            self.itemtable.setRowCount(0)
            with connr.cursor() as cursor:
                
                sql = "SELECT `item`,`question`,`topic`,`average`, `difficulty` FROM `"+examtable+"`"
                
                curs = connr.cursor()
                #try:
                if True:
                    curs.execute(sql)
                    result = curs.fetchall()
                    
                    cnt=0
                    
                    self.itemtable.setRowCount(len(result))
                    
                    for row in result:
                          if filtertable==row[2]:   
                             self.itemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                             self.itemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                             self.itemtable.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(row[2])+""))
                             self.itemtable.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str((float(row[3])/totalstudent)*100)+"%"))
                             self.itemtable.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(row[4])+""))
                             cnt=cnt+1
                          elif filtertable=="All":
                             self.itemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                             self.itemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                             self.itemtable.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(row[2])+""))
                             self.itemtable.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str((float(row[3])/totalstudent)*100)+"%"))
                             self.itemtable.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(row[4])+""))
                             cnt=cnt+1 
            connr.commit()
        finally:
            
            print("")
    def analysisfunc(self):
         totalstudent=0
         examr=subjecttable+"attendance"
         connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
         try:
            with connr.cursor() as cursor:
                sql = "SELECT `studentname`,`deviceid` FROM `"+examtable+"`"
                
                
                curs = connr.cursor()
                curs.execute(sql)
                result = curs.fetchall()
                totalstudent=len(result)
         except:
            print("Something Wrong!")
         examr=subjecttable+"results"
         connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
         try:
            with connr.cursor() as cursor:
                
                sql = "SELECT `item`,`question`,`topic`,`average`, `difficulty` FROM `"+examtable+"`"
                print(sql)
                curs = connr.cursor()
                #try:
                if True:
                    curs.execute(sql)
                    result = curs.fetchall()
                    print(str(result))
                    cnt=0
                    self.itemtable.setRowCount(len(result))
                    
                    for row in result:
                             
                             average=(float(row[3])/float(totalstudent))*100
                             print(average)
                             #Mark
                             PoorL = float(self.i2l.text())
                             PoorU = float(self.i2u.text())
                             AverageL = float(self.i4l.text())
                             AverageU = float(self.i4u.text())
                             AboveAverageL = float(self.i6l.text())
                             AboveAverageU = float(self.i6u.text())

                             print(PoorL)
                             print(PoorU)
                             print(AverageL)
                             print(AverageU)
                             print(AboveAverageL)
                             print(AboveAverageU)
                             
                             if average>PoorL and average<=PoorU:
                                 try:
                                    with connr.cursor() as cursor:
                                        cur=connr.cursor()
                                        modedif="Poor"
                                        itemcnt=cnt+1
                                        print(itemcnt)
                                        curtext = "UPDATE `"+examtable+"` SET difficulty='"+modedif+"' where item="+str(itemcnt)
                                        print(curtext)
                                        cur.execute(curtext)
                                        connr.commit()
                                 except:
                                     print("Error")
                             elif average>AverageL and average<=AverageU:
                                 try:
                                    with connr.cursor() as cursor:
                                        cur=connr.cursor()
                                        modedif="Average"
                                        itemcnt=cnt+1
                                        print(itemcnt)
                                        curtext = "UPDATE `"+examtable+"` SET difficulty='"+modedif+"' where item="+str(itemcnt)
                                        print(curtext)
                                        cur.execute(curtext)
                                        connr.commit()
                                 except:
                                     print("Error")
                             elif average>AboveAverageL and average<=AboveAverageU:
                                 try:
                                    with connr.cursor() as cursor:
                                        cur=connr.cursor()
                                        modedif="Above Average"
                                        itemcnt=cnt+1
                                        print(itemcnt)
                                        curtext = "UPDATE `"+examtable+"` SET difficulty='"+modedif+"' where item="+str(itemcnt)
                                        print(curtext)
                                        cur.execute(curtext)
                                        connr.commit()
                                 except:
                                     print("Error")
                             cnt=cnt+1
                        
         
                #except:
                    #print("Oops! Something wrong")
         
            connr.commit()
         finally:
            #conn.close()
            print("")
         
         
         try:
            with connr.cursor() as cursor:
                
                sql = "SELECT `item`,`question`,`topic`,`average`, `difficulty` FROM `"+examtable+"`"
                print(sql)
                curs = connr.cursor()
                #try:
                if True:
                    curs.execute(sql)
                    result = curs.fetchall()
                    print(str(result))
                    cnt=0
                    self.itemtable.setRowCount(len(result))
                    
                    for row in result:
                             
                             self.itemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                             self.itemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                             self.itemtable.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(row[2])+""))
                             self.itemtable.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str((float(row[3])/totalstudent)*100)+"%"))
                             self.itemtable.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(row[4])+""))
                             cnt=cnt+1
            connr.commit()
         finally:
            #conn.close()
            print("")
    def activatefunc(self):
        global examtable,subjecttable
        
        print(examtable)
        examdb=subjecttable+"attendance"
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examdb,
                                  )
        try:
            with conn.cursor() as cursor:
                
                sql = "TRUNCATE TABLE `"+examtable+"`"
                print(sql)
                if True:
                    cursor.execute(sql)
                    
         
            conn.commit()
        finally:
            print("")
            
        examdb=subjecttable+"results"
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examdb,
                                  )

        
                        
        try:
            with conn.cursor() as cursor:
                cur=conn.cursor()
                sql = "SELECT `id`,`item`, `question`, `topic`,`average`, `difficulty` FROM `"+examtable+"`"
                cur.execute(sql)
                result = cur.fetchall()
                
                cnt=0
                for i in range(len(result)):
                    curtext = "UPDATE `"+examtable+"` SET average = '0' where item="+str(i+1)
                    cur.execute(curtext)
                    conn.commit()
                
                
        except:
            x=0
    def savefunc(self):
        x=0
    def editfunc(self):
        global examtable,conn,cur
        indexes = self.viewlist.selectionModel().selectedRows()
        
        for index in sorted(indexes):
           print('Row %d is selected' % index.row())
           item=self.viewlist.item(index.row(),0).text()
           question=self.viewlist.item(index.row(),1).text()
           choice1=self.viewlist.item(index.row(),2).text()
           choice2=self.viewlist.item(index.row(),3).text()
           choice3=self.viewlist.item(index.row(),4).text()
           choice4=self.viewlist.item(index.row(),5).text()
           answer=self.viewlist.item(index.row(),6).text()
           topic=self.viewlist.item(index.row(),7).text()
           difficulty=self.viewlist.item(index.row(),8).text()
           
        print(item)    
        print(question)
        print(choice1)
        print(choice2)
        print(choice3)
        print(choice4)
        print(answer)
        print(topic)
        print(difficulty)
        examdb=subjecttable
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examdb,
                                  )
        try:
            with conn.cursor() as cursor:
                cur=conn.cursor()
                curtext = "UPDATE `"+examtable+"` SET question='"+question+"' where item="+item
                print(curtext)
                cur.execute(curtext)
                conn.commit()
                
                curtext = "UPDATE `"+examtable+"` SET choice1 ='"+choice1+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                curtext = "UPDATE `"+examtable+"` SET choice2 ='"+choice2+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                curtext = "UPDATE `"+examtable+"` SET choice3 ='"+choice3+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                curtext = "UPDATE `"+examtable+"` SET choice4 ='"+choice4+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                curtext = "UPDATE `"+examtable+"` SET answer ='"+answer+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                curtext = "UPDATE `"+examtable+"` SET topic ='"+topic+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                curtext = "UPDATE `"+examtable+"` SET difficulty ='"+difficulty+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                
        except:
            x=0
        examdb=subjecttable+"results"
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examdb,
                                  )
        try:
            with conn.cursor() as cursor:
                cur=conn.cursor()
                
                curtext = "UPDATE `"+examtable+"` SET topic ='"+topic+"' where item="+item
                cur.execute(curtext)
                conn.commit()
                
                
        except:
            x=0
    def deletefunc(self):
        global examtable,conn,cur,subjecttable,item
        indexes = self.viewlist.selectionModel().selectedRows()
        examr=subjecttable
        print(examr)
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        for index in sorted(indexes):
           print('Row %d is selected' % index.row())
           item=self.viewlist.item(index.row(),0).text()
           
           
           #Update Table
           try:
                with conn.cursor() as cursor:
                    cur=conn.cursor()
                    curtext = "DELETE FROM `"+examtable+"` where item="+str(item)
                    print(curtext)
                    cur.execute(curtext)
                    conn.commit()
                    sql = "SELECT `item`,`question`, `choice1`, `choice2`, `choice3`, `choice4`, `answer`, `topic`, `difficulty` FROM `"+examtable+"`"
                    print(sql)  
                    #try:
                    if True:
                        cur.execute(sql)
                        result = cur.fetchall()
                        print(str(result))
                        cnt=0
                        self.viewlist.setRowCount(len(result))
                        for row in result:
                                 
                                 self.viewlist.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                                 self.viewlist.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                                 self.viewlist.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(row[2])+""))
                                 self.viewlist.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(row[3])+""))
                                 self.viewlist.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(row[4])+""))
                                 self.viewlist.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(row[5])+""))
                                 self.viewlist.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(row[6])+""))
                                 self.viewlist.setItem(cnt, 7, QtGui.QTableWidgetItem(""+str(row[7])+""))
                                 self.viewlist.setItem(cnt, 8, QtGui.QTableWidgetItem(""+str(row[8])+""))
                                 cnt=cnt+1
                            
             
                    #except:
                        #print("Oops! Something wrong")
             
                conn.commit()
           finally:
                conn.close()
                print("")
           examr=subjecttable+"results"
           print(examr)
           conn = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examr,
                                      )
           try:
               with conn.cursor() as cursor:
                   cur=conn.cursor()
                   curtext = "DELETE FROM `"+examtable+"` where item="+str(item)
                   print(curtext)
                   cur.execute(curtext)
                   conn.commit()
           except:
               x=0
    def insertfunc(self):
        global examtable,newquiz,conn,topicsel
        difficultysel="----"
        newquiz=str(self.q2.text())
        question = str(self.l2.text())
        c1 = str(self.l4.text())
        c2 = str(self.l6.text())
        c3 = str(self.l8.text())
        c4 = str(self.l10.text())
        answer = str(self.l12.text())
        examr=subjecttable
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        try:    
            with conn.cursor() as cursor:
                
                sql = "SELECT `item`,`question`, `choice1`, `choice2`, `choice3`, `choice4`, `answer`, `topic`, `difficulty` FROM `"+newquiz+"`"
                print(sql)  
                
                if True:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    print(len(result))
                    itemnumber=str(len(result)+1)
        finally:
            print("")
        #Insert Table
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO `"+newquiz+"`(`item`,`question`, `choice1`, `choice2`, `choice3`, `choice4`, `answer`, `topic`, `difficulty`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (itemnumber,question, c1, c2,c3,c4,answer,topicsel,difficultysel))
                    print("Task added successfully")
                except:
                    print("Oops! Something wrong")
         
            conn.commit()
        finally:
            print("")
        #Update Table
        try:
            with conn.cursor() as cursor:
                
                sql = "SELECT `item`,`question`, `choice1`, `choice2`, `choice3`, `choice4`, `answer`, `topic`, `difficulty` FROM `"+newquiz+"`"
                print(sql)  
                #try:
                if True:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    print(str(result))
                    cnt=0
                    self.questionlist.setRowCount(len(result))
                    for row in result:
                             
                             self.questionlist.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                             self.questionlist.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                             self.questionlist.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(row[2])+""))
                             self.questionlist.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(row[3])+""))
                             self.questionlist.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(row[4])+""))
                             self.questionlist.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(row[5])+""))
                             self.questionlist.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(row[6])+""))
                             self.questionlist.setItem(cnt, 7, QtGui.QTableWidgetItem(""+str(row[7])+""))
                             self.questionlist.setItem(cnt, 8, QtGui.QTableWidgetItem(""+str(row[8])+""))
                             cnt=cnt+1
                        
         
                #except:
                    #print("Oops! Something wrong")
         
            conn.commit()
        finally:
            #conn.close()
            print("")
        examr=subjecttable+"results"
        conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO `"+newquiz+"`(`id`,`item`,`question`, `topic`, `average`, `difficulty`) VALUES (%s,%s, %s, %s,%s, %s)"
                try:
                    defaultval=str(0)
                    cursor.execute(sql, (itemnumber,itemnumber,question,topicsel,defaultval,difficultysel))
                    print("Task added successfully")
                except:
                    print("Oops! Something wrong")
         
            conn.commit()
        finally:
            print("")
    def examselect(self,examflag):
        global examtable
        examtable=self.examlist.itemText(examflag)
        print(examtable)
    def topicselect(self,topflag):
        global topicsel
        topicsel=self.topiclist.itemText(topflag)
        print(topicsel)
    
    def attendanceselect(self,alistflag):
        global examtable,subjecttable,safeflag,ipaddress
        
        try:
         if safeflag==1:
            self.setWindowTitle("Exam Database - "+ipaddress+" - Attendance")
            examtable=self.attendancebutton.itemText(alistflag)
            print(examtable)
            self.itemlist.setCurrentIndex(0)
            self.analysislist.setCurrentIndex(0)
            self.selectlist.setCurrentIndex(0)
            self.attendancebutton.setCurrentIndex(alistflag)
     
            if subjecttable=="Course":
                x=0
            else:
                self.itemlist.setCurrentIndex(0)
                self.analysislist.setCurrentIndex(0)
                self.selectlist.setCurrentIndex(0)
                self.frame.setVisible(0)
                self.q1.setVisible(0)
                self.q2.setVisible(0)
                self.questionlist.setVisible(0)
                self.insertbutton.setVisible(0)
                self.l1.setVisible(0)
                self.l2.setVisible(0)
                self.l3.setVisible(0)
                self.l4.setVisible(0)
                self.l5.setVisible(0)
                self.l6.setVisible(0)
                self.l7.setVisible(0)
                self.l8.setVisible(0)
                self.l9.setVisible(0)
                self.l10.setVisible(0)
                self.l11.setVisible(0)
                self.l12.setVisible(0)
                self.examlist.setVisible(0)
                self.createquiz.setVisible(0)
                self.selecttable.setVisible(0)
                self.itemtable.setVisible(0)
                self.attendancelist.setVisible(1)
                self.plotbar.setVisible(0)
                self.frame2.setVisible(0)
                self.tabletopic.setVisible(0)
                self.tablequiz.setVisible(0)
                self.createtopic.setVisible(0)
                self.topiclist.setVisible(0)
                self.systemtable.setVisible(0)
                self.savebutton.setVisible(0)
                self.deletebutton.setVisible(0)
                self.editbutton.setVisible(0)
                self.viewlist.setVisible(0)
                self.activatebutton.setVisible(0)
                self.comparisonlist.setVisible(0)
                self.compareadd.setVisible(0)
                self.scoredisp.setVisible(0)
                self.systembutton.setVisible(0)
                self.a1.setVisible(0)
                self.i1.setVisible(0)
                self.i2l.setVisible(0)
                self.i2u.setVisible(0)
                self.i3.setVisible(0)
                self.i4l.setVisible(0)
                self.i4u.setVisible(0)
                self.i5.setVisible(0)
                self.i6l.setVisible(0)
                self.i6u.setVisible(0)
                self.filterlist.setVisible(0)
                self.a2.setVisible(0)
                self.difficultyanalysis.setVisible(0)
                self.l13.setVisible(0)
                #########
                examdb=subjecttable+"attendance"
                conna = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examdb,
                                          )
                #try:
                if True:
                    with conna.cursor() as cursor:
                        
                        sql = "SELECT `studentname`, `deviceid` FROM `"+examtable+"`"
                        print(sql)
                        cura = conna.cursor()
                        #try:
                        if True:
                            cura.execute(sql)
                            resulta = cura.fetchall()
                            print(str(resulta))
                            
                            cnt=0
                            userflag=0
                            userchoice=np.array([])
                            for row in resulta:
                                     
                                     if userflag==0:
                                            userchoice=np.array([str(row[0]),str(row[1])])
                                            print(userchoice)
                                            userflag=1
                                     elif userflag==1:
                                            userchoice=np.vstack([userchoice,np.array([str(row[0]),str(row[1])])])
                                            print(userchoice)
                                     
                                     cnt=cnt+1
                                
                 
                    conna.commit()
                #finally:
                    
                    #print("There is something wrong!")
                #########
                print(len(userchoice))
                 
                self.attendancelist.setRowCount(len(userchoice))
                
                if len(userchoice)==1:
                    self.attendancelist.setItem(0, 0, QtGui.QTableWidgetItem(""+userchoice[0]+""))
                    self.attendancelist.setItem(0, 1, QtGui.QTableWidgetItem(""+userchoice[1]+""))
                
                else:
                    cnt=0
                    for i in range(len(userchoice)):
                             
                             self.attendancelist.setItem(cnt, 0, QtGui.QTableWidgetItem(""+userchoice[cnt][0]+""))
                             self.attendancelist.setItem(cnt, 1, QtGui.QTableWidgetItem(""+userchoice[cnt][1]+""))
                             
                             
                             cnt=cnt+1
                                
                 
        except:
            x=0
            
    def slistselect(self,slistflag):
        global examtable,safeflag
        
        try:
          if safeflag==1:  
            examr=subjecttable
            print(examr)
            conn = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examr,
                                      ) 
            examtable=self.selectlist.itemText(slistflag)
            self.viewlist.setRowCount(0)
            print(examtable)
            self.itemlist.setCurrentIndex(0)
            self.analysislist.setCurrentIndex(0)
            self.attendancebutton.setCurrentIndex(0)
            self.systemlist.setCurrentIndex(0)
            self.selectlist.setCurrentIndex(slistflag)
            #Visibility
            self.selecttable.setVisible(0)
            self.frame2.setVisible(0)
            self.q1.setVisible(0)
            self.q2.setVisible(0)
            self.attendancelist.setVisible(0)    
            self.questionlist.setVisible(0)
            self.insertbutton.setVisible(0)
            self.l1.setVisible(0)
            self.l2.setVisible(0)
            self.l3.setVisible(0)
            self.l4.setVisible(0)
            self.l5.setVisible(0)
            self.l6.setVisible(0)
            self.l7.setVisible(0)
            self.l8.setVisible(0)
            self.l9.setVisible(0)
            self.l10.setVisible(0)
            self.l11.setVisible(0)
            self.l12.setVisible(0)
            self.examlist.setVisible(0)
            self.createquiz.setVisible(0)
            self.itemtable.setVisible(0)
            self.plotbar.setVisible(0)
            self.tablequiz.setVisible(0)
            self.tabletopic.setVisible(0)
            self.createtopic.setVisible(0)
            self.topiclist.setVisible(0)
            self.systemtable.setVisible(0)
            self.viewlist.setVisible(1)
            self.deletebutton.setVisible(1)
            self.editbutton.setVisible(1)
            self.savebutton.setVisible(0)
            self.activatebutton.setVisible(1)
            self.comparisonlist.setVisible(0)
            self.compareadd.setVisible(0)
            self.scoredisp.setVisible(0)
            self.systembutton.setVisible(0)
            self.a1.setVisible(0)
            self.i1.setVisible(0)
            self.i2l.setVisible(0)
            self.i2u.setVisible(0)
            self.i3.setVisible(0)
            self.i4l.setVisible(0)
            self.i4u.setVisible(0)
            self.i5.setVisible(0)
            self.i6l.setVisible(0)
            self.i6u.setVisible(0)
            self.filterlist.setVisible(0)
            self.a2.setVisible(0)
            self.difficultyanalysis.setVisible(0)
            self.l13.setVisible(0)
            self.setWindowTitle("Exam Database - "+ipaddress+" - Select Quiz")
            #Update Table
            try:
                with conn.cursor() as cursor:
                    
                    sql = "SELECT `item`,`question`, `choice1`, `choice2`, `choice3`, `choice4`, `answer`, `topic`, `difficulty` FROM `"+examtable+"`"
                    print(sql)  
                    #try:
                    if True:
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        print(str(result))
                        cnt=0
                        self.viewlist.setRowCount(len(result))
                        for row in result:
                                 
                                 self.viewlist.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                                 self.viewlist.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                                 self.viewlist.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(row[2])+""))
                                 self.viewlist.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(row[3])+""))
                                 self.viewlist.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(row[4])+""))
                                 self.viewlist.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(row[5])+""))
                                 self.viewlist.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(row[6])+""))
                                 self.viewlist.setItem(cnt, 7, QtGui.QTableWidgetItem(""+str(row[7])+""))
                                 self.viewlist.setItem(cnt, 8, QtGui.QTableWidgetItem(""+str(row[8])+""))
                                 cnt=cnt+1
                            
             
                    #except:
                        #print("Oops! Something wrong")
             
                conn.commit()
            finally:
                #conn.close()
                print("")
        except:
            x=0
    def comparisonselect(self,comparisonflag):
        global comparisonsel
        comparisonsel=self.comparisonlist.itemText(comparisonflag)
        print(comparisonsel)
    def compareaddfunc(self):
        global comparisonsel,subjecttable,x,y,examtable,percenttotal,iflag,resulttext,percenttext
        examr=subjecttable+"attendance"
        connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        try:
            with connr.cursor() as cursor:
                sql = "SELECT `studentname`,`deviceid` FROM `"+comparisonsel+"`"
                
                
                curs = connr.cursor()
                curs.execute(sql)
                result = curs.fetchall()
                totalstudent=len(result)
        except:
            print("Something Wrong!")
            
        examr=subjecttable+"results"
        connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        percenttotal=0
        try:
            with connr.cursor() as cursor:
                
                sql = "SELECT `item`,`average`, `difficulty` FROM `"+comparisonsel+"`"
                print(sql)
                curs = connr.cursor()
                
                if True:
                    curs.execute(sql)
                    result = curs.fetchall()
                    print(str(result))
                    
                    cnt=0
                    
                    for row in result:
                             
                             percenttotal=percenttotal+float(row[1])
                               
                             cnt=cnt+1
                    
                    percenttotal=(percenttotal/(len(result)*totalstudent))*100 
                    print(str(percenttotal)+" %")
         
            connr.commit()
        finally:
            #conn.close()
            print("")
        
        y.append(percenttotal)
        print(y)
        
        x.append(len(x)+1)
        print(x)
        self.plotbar.setXRange(1, len(x)+1)
        
        bg = pg.BarGraphItem(x=x, height=y, width=0.6, brush='r')
        self.plotbar.addItem(bg)
        if iflag==1:
            resulttext=examtable+"   -   "+comparisonsel
            percenttext=percenttext+"   -   "+str("{:.2f}".format(percenttotal))
            disptext=resulttext+"\n"+percenttext
            iflag=0
        else:
            resulttext=resulttext+"   -   "+comparisonsel
            percenttext=percenttext+"   -   "+str("{:.2f}".format(percenttotal))
            disptext=resulttext+"\n"+percenttext
        self.scoredisp.setText(disptext)
    def analysisselect(self,analysisflag):
        global examtable,subjecttable,x,y,examtable,percenttotal,iflag,percenttext,safeflag
        try:
         if safeflag==1:
            iflag=1
            self.itemlist.setCurrentIndex(0)
            self.selectlist.setCurrentIndex(0)
            self.attendancebutton.setCurrentIndex(0)
            self.systemlist.setCurrentIndex(0)
            self.analysislist.setCurrentIndex(analysisflag)
            examtable=self.analysislist.itemText(analysisflag)
            print(examtable)
            self.plotbar.setVisible(1)
            #Visibility
            self.viewlist.setVisible(0)
            self.itemtable.setVisible(0)
            self.frame2.setVisible(0)
            self.q1.setVisible(0)
            self.q2.setVisible(0)
            self.attendancelist.setVisible(0)    
            self.questionlist.setVisible(0)
            self.insertbutton.setVisible(0)
            self.l1.setVisible(0)
            self.l2.setVisible(0)
            self.l3.setVisible(0)
            self.l4.setVisible(0)
            self.l5.setVisible(0)
            self.l6.setVisible(0)
            self.l7.setVisible(0)
            self.l8.setVisible(0)
            self.l9.setVisible(0)
            self.l10.setVisible(0)
            self.l11.setVisible(0)
            self.l12.setVisible(0)
            self.examlist.setVisible(0)
            self.createquiz.setVisible(0)
            self.selecttable.setVisible(0)
            self.tablequiz.setVisible(0)
            self.tabletopic.setVisible(0)
            self.createtopic.setVisible(0)
            self.topiclist.setVisible(0)
            self.systemtable.setVisible(0)
            self.savebutton.setVisible(0)
            self.deletebutton.setVisible(0)
            self.editbutton.setVisible(0)
            self.activatebutton.setVisible(0)
            self.comparisonlist.setVisible(1)
            self.compareadd.setVisible(1)
            self.scoredisp.setVisible(1)
            self.systembutton.setVisible(0)
            self.a1.setVisible(0)
            self.i1.setVisible(0)
            self.i2l.setVisible(0)
            self.i2u.setVisible(0)
            self.i3.setVisible(0)
            self.i4l.setVisible(0)
            self.i4u.setVisible(0)
            self.i5.setVisible(0)
            self.i6l.setVisible(0)
            self.i6u.setVisible(0)
            self.difficultyanalysis.setVisible(0)
            self.difficultyanalysis.setVisible(0)
            self.filterlist.setVisible(0)
            self.a2.setVisible(0)
            self.l13.setVisible(0)
            totalstudent=0
            examr=subjecttable+"attendance"
            connr = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examr,
                                      )
            try:
                with connr.cursor() as cursor:
                    sql = "SELECT `studentname`,`deviceid` FROM `"+examtable+"`"
                    
                    
                    curs = connr.cursor()
                    curs.execute(sql)
                    result = curs.fetchall()
                    totalstudent=len(result)
            except:
                print("Something Wrong!")
                
            examr=subjecttable+"results"
            connr = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examr,
                                      )
            percenttotal=0
            try:
                with connr.cursor() as cursor:
                    
                    sql = "SELECT `item`,`average`, `difficulty` FROM `"+examtable+"`"
                    print(sql)
                    curs = connr.cursor()
                    
                    if True:
                        curs.execute(sql)
                        result = curs.fetchall()
                        print(str(result))
                        
                        cnt=0
                        
                        
                        for row in result:
                                 
                                 percenttotal=percenttotal+float(row[1])  

                                 cnt=cnt+1
                        print(len(result))    
                        percenttotal=(percenttotal/(len(result)*totalstudent))*100 
                        print(str(percenttotal)+" %")
             
                connr.commit()
            finally:
                #conn.close()
                print("")
            self.plotbar.clear()    
            y =[percenttotal]
            x = [1]
            bg = pg.BarGraphItem(x=x, height=y, width=0.6, brush='r')
            self.plotbar.addItem(bg)
            percenttext=str("{:.2f}".format(percenttotal))
            resulttext=examtable+"\n"+percenttext
            self.scoredisp.setText(resulttext)
            self.setWindowTitle("Exam Database - "+ipaddress+" - Exam Analysis")
        except:
            x=0
        
    def itemselect(self,itemflag):
        global examtable,connr,subjecttable,safeflag
        self.filterlist.setCurrentIndex(0)
        try:
         if safeflag==1:
            examtable=self.itemlist.itemText(itemflag)
            self.selectlist.setCurrentIndex(0)
            self.analysislist.setCurrentIndex(0)
            self.attendancebutton.setCurrentIndex(0)
            self.systemlist.setCurrentIndex(0)
            
            self.itemlist.setCurrentIndex(itemflag)
            #Visibility
            self.frame2.setVisible(0)    
            self.itemtable.setVisible(1)
            self.frame.setVisible(0)
            self.q1.setVisible(0)
            self.q2.setVisible(0)
            self.attendancelist.setVisible(0)    
            self.questionlist.setVisible(0)
            self.insertbutton.setVisible(0)
            self.l1.setVisible(0)
            self.l2.setVisible(0)
            self.l3.setVisible(0)
            self.l4.setVisible(0)
            self.l5.setVisible(0)
            self.l6.setVisible(0)
            self.l7.setVisible(0)
            self.l8.setVisible(0)
            self.l9.setVisible(0)
            self.l10.setVisible(0)
            self.l11.setVisible(0)
            self.l12.setVisible(0)
            self.examlist.setVisible(0)
            self.createquiz.setVisible(0)
            self.selecttable.setVisible(0)
            self.plotbar.setVisible(0)
            self.tablequiz.setVisible(0)
            self.tabletopic.setVisible(0)
            self.createtopic.setVisible(0)
            self.topiclist.setVisible(0)
            self.systemtable.setVisible(0)
            self.savebutton.setVisible(0)
            self.deletebutton.setVisible(0)
            self.editbutton.setVisible(0)
            self.viewlist.setVisible(0)
            self.activatebutton.setVisible(0)
            self.comparisonlist.setVisible(0)
            self.compareadd.setVisible(0)
            self.scoredisp.setVisible(0)
            self.systembutton.setVisible(0)
            self.a1.setVisible(1)
            self.i1.setVisible(1)
            self.i2l.setVisible(1)
            self.i2u.setVisible(1)
            self.i3.setVisible(1)
            self.i4l.setVisible(1)
            self.i4u.setVisible(1)
            self.i5.setVisible(1)
            self.i6l.setVisible(1)
            self.i6u.setVisible(1)
            self.difficultyanalysis.setVisible(1)
            self.filterlist.setVisible(1)
            self.a2.setVisible(1)
            self.l13.setVisible(0)
            totalstudent=0
            examr=subjecttable+"attendance"
            connr = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examr,
                                      )
            try:
                with connr.cursor() as cursor:
                    sql = "SELECT `studentname`,`deviceid` FROM `"+examtable+"`"
                    
                    
                    curs = connr.cursor()
                    curs.execute(sql)
                    result = curs.fetchall()
                    totalstudent=len(result)
            except:
                print("Something Wrong!")
                
            examr=subjecttable+"results"
            connr = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examr,
                                      )
            try:
                with connr.cursor() as cursor:
                    
                    sql = "SELECT `item`,`question`,`topic`,`average`, `difficulty` FROM `"+examtable+"`"
                    print(sql)
                    curs = connr.cursor()
                    #try:
                    if True:
                        curs.execute(sql)
                        result = curs.fetchall()
                        print(str(result))
                        cnt=0
                        self.itemtable.setRowCount(len(result))
                        
                        for row in result:
                                 
                                 self.itemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                                 self.itemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                                 self.itemtable.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(row[2])+""))
                                 self.itemtable.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str((float(row[3])/totalstudent)*100)+"%"))
                                 self.itemtable.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(row[4])+""))
                                 
                                 cnt=cnt+1
                            
             
                    #except:
                        #print("Oops! Something wrong")
             
                connr.commit()
            finally:
                #conn.close()
                print("")

            
            
            try:
                
                    
                #Mark2
                #SQL Selector
                examf=subjecttable+"time"
                conn = pymysql.connect(
                                            host='localhost',
                                            user='francis',
                                            password='1234',
                                            db=examf,
                                      )
                
                self.filterlist.clear()
                self.filterlist.addItems(["All"])
                try:
                    with conn.cursor() as cursor:
                        
                        sql = "SELECT `topic`,`time` FROM `"+examtable+"`"
                        
                        curs = conn.cursor()
                        #try:
                        if True:
                            curs.execute(sql)
                            result = curs.fetchall()
                            
                            cnt=0
                            
                            for row in result:
                                 self.filterlist.addItems([row[0]])
                                 
                                 cnt=cnt+1
                            
                
                except:
                    print("Error")
                    
                    self.filterlist.addItems([str(table)])
                    
            except:
                x=0
            self.setWindowTitle("Exam Database - "+ipaddress+" - Student Understanding")
            
        except:
            x=0
        
    def subjectselect(self,subjectflag):
        global subjecttable,cur,conn,safeflag,ipaddress
        self.setWindowTitle("Exam Database - "+ipaddress+" - Syllabus")
        subjecttable=self.subjectlist.itemText(subjectflag)
        
        print(subjecttable)
        self.frame.setVisible(0)
        self.frame2.setStyleSheet("border-image: url("+subjecttable+".png);");
        #self.frame2.setScaledContents(true);
        self.frame2.setVisible(1)
        self.itemtable.setVisible(0)
        self.plotbar.setVisible(0)
        self.viewlist.setVisible(0)
        self.savebutton.setVisible(0)
        self.deletebutton.setVisible(0)
        self.editbutton.setVisible(0)
        safeflag=0
        if subjecttable=="Course":
            safeflag=0
            self.selectlist.clear()
            self.selectlist.addItems(["Select Quiz"])

            self.analysislist.clear()
            self.analysislist.addItems(["Exam Analysis"])

            self.itemlist.clear()
            self.itemlist.addItems(["Student Understanding"])

            self.attendancebutton.clear()
            self.attendancebutton.addItems(["Attendance"])

            self.systemlist.clear()
            self.systemlist.addItems(["System Recommendation"])
            
            self.frame.setVisible(1)
            self.attendancelist.setVisible(0)
            self.q1.setVisible(0)
            self.q2.setVisible(0)
            self.questionlist.setVisible(0)
            self.insertbutton.setVisible(0)
            self.l1.setVisible(0)
            self.l2.setVisible(0)
            self.l3.setVisible(0)
            self.l4.setVisible(0)
            self.l5.setVisible(0)
            self.l6.setVisible(0)
            self.l7.setVisible(0)
            self.l8.setVisible(0)
            self.l9.setVisible(0)
            self.l10.setVisible(0)
            self.l11.setVisible(0)
            self.l12.setVisible(0)
            self.tablequiz.setVisible(0)
            self.tabletopic.setVisible(0)
            self.createtopic.setVisible(0)
            self.examlist.setVisible(0)
            self.createquiz.setVisible(0)
            self.selecttable.setVisible(0)
            self.itemtable.setVisible(0)
            self.plotbar.setVisible(0)
            self.topiclist.setVisible(0)
            self.systemtable.setVisible(0)
            self.savebutton.setVisible(0)
            self.deletebutton.setVisible(0)
            self.editbutton.setVisible(0)
            self.viewlist.setVisible(0)
            self.activatebutton.setVisible(0)
            self.comparisonlist.setVisible(0)
            self.compareadd.setVisible(0)
            self.scoredisp.setVisible(0)
            self.systembutton.setVisible(0)
            self.a1.setVisible(0)
            self.i1.setVisible(0)
            self.i2l.setVisible(0)
            self.i2u.setVisible(0)
            self.i3.setVisible(0)
            self.i4l.setVisible(0)
            self.i4u.setVisible(0)
            self.i5.setVisible(0)
            self.i6l.setVisible(0)
            self.i6u.setVisible(0)
            self.difficultyanalysis.setVisible(0)
            self.filterlist.setVisible(0)
            self.a2.setVisible(0)
            self.l13.setVisible(0)
        else:
            
            self.attendancelist.setVisible(0)
            self.q1.setVisible(0)
            self.q2.setVisible(0)
            self.questionlist.setVisible(0)
            self.insertbutton.setVisible(0)
            self.l1.setVisible(0)
            self.l2.setVisible(0)
            self.l3.setVisible(0)
            self.l4.setVisible(0)
            self.l5.setVisible(0)
            self.l6.setVisible(0)
            self.l7.setVisible(0)
            self.l8.setVisible(0)
            self.l9.setVisible(0)
            self.l10.setVisible(0)
            self.l11.setVisible(0)
            self.l12.setVisible(0)
            self.tablequiz.setVisible(0)
            self.tabletopic.setVisible(0)
            self.createtopic.setVisible(0)
            self.examlist.setVisible(0)
            self.createquiz.setVisible(0)
            self.selecttable.setVisible(0)
            self.itemtable.setVisible(0)
            self.plotbar.setVisible(0)
            self.topiclist.setVisible(0)
            self.systemtable.setVisible(0)
            self.savebutton.setVisible(0)
            self.deletebutton.setVisible(0)
            self.editbutton.setVisible(0)
            self.viewlist.setVisible(0)
            self.activatebutton.setVisible(0)
            self.comparisonlist.setVisible(0)
            self.compareadd.setVisible(0)
            self.scoredisp.setVisible(0)
            self.systembutton.setVisible(0)
            self.a1.setVisible(0)
            self.i1.setVisible(0)
            self.i2l.setVisible(0)
            self.i2u.setVisible(0)
            self.i3.setVisible(0)
            self.i4l.setVisible(0)
            self.i4u.setVisible(0)
            self.i5.setVisible(0)
            self.i6l.setVisible(0)
            self.i6u.setVisible(0)
            self.difficultyanalysis.setVisible(0)
            self.filterlist.setVisible(0)
            self.a2.setVisible(0)
            self.l13.setVisible(0)
            self.selectlist.clear()
            self.selectlist.addItems(["Select Quiz"])

            self.analysislist.clear()
            self.analysislist.addItems(["Exam Analysis"])

            self.itemlist.clear()
            self.itemlist.addItems(["Student Understanding"])

            self.attendancebutton.clear()
            self.attendancebutton.addItems(["Attendance"])

            self.systemlist.clear()
            self.systemlist.addItems(["System Recommendation"])
            safeflag=1
        try:
            
                
            
            #SQL Selector
            conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=subjecttable,
                                  )
            cur = conn.cursor()
            curtext="SELECT table_name FROM information_schema.tables WHERE table_schema = '"+subjecttable+"'"
            #print(curtext)
            cur.execute(curtext)

        
        
            initflag=0
            for table in [tables[0] for tables in cur.fetchall()]:
                #print(table)
                self.selectlist.addItems([str(table)])
                self.analysislist.addItems([str(table)])
                self.itemlist.addItems([str(table)])
                self.attendancebutton.addItems([str(table)])
                self.comparisonlist.addItems([str(table)])
                self.systemlist.addItems([str(table)])
                if initflag==0:
                    examtable=str(table)
                    initflag=1
        except:
            x=0
        
   
    
    def topicfunc(self):
        global topicflag,topicchoice,rowlength
        rowlength=self.tabletopic.rowCount()
        rowlength=rowlength+1
        print(rowlength)
        
        self.tabletopic.setRowCount(rowlength)
        
    def tablequizfunc(self):
            global rowlength,subjecttable,newquiz
            try:
                examr=subjecttable+"time"
                connr = pymysql.connect(
                                                    host='localhost',
                                                    user='francis',
                                                    password='1234',
                                                    db=examr,
                                              )
                try:
                        with connr.cursor() as cursor:
                            sql="CREATE TABLE `"+newquiz+"`(topic TEXT, time TEXT)"
                            
                            
                            curs = connr.cursor()
                            curs.execute(sql)
                except:
                    print("Something Wrong!")
                timetotal=0
                topicflag=0
                self.topiclist.clear()
                for rowtable in range(rowlength):
                       
                       topicdata=self.tabletopic.item(rowtable,0).text()
                       timesel=self.tabletopic.item(rowtable,1).text()
                       #Insert Table
                       try:
                            with connr.cursor() as cursor:
                                sql = "INSERT INTO `"+newquiz+"`(`topic`,`time`) VALUES (%s,%s)"
                                try:
                                    cursor.execute(sql, (topicdata,timesel))
                                    
                                except:
                                    print("Oops! Something wrong")
                         
                            connr.commit()
                       finally:
                            print("")
                       timetotal=timetotal+float(timesel)
                       if topicflag==0:
                            topicchoice=np.array([topicdata])
                            print(topicchoice)
                            topicflag=1
                       elif topicflag==1:
                            topicchoice=np.hstack([topicchoice,topicdata])
                   
                print(timetotal)
                for i in range(len(topicchoice)):
                
                    self.topiclist.addItems([topicchoice[i]])
                
                print(topicchoice)
                if timetotal<=45 and timetotal>=4.5:
                    self.itemlist.setCurrentIndex(0)
                    self.analysislist.setCurrentIndex(0)
                    self.selectlist.setCurrentIndex(0)
                    self.attendancebutton.setCurrentIndex(0)
                    self.systemlist.setCurrentIndex(0)
                    self.selecttable.setVisible(0)
                    self.itemtable.setVisible(0)
                    self.frame.setVisible(0)
                    self.q1.setVisible(0)
                    self.q2.setVisible(0)
                    self.attendancelist.setVisible(0)
                    self.createquiz.setVisible(0)
                    #
                    self.questionlist.setVisible(1)
                    self.insertbutton.setVisible(1)
                    self.l1.setVisible(1)
                    self.l2.setVisible(1)
                    self.l3.setVisible(1)
                    self.l4.setVisible(1)
                    self.l5.setVisible(1)
                    self.l6.setVisible(1)
                    self.l7.setVisible(1)
                    self.l8.setVisible(1)
                    self.l9.setVisible(1)
                    self.l10.setVisible(1)
                    self.l11.setVisible(1)
                    self.l12.setVisible(1)
                    self.topiclist.setVisible(1)
                    #
                    
                    self.plotbar.setVisible(0)
                    self.frame2.setVisible(0)
                    self.tablequiz.setVisible(0)
                    self.tabletopic.setVisible(0)
                    self.createtopic.setVisible(0)
                    self.savebutton.setVisible(0)
                    self.deletebutton.setVisible(0)
                    self.editbutton.setVisible(0)
                    self.viewlist.setVisible(0)
                    self.activatebutton.setVisible(0)
                    self.comparisonlist.setVisible(0)
                    self.compareadd.setVisible(0)
                    self.scoredisp.setVisible(0)
                    self.systembutton.setVisible(0)
                    self.a1.setVisible(0)
                    self.i1.setVisible(0)
                    self.i2l.setVisible(0)
                    self.i2u.setVisible(0)
                    self.i3.setVisible(0)
                    self.i4l.setVisible(0)
                    self.i4u.setVisible(0)
                    self.i5.setVisible(0)
                    self.i6l.setVisible(0)
                    self.i6u.setVisible(0)
                    self.difficultyanalysis.setVisible(0)
                    self.filterlist.setVisible(0)
                    self.a2.setVisible(0)
                    self.l13.setVisible(0)
                    self.systemtable.setVisible(0)
                    
                else:
                    print("Adjust time of each topic with a total of 45 hours.")
            except:
                   print("Please delete extra row.")
    def quizfunc(self):
        global newquiz,cur,topicchoice,subjecttable
        
        newquiz=str(self.q2.text())
        curtext="CREATE TABLE `"+newquiz+"`(id int,item TEXT, question TEXT, choice1 TEXT, choice2 TEXT, choice3 TEXT, choice4 TEXT, answer TEXT, topic TEXT, difficulty TEXT)"
        
        print(curtext)
        cur.execute(curtext)
        examdb="studentinfo"
        conna = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examdb,
                                  )
        #try:
        if True:
            with conna.cursor() as cursor:
                
                sql = "SELECT `username`,`password`, `deviceid`,  `studentname` FROM `credentials`"
                
                
                cura = conna.cursor()
                
                #try:
                if True:
                    cura.execute(sql)
                    resulta = cura.fetchall()
                    #print(str(resulta))
                    
                    cnt=0
                    userflag=0
                    for row in resulta:
                             
                             if userflag==0:
                                    userchoice=np.array([str(row[0]),str(row[2])])
                                    
                                    userflag=1
                             elif userflag==1:
                                    userchoice=np.vstack([userchoice,np.array([str(row[0]),str(row[2])])])
                                    
                             
                             cnt=cnt+1
                        
         
            conna.commit()
        ####    
        examr=subjecttable+"attendance"
        connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        try:
            with connr.cursor() as cursor:
                sql="CREATE TABLE `"+newquiz+"`(studentname TEXT, deviceid TEXT)"
                
                
                curs = connr.cursor()
                curs.execute(sql)
        except:
            print("Something Wrong!")
        
        #Insert Table 
        try:
            with connr.cursor() as cursor:
                sql = "INSERT INTO `"+newquiz+"`(`studentname`,`deviceid`) VALUES (%s,%s )"
                try:
                    for row in resulta:
                        cursor.execute(sql, (str(row[0]),str(row[2])))
                    
                except:
                    print("Oops! Something wrong")
         
            connr.commit()
        except:
            
            print("Something Wrong!")

        #####
        examr=subjecttable+"results"
        connr = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=examr,
                                  )
        try:
            with connr.cursor() as cursor:
                sql="CREATE TABLE `"+newquiz+"`(id int, item TEXT, question TEXT, topic TEXT, average TEXT, difficulty TEXT)"
                
                
                curs = connr.cursor()
                curs.execute(sql)
        except:
            print("Something Wrong!")
        
        
        try:
            self.selectlist.clear()
            self.selectlist.addItems(["Select Quiz"])

            self.analysislist.clear()
            self.analysislist.addItems(["Exam Analysis"])

            self.itemlist.clear()
            self.itemlist.addItems(["Student Understanding"])

            self.attendancebutton.clear()
            self.attendancebutton.addItems(["Attendance"])
            #SQL Selector
            conn = pymysql.connect(
                                        host='localhost',
                                        user='francis',
                                        password='1234',
                                        db=subjecttable,
                                  )
            cur = conn.cursor()
            curtext="SELECT table_name FROM information_schema.tables WHERE table_schema = '"+subjecttable+"'"
            #print(curtext)
            cur.execute(curtext)

        
        
            initflag=0
            for table in [tables[0] for tables in cur.fetchall()]:
                #print(table)
                self.selectlist.addItems([str(table)])
                self.analysislist.addItems([str(table)])
                self.itemlist.addItems([str(table)])
                self.attendancebutton.addItems([str(table)])
                if initflag==0:
                    examtable=str(table)
                    initflag=1
        except:
            x=0
        if subjecttable=="Course":
            x=0
        else:
            
            self.itemlist.setCurrentIndex(0)
            self.analysislist.setCurrentIndex(0)
            self.selectlist.setCurrentIndex(0)
            self.attendancebutton.setCurrentIndex(0)
            self.systemlist.setCurrentIndex(0)
            self.selecttable.setVisible(0)
            self.itemtable.setVisible(0)
            self.frame.setVisible(0)
            self.q1.setVisible(0)
            self.q2.setVisible(0)
            self.attendancelist.setVisible(0)
            self.createquiz.setVisible(0)
            
            self.tabletopic.setVisible(0)
            
            self.plotbar.setVisible(0)
            self.frame2.setVisible(0)
            self.tabletopic.setVisible(1)
            self.tablequiz.setVisible(1)
            self.createquiz.setVisible(0)
            self.createtopic.setVisible(1)
            self.savebutton.setVisible(0)
            self.deletebutton.setVisible(0)
            self.editbutton.setVisible(0)
            self.viewlist.setVisible(0)
            self.activatebutton.setVisible(0)
            self.comparisonlist.setVisible(0)
            self.compareadd.setVisible(0)
            self.scoredisp.setVisible(0)
            self.systembutton.setVisible(0)
            self.a1.setVisible(0)
            self.i1.setVisible(0)
            self.i2l.setVisible(0)
            self.i2u.setVisible(0)
            self.i3.setVisible(0)
            self.i4l.setVisible(0)
            self.i4u.setVisible(0)
            self.i5.setVisible(0)
            self.i6l.setVisible(0)
            self.i6u.setVisible(0)
            self.difficultyanalysis.setVisible(0)
            self.systemtable.setVisible(0)
            self.filterlist.setVisible(0)
            self.a2.setVisible(0)
            self.l13.setVisible(0)
    def createfunc(self):
        global topicflag,ipaddress
        topicflag=0
        self.q2.setText("")
        
        if subjecttable=="Course":
            x=0
        else:
            self.topiclist.clear()
            self.tabletopic.setRowCount(0)
            self.itemlist.setCurrentIndex(0)
            self.analysislist.setCurrentIndex(0)
            self.selectlist.setCurrentIndex(0)
            self.attendancebutton.setCurrentIndex(0)
            self.systemlist.setCurrentIndex(0)
            self.frame.setVisible(0)
            self.attendancelist.setVisible(0)
            
            self.q1.setVisible(0)
            self.q2.setVisible(0)
            self.questionlist.setVisible(0)
            self.insertbutton.setVisible(0)
            self.l1.setVisible(0)
            self.l2.setVisible(0)
            self.l3.setVisible(0)
            self.l4.setVisible(0)
            self.l5.setVisible(0)
            self.l6.setVisible(0)
            self.l7.setVisible(0)
            self.l8.setVisible(0)
            self.l9.setVisible(0)
            self.l10.setVisible(0)
            self.l11.setVisible(0)
            self.l12.setVisible(0)
            self.examlist.setVisible(0)
            self.createquiz.setVisible(0)
            self.selecttable.setVisible(0)
            self.itemtable.setVisible(0)
            self.createquiz.setVisible(1)
            self.q1.setVisible(1)
            self.q2.setVisible(1)
            self.plotbar.setVisible(0)
            self.frame2.setVisible(0)
            self.tabletopic.setVisible(0)
            self.tablequiz.setVisible(0)
            self.createtopic.setVisible(0)#
            self.topiclist.setVisible(0)
            self.filterlist.setVisible(0)
            self.a2.setVisible(0)
            self.savebutton.setVisible(0)
            self.deletebutton.setVisible(0)
            self.editbutton.setVisible(0)
            self.viewlist.setVisible(0)
            self.activatebutton.setVisible(0)
            self.comparisonlist.setVisible(0)
            self.compareadd.setVisible(0)
            self.scoredisp.setVisible(0)
            self.systembutton.setVisible(0)
            self.a1.setVisible(0)
            self.i1.setVisible(0)
            self.i2l.setVisible(0)
            self.i2u.setVisible(0)
            self.i3.setVisible(0)
            self.i4l.setVisible(0)
            self.i4u.setVisible(0)
            self.i5.setVisible(0)
            self.i6l.setVisible(0)
            self.i6u.setVisible(0)
            self.difficultyanalysis.setVisible(0)
            self.systemtable.setVisible(0)
            self.l13.setVisible(0)
        self.setWindowTitle("Exam Database - "+ipaddress+" - Create Quiz")
    def systemselect(self,systemflag):
        global subjecttable,average,examtable,safeflag
        try:
         if safeflag==1:   
        
            
            if subjecttable=="Course":
                x=0
            else:
                self.itemlist.setCurrentIndex(0)
                self.analysislist.setCurrentIndex(0)
                self.selectlist.setCurrentIndex(0)
                self.attendancebutton.setCurrentIndex(0)
               
                self.frame.setVisible(0)
                self.attendancelist.setVisible(0)
                
                self.q1.setVisible(0)
                self.q2.setVisible(0)
                self.questionlist.setVisible(0)
                self.insertbutton.setVisible(0)
                self.l1.setVisible(0)
                self.l2.setVisible(0)
                self.l3.setVisible(0)
                self.l4.setVisible(0)
                self.l5.setVisible(0)
                self.l6.setVisible(0)
                self.l7.setVisible(0)
                self.l8.setVisible(0)
                self.l9.setVisible(0)
                self.l10.setVisible(0)
                self.l11.setVisible(0)
                self.l12.setVisible(0)
                self.examlist.setVisible(0)
                self.createquiz.setVisible(0)
                self.selecttable.setVisible(0)
                self.itemtable.setVisible(0)
                self.createquiz.setVisible(0)
                self.q1.setVisible(0)
                self.q2.setVisible(0)
                self.plotbar.setVisible(0)
                self.frame2.setVisible(0)
                self.tablequiz.setVisible(0)
                self.tabletopic.setVisible(0)
                self.createtopic.setVisible(0)
                self.topiclist.setVisible(0)
                self.systembutton.setVisible(1)
                self.savebutton.setVisible(0)
                self.deletebutton.setVisible(0)
                self.editbutton.setVisible(0)
                self.viewlist.setVisible(0)
                self.activatebutton.setVisible(0)
                self.comparisonlist.setVisible(0)
                self.compareadd.setVisible(0)
                self.scoredisp.setVisible(0)
                self.filterlist.setVisible(0)
                self.a2.setVisible(0)
                self.a1.setVisible(0)
                self.i1.setVisible(0)
                self.i2l.setVisible(0)
                self.i2u.setVisible(0)
                self.i3.setVisible(0)
                self.i4l.setVisible(0)
                self.i4u.setVisible(0)
                self.i5.setVisible(0)
                self.i6l.setVisible(0)
                self.i6u.setVisible(0)
                self.l13.setVisible(1)
                self.difficultyanalysis.setVisible(0)
                self.systemtable.setVisible(1)
                self.systemlist.setCurrentIndex(systemflag)
                examtable=self.systemlist.itemText(systemflag)
                

                
                
                examr=subjecttable+"time"
                connr = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examr,
                                          )
                totalhours=0
                hourflag=0
                try:
                    with connr.cursor() as cursor:
                        
                        sql = "SELECT `topic`,`time` FROM `"+examtable+"`"
                        
                        curs = connr.cursor()
                        #try:
                        if True:
                            curs.execute(sql)
                            result = curs.fetchall()
                            
                            cnt=0
                            self.systemtable.setRowCount(len(result))
                            for row in result:
                             
                                 
                                 totalhours=totalhours+float(row[1])
                                 if hourflag==0:
                                            topicdata=np.array([row[0]]) 
                                            hourdata=np.array([row[1]])
                                            
                                            hourflag=1
                                 elif hourflag==1:
                                            topicdata=np.hstack([topicdata,np.array([row[0]])])
                                            hourdata=np.hstack([hourdata,np.array([row[1]])])
                                 self.systemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                                 self.systemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str("{:.2f}".format(float(hourdata[cnt])))+""))
                                 self.systemtable.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str("{:.2f}".format(float(row[1])))+""))          
                                 cnt=cnt+1
                            print(topicdata)
                            print(hourdata)
                            print(totalhours)
                            
                            
                
                except:
                    print("Error")
                connr.commit()
                totalstudent=0
                self.l13.setText("Total Time: "+str(totalhours)+" Hours")
                examr=subjecttable+"attendance"
                connr = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examr,
                                          )
                try:
                    with connr.cursor() as cursor:
                        sql = "SELECT `studentname`,`deviceid` FROM `"+examtable+"`"
                        
                        
                        curs = connr.cursor()
                        curs.execute(sql)
                        result = curs.fetchall()
                        totalstudent=len(result)
                except:
                    print("Something Wrong!")
                examr=subjecttable+"results"
                connr = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examr,
                                          )
                scoreflag=0
                averageresult=0
                for i in range(len(topicdata)):
                    topicsearch=topicdata[i]
                    print(topicsearch)
                    try:
                        with connr.cursor() as cursor:
                            
                            sql = "SELECT `item`,`question`,`topic`,`average`, `difficulty` FROM `"+examtable+"`"
                            
                            curs = connr.cursor()
                            
                            if True:
                                curs.execute(sql)
                                result = curs.fetchall()
                                
                                cnt=0
                                self.itemtable.setRowCount(len(result))
                                average=0
                                for row in result:
                                         if topicsearch==str(row[2]):
                                             
                                             average=average+(float(row[3])/totalstudent)
                                             
                                             
                                             cnt=cnt+1
                                             totalaverage=average/cnt
                                
                                
                                
                                
                                if scoreflag==0:
                                            scoredata=np.array([totalaverage])
                                            averageresult=averageresult+totalaverage
                                            
                                            scoreflag=1
                                elif scoreflag==1:
                                            scoredata=np.hstack([scoredata,totalaverage])
                                            averageresult=averageresult+totalaverage
                                            
                                
                        connr.commit()
                    finally:
                        print("")
                print(scoredata)
                averagehour=totalhours/len(topicdata)
                averageresult=averageresult/len(topicdata)
                print("Average Hour="+str(averagehour))
                print("Average Result="+str(averageresult))
                
                cnt=0
                for i in range(len(scoredata)):
                    topicsearch=topicdata[i]
                    print(topicsearch)
                    timedistribution=averagehour+averagehour*(averageresult-float(scoredata[i]))-(averagehour-float(hourdata[i]))
                    print(timedistribution)
                    self.systemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(topicsearch)+""))
                    self.systemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str("{:.2f}".format(float(hourdata[i])))+""))
                    self.systemtable.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str("{:.2f}".format(float(timedistribution)))+""))

                    cnt=cnt+1
                self.setWindowTitle("Exam Database - "+ipaddress+" - System Recommendation")
                    
                
        except:
            x=0
        
    def systemfunc(self):
                global subjecttable,average,examtable

                examr=subjecttable+"time"
                connr = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examr,
                                          )
                totalhours=0
                hourflag=0
                try:
                
                    with connr.cursor() as cursor:
                        
                        sql = "SELECT `topic`,`time` FROM `"+examtable+"`"
                        
                        curs = connr.cursor()
                        #try:
                        if True:
                            curs.execute(sql)
                            result = curs.fetchall()
                            
                            cnt=0
                            self.systemtable.setRowCount(len(result))
                            for row in result:
                             
                                 self.systemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                                 self.systemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                                 totalhours=totalhours+float(row[1])
                                 if hourflag==0:
                                            topicdata=np.array([row[0]]) 
                                            hourdata=np.array([row[1]])
                                            
                                            hourflag=1
                                 elif hourflag==1:
                                            topicdata=np.hstack([topicdata,np.array([row[0]])])
                                            hourdata=np.hstack([hourdata,np.array([row[1]])])
                                            
                                 cnt=cnt+1
                            print(topicdata)
                            print(hourdata)
                            print(totalhours)
                            
                
                except:
                    print("Error")
                connr.commit()
                totalstudent=0
                examr=subjecttable+"attendance"
                connr = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examr,
                                          )
                try:
                    with connr.cursor() as cursor:
                        sql = "SELECT `studentname`,`deviceid` FROM `"+examtable+"`"
                        
                        
                        curs = connr.cursor()
                        curs.execute(sql)
                        result = curs.fetchall()
                        totalstudent=len(result)
                except:
                    print("Something Wrong!")
                examr=subjecttable+"results"
                connr = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examr,
                                          )
                scoreflag=0
                averageresult=0
                for i in range(len(topicdata)):
                    topicsearch=topicdata[i]
                    print(topicsearch)
                    try:
                        with connr.cursor() as cursor:
                            
                            sql = "SELECT `item`,`question`,`topic`,`average`, `difficulty` FROM `"+examtable+"`"
                            
                            curs = connr.cursor()
                            
                            if True:
                                curs.execute(sql)
                                result = curs.fetchall()
                                
                                cnt=0
                                self.itemtable.setRowCount(len(result))
                                average=0
                                for row in result:
                                         if topicsearch==str(row[2]):
                                             
                                             average=average+(float(row[3])/totalstudent)
                                             
                                             
                                             cnt=cnt+1
                                             totalaverage=average/cnt
                                
                                
                                
                                
                                if scoreflag==0:
                                            scoredata=np.array([totalaverage])
                                            averageresult=averageresult+totalaverage
                                            
                                            scoreflag=1
                                elif scoreflag==1:
                                            scoredata=np.hstack([scoredata,totalaverage])
                                            averageresult=averageresult+totalaverage
                                            
                                
                        connr.commit()
                    finally:
                        print("")
                print(scoredata)
                averagehour=totalhours/len(topicdata)
                averageresult=averageresult/len(topicdata)
                print("Average Hour="+str(averagehour))
                print("Average Result="+str(averageresult))
                examdb=subjecttable+"time"
                conn = pymysql.connect(
                                                host='localhost',
                                                user='francis',
                                                password='1234',
                                                db=examdb,
                                          )
                for i in range(len(scoredata)):
                    topicsearch=topicdata[i]
                    print(topicsearch)
                    timedistribution=averagehour+averagehour*(averageresult-float(scoredata[i]))-(averagehour-float(hourdata[i]))
                    print(timedistribution)
                    
                    try:
                    
                        with conn.cursor() as cursor:
                            cur=conn.cursor()
                            curtext = "UPDATE `"+examtable+"` SET time='"+str(timedistribution)+"' where topic='"+str(topicsearch)+"'"
                            print(curtext)
                            cur.execute(curtext)
                            conn.commit()
                            
                    except:
                        x=0
                
                try:
                    with conn.cursor() as cursor:
                        
                        sql = "SELECT `topic`,`time` FROM `"+examtable+"`"
                        
                        curs = conn.cursor()
                        #try:
                        if True:
                            curs.execute(sql)
                            result = curs.fetchall()
                            
                            cnt=0
                            self.systemtable.setRowCount(len(result))
                            for row in result:
                             
                                 self.systemtable.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(row[0])+""))
                                 self.systemtable.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(row[1])+""))
                                 cnt=cnt+1
                            
                
                except:
                    print("Error")
                conn.commit()      
    def Loop(self):
        x=0
            
                    
                
           
  
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
