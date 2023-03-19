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
import webbrowser
import pyautogui
class Main(QtWidgets.QMainWindow):

        def __init__(self):
            super().__init__()

            self.initUI()
        def initUI(self):
             global emailflag,url,pagehistory,flagtimer,url,url2
             flagtimer=0
             emailflag=0
             pagehistory="?&pageHistory=0,1,2,3,4,5,6"
             #url1="https://docs.google.com/forms/d/e/1FAIpQLSfW1xvBnEAl_C7pFCUV1Pq3egnUey4Q1jqY43N5ppkHPENoaw"
             #url1="https://docs.google.com/forms/d/e/1FAIpQLSeG6MLgdIsFkVuLU4I97CF74_NHVNT3ArC-HhqekkfICFqORg"
             #url1="https://docs.google.com/forms/d/e/1FAIpQLSdz9CPfXp0rHlvRjeAiNYAqbpOeBPhlSFdldTTpu2PCP6BSYQ"
             url1="https://docs.google.com/forms/d/e/1FAIpQLSek3p5Ae6RNJ6Rmc8atuVRtTEduMCQpvw8AnDAaQQcyqqSE9w"
             url=url1+"/formResponse"
             url2=url1+"/viewform?usp=pp_url"
             self.timer = QtCore.QTimer(self)
             self.timer.timeout.connect(self.Loop)
             self.timer.start()
             self.scanbutton = QtWidgets.QPushButton("Scan Form",self)
             self.scanbutton.clicked.connect(self.scanform)
             self.scanbutton.move(50,150)
            
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
             self.emailtoggle = QtWidgets.QComboBox(self)
             self.emailtoggle.addItems(["Disable","Enable"])
             self.emailtoggle.currentIndexChanged.connect(self.emailselect)
             self.emailtoggle.move(90,250)
             self.emailtoggle.resize(80,30)
             self.emailtoggle.setCurrentIndex(0)
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
        def emailselect(self,ex):
            global emailflag
            if ex==0:
                emailflag=0
            elif ex==1:
                emailflag=1
            print(emailflag)     
        def scanform(self):
            global emailflag,url
            file = open("questionlist.txt","w")
            file.close()

            html_data = requests.get(url).text
            data=re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*);', html_data, flags=re.S).group(0)
            data=data.strip("FB_PUBLIC_LOAD_DATA_ = ")
            data=data[:-1]

            with open('json_data.json', 'w') as outfile:
                outfile.write(data)
            data = json.loads(data)
            headdf=[]
            
            if emailflag==1:
                headdf.append("Email Address")
            for i in range(len(data[1][1])):
                    print("i = "+str(i))
                    #Question Description
                    questiondesc=str(data[1][1][i][1])
                    print("Title: "+questiondesc)
                    
                    #Question Type, Answer List and Entry ID
                    questiontype=data[1][1][i][3]
                    switchquest=0
                    if questiontype==4:
                        print("\nType: Check Boxes Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        answerlen=len(data[1][1][i][4][0][1])
                        print("Answer List:")
                        f = open('questionlist.txt', 'a')
                        f.write("Title: "+questiondesc+"\nType: Check Boxes Field\n"+"Entry ID: "+str(entryid)+"\nAnswer List:\n")
                        f.close()
                        for j in range(answerlen): 
                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                             f = open('questionlist.txt', 'a')
                             f.write(">>"+str(data[1][1][i][4][0][1][j][0])+"\n")
                        f.write("\n")   
                        f.close()
                        headdf.append(questiondesc)
                    elif questiontype==0:
                        print("Type: Short Answer Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        f = open('questionlist.txt', 'a')
                        f.write("Title: "+questiondesc+"\nType: Short Answer Field\nEntry ID: "+str(entryid)+"\n\n")  
                        f.close()
                        headdf.append(questiondesc)
                    elif questiontype==3:
                        print("Type: Drop Down Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        answerlen=len(data[1][1][i][4][0][1])
                        print("Answer List:")
                            
                        f = open('questionlist.txt', 'a')
                        f.write("Title: "+questiondesc+"\nType: Drop Down Field\n"+"Entry ID: "+str(entryid)+"\nAnswer List:\n")
                        f.close()
                        
                        for j in range(answerlen): 
                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                             f = open('questionlist.txt', 'a')
                             f.write(">>"+str(data[1][1][i][4][0][1][j][0])+"\n")
                        f.write("\n")   
                        f.close()
                        headdf.append(questiondesc)
                    elif questiontype==2:
                        print("Type: Multiple Choice Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        answerlen=len(data[1][1][i][4][0][1])
                        print("Answer List:")
                        
                        f = open('questionlist.txt', 'a')
                        f.write("Title: "+questiondesc+"\nType: Multiple Choice Field\n"+"Entry ID: "+str(entryid)+"\nAnswer List:\n")
                        f.close()
                        for j in range(answerlen): 
                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                             f = open('questionlist.txt', 'a')
                             f.write(">>"+str(data[1][1][i][4][0][1][j][0])+"\n")
                        f.write("\n")   
                        f.close()
                        headdf.append(questiondesc)
                    else:
                        print("Type: ---")
                        print("Entry ID: ---")
                    print("\n")
            pathsave="outputdata.csv"
           
            df = pd.DataFrame(columns=headdf)
            df.to_csv(pathsave,  index = False)
        def sendform(self):
            global emailflag,url,pagehistory,url2
            
                
            html_data = requests.get(url).text
            data=re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*);', html_data, flags=re.S).group(0)
            data=data.strip("FB_PUBLIC_LOAD_DATA_ = ")
            data=data[:-1]

            with open('json_data.json', 'w') as outfile:
                outfile.write(data)
            data = json.loads(data)
            print(data)
            df=pd.read_csv("input.csv",header=0)
            np_df = df.values
            nphead=pd.read_csv('input.csv', index_col=0, nrows=0).columns.tolist()
            #for i in range(nphead):
                #print(np_head)

    
        
            for z in range(len(np_df)):
                payload=""
                
                if emailflag==1:
                    payload="&emailAddress="+str(np_df[z][0])

                for i in range(len(data[1][1])):
                    print("i = "+str(i))
                    #Question Description
                    questiondesc=data[1][1][i][1]
                    print("Title: "+questiondesc)

                    #Question Type, Answer List and Entry ID
                    questiontype=data[1][1][i][3]
                    switchquest=0
                    if questiontype==4:
                        print("Type: Check Boxes Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        answerlen=len(data[1][1][i][4][0][1])
                        print("Answer List:")
                        for j in range(answerlen): 
                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                        index = nphead.index(indexfind[0])
                        ansload=np_df[z][index+1]
                        payload=payload+"&entry."+str(entryid)+"="+str(ansload)      
                        
                    elif questiontype==0:
                        print("Type: Short Answer Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                        index = nphead.index(indexfind[0])
                        ansload=np_df[z][index+1]
                        print(np_df[z][index+1])
                        payload=payload+"&entry."+str(entryid)+"="+str(ansload) 
                       
                        
                    elif questiontype==3:
                        print("Type: Drop Down Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        answerlen=len(data[1][1][i][4][0][1])
                        print("Answer List:")
                        for j in range(answerlen): 
                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                        index = nphead.index(indexfind[0])
                        ansload=np_df[z][index+1]
                        payload=payload+"&entry."+str(entryid)+"="+str(ansload) 
                    elif questiontype==2:
                        print("Type: Multiple Choice Field")
                        entryid=data[1][1][i][4][0][0]
                        print("Entry ID: "+str(entryid))
                        answerlen=len(data[1][1][i][4][0][1])
                        print("Answer List:")
                        for j in range(answerlen): 
                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                        index = nphead.index(indexfind[0])
                        ansload=np_df[z][index+1]
                        payload=payload+"&entry."+str(entryid)+"="+str(ansload)              
                    
                    else:
                        print("Type: ---")
                        print("Entry ID: ---")
                    #print(payload)
                    print("\n")
                
                urlpayload=url2+payload
                webbrowser.register('chrome',
                        None,
                        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
                webbrowser.get('chrome').open(urlpayload)
                time.sleep(0.5)
                pyautogui.click(500, 500)
               
                flag=0
                while flag==0:
                    pyautogui.scroll(-20000)
                    try:
                        x, y = pyautogui.locateCenterOnScreen('next.png', grayscale=True, confidence=0.8)
                        pyautogui.click(x, y)
                    except:
                        print("Next not found")
                    time.sleep(0.5)
                    #pyautogui.moveTo(0, 0)
                    try:
                            
                            x, y = pyautogui.locateCenterOnScreen('submit.png', grayscale=True, confidence=0.8)
                            pyautogui.click(x, y)
                            flag=1
                    except:
                            print("Submit not found")
                time.sleep(0.1)     
                #pyautogui.keyDown('ctrl')
                #pyautogui.press('w')
                #pyautogui.keyUp('ctrl')
                urlpayload=""
        def Loop(self):
             global emailflag,url,pagehistory,flagtimer,url2
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
                            html_data = requests.get(url).text
                            data=re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*);', html_data, flags=re.S).group(0)
                            data=data.strip("FB_PUBLIC_LOAD_DATA_ = ")
                            data=data[:-1]

                            with open('json_data.json', 'w') as outfile:
                                outfile.write(data)
                            data = json.loads(data)
                            print(data)
                            df=pd.read_csv("input.csv",header=0)
                            np_df = df.values
                            nphead=pd.read_csv('input.csv', index_col=0, nrows=0).columns.tolist()
                            #for i in range(nphead):
                                #print(np_head)

                    
                        
                            for z in range(len(np_df)):
                                payload=""
                                
                                if emailflag==1:
                                    payload="&emailAddress="+str(np_df[z][0])

                                for i in range(len(data[1][1])):
                                    print("i = "+str(i))
                                    #Question Description
                                    questiondesc=data[1][1][i][1]
                                    print("Title: "+questiondesc)

                                    #Question Type, Answer List and Entry ID
                                    questiontype=data[1][1][i][3]
                                    switchquest=0
                                    if questiontype==4:
                                        print("Type: Check Boxes Field")
                                        entryid=data[1][1][i][4][0][0]
                                        print("Entry ID: "+str(entryid))
                                        answerlen=len(data[1][1][i][4][0][1])
                                        print("Answer List:")
                                        for j in range(answerlen): 
                                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                                        index = nphead.index(indexfind[0])
                                        ansload=np_df[z][index+1]
                                        payload=payload+"&entry."+str(entryid)+"="+str(ansload)      
                                        
                                    elif questiontype==0:
                                        print("Type: Short Answer Field")
                                        entryid=data[1][1][i][4][0][0]
                                        print("Entry ID: "+str(entryid))
                                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                                        index = nphead.index(indexfind[0])
                                        ansload=np_df[z][index+1]
                                        print(np_df[z][index+1])
                                        payload=payload+"&entry."+str(entryid)+"="+str(ansload) 
                                       
                                        
                                    elif questiontype==3:
                                        print("Type: Drop Down Field")
                                        entryid=data[1][1][i][4][0][0]
                                        print("Entry ID: "+str(entryid))
                                        answerlen=len(data[1][1][i][4][0][1])
                                        print("Answer List:")
                                        for j in range(answerlen): 
                                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                                        index = nphead.index(indexfind[0])
                                        ansload=np_df[z][index+1]
                                        payload=payload+"&entry."+str(entryid)+"="+str(ansload) 
                                    elif questiontype==2:
                                        print("Type: Multiple Choice Field")
                                        entryid=data[1][1][i][4][0][0]
                                        print("Entry ID: "+str(entryid))
                                        answerlen=len(data[1][1][i][4][0][1])
                                        print("Answer List:")
                                        for j in range(answerlen): 
                                             print(">>"+str(data[1][1][i][4][0][1][j][0]))
                                        indexfind=difflib.get_close_matches(questiondesc,nphead,n=1)
                                        index = nphead.index(indexfind[0])
                                        ansload=np_df[z][index+1]
                                        payload=payload+"&entry."+str(entryid)+"="+str(ansload)              
                                    
                                    else:
                                        print("Type: ---")
                                        print("Entry ID: ---")
                                    #print(payload)
                                    print("\n")
                                
                                urlpayload=url2+payload
                                webbrowser.register('chrome',
                                        None,
                                        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
                                webbrowser.get('chrome').open(urlpayload)
                                time.sleep(0.5)
                                pyautogui.click(500, 500)
                               
                                flag=0
                                while flag==0:
                                    pyautogui.scroll(-20000)
                                    try:
                                        x, y = pyautogui.locateCenterOnScreen('next.png', grayscale=True, confidence=0.8)
                                        pyautogui.click(x, y)
                                    except:
                                        print("Next not found")
                                    time.sleep(0.5)
                                    #pyautogui.moveTo(0, 0)
                                    try:
                                            
                                            x, y = pyautogui.locateCenterOnScreen('submit.png', grayscale=True, confidence=0.8)
                                            pyautogui.click(x, y)
                                            flag=1
                                    except:
                                            print("Submit not found")
                                time.sleep(0.1)     
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
