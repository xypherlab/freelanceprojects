import numpy as np
import os
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from collections import Counter
import sys
from PyQt4 import QtGui, QtCore

import time

class Main(QtGui.QMainWindow):
 
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.initUI()
 
	def initUI(self):
            
            centralwidget = QtGui.QWidget(self)
            
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.Loop)
            self.timer.start()
            self.setGeometry(100,100, 480,420)
            
	    self.registerbutton = QtGui.QPushButton("Register Gesture",self)
	    self.registerbutton.clicked.connect(self.register)
	    self.undobutton = QtGui.QPushButton("Delete",self)
	    self.undobutton.clicked.connect(self.undoregister)
	   
	    self.registerbutton.move(180,250)
	    self.undobutton.move(180,300)
	    self.snoretype = QtGui.QComboBox(self)
            self.snoretype.addItems(["No Snore","Mild","High","Intense"])
            self.snoretype.currentIndexChanged.connect(self.dataselect)
            self.snoretype.move(310,380)
            self.snoretype.resize(60,20)
            
        def undoregister(self):
            if os.path.isfile('snoredata.npy'):
                            snoredi=np.load('snoredata.npy')
                            snoreli=np.load('snoredatalabel.npy')
                            x=len(snoredi)-1
                            y=len(snoreli)-1
                            snoredi=np.delete(snoredi,x,0)
                            snoreli=np.delete(snoreli,x,0)
                            np.save('snoredata',snoredi)
                            np.save('snoredatalabel',snoreli)
                            print "snore data deleted."
                            print snoredi
                            print snoreli
            else:
                            print "File doesn't exist"
                    
                    
                    
            
        def register(self):
            global snorepos
            stackdata=np.array([1,2])
            if snorepos==0:
                    snorereg="A"
            elif snorepos==1:
                    snorereg="B"
            elif snorepos==2:
                    snorereg="C"
            elif snorepos==3:
                    snorereg="D"
            if os.path.isfile('snoredata.npy'):
                                    
                            snoredi=np.load('snoredata.npy')
                            snoreli=np.load('snoredatalabel.npy')
                            snorel=np.hstack([snoreli,snorereg])#Label
                            snoredi=np.vstack([snoredi,stackdata])#Data
                            np.save('snoredata.npy',snoredi)
                            np.save('snoredatalabel.npy',snorel)
                            print snoredi
                            print snoredi.shape
                            print snorel
            else:
                            
                            snorel=np.array([snorereg])#Label
                            np.save('snoredata.npy',stackdata)#Data
                            np.save('snoredatalabel.npy',snorel)  
        def dataselect(self,ax):
            global snorepos
            if ax==0:
                snorepos=0
            elif ax==1:
                snorepos=1
            elif ax==2:
                snorepos=2
            elif ax==3:
                snorepos=3
        def Loop(self):
            x=0
            

            
def main():
    
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
    


    
    
     
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    main()
