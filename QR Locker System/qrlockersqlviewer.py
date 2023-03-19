import mysql.connector
from mysql.connector import Error
from PyQt4 import QtGui, QtCore
import sys
import time
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global start_time
        start_time = time.time()
        
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.setGeometry(0,20,800,650)
        font12 = QtGui.QFont("Helvetica", 12)
        font16 = QtGui.QFont("Helvetica", 16)
        self.l1=QtGui.QLabel("QR Locker System Report",self)
        self.l1.move(300,5)
        self.l1.setFont(font12)
        self.l1.setStyleSheet('color: red')
        self.l1.resize(300,30)
        self.l2=QtGui.QLabel("Total Profit:",self)
        self.l2.move(130,500)
        self.l2.setFont(font16)
        self.l2.resize(200,30)
        self.l3=QtGui.QLabel("",self)
        self.l3.move(250,500)
        self.l3.setFont(font16)
        self.l3.resize(200,30)
        
        mydb = mysql.connector.connect(
                   host='sql12.freemysqlhosting.net',
                   database='sql12273787',
                   user='sql12273787',
                   password='KdIxjNH8TK'
                )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM qrlockerdata")

        myresult = mycursor.fetchall()
        z=0
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.move(50,50)
        self.table.setHorizontalHeaderLabels(['                   Locker ID                    ','              Number                 ',
                                                      '              Time             ','               Date                   ','           Credit          '])
         
        self.table.resize(700,400)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        self.table.setRowCount(len(myresult))
        profit=0
        for x in myresult:
          self.table.setItem(z, 0, QtGui.QTableWidgetItem(""+str(x[0])+""))
          self.table.setItem(z, 1, QtGui.QTableWidgetItem(""+str(x[1])+""))
          self.table.setItem(z, 2, QtGui.QTableWidgetItem(""+str(x[2])+""))
          self.table.setItem(z, 3, QtGui.QTableWidgetItem(""+str(x[3])+""))
          self.table.setItem(z, 4, QtGui.QTableWidgetItem(""+str(x[4])+""))
          z=z+1
          profit=profit+int(x[4])
        self.l3.setText(str(profit)+" php") 

        
        
          
             
    def Loop(self):
            global start_time
           
            elapsed_time=time.time()-start_time
            if elapsed_time>=60:
                start_time = time.time()
                mydb = mysql.connector.connect(
                   host='sql12.freemysqlhosting.net',
                   database='sql12273787',
                   user='sql12273787',
                   password='KdIxjNH8TK'
                )

                mycursor = mydb.cursor()

                mycursor.execute("SELECT * FROM qrlockerdata")

                myresult = mycursor.fetchall()
                z=0
                self.table = QtGui.QTableWidget(self)
                self.table.setColumnCount(5)
                self.table.move(50,50)
                self.table.setHorizontalHeaderLabels(['                   Locker ID                    ','              Number                 ',
                                                      '              Time             ','               Date                   ','           Credit          '])
         
       
                self.table.resize(700,400)
                self.table.resizeColumnsToContents()
                self.table.verticalHeader().setVisible(0)
                self.table.setRowCount(len(myresult))
                profit=0
                for x in myresult:
                  self.table.setItem(z, 0, QtGui.QTableWidgetItem(""+str(x[0])+""))
                  self.table.setItem(z, 1, QtGui.QTableWidgetItem(""+str(x[1])+""))
                  self.table.setItem(z, 2, QtGui.QTableWidgetItem(""+str(x[2])+""))
                  self.table.setItem(z, 3, QtGui.QTableWidgetItem(""+str(x[3])+""))
                  self.table.setItem(z, 4, QtGui.QTableWidgetItem(""+str(x[4])+""))
                  z=z+1
                  profit=profit+int(x[4])
                self.l3.setText(str(profit)+" php") 
                  

def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
