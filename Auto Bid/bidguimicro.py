import re
import json
import requests
import pandas as pd
import difflib #Pattern Recognition
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import time
import os
from datetime import datetime
sys.setrecursionlimit(40000)
from selenium import webdriver
import pyautogui
class Main(QtWidgets.QMainWindow):

        def __init__(self):
            super().__init__()

            self.initUI()
        def initUI(self):
             global emailflag,url,pagehistory,flagtimer,url,url2,urlpayload
             flagtimer=0
             emailflag=0
             #pagehistory="?&pageHistory=0,1,2,3,4,5,6"
             #url1="https://docs.google.com/forms/d/e/1FAIpQLSek3p5Ae6RNJ6Rmc8atuVRtTEduMCQpvw8AnDAaQQcyqqSE9w"
             #url=url1+"/formResponse"
             #url2=url1+"/viewform?usp=pp_url"
             urlpayload="https://forms.office.com/pages/responsepage.aspx?id=YITPJFFnikKrGajrBN_kRxgEKJ-5baBOqb8ydZakcbZUOU5LSDVVWUI3VFpYVUtHWkVNRzRJV1lSRS4u"                
        
             self.timer = QtCore.QTimer(self)
             self.timer.timeout.connect(self.Loop)
             self.timer.start()
            
             self.sendbutton = QtWidgets.QPushButton("Send Data",self)
             self.sendbutton.clicked.connect(self.sendform)
             self.sendbutton.move(50,200)

             self.e1=QtWidgets.QLineEdit(self)
             self.e1.move(50,80)
             self.e1.resize(100,20)
            
             self.activatebutton = QtWidgets.QPushButton("Auto Deactivated",self)
             self.activatebutton.clicked.connect(self.activatedata)
             self.activatebutton.move(50,110)
             
             
             self.t2=QtWidgets.QLabel("Car Bidding Google Form",self)
             self.t2.move(50,20)
             self.t2.resize(250,20)
             self.t3=QtWidgets.QLabel("Time: ",self)
             self.t3.move(50,50)
             self.t3.resize(250,20)

             self.t1=QtWidgets.QLabel("Email: ",self)
             self.t1.move(50,250)
           
             self.setGeometry(0,20,250,300) #GUI Size (X Location, Y Location, X Size, Y Size
             self.show()
        def activatedata(self):
                global flagtimer
                if flagtimer==0:
                        flagtimer=1
                        self.activatebutton.setText("Auto Activated")
                elif flagtimer==1:
                        flagtimer=0
                        self.activatebutton.setText("Auto Deactivated")
        
        def sendform(self):
            global emailflag,url,pagehistory,url2,urlpayload
            #urlpayload="https://forms.office.com/Pages/ResponsePage.aspx?id=YITPJFFnikKrGajrBN_kRz-9qav7UhVJrcg4DBqpWv5UOVM1OVE3T1VaM05FNDI4TE9ZTEhXVDNYQy4u&fbclid=IwAR0DkGBqxA0NiFD7Klmz_0e1F9GCvvMv_xQnxUOJbQ4sWVai5WQgSD3cx9o"                
            df=pd.read_csv("input.csv",header=0)
            np_df = df.values
            nphead=pd.read_csv('input.csv', index_col=0, nrows=0).columns.tolist()
            
            z=0
            #for z in range(len(np_df)):
            if True:
                #option = webdriver.ChromeOptions()
                #option.add_argument("-incognito")
                #browser = webdriver.Chrome(executable_path="D://Auto Bid//chromedriver.exe", options=option)
                browser = webdriver.Firefox(executable_path="D://Auto Bid//geckodriver.exe")
                browser.get(urlpayload)
                time.sleep(1)
                #Email Input and Submission
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.write(str(np_df[z][0]))
                pyautogui.press('tab')
                pyautogui.press('space')
                
                #Email Input and Submission
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('space')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('space')
                #Bid Type
                if str(np_df[z][1])=="1":
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Information
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.write(str(np_df[z][7]))
                        pyautogui.press('tab')
                        pyautogui.write(str(np_df[z][8]))
                        pyautogui.press('tab')
                        pyautogui.write(str(np_df[z][9]))
                        pyautogui.press('tab')
                        pyautogui.write(str(np_df[z][4]))
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        print(int(np_df[z][5]))
                        for i in range(int(np_df[z][5])):
                                pyautogui.press('down')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.write(str(np_df[z][6]))
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Next
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Agreement
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Submit Form
                        #pyautogui.press('tab')
                        #pyautogui.press('tab')
                        #pyautogui.press('space')
                        #pyautogui.keyDown('ctrl')
                        #pyautogui.press('w')
                        #pyautogui.keyUp('ctrl')
                        
                if str(np_df[z][1])=="2":
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Information
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.write(str(np_df[z][2]))
                        pyautogui.press('tab')
                        pyautogui.write(str(np_df[z][3]))
                        pyautogui.press('tab')
                        pyautogui.write(str(np_df[z][4]))
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        print(int(np_df[z][5]))
                        for i in range(int(np_df[z][5])):
                                pyautogui.press('down')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.write(str(np_df[z][6]))
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Next
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Agreement
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                        pyautogui.press('space')
                        #Submit Form
                        #pyautogui.press('tab')
                        #pyautogui.press('tab')
                        #pyautogui.press('space')
                        #pyautogui.keyDown('ctrl')
                        #pyautogui.press('w')
                        #pyautogui.keyUp('ctrl')
               
        def Loop(self):
             global emailflag,url,pagehistory,flagtimer,url2,urlpayload
             now = datetime.now()

             current_time = now.strftime("%H:%M:%S")   
             self.t3.setText("Time: "+current_time)
             try: 
                     if flagtimer==1:
                        timecheck=str(self.e1.text())
                        #print(timecheck)
                        hourcheck=timecheck.split(":")[0]
                        minutecheck=timecheck.split(":")[1]     
                        if str(now.hour) == hourcheck and str(now.minute) == minutecheck:     
                               
                                    #urlpayload="https://forms.office.com/Pages/ResponsePage.aspx?id=YITPJFFnikKrGajrBN_kRz-9qav7UhVJrcg4DBqpWv5UOVM1OVE3T1VaM05FNDI4TE9ZTEhXVDNYQy4u&fbclid=IwAR0DkGBqxA0NiFD7Klmz_0e1F9GCvvMv_xQnxUOJbQ4sWVai5WQgSD3cx9o"                
                                    df=pd.read_csv("input.csv",header=0)
                                    np_df = df.values
                                    nphead=pd.read_csv('input.csv', index_col=0, nrows=0).columns.tolist()
                                    
                                    z=0
                                    for z in range(len(np_df)):
                                    #if True:
                                        #option = webdriver.ChromeOptions()
                                        #option.add_argument("-incognito")
                                        #browser = webdriver.Chrome(executable_path="D://Auto Bid//chromedriver.exe", options=option)
                                        browser = webdriver.Firefox(executable_path="D://Auto Bid//geckodriver.exe")
                                        browser.get(urlpayload)
                                        time.sleep(1)
                                        #Email Input and Submission
                                        pyautogui.press('tab')
                                        pyautogui.press('tab')
                                        pyautogui.press('tab')
                                        pyautogui.write(str(np_df[z][0]))
                                        pyautogui.press('tab')
                                        pyautogui.press('space')
                                        
                                        #Email Input and Submission
                                        pyautogui.press('tab')
                                        pyautogui.press('tab')
                                        pyautogui.press('tab')
                                        pyautogui.press('space')
                                        pyautogui.press('tab')
                                        pyautogui.press('tab')
                                        pyautogui.press('space')
                                        #Bid Type
                                        if str(np_df[z][1])=="1":
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Information
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.write(str(np_df[z][7]))
                                                pyautogui.press('tab')
                                                pyautogui.write(str(np_df[z][8]))
                                                pyautogui.press('tab')
                                                pyautogui.write(str(np_df[z][9]))
                                                pyautogui.press('tab')
                                                pyautogui.write(str(np_df[z][4]))
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                print(int(np_df[z][5]))
                                                for i in range(int(np_df[z][5])):
                                                        pyautogui.press('down')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.write(str(np_df[z][6]))
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Next
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Agreement
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Submit Form
                                                #pyautogui.press('tab')
                                                #pyautogui.press('tab')
                                                #pyautogui.press('space')
                                                #pyautogui.keyDown('ctrl')
                                                #pyautogui.press('w')
                                                #pyautogui.keyUp('ctrl')
                                                
                                        if str(np_df[z][1])=="2":
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Information
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.write(str(np_df[z][2]))
                                                pyautogui.press('tab')
                                                pyautogui.write(str(np_df[z][3]))
                                                pyautogui.press('tab')
                                                pyautogui.write(str(np_df[z][4]))
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                print(int(np_df[z][5]))
                                                for i in range(int(np_df[z][5])):
                                                        pyautogui.press('down')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.write(str(np_df[z][6]))
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Next
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Agreement
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                                #Submit Form
                                                #pyautogui.press('tab')
                                                #pyautogui.press('tab')
                                                #pyautogui.press('space')
                                                #pyautogui.keyDown('ctrl')
                                                #pyautogui.press('w')
                                                #pyautogui.keyUp('ctrl')
                                        
                                    urlpayload=""
                                    flagtimer=0
                                    self.activatebutton.setText("Auto Deactivated")
             except:
                      print("Data Error")
             
             QtCore.QCoreApplication.processEvents()



def main():

    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
