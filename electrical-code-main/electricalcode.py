from PyQt4 import QtGui, QtCore
import sys
import time
import numpy as np
import pandas as pd
import os
import math
class Main(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.framebg = QtGui.QFrame(self)
        self.framebg.setFrameStyle(QtGui.QFrame.NoFrame);
        self.framebg.resize(600,400)
        self.framebg.move(0,0)
        self.framebg.setStyleSheet(" border-image: url(background.png);");
        self.setWindowTitle("ELECTRICAL CODE SIMULATOR")
        centralwidget = QtGui.QWidget(self)
        self.setGeometry(500,500,500,400)
        self.infodisp=QtGui.QLabel("	    SELECT TYPE OF SYSTEM	",self)
        self.infodisp.move(10,80)
        self.infodisp.setStyleSheet('color: black')
        self.infodisp.resize(500,50)
        font = QtGui.QFont("Times", 14)
        self.infodisp.setFont(font)
        self.residential = QtGui.QPushButton("Single Phase",self)
        self.residential.clicked.connect(self.residentialfunc)
        self.commercial = QtGui.QPushButton("Three Phase",self)
        self.commercial.clicked.connect(self.commercialfunc)
        self.residential.move(200,150)
        self.commercial.move(200,210)
        self.residentialpage = residentialgui(self)
     
        self.commercialpage = commercialgui(self)
  
    def residentialfunc(self):
         
         self.residentialpage.exec_()
    def commercialfunc(self):
        self.commercialpage.exec_()
######################################################Residential#############################################################   
class residentialgui(QtGui.QDialog):
    def __init__(self,parent=None):
        super(residentialgui, self).__init__(parent)
        self.framebg = QtGui.QFrame(self)
        self.framebg.setFrameStyle(QtGui.QFrame.NoFrame);
        self.framebg.resize(720,760)
        self.framebg.move(0,0)
        self.framebg.setStyleSheet(" border-image: url(background.png);");
        self.setWindowTitle("SINGLE PHASE")
        global ampflag,specflag,airconflag,wireflag,conduitflag
        wireflag=0
        conduitflag=0
        airconflag=0
        specflag=0
        ampflag=0
        self.setGeometry(20,20,720,760)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        font12 = QtGui.QFont("Helvetica", 12)
        font10 = QtGui.QFont("Helvetica", 10)
        self.l1=QtGui.QLabel("Single Phase Unit Design",self)
        self.l1.move(7,5)
        self.l1.setFont(font12)
        self.l1.setStyleSheet('color: red')
        self.l2=QtGui.QLabel("Panel Board Name:",self)
        self.l2.move(20,75)
        self.l2.setFont(font10)
        self.l3=QtGui.QLineEdit(self)
        self.l3.move(170,75)
        self.l3.resize(150,20)
        self.l4=QtGui.QLabel("	Demand Factor:",self)
        self.l4.move(300,75)
        self.l4.setFont(font10)
        self.l5=QtGui.QLineEdit(self)
        self.l5.move(485,75)
        self.l5.resize(50,20)
        self.l6=QtGui.QLabel("Load Specifications",self)
        self.l6.move(10,95)
        self.l6.setFont(font10)
        self.l6.setStyleSheet('color: red')
        self.l7=QtGui.QLabel("Type:",self)
        self.l7.move(20,130)
        self.l7.setFont(font10)
        self.typeload = QtGui.QComboBox(self)
        self.typeload.addItems(["","General Lighting Loads","Appliance Loads","Cooking Loads","Laundry Loads","Motor Loads","Other Loads"])
        self.typeload.currentIndexChanged.connect(self.typeselect)
        self.typeload.move(65,130)
        self.typeload.resize(140,20)
        self.l8=QtGui.QLabel("Load:",self)
        self.l8.move(220,130)
        self.l8.setFont(font10)
        self.specload = QtGui.QComboBox(self)
        self.specload.addItems([])
        self.specload.currentIndexChanged.connect(self.specselect)
        self.specload.move(270,130)
        self.specload.resize(180,20)
        self.l9=QtGui.QLabel("Load Name:",self)
        self.l9.move(480,130)
        self.l9.setFont(font10)
        self.l10=QtGui.QLineEdit(self)
        self.l10.move(580,130)
        self.l10.resize(100,20)
        self.l11=QtGui.QLabel("Rating:",self)
        self.l11.move(20,170)
        self.l11.setFont(font10)
        self.l12=QtGui.QLineEdit(self)
        self.l12.move(75,170)
        self.l12.resize(70,20)
        self.unitload = QtGui.QComboBox(self)
        self.unitload.addItems([])
        self.unitload.currentIndexChanged.connect(self.loadselect)
        self.unitload.move(135,170)
        self.unitload.resize(40,20)
        self.l13=QtGui.QLabel("Quantity:",self)
        self.l13.move(195,170)
        self.l13.setFont(font10)
        self.l14=QtGui.QLineEdit(self)
        self.l14.move(270,170)
        self.l14.resize(40,20)
        self.n1=QtGui.QLabel("Project Name:",self)
        self.n1.move(20,45)
        self.n1.setFont(font10)
        self.n2=QtGui.QLineEdit(self)
        self.n2.move(170,45)
        self.n2.resize(100,20)
        self.n3=QtGui.QLabel("Unit Type:",self)
        self.n3.move(355,45)
        self.n3.setFont(font10)
        self.n4=QtGui.QLabel("Area:",self)
        self.n4.move(550,75)
        self.n4.setFont(font10)
        self.n5=QtGui.QLineEdit(self)
        self.n5.move(600,75)
        self.n5.resize(50,20)
        self.typeunit = QtGui.QComboBox(self)
        self.typeunit.addItems(["","Armories and Auditoriums","Banks","Babershops and Beauty Parlors","Churches","Clubs","Courtrooms","Dwelling Units","Garage","Hospitals","Hotels and Motels","Lodge Rooms",
                                "Office Buildings","Restaurants","Schools","Stores","Assembly Halls","Corridors and Halls","Storage Spaces"])
        self.typeunit.currentIndexChanged.connect(self.unitselect)
        self.typeunit.move(450,45)
        self.typeunit.resize(170,20)
        self.addinput = QtGui.QPushButton("Add",self)
        self.addinput.clicked.connect(self.adddata)
        self.addinput.move(10,220)
        self.deleteinput = QtGui.QPushButton("Delete",self)
        self.deleteinput.clicked.connect(self.deletedata)
        self.deleteinput.move(90,220)
        self.loadinput = QtGui.QPushButton("Load",self)
        self.loadinput.clicked.connect(self.loaddata)
        self.loadinput.move(180,220)
        
        self.l17=QtGui.QLabel("Type of Wire",self)
        self.l17.move(350,170)
        self.l17.setFont(font10)
        self.l18=QtGui.QLabel("Type of Conduit",self)
        self.l18.move(500,170)
        self.l18.setFont(font10)
        self.l19=QtGui.QLabel(self)
        self.l19.move(10,735)
        self.l19.resize(500,30)
        
        self.wiretype = QtGui.QComboBox(self)
        self.wiretype.addItems(["","TW - Copper","UF - Copper","RHW - Copper","THW - Copper","THWN - Copper","RHH - Copper","THHN - Copper","THHW - Copper","XHH - Copper","XHHW - Copper","TW - Aluminum","UF - Aluminum","RHW - Aluminum","THW - Aluminum","THWN - Aluminum","RHH - Aluminum","THHN - Aluminum","THHW - Aluminum","XHH - Aluminum","XHHW - Aluminum"])
        self.wiretype.currentIndexChanged.connect(self.wireselect)
        self.wiretype.move(350,200)
        self.wiretype.resize(120,20)
        self.conduittype = QtGui.QComboBox(self)
        self.conduittype.addItems(["","EMT","ENMT","FMC","IMC","Liquidtight FNMC","Liquidtight FMC","RMC","Rigid PVC"])
        self.conduittype.currentIndexChanged.connect(self.conduitselect)
        self.conduittype.move(500,200)
        self.conduittype.resize(120,20)
        self.compinput = QtGui.QPushButton("Generate",self)
        self.compinput.clicked.connect(self.computedata)
        self.compinput.move(580,700)
       
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.move(50,250)
        self.table.setHorizontalHeaderLabels([' 		 Ckt. No.  ','  Qty  ','		Load Description		', '		Rating		'])#Space
        self.table.resize(600,400)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        self.outputpanelresidential = paneloutputresidential(self)
    def unitselect(self,kx):
        global areaflag
        if kx==0:
            areaflag=0
        elif kx==1:
            areaflag=1
        elif kx==2:
            areaflag=2
        elif kx==3:
            areaflag=3
        elif kx==4:
            areaflag=4
        elif kx==5:
            areaflag=5
        elif kx==6:
            areaflag=6
        elif kx==7:
            areaflag=7
        elif kx==8:
            areaflag=8
        elif kx==9:
            areaflag=9
        elif kx==10:
            areaflag=10
        elif kx==11:
            areaflag=11
        elif kx==12:
            areaflag=12
        elif kx==13:
            areaflag=13
        elif kx==13:
            areaflag=13
        elif kx==14:
            areaflag=14
        elif kx==15:
            areaflag=15
        elif kx==16:
            areaflag=16
        elif kx==17:
            areaflag=17
        elif kx==18:
            areaflag=18    
    def computedata(self,ax):
         global wireflag,groundtype,directory,areaflag
         unitarea=str(self.n5.text())
         directory=str(self.n2.text())
         panelboard=str(self.l3.text())
         try:
             demandfactor=self.l5.text()
             if demandfactor=="":
                 self.l19.setText("Please input demand factor.")
             else:
                 demandfactor=float(self.l5.text())
         except:
             self.l19.setText("Invalid input for demand factor.")
         pathtarget=directory+"/"+panelboard+".csv"
         try:
             df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize'],skiprows=1)
             np_df = df.as_matrix()
         except:
             self.l19.setText("Project doesn't exist.")
         if wireflag==0:
                 self.l19.setText("Please select type of wire.")
         elif conduitflag==0:
             self.l19.setText("Please select type of conduit.")
         if wireflag!=0 and conduitflag!=0:
             It=0
             itx=0
             for i in xrange(len(np_df)):
                 It=It+np_df[itx][9]
                 itx=itx+1
             try:    
                 dfmotor=df[df.Motor != 0]
                 dfmotor = dfmotor.sort_values(['Ampere'], ascending=[False])
                 print dfmotor
                 np_dfmotor=dfmotor.as_matrix()
                 highestmotor=np_dfmotor[0][10]
                 
                 Icb=It*demandfactor+1.5*highestmotor
                 Iwire=It*demandfactor+0.25*highestmotor
                 print "Highest Rated Motor(A): "+str(highestmotor)
             except:
                 Icb=It*demandfactor
                 Iwire=It*demandfactor
             
             print "It: "+str(It)
             print "Icb: "+str(Icb)
             print "Iwire: "+str(Iwire)
             atdata="ATParse.csv"
             dfat=pd.read_csv(atdata,names=['AT','Low','High'],skiprows=1)
             np_dfat = dfat.as_matrix()
             
             atcnt=0
             for i in xrange(len(np_dfat)):
                   
                   if Icb>np_dfat[atcnt][1] and Icb<=np_dfat[atcnt][2]:
                         amperetrip=np_dfat[atcnt][0]
                         print "AT: "+str(amperetrip)
                   atcnt=atcnt+1
                   
             try:
                 self.l19.setText("")
                 afdata="AFParse.csv"
                 dfaf=pd.read_csv(afdata,names=['AF','AT'],skiprows=1)
                 afout=np.where(dfaf["AT"] == amperetrip)
                 np_dfaf = dfaf.as_matrix()
                 
                 afout=afout[0][0]
                 afout=np_dfaf[afout][0]
                 print "AF: "+str(afout)
             except:
                 afout="Out of Range"
                 print "Adjust AF Table: Out of Range"
                 self.l19.setText("Adjust AF Table: Out of Range")
             wiredata="MainWireParse.csv"
             dfwire=pd.read_csv(wiredata,names=['Size','A','B','C','D','E','F'],skiprows=1)
             np_dfwire = dfwire.as_matrix()
             wireat=Iwire
             if wireflag==1:
                 
                 if wireat<=405:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][1] and wireat<=np_dfwire[wirecnt+1][1]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>405 and wireat<=445:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>445:
                     wireatout=wireat
                     while wireatout>445:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][1] and wireatout<=np_dfwire[wirecnt+1][1]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==2:
                 
                 if wireat<=485:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][2] and wireat<=np_dfwire[wirecnt+1][2]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>485 and wireat<=540:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>540:
                     wireatout=wireat
                     while wireatout>540:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][2] and wireatout<=np_dfwire[wirecnt+1][2]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==3:
                 
                 if wireat<=515:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][3] and wireat<=np_dfwire[wirecnt+1][3]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>515 and wireat<=580:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>580:
                     wireatout=wireat
                     while wireatout>580:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][3] and wireatout<=np_dfwire[wirecnt+1][3]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==4:
                 
                 if wireat<=335:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][4] and wireat<=np_dfwire[wirecnt+1][4]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>335 and wireat<=370:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>370:
                     wireatout=wireat
                     while wireatout>370:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][4] and wireatout<=np_dfwire[wirecnt+1][4]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==5:
                 
                 if wireat<=405:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][5] and wireat<=np_dfwire[wirecnt+1][5]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>405 and wireat<=440:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>440:
                     wireatout=wireat
                     while wireatout>440:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][5] and wireatout<=np_dfwire[wirecnt+1][5]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==6:
                 
                 if wireat<=460:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][6] and wireat<=np_dfwire[wirecnt+1][6]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>460 and wireat<=495:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>495:
                     wireatout=wireat
                     while wireatout>495:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][6] and wireatout<=np_dfwire[wirecnt+1][6]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             grounddata="groundwire.csv"
             dfground=pd.read_csv(grounddata,names=['AT','Copper','Aluminum'],skiprows=1)
             

             if groundtype==0:
                 np_dfground = dfground.as_matrix()
                 groundcnt=0
                 groundat=Iwire
                 for i in xrange(len(np_dfground)-1):
                     
                        if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                         
                             groundsize=np_dfground[groundcnt+1][1]
                             print "Ground Wire: "+str(groundsize)
                         
                        groundcnt=groundcnt+1
             elif groundtype==1:
                 np_dfground = dfground.as_matrix()
                 groundcnt=0
                 groundat=amperetrip
                 for i in xrange(len(np_dfground)-1):
                     
                        if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                         
                             groundsize=np_dfground[groundcnt+1][2]
                             print "Ground Wire: "+str(groundsize)
                         
                        groundcnt=groundcnt+1
             totalwire=3
             try:
                 self.l19.setText("")
                 if conduitflag==1:
                    conduitrange=10
                    if emtflag==1:
                        pathwire="conduit_csv/emt_A.csv"
                    elif emtflag==2:
                        pathwire="conduit_csv/emt_B.csv"
                    elif emtflag==3:
                        pathwire="conduit_csv/emt_C.csv"
                    elif emtflag==4:
                        pathwire="conduit_csv/emt_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                     
                 elif conduitflag==2:
                    conduitrange=6
                    if entflag==1:
                        pathwire="conduit_csv/ent_A.csv"
                    elif entflag==2:
                        pathwire="conduit_csv/ent_B.csv"
                    elif entflag==3:
                        pathwire="conduit_csv/ent_C.csv"
                    elif entflag==4:
                        pathwire="conduit_csv/ent_D.csv"
                    elif entflag==5:
                        pathwire="conduit_csv/ent_E.csv"
                            
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F'],skiprows=1)
                    
                 elif conduitflag==3:
                    conduitrange=10
                    if fmcflag==1:
                        pathwire="conduit_csv/fmc_A.csv"
                    elif fmcflag==2:
                        pathwire="conduit_csv/fmc_B.csv"
                    elif fmcflag==3:
                        pathwire="conduit_csv/fmc_C.csv"
                    elif fmcflag==4:
                        pathwire="conduit_csv/fmc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)  
                 elif conduitflag==4:
                    conduitrange=10
                    if imcflag==1:
                        pathwire="conduit_csv/imc_A.csv"
                    elif imcflag==2:
                        pathwire="conduit_csv/imc_B.csv"
                    elif imcflag==3:
                        pathwire="conduit_csv/imc_C.csv"
                    elif imcflag==4:
                        pathwire="conduit_csv/imc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                 elif conduitflag==5:
                    conduitrange=7
                    if lfnmcflag==1:
                        pathwire="conduit_csv/lfnmc_A.csv"
                    elif lfnmcflag==2:
                        pathwire="conduit_csv/lfnmc_B.csv"
                    elif lfnmcflag==3:
                        pathwire="conduit_csv/lfnmc_C.csv"
                    elif lfnmcflag==4:
                        pathwire="conduit_csv/lfnmc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G'],skiprows=1)
                 elif conduitflag==6:
                    conduitrange=10
                    if lfmcflag==1:
                        pathwire="conduit_csv/lfmc_A.csv"
                    elif lfmcflag==2:
                        pathwire="conduit_csv/lfmc_B.csv"
                    elif lfmcflag==3:
                        pathwire="conduit_csv/lfmc_C.csv"
                    elif lfmcflag==4:
                        pathwire="conduit_csv/lfmc_D.csv"
                    elif lfmcflag==5:
                        pathwire="conduit_csv/lfmc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                 elif conduitflag==7:
                    conduitrange=12
                    if rmcflag==1:
                        pathwire="conduit_csv/rmc_A.csv"
                    elif rmcflag==2:
                        pathwire="conduit_csv/rmc_B.csv"
                    elif rmcflag==3:
                        pathwire="conduit_csv/rmc_C.csv"
                    elif rmcflag==4:
                        pathwire="conduit_csv/rmc_D.csv"
                    elif rmcflag==5:
                        pathwire="conduit_csv/rmc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                 elif conduitflag==8:
                    conduitrange=12
                    if rpvcflag==1:
                        pathwire="conduit_csv/rpvc_A.csv"
                    elif rpvcflag==2:
                        pathwire="conduit_csv/rpvc_B.csv"
                    elif rpvcflag==3:
                        pathwire="conduit_csv/rpvc_C.csv"
                    elif rpvcflag==4:
                        pathwire="conduit_csv/rpvc_D.csv"
                    elif rpvcflag==5:
                        pathwire="conduit_csv/rpvc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                 
                 print pathwire
                 
                 wireid=np.where(dfw["Output"] == wiresize)
                 np_dfw = dfw.as_matrix()
                 wireid=wireid[0][0]
             except:
                 self.l19.setText("Wire Size Out of Range on Selected Type of Wire and Conduit.")
         
             conduitcnt=1
             for i in xrange(10): 
                    try:
                        
                        
                        if np_dfw[wireid][conduitcnt]!=np_dfw[wireid][conduitcnt+1] and totalwire>np_dfw[wireid][conduitcnt]:
                            if totalwire>np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                 
                                 conduitsize=np_dfw[0][conduitcnt+1]
                                 
                        elif totalwire<=np_dfw[wireid][1]:
                            conduitsize=np_dfw[0][1]
                            
                        else:
                             if totalwire>=np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                 
                                 conduitsize=np_dfw[0][conduitcnt+1]
                                 
                    except:
                         print ""
                    conduitcnt=conduitcnt+1
             print "Conduit Size: "+str(conduitsize) 
             pathsave="outputdata.csv"
             columns = ['Panel','AT','AF', 'Sets','WireSize','GroundingWire','Conduit']
             df = pd.DataFrame(columns=columns)
             print pathtarget
             df = df.append({'Panel':pathtarget,'AT':amperetrip,'AF':afout, 'Sets':1,'WireSize':wiresize,'GroundingWire':groundsize,'Conduit':conduitsize}, ignore_index=True)
             df.to_csv(pathsave,  index = False)
             pathres="areaflag.csv"
             columns = ['Areaflag','Area']
             df = pd.DataFrame(columns=columns)
             df = df.append({'Areaflag':areaflag,'Area':unitarea}, ignore_index=True)
             df.to_csv(pathres,  index = False)
             self.accept()
             self.close()
             self.outputpanelresidential.exec_()

    def adddata(self,cx):
         #try:  
             global airconflag,ampflag,unitflag,specflag,ampere,appliancesflag,wireflag,groundtype,emtflag,entflag,fmcflag,imcflag,lfnmcflag,lfmcflag,rmcflag,rpvcflag,conduitflag,directory,spareflag,spaceflag,waterheaterflag
             directory=str(self.n2.text())
             if directory!="":
                 if not os.path.exists(directory):
                     os.makedirs(directory)
             self.l19.setText("")
             panelboard=str(self.l3.text())
              
             pathtarget=directory+"/"+panelboard+".csv"
             loadname=str(self.l10.text())
             voltage=230
             quantity=str(self.l14.text())
             wireset=1
             wirenumber=3
             totalwire=wireset*wirenumber
             rating=str(self.l12.text())
             if directory=="":
                 self.l19.setText("Indicate project name.")
             elif panelboard=="":
                 self.l19.setText("Indicate panel board.")
             elif ampflag==0:
                 self.l19.setText("Please select type of load.")
             elif specflag==0 and ampflag!=1:
                 self.l19.setText("Please select specific load.")
             elif loadname=="":
                 self.l19.setText("Indicate load name.")
             elif rating=="":
                 self.l19.setText("Input rating.")
                
             elif quantity=="":
                 self.l19.setText("Input quantity.")
             
             if rating!="":
                 try:
                     rating=float(self.l12.text())
                 except:
                     self.l19.setText("Invalid input for rating.")     
             if quantity!="":
                 try:    
                     quantity=int(self.l14.text())
                 except:
                     self.l19.setText("Invalid input for quantity.")
             if wireflag==0:
                 self.l19.setText("Please select type of wire.")
             elif conduitflag==0:
                 self.l19.setText("Please select type of conduit.")
             if wireflag!=0 and conduitflag!=0:
                 if ampflag==1:
                      typeflag=0
                      lightingflag=1
                      if specflag==1:
                          ampere=0
                      else:
                         if unitflag==1:
                             rating=float(self.l12.text())
                         elif unitflag==2:
                             rating=float(self.l12.text())*1000
                         quantity=float(self.l14.text())
                         ampere=(rating*quantity)/230
                 elif ampflag==2:
                     typeflag=0
                     lightingflag=0
                     if unitflag==1:
                         rating=float(self.l12.text())
                     elif unitflag==2:
                         rating=float(self.l12.text())*1000
                     quantity=float(self.l14.text())
                     pathid="cookingappliance.csv"
                     df=pd.read_csv(pathid,names=['Qty','A','B','C'],skiprows=1)
                     if ((df['Qty'] == quantity)).any()==True:
                         cookid=np.where(df["Qty"] == quantity)
                         np_df = df.as_matrix()
                         numid=cookid[0][0]
                         A=float(np_df[numid][1])/100
                         B=float(np_df[numid][2])/100
                         C=float(np_df[numid][3])/100
                     
                         if rating<3500 and quantity<=60:
                             ampere=((rating*quantity)/230)*A
                         elif rating>=3500 and rating<=8750 and quantity<=60:
                             ampere=((rating*quantity)/230)*B
                         elif rating>8750 and quantity<26:
                             ampere=((rating*quantity)/230)*C
                         elif rating>8750 and quantity>=26 and quantity<41:
                             ampere=((1000*quantity+15000)/230)
                         elif rating>8750 and quantity<61 and quantity>=41:
                             ampere=((750*quantity+25000)/230)
                     else:
                         if rating<3500 and quantity>=61:
                             ampere=((rating*quantity)/230)*0.3
                         elif rating>=3500 and rating<=8750 and quantity>=61:
                             ampere=((rating*quantity)/230)*0.16
                         elif rating>8750 and quantity>=61:
                             ampere=((750*quantity+25000)/230)
                                 
                         
                 elif ampflag==3:
                     typeflag=1
                     lightingflag=0
                     
                     pathid="motorload.csv"
                     df=pd.read_csv(pathid,names=['Motor','Ampere','VA'],skiprows=1)
                     ratingmotor=self.l12.text()
                     if unitflag==1:
                         if ((df['Motor'] == ratingmotor)).any()==True:
                             
                             motorid=np.where(df["Motor"] == ratingmotor)
                             np_df = df.as_matrix()
                             numid=motorid[0][0]
                             ampere=float(np_df[numid][1])
                             rating=float(np_df[numid][2])
                         else:
                             ampere="Out of Range"
                     elif unitflag==2:
                         rating=float(self.l12.text())
                         #quantity=float(self.l14.text())
                         ampere=(rating)/230
                         
                         
                 elif ampflag==4:
                      typeflag=0
                      lightingflag=0
                      if appliancesflag==1:
                          rating=180
                          quantity=float(self.l14.text())
                          ampere=(rating*quantity)/230

                      elif appliancesflag==0:
                         if unitflag==1:
                             rating=float(self.l12.text())
                         elif unitflag==2:
                             rating=float(self.l12.text())*1000
                         quantity=float(self.l14.text())
                         ampere=(rating*quantity)/230

                 elif ampflag==5:
                          typeflag=0
                          lightingflag=0
                          if laundryflag==1:
                             if unitflag==1:
                                 rating=float(self.l12.text())
                             elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                             ampere=(rating*quantity)/230
                          elif laundryflag==2:
                              if unitflag==1:
                                 rating=float(self.l12.text())
                              elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                              if quantity>=1 and quantity<=4:
                                      ampere=((rating*quantity)/230)*1
                              elif quantity==5:
                                  ampere=((rating*quantity)/230)*0.85
                              elif quantity==6:
                                  ampere=((rating*quantity)/230)*0.75
                              elif quantity==7:
                                  ampere=((rating*quantity)/230)*0.65
                              elif quantity==8:
                                  ampere=((rating*quantity)/230)*0.60
                              elif quantity==9:
                                  ampere=((rating*quantity)/230)*0.55
                              elif quantity==10:
                                  ampere=((rating*quantity)/230)*0.50
                              elif quantity==11:
                                  ampere=((rating*quantity)/230)*0.47
                              elif quantity>=12 and quantity<=22:
                                  ampere=((rating*quantity)/230)*(47-(quantity-11))*0.01
                              elif quantity==23:
                                  ampere=((rating*quantity)/230)*0.35
                              elif quantity>=24 and quantity<=42:
                                  ampere=((rating*quantity)/230)*(0.5*(quantity-23))*0.01
                              elif quantity>=43:
                                  ampere=((rating*quantity)/230)*0.25
                 elif ampflag==6:
                             lightingflag=0
                             typeflag=0
                             if unitflag==1:
                                 rating=float(self.l12.text())
                             elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                             ampere=(rating*quantity)/230
              
                 else:
                     ampere=0
                 ampere=round(ampere, 2)
                 if typeflag==1:
                         wireat=ampere*1.25
                         atampere=ampere*2.5
                 else:    
                     wireat=ampere/0.8
                     atampere=ampere/0.8
                 print "Wire Reference: "+str(wireat)
                 print "AT Reference: "+str(atampere)
                 atdata="ATParse.csv"
                 dfat=pd.read_csv(atdata,names=['AT','Low','High'],skiprows=1)
                 np_dfat = dfat.as_matrix()
                 atcnt=0
                 for i in xrange(len(np_dfat)):
                       if atampere>np_dfat[atcnt][1] and atampere<=np_dfat[atcnt][2]:
                             amperetrip=np_dfat[atcnt][0]
                             
                       atcnt=atcnt+1
                 wiredata="WireParse.csv"
                 dfwire=pd.read_csv(wiredata,names=['Size','A','B','C','D','E','F'],skiprows=1)
                 np_dfwire = dfwire.as_matrix()
                 if airconflag==1 and ampflag==3 and amperetrip<=30:
                                           ampertrip=30
                             
                 print "AT: "+str(amperetrip)

          
                 if wireflag==1:
                     
                     if wireat<=405:
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireat>np_dfwire[wirecnt][1] and wireat<=np_dfwire[wirecnt+1][1]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                     elif wireat>405 and wireat<=445:
                         wiresize=np_dfwire[wirecnt+1][0]
                         print "Wire Size:"+str(wiresize)
                     elif wireat>445:
                         wireatout=wireat
                         while wireatout>445:
                             if wireset<2:
                                 wireset=wireset+1
                             wireatout=wireat/wireset
                             wireset=wireset+1
                         print "AT: "+str(wireatout)
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireatout>np_dfwire[wirecnt][1] and wireatout<=np_dfwire[wirecnt+1][1]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                 elif wireflag==2:
                     
                     if wireat<=485:
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireat>np_dfwire[wirecnt][2] and wireat<=np_dfwire[wirecnt+1][2]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                     elif wireat>485 and wireat<=540:
                         wiresize=np_dfwire[wirecnt+1][0]
                         print "Wire Size:"+str(wiresize)
                     elif wireat>540:
                         wireatout=wireat
                         while wireatout>540:
                             if wireset<2:
                                 wireset=wireset+1
                             wireatout=wireat/wireset
                             wireset=wireset+1
                         print "AT: "+str(wireatout)
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireatout>np_dfwire[wirecnt][2] and wireatout<=np_dfwire[wirecnt+1][2]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                 elif wireflag==3:
                     
                     if wireat<=515:
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireat>np_dfwire[wirecnt][3] and wireat<=np_dfwire[wirecnt+1][3]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                     elif wireat>515 and wireat<=580:
                         wiresize=np_dfwire[wirecnt+1][0]
                         print "Wire Size:"+str(wiresize)
                     elif wireat>580:
                         wireatout=wireat
                         while wireatout>580:
                             if wireset<2:
                                 wireset=wireset+1
                             wireatout=wireat/wireset
                             wireset=wireset+1
                         print "AT: "+str(wireatout)
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireatout>np_dfwire[wirecnt][3] and wireatout<=np_dfwire[wirecnt+1][3]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                 elif wireflag==4:
                     
                     if wireat<=335:
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireat>np_dfwire[wirecnt][4] and wireat<=np_dfwire[wirecnt+1][4]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                     elif wireat>335 and wireat<=370:
                         wiresize=np_dfwire[wirecnt+1][0]
                         print "Wire Size:"+str(wiresize)
                     elif wireat>370:
                         wireatout=wireat
                         while wireatout>370:
                             if wireset<2:
                                 wireset=wireset+1
                             wireatout=wireat/wireset
                             wireset=wireset+1
                         print "AT: "+str(wireatout)
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireatout>np_dfwire[wirecnt][4] and wireatout<=np_dfwire[wirecnt+1][4]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                 elif wireflag==5:
                     
                     if wireat<=405:
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireat>np_dfwire[wirecnt][5] and wireat<=np_dfwire[wirecnt+1][5]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                     elif wireat>405 and wireat<=440:
                         wiresize=np_dfwire[wirecnt+1][0]
                         print "Wire Size:"+str(wiresize)
                     elif wireat>440:
                         wireatout=wireat
                         while wireatout>440:
                             if wireset<2:
                                 wireset=wireset+1
                             wireatout=wireat/wireset
                             wireset=wireset+1
                         print "AT: "+str(wireatout)
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireatout>np_dfwire[wirecnt][5] and wireatout<=np_dfwire[wirecnt+1][5]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                 elif wireflag==6:
                     
                     if wireat<=460:
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireat>np_dfwire[wirecnt][6] and wireat<=np_dfwire[wirecnt+1][6]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                     elif wireat>460 and wireat<=495:
                         wiresize=np_dfwire[wirecnt+1][0]
                         print "Wire Size:"+str(wiresize)
                     elif wireat>495:
                         wireatout=wireat
                         while wireatout>495:
                             if wireset<2:
                                 wireset=wireset+1
                             wireatout=wireat/wireset
                             wireset=wireset+1
                         print "AT: "+str(wireatout)
                         wirecnt=0
                         for i in xrange(len(np_dfwire)-1):
                             
                                if wireatout>np_dfwire[wirecnt][6] and wireatout<=np_dfwire[wirecnt+1][6]:
                                 
                                     wiresize=np_dfwire[wirecnt+1][0]
                                     print "Wire Size:"+str(wiresize)
                                 
                                wirecnt=wirecnt+1
                 try:
                     self.l19.setText("")
                     afdata="AFParse.csv"
                     dfaf=pd.read_csv(afdata,names=['AF','AT'],skiprows=1)
                     afout=np.where(dfaf["AT"] == amperetrip)
                     np_dfaf = dfaf.as_matrix()
                     
                     afout=afout[0][0]
                     afout=np_dfaf[afout][0]
                     print "AF: "+str(afout)
                 except:
                     afout="Out of Range"
                     print "Adjust AF Table: Out of Range"
                     self.l19.setText("Adjust AF Table: Out of Range")
                     
                 grounddata="groundwire.csv"
                 dfground=pd.read_csv(grounddata,names=['AT','Copper','Aluminum'],skiprows=1)
                 
       
                 if groundtype==0:
                     np_dfground = dfground.as_matrix()
                     groundcnt=0
                     groundat=amperetrip
                     for i in xrange(len(np_dfground)-1):
                         
                            if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                             
                                 groundsize=np_dfground[groundcnt+1][1]
                                 print "Ground Wire: "+str(groundsize)
                             
                            groundcnt=groundcnt+1
                 elif groundtype==1:
                     np_dfground = dfground.as_matrix()
                     groundcnt=0
                     groundat=amperetrip
                     for i in xrange(len(np_dfground)-1):
                         
                            if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                             
                                 groundsize=np_dfground[groundcnt+1][2]
                                 print "Ground Wire: "+str(groundsize)
                             
                            groundcnt=groundcnt+1
                 
                 if conduitflag==1:
                    conduitrange=10
                    if emtflag==1:
                        pathwire="conduit_csv/emt_A.csv"
                    elif emtflag==2:
                        pathwire="conduit_csv/emt_B.csv"
                    elif emtflag==3:
                        pathwire="conduit_csv/emt_C.csv"
                    elif emtflag==4:
                        pathwire="conduit_csv/emt_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                     
                 elif conduitflag==2:
                    conduitrange=6
                    if entflag==1:
                        pathwire="conduit_csv/ent_A.csv"
                    elif entflag==2:
                        pathwire="conduit_csv/ent_B.csv"
                    elif entflag==3:
                        pathwire="conduit_csv/ent_C.csv"
                    elif entflag==4:
                        pathwire="conduit_csv/ent_D.csv"
                    elif entflag==5:
                        pathwire="conduit_csv/ent_E.csv"
                            
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F'],skiprows=1)
                    
                 elif conduitflag==3:
                    conduitrange=10
                    if fmcflag==1:
                        pathwire="conduit_csv/fmc_A.csv"
                    elif fmcflag==2:
                        pathwire="conduit_csv/fmc_B.csv"
                    elif fmcflag==3:
                        pathwire="conduit_csv/fmc_C.csv"
                    elif fmcflag==4:
                        pathwire="conduit_csv/fmc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)  
                 elif conduitflag==4:
                    conduitrange=10
                    if imcflag==1:
                        pathwire="conduit_csv/imc_A.csv"
                    elif imcflag==2:
                        pathwire="conduit_csv/imc_B.csv"
                    elif imcflag==3:
                        pathwire="conduit_csv/imc_C.csv"
                    elif imcflag==4:
                        pathwire="conduit_csv/imc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                 elif conduitflag==5:
                    conduitrange=7
                    if lfnmcflag==1:
                        pathwire="conduit_csv/lfnmc_A.csv"
                    elif lfnmcflag==2:
                        pathwire="conduit_csv/lfnmc_B.csv"
                    elif lfnmcflag==3:
                        pathwire="conduit_csv/lfnmc_C.csv"
                    elif lfnmcflag==4:
                        pathwire="conduit_csv/lfnmc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G'],skiprows=1)
                 elif conduitflag==6:
                    conduitrange=10
                    if lfmcflag==1:
                        pathwire="conduit_csv/lfmc_A.csv"
                    elif lfmcflag==2:
                        pathwire="conduit_csv/lfmc_B.csv"
                    elif lfmcflag==3:
                        pathwire="conduit_csv/lfmc_C.csv"
                    elif lfmcflag==4:
                        pathwire="conduit_csv/lfmc_D.csv"
                    elif lfmcflag==5:
                        pathwire="conduit_csv/lfmc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                 elif conduitflag==7:
                    conduitrange=12
                    if rmcflag==1:
                        pathwire="conduit_csv/rmc_A.csv"
                    elif rmcflag==2:
                        pathwire="conduit_csv/rmc_B.csv"
                    elif rmcflag==3:
                        pathwire="conduit_csv/rmc_C.csv"
                    elif rmcflag==4:
                        pathwire="conduit_csv/rmc_D.csv"
                    elif rmcflag==5:
                        pathwire="conduit_csv/rmc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                 elif conduitflag==8:
                    conduitrange=12
                    if rpvcflag==1:
                        pathwire="conduit_csv/rpvc_A.csv"
                    elif rpvcflag==2:
                        pathwire="conduit_csv/rpvc_B.csv"
                    elif rpvcflag==3:
                        pathwire="conduit_csv/rpvc_C.csv"
                    elif rpvcflag==4:
                        pathwire="conduit_csv/rpvc_D.csv"
                    elif rpvcflag==5:
                        pathwire="conduit_csv/rpvc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                 
                 print pathwire
                 wireid=np.where(dfw["Output"] == wiresize)
                 np_dfw = dfw.as_matrix()
                 wireid=wireid[0][0]
             
                 conduitcnt=1
                 for i in xrange(conduitrange): 
                        try:
                            
                            
                            if np_dfw[wireid][conduitcnt]!=np_dfw[wireid][conduitcnt+1] and totalwire>np_dfw[wireid][conduitcnt]:
                                if totalwire>np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                     
                                     conduitsize=np_dfw[0][conduitcnt+1]
                                     
                            elif totalwire<=np_dfw[wireid][1]:
                                conduitsize=np_dfw[0][1]
                                
                            else:
                                 if totalwire>=np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                     
                                     conduitsize=np_dfw[0][conduitcnt+1]
                                     
                        except:
                             print ""
                        conduitcnt=conduitcnt+1
                 print "Conduit Size: "+str(conduitsize)
                 if spareflag==1 and ampflag==6:
                     wiresize=0
                     groundsize=0
                     conduitsize=0
                 if spaceflag==1 and ampflag==6:
                     rating=0
                     wireset=0
                     wirenumber=0
                     amperetrip=0
                     afout=0
                     ampere=0
                     wiresize=0
                     groundsize=0
                     conduitsize=0
                 if os.path.exists(pathtarget):
                     
                     df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
                     np_df = df.as_matrix()
                     df = df.append({'Circuit':len(np_df)+1, 'Quantity':quantity, 'LoadDescription':loadname,'Rating':rating,'Voltage':230,'Wireset':wireset,'Wirenumber':wirenumber,'AT':amperetrip,'AF':afout,'Motor':typeflag,
                                     'Ampere':ampere,'WireSize':wiresize,'GroundSize':groundsize,'ConduitSize':conduitsize,'Lighting':lightingflag}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                 else:
                     
                     columns = ['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize','Lighting']
                     df = pd.DataFrame(columns=columns)
                     np_df = df.as_matrix()
                     
                     df = df.append({'Circuit':1, 'Quantity':quantity, 'LoadDescription':loadname,'Rating':rating,'Voltage':230,'Wireset':wireset,'Wirenumber':wirenumber,
                                     'AT':amperetrip,'AF':afout,'Motor':typeflag,'Ampere':ampere,'WireSize':wiresize,'GroundSize':groundsize,'ConduitSize':conduitsize,'Lighting':lightingflag}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                 
                 cnt=0
                 np_df = df.as_matrix()
                 self.table.setRowCount(len(np_df))
                 
                 for i in xrange(len(np_df)):
                     self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(int(cnt+1))+""))#Space
                     self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][1]))+""))#Space
                     self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))#Space
                     self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))#Space
                     cnt=cnt+1
         #except:
               #self.l19.setText("Please fill up all required information.")
    def deletedata(self,dx):
         
         directory=str(self.n2.text())
         panelboard=str(self.l3.text())
         pathtarget=directory+"/"+panelboard+".csv"
         x=0
         indexes = self.table.selectionModel().selectedRows()
         for index in sorted(indexes):
            print index.row()
         df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
         df.drop(index.row(), inplace=True)
         df = df.reset_index(drop=True)
         df.to_csv(pathtarget,  index = False)
         np_df = df.as_matrix()
         cnt=0
         print np_df
         
         columns = ['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize','Lighting']
         df = pd.DataFrame(columns=columns)
         for i in xrange(len(np_df)):
             
             df = df.append({'Circuit':cnt+1, 'Quantity':np_df[cnt][1], 'LoadDescription':np_df[cnt][2],'Rating':np_df[cnt][3],'Voltage':np_df[cnt][4],'Wireset':np_df[cnt][5],'Wirenumber':np_df[cnt][6],'AT':np_df[cnt][7],
                             'AF':np_df[cnt][8],'Motor':np_df[cnt][9],'Ampere':np_df[cnt][10],'WireSize':np_df[cnt][11],'GroundSize':np_df[cnt][12],'ConduitSize':np_df[cnt][13],'Lighting':np_df[cnt][14]}, ignore_index=True)
             cnt=cnt+1
         df.to_csv(pathtarget,  index = False)
         cnt=0
         np_df = df.as_matrix()
         self.table.setRowCount(len(np_df))
         for i in xrange(len(np_df)):
             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(int(cnt+1))+""))#Space
             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][1]))+""))#Space
             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))#Space
             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))#Space
             cnt=cnt+1
    def loaddata(self,dx):
         try:
             self.l19.setText("")
             directory=str(self.n2.text())
             panelboard=str(self.l3.text())
             pathtarget=directory+"/"+panelboard+".csv"
             df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
             np_df = df.as_matrix()
             self.table.setRowCount(len(np_df))
             cnt=0
             
             for i in xrange(len(np_df)):
                 self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+"    "+str(cnt+1)+""))#Space
                 self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+"    "+str(np_df[cnt][1])+""))#Space
                 self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+"    "+str(np_df[cnt][2])+""))#Space
                 self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+"    "+str(np_df[cnt][3])+""))#Space
                 cnt=cnt+1
             
         except:
             self.l19.setText("File doesn't exist.")
    def typeselect(self,ex):
        global ampflag,specflag,spareflag,spaceflag
        self.specload.clear()
        self.unitload.clear()
        if ex==1:
            spareflag=0
            spaceflag=0
            ampflag=1
            self.specload.addItems([])
            self.unitload.addItems(["VA","kW"])
            specflag=0
        elif ex==2:
            ampflag=4
            self.specload.addItems(["","General Purpose Receptacle","Special Purpose Receptacle",])
            self.unitload.addItems(["VA","kW"])
            specflag=0
        elif ex==3:
            ampflag=2
            
            self.specload.addItems(["","Microwave","Dishwasher","Electric range","Electric griller","Refrigerator","Cooking equipment"])
            self.unitload.addItems(["VA","kW"])
        elif ex==4:
            ampflag=5
            self.specload.addItems(["","Washing machine","Electric Dryer"])
            self.unitload.addItems(["HP","VA"])
        elif ex==5:
            ampflag=3
            self.specload.addItems(["","Air conditioning units","Water pump","Compressor"])
            self.unitload.addItems(["HP","VA"])
        elif ex==6:
            ampflag=6
            self.specload.addItems(["","Water heater","Spare","Space"])
            self.unitload.addItems(["VA","kW"])
            
        
    def loadselect(self,fx):
        global ampflag,unitflag
        if ampflag!=5:
            if fx==0:
                unitflag=1
            elif fx==1:
                unitflag=2
    def specselect(self,gx):
        global specflag,appliancesflag,laundryflag,spareflag,spaceflag,waterheaterflag,airconflag
        if gx==2:
            spareflag=1
            waterheaterflag=0
            spaceflag=0
        elif gx==3:
            spaceflag=1
            waterheaterflag=0
            spareflag=0
        elif gx==1:
            spareflag=0
            spaceflag=0
            waterheaterflag=1
			
        if gx==1:
           appliancesflag=1
           laundryflag=1
           airconflag=1
        elif gx==2:
           specflag=1
           laundryflag=2
           appliancesflag=0
        elif gx==3:
           specflag=1
        else:
           airconflag=0	
           specflag=0
           appliancesflag=0
    def wireselect(self,hx):
        global wireflag,groundtype,emtflag,entflag,fmcflag,imcflag,lfnmcflag,lfmcflag,rmcflag,rpvcflag
        if hx==1 or hx==2:
            wireflag=1
        elif hx==3 or hx==4 or hx==5:
            wireflag=2
        elif hx==6 or hx==7 or hx==8 or hx==9 or hx==10:
            wireflag=3
        elif hx==11 or hx==12:
            wireflag=4
        elif hx==13 or hx==14 or hx==15:
            wireflag=5
        elif hx==16 or hx==17 or hx==18 or hx==19 or hx==20:
            wireflag=6
        else:
            wireflag=0
        if hx==1 or hx==2 or hx==3 or hx==4 or hx==5 or hx==6 or hx==7 or hx==8 or hx==9 or hx==10:
            groundtype=0
        elif hx==11 or hx==12 or hx==13 or hx==14 or hx==15 or hx==16 or hx==17 or hx==18 or hx==19 or hx==20:
            groundtype=1
        if hx==3 or hx==13 or hx==6 or hx==16:#RHW - RHH
            emtflag=1
            entflag=1
            fmcflag=1
            imcflag=1
            lfnmcflag=1
            lfmcflag=1
            rmcflag=1
            rpvcflag=1
        elif hx==1 or hx==11:#TW
            emtflag=2
            entflag=2
            fmcflag=2
            imcflag=2
            lfnmcflag=2
            lfmcflag=2
            rmcflag=2
            rpvcflag=2
        elif hx==8 or hx==18 or hx==4 or hx==14:#THHW - THW
            entflag=3
            fmcflag=2
            imcflag=2
            lfnmcflag=2
            lfmcflag=3
            rmcflag=3
            rpvcflag=3
        elif hx==7 or hx==17 or hx==5 or hx==15:#THHN - THWN
            emtflag=3
            entflag=4
            fmcflag=3
            imcflag=3
            lfnmcflag=3
            lfmcflag=4
            rmcflag=4
            rpvcflag=4
        
        elif hx==9 or hx==19 or hx==10 or hx==20:#XHH - XHHW
            emtflag=4
            entflag=5
            fmcflag=4
            imcflag=4
            lfnmcflag=4
            lfmcflag=5
            rmcflag=5
            rpvcflag=5
                
      
        
    def conduitselect(self,ix):
        global conduitflag
        if ix==1:
            conduitflag=1
        elif ix==2:
            conduitflag=2
        elif ix==3:
            conduitflag=3
        elif ix==4:
            conduitflag=4
        elif ix==5:
            conduitflag=5
        elif ix==6:
            conduitflag=6
        elif ix==7:
            conduitflag=7
        elif ix==8:
            conduitflag=8
        else:
            conduitflag=0
            
class paneloutputresidential(QtGui.QDialog):
    def __init__(self,parent=None):
        super(paneloutputresidential, self).__init__(parent)
        
        self.setWindowTitle("SINGLE PHASE LOAD SCHEDULE")
        self.setGeometry(20,20,1200,780)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(11)
        self.table.move(120,50)
        self.table.setHorizontalHeaderLabels(['Ckt. No.','       Load Description      ','     V    ','       VA     ','    Ampere      ',' AT ',' AF ','  Sets  ','  Wire Size  ','  Ground Wire  ','   Conduit  '])#Space
        self.table.resize(950,400)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        self.tablediag = QtGui.QTableWidget(self)
        self.tablediag.setColumnCount(6)
        self.tablediag.move(120,500)
        self.tablediag.setHorizontalHeaderLabels(['Main Feeder AT                           ','Main Feeder AF                ','Sets                 ','Wire Size                ','Grounding Wire               ','Conduit         '])#Space
        self.tablediag.resize(950,100)
        self.tablediag.resizeColumnsToContents()
        self.tablediag.verticalHeader().setVisible(0)
        font10 = QtGui.QFont("Helvetica", 10)
        self.dt=QtGui.QLabel("Disclaimer: The data from this software must only be for verification purposes.",self)
        self.dt.move(10,730)
        self.dt.setFont(font10)
        self.dx=QtGui.QLabel("It is based from the PEC 2009 provisions that are considered minimum requirements necessary for safety.",self)
        self.dx.move(10,750)
        self.dx.setFont(font10)
        self.lt=QtGui.QLabel("Minimum Lighting Load: ",self)
        self.lt.move(10,650)
        self.lt.resize(210,30)
        self.lt.setFont(font10)
        self.lto=QtGui.QLabel(self)
        self.lto.move(250,650)
        self.lto.resize(100,30)
        self.lto.setFont(font10)
        self.displayinput = QtGui.QPushButton("Diagram",self)
        self.displayinput.clicked.connect(self.displaydata)
        self.displayinput.move(410,700)
        self.updateinput = QtGui.QPushButton("Display",self)
        self.updateinput.clicked.connect(self.updatedata)
        self.updateinput.move(310,700)
        self.residentialdiagram=diagramresidential(self)
    def displaydata(self):
        self.residentialdiagram.exec_()
        #python = sys.executable
        #os.execl(python, python, * sys.argv)
        self.close()
    def updatedata(self):
        pathsave="outputdata.csv"
        dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','Conduit'],skiprows=1)
        np_dfo = dfo.as_matrix()
        pathtarget=str(np_dfo[0][0])
        df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
        np_df = df.as_matrix()
        self.table.setRowCount(len(np_df))
        self.tablediag.setRowCount(1)
        self.tablediag.setItem(0, 0, QtGui.QTableWidgetItem(""+str(np_dfo[0][1])))#Space
        self.tablediag.setItem(0, 1, QtGui.QTableWidgetItem(""+str(np_dfo[0][2])))#Space
        self.tablediag.setItem(0, 2, QtGui.QTableWidgetItem(""+str(int(np_dfo[0][3]))))#Space
        self.tablediag.setItem(0, 3, QtGui.QTableWidgetItem(" 2 - "+str(np_dfo[0][4])))#Space
        self.tablediag.setItem(0, 4, QtGui.QTableWidgetItem(" 1 - "+str(np_dfo[0][5])))#Space
        self.tablediag.setItem(0, 5, QtGui.QTableWidgetItem(""+str(np_dfo[0][6])))#Space
        
        pathres="areaflag.csv"
        dfr=pd.read_csv(pathres,names=['Areaflag','Area'],skiprows=1)
        np_dfr = dfr.as_matrix()
        itx=0
        areaflag=int(np_dfr[0][0])
        unitarea=float(np_dfr[0][1])
        dflighting=df[df.Lighting != 0]
        np_dflighting=dflighting.as_matrix()
        print np_dflighting
        lightingtotal=0
        for i in xrange(len(np_dflighting)):
             lighting=np_dflighting[itx][3]
             lightingtotal=lightingtotal+lighting
             itx=itx+1
        print lightingtotal  
        if unitarea!="":
             
             if areaflag==1:
                 vasq=8
             elif areaflag==2:
                 vasq=28
             elif areaflag==3:
                 vasq=24
             elif areaflag==4:
                 vasq=8
             elif areaflag==5:
                 vasq=16
             elif areaflag==6:
                 vasq=16
             elif areaflag==7:
                 vasq=24
             elif areaflag==8:
                 vasq=4
             elif areaflag==9:
                 vasq=16
             elif areaflag==10:
                 vasq=16
             elif areaflag==11:
                 vasq=12
             elif areaflag==12:
                 vasq=28
             elif areaflag==13:
                 vasq=16
             elif areaflag==14:
                 vasq=24
             elif areaflag==15:
                 vasq=24
             elif areaflag==16:
                 vasq=8
             elif areaflag==17:
                 vasq=4
             elif areaflag==18:
                 vasq=2
             if areaflag!=0:
                 vaunit=unitarea*vasq
               
                 if lightingtotal>=vaunit:
                    self.lto.setText(str(lightingtotal))
                    self.lto.setStyleSheet('color: green')
                 elif lightingtotal<vaunit:
                    self.lto.setText(str(lightingtotal))
                    self.lto.setStyleSheet('color: red')
             else:
                 self.lto.setText("No Input")
                 self.lto.setStyleSheet('color: red')
        cnt=0
        for i in xrange(len(np_df)):
            
             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][0]))))#Space
             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])))#Space
             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][4])))#Space
             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])))#Space
             self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][10])))#Space
             self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(np_df[cnt][7])))#Space
             self.table.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(np_df[cnt][8])))#Space
             self.table.setItem(cnt, 7, QtGui.QTableWidgetItem(""+str(np_df[cnt][5])))#Space
             self.table.setItem(cnt, 8, QtGui.QTableWidgetItem(" 2 - "+str(np_df[cnt][11])))#Space
             self.table.setItem(cnt, 9, QtGui.QTableWidgetItem(" 1 - "+str(np_df[cnt][12])))#Space
             self.table.setItem(cnt, 10, QtGui.QTableWidgetItem(""+str(np_df[cnt][13])))#Space
              
             cnt=cnt+1

             
class diagramresidential(QtGui.QDialog):
    def __init__(self,parent=None):
        super(diagramresidential, self).__init__(parent)
                     
        self.setWindowTitle("SINGLE PHASE PB DIAGRAM")
        self.setGeometry(20,20,942,760)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        
        
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame.resize(800,700)
        self.frame.move(85,-20)
        self.frame.setStyleSheet(" border-image: url(spbg.png);");
        
        self.frame1 = QtGui.QFrame(self)
        self.frame1.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame1.resize(500,80)
        self.frame1.move(42,145)
        
        self.frame3 = QtGui.QFrame(self)
        self.frame3.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame3.resize(500,80)
        self.frame3.move(42,175)
        self.frame5 = QtGui.QFrame(self)
        self.frame5.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame5.resize(500,80)
        self.frame5.move(42,205)
        self.frame7 = QtGui.QFrame(self)
        self.frame7.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame7.resize(500,80)
        self.frame7.move(42,235)
        self.frame9 = QtGui.QFrame(self)
        self.frame9.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame9.resize(500,80)
        self.frame9.move(42,265)
        self.frame11 = QtGui.QFrame(self)
        self.frame11.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame11.resize(500,80)
        self.frame11.move(42,295)
        self.frame13 = QtGui.QFrame(self)
        self.frame13.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame13.resize(500,80)
        self.frame13.move(42,325)
        self.frame15 = QtGui.QFrame(self)
        self.frame15.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame15.resize(500,80)
        self.frame15.move(42,355)
        self.frame17 = QtGui.QFrame(self)
        self.frame17.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame17.resize(500,80)
        self.frame17.move(42,385)
        self.frame19 = QtGui.QFrame(self)
        self.frame19.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame19.resize(500,80)
        self.frame19.move(42,415)

        
        self.frame2 = QtGui.QFrame(self)
        self.frame2.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame2.resize(500,80)
        self.frame2.move(430,145)
        self.frame4 = QtGui.QFrame(self)
        self.frame4.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame4.resize(500,80)
        self.frame4.move(430,175)
        self.frame6 = QtGui.QFrame(self)
        self.frame6.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame6.resize(500,80)
        self.frame6.move(430,205)
        self.frame8 = QtGui.QFrame(self)
        self.frame8.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame8.resize(500,80)
        self.frame8.move(430,235)
        self.frame10 = QtGui.QFrame(self)
        self.frame10.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame10.resize(500,80)
        self.frame10.move(430,265)
        self.frame12 = QtGui.QFrame(self)
        self.frame12.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame12.resize(500,80)
        self.frame12.move(430,295)
        self.frame14 = QtGui.QFrame(self)
        self.frame14.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame14.resize(500,80)
        self.frame14.move(430,325)
        self.frame16 = QtGui.QFrame(self)
        self.frame16.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame16.resize(500,80)
        self.frame16.move(430,355)
        self.frame18 = QtGui.QFrame(self)
        self.frame18.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame18.resize(500,80)
        self.frame18.move(430,385)
        self.frame20 = QtGui.QFrame(self)
        self.frame20.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame20.resize(500,80)
        self.frame20.move(430,415)

        
        #self.frame1.setStyleSheet(" border-image: url(spleftAB.png);");
        #self.frame2.setStyleSheet(" border-image: url(spleftABC.png);");
        #self.frame3.setStyleSheet(" border-image: url(spleftspare.png);");
        #self.frame4.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame5.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame6.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame7.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame8.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame9.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame10.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame11.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame12.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame13.setStyleSheet(" border-image: url(spleftBC.png);");
        #self.frame14.setStyleSheet(" border-image: url(sprightABC.png);");
        #self.frame15.setStyleSheet(" border-image: url(sprightspare.png);");
        #self.frame16.setStyleSheet(" border-image: url(sprightCA.png);");
        #self.frame17.setStyleSheet(" border-image: url(sprightBC.png);");
        #self.frame18.setStyleSheet(" border-image: url(sprightBC.png);");
        #self.frame19.setStyleSheet(" border-image: url(sprightBC.png);");
        #self.frame20.setStyleSheet(" border-image: url(sprightBC.png);");

      
        self.displayinput = QtGui.QPushButton("Diagram",self)
        self.displayinput.clicked.connect(self.displaydata)
        self.displayinput.move(410,700)
        font10 = QtGui.QFont("Helvetica", 10)
        self.a1=QtGui.QLabel(self)
        self.a1.move(150,150)
        self.a1.setFont(font10)
        self.a3=QtGui.QLabel(self)
        self.a3.move(150,180)
        self.a3.setFont(font10)
        self.a5=QtGui.QLabel(self)
        self.a5.move(150,210)
        self.a5.setFont(font10)
        self.a7=QtGui.QLabel(self)
        self.a7.move(150,240)
        self.a7.setFont(font10)
        self.a9=QtGui.QLabel(self)
        self.a9.move(150,270)
        self.a9.setFont(font10)
        self.a11=QtGui.QLabel(self)
        self.a11.move(150,300)
        self.a11.setFont(font10)
        self.a13=QtGui.QLabel(self)
        self.a13.move(150,330)
        self.a13.setFont(font10)
        self.a15=QtGui.QLabel(self)
        self.a15.move(150,360)
        self.a15.setFont(font10)
        self.a17=QtGui.QLabel(self)
        self.a17.move(150,390)
        self.a17.setFont(font10)
        self.a19=QtGui.QLabel(self)
        self.a19.move(150,420)
        self.a19.setFont(font10)
        self.a2=QtGui.QLabel(self)
        self.a2.move(800,150)
        self.a2.setFont(font10)
        self.a4=QtGui.QLabel(self)
        self.a4.move(800,180)
        self.a4.setFont(font10)
        self.a6=QtGui.QLabel(self)
        self.a6.move(800,210)
        self.a6.setFont(font10)
        self.a8=QtGui.QLabel(self)
        self.a8.move(800,240)
        self.a8.setFont(font10)
        self.a10=QtGui.QLabel(self)
        self.a10.move(800,270)
        self.a10.setFont(font10)
        self.a12=QtGui.QLabel(self)
        self.a12.move(800,300)
        self.a12.setFont(font10)
        self.a14=QtGui.QLabel(self)
        self.a14.move(800,330)
        self.a14.setFont(font10)
        self.a16=QtGui.QLabel(self)
        self.a16.move(800,360)
        self.a16.setFont(font10)
        self.a18=QtGui.QLabel(self)
        self.a18.move(800,390)
        self.a18.setFont(font10)
        self.a20=QtGui.QLabel(self)
        self.a20.move(800,420)
        self.a20.setFont(font10)
        self.b1=QtGui.QLabel(self)
        self.b1.move(250,150)
        self.b1.setFont(font10)
        self.b3=QtGui.QLabel(self)
        self.b3.move(250,180)
        self.b3.setFont(font10)
        self.b5=QtGui.QLabel(self)
        self.b5.move(250,210)
        self.b5.setFont(font10)
        self.b7=QtGui.QLabel(self)
        self.b7.move(250,240)
        self.b7.setFont(font10)
        self.b9=QtGui.QLabel(self)
        self.b9.move(250,270)
        self.b9.setFont(font10)
        self.b11=QtGui.QLabel(self)
        self.b11.move(250,300)
        self.b11.setFont(font10)
        self.b13=QtGui.QLabel(self)
        self.b13.move(250,330)
        self.b13.setFont(font10)
        self.b15=QtGui.QLabel(self)
        self.b15.move(250,360)
        self.b15.setFont(font10)
        self.b17=QtGui.QLabel(self)
        self.b17.move(250,390)
        self.b17.setFont(font10)
        self.b19=QtGui.QLabel(self)
        self.b19.move(250,420)
        self.b19.setFont(font10)
        self.b2=QtGui.QLabel(self)
        self.b2.move(700,150)
        self.b2.setFont(font10)
        self.b4=QtGui.QLabel(self)
        self.b4.move(700,180)
        self.b4.setFont(font10)
        self.b6=QtGui.QLabel(self)
        self.b6.move(700,210)
        self.b6.setFont(font10)
        self.b8=QtGui.QLabel(self)
        self.b8.move(700,240)
        self.b8.setFont(font10)
        self.b10=QtGui.QLabel(self)
        self.b10.move(700,270)
        self.b10.setFont(font10)
        self.b12=QtGui.QLabel(self)
        self.b12.move(700,300)
        self.b12.setFont(font10)
        self.b14=QtGui.QLabel(self)
        self.b14.move(700,330)
        self.b14.setFont(font10)
        self.b16=QtGui.QLabel(self)
        self.b16.move(700,360)
        self.b16.setFont(font10)
        self.b18=QtGui.QLabel(self)
        self.b18.move(700,390)
        self.b18.setFont(font10)
        self.b20=QtGui.QLabel(self)
        self.b20.move(700,420)
        self.b20.setFont(font10)
    def displaydata(self):
         pathsave="outputdata.csv"
         dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
         np_dfo = dfo.as_matrix()
         pathtarget=str(np_dfo[0][0])
         df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
         np_df = df.as_matrix()
         itx=0
         mod=1
         for i in xrange(len(np_df)):
             if np_df[itx][10]>0 and mod%2!=0 and np_df[itx][13]!=0:
                 disp='setStyleSheet(" border-image: url(spleftload.png);")'
                 disp = disp.replace("'", "")
                 print "Left Load"
                 exec("self.frame%d.%s" % (i + 1, disp));


             elif np_df[itx][10]==0  and mod%2!=0 and np_df[itx][13]==0:
                 disp='setStyleSheet(" border-image: url(spleftspace.png);")'
                 disp = disp.replace("'", "")
                 print "Left Space"
                 exec("self.frame%d.%s" % (i + 1, disp));
                 
             elif np_df[itx][10]!=0 and mod%2!=0 and np_df[itx][13]==0 :
                 disp='setStyleSheet(" border-image: url(spleftspare.png);")'
                 disp = disp.replace("'", "")
                 print "Left Spare"
                 exec("self.frame%d.%s" % (i + 1, disp));
                 
             elif np_df[itx][10]>0 and mod%2==0 and np_df[itx][13]!=0:
                 disp='setStyleSheet(" border-image: url(sprightload.png);")'
                 disp = disp.replace("'", "")
                 print "Right Load"
                 exec("self.frame%d.%s" % (i + 1, disp));
  
             elif np_df[itx][10]==0 and mod%2==0 and np_df[itx][13]==0:
                 disp='setStyleSheet(" border-image: url(sprightspace.png);")'
                 disp = disp.replace("'", "")
                 print "Right Space"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]!=0 and mod%2==0 and np_df[itx][13]==0:
                 disp='setStyleSheet(" border-image: url(sprightspare.png);")'
                 disp = disp.replace("'", "")
                 print "Right Spare"
                 exec("self.frame%d.%s" % (i + 1, disp));
             print np_df[itx][7]
             disp='setText(str('+str(np_df[itx][7])+'))'
             disp = disp.replace("'", "")
             resdisp='resize(100,30)'
             resdisp = resdisp.replace("'", "")
             loaddisp='setText("'+str(np_df[itx][2])+'")'
             loaddisp = loaddisp.replace("'", "")
             exec("self.a%d.%s" % (i + 1, disp));
             exec("self.a%d.%s" % (i + 1, resdisp));
             exec("self.b%d.%s" % (i + 1, loaddisp));
             exec("self.b%d.%s" % (i + 1, resdisp)); 
             itx=itx+1
             mod=mod+1
         if len(np_df)%2!=0:
             disp='setStyleSheet(" border-image: url(sprightspare.png);")'
             disp = disp.replace("'", "")
             exec("self.frame%d.%s" % (len(np_df) + 1, disp));
             print "Right Spare"
             resdisp='resize(100,30)'
             resdisp = resdisp.replace("'", "")
             loaddisp='setText("Spare")'
             loaddisp = loaddisp.replace("'", "")
             exec("self.b%d.%s" % (len(np_df) + 1, loaddisp));
             exec("self.b%d.%s" % (len(np_df) + 1, resdisp));
##############################################################Commercial##############################################################         
class commercialgui(QtGui.QDialog):
    def __init__(self,parent=None):
        super(commercialgui, self).__init__(parent)
        self.framebg = QtGui.QFrame(self)
        self.framebg.setFrameStyle(QtGui.QFrame.NoFrame);
        self.framebg.resize(720,760)
        self.framebg.move(0,0)
        self.framebg.setStyleSheet(" border-image: url(background.png);");
        self.setWindowTitle("THREE PHASE")
        global ampflag,areaflag,specflag,airconflag,wireflag,conduitflag,phaseflag
        phaseflag=0
        ampflag=0
        areaflag=0
        wireflag=0
        conduitflag=0
        airconflag=0
        specflag=0
        self.setGeometry(20,20,720,760)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        font12 = QtGui.QFont("Helvetica", 12)
        font10 = QtGui.QFont("Helvetica", 10)
        self.l1=QtGui.QLabel("Three Phase Layout Design",self)
        self.l1.move(10,5)
        self.l1.setFont(font12)
        self.l1.setStyleSheet('color: red')
        self.n1=QtGui.QLabel("Project Name:",self)
        self.n1.move(20,45)
        self.n1.setFont(font10)
        self.n2=QtGui.QLineEdit(self)
        self.n2.move(130,45)
        self.n2.resize(100,20)
        self.n3=QtGui.QLabel("Unit Type:",self)
        self.n3.move(350,45)
        self.n3.setFont(font10)
        self.n4=QtGui.QLabel("Area:",self)
        self.n4.move(550,75)
        self.n4.setFont(font10)
        self.n5=QtGui.QLineEdit(self)
        self.n5.move(600,75)
        self.n5.resize(50,20)
        
        self.typeunit = QtGui.QComboBox(self)
        self.typeunit.addItems(["","Armories and Auditoriums","Banks","Babershops and Beauty Parlors","Churches","Clubs","Courtrooms","Dwelling Units","Garage","Hospitals","Hotels and Motels","Lodge Rooms",
                                "Office Buildings","Restaurants","Schools","Stores","Assembly Halls","Corridors and Halls","Storage Spaces"])
        self.typeunit.currentIndexChanged.connect(self.unitselect)
        self.typeunit.move(440,45)
        self.typeunit.resize(170,20)
        
        self.l2=QtGui.QLabel("Panel Board Name:",self)
        self.l2.move(20,75)
        self.l2.setFont(font10)
        self.l3=QtGui.QLineEdit(self)
        self.l3.move(170,75)
        self.l3.resize(100,20)
        self.l4=QtGui.QLabel("Demand Factor:",self)
        self.l4.move(350,75)
        self.l4.setFont(font10)
        self.l5=QtGui.QLineEdit(self)
        self.l5.move(480,75)
        self.l5.resize(50,20)
        self.l6=QtGui.QLabel("Load Specifications",self)
        self.l6.move(10,95)
        self.l6.setFont(font10)
        self.l6.setStyleSheet('color: red')
        self.l7=QtGui.QLabel("Type:",self)
        self.l7.move(20,130)
        self.l7.setFont(font10)
        self.typeload = QtGui.QComboBox(self)
        self.typeload.addItems(["","General Lighting Loads","Appliance Loads","Cooking Loads","Laundry Loads","Motor Loads","Other Loads"])
        self.typeload.currentIndexChanged.connect(self.typeselect)
        self.typeload.move(65,130)
        self.typeload.resize(140,20)
        self.l8=QtGui.QLabel("Load:",self)
        self.l8.move(210,130)
        self.l8.setFont(font10)
        self.specload = QtGui.QComboBox(self)
        self.specload.addItems([])
        self.specload.currentIndexChanged.connect(self.specselect)
        self.specload.move(260,130)
        self.specload.resize(120,20)
        self.l9=QtGui.QLabel("Load Name:",self)
        self.l9.move(400,130)
        self.l9.setFont(font10)
        self.l10=QtGui.QLineEdit(self)
        self.l10.move(500,130)
        self.l10.resize(100,20)
        self.l11=QtGui.QLabel("Rating:",self)
        self.l11.move(20,170)
        self.l11.setFont(font10)
        self.l12=QtGui.QLineEdit(self)
        self.l12.move(75,170)
        self.l12.resize(70,20)
        self.unitload = QtGui.QComboBox(self)
        self.unitload.addItems([])
        self.unitload.currentIndexChanged.connect(self.loadselect)
        self.unitload.move(135,170)
        self.unitload.resize(40,20)
        self.l13=QtGui.QLabel("Quantity:",self)
        self.l13.move(210,170)
        self.l13.setFont(font10)
        self.l14=QtGui.QLineEdit(self)
        self.l14.move(280,170)
        self.l14.resize(40,20)
        self.addinput = QtGui.QPushButton("Add",self)
        self.addinput.clicked.connect(self.adddata)
        self.addinput.move(10,250)
        self.deleteinput = QtGui.QPushButton("Delete",self)
        self.deleteinput.clicked.connect(self.deletedata)
        self.deleteinput.move(90,250)
        self.loadinput = QtGui.QPushButton("Load",self)
        self.loadinput.clicked.connect(self.loaddata)
        self.loadinput.move(170,250)
        
        self.l17=QtGui.QLabel("Type of Wire:",self)
        self.l17.move(20,200)
        self.l17.setFont(font10)
        self.l18=QtGui.QLabel("Type of Conduit:",self)
        self.l18.move(280,200)
        self.l18.setFont(font10)
        self.l19=QtGui.QLabel(self)
        self.l19.move(10,735)
        self.l19.resize(500,30)
        self.p0=QtGui.QLabel("Phase: ",self)
        self.p0.move(400,170)
        self.p0.setFont(font10)
        
        self.phasetype = QtGui.QComboBox(self)
        self.phasetype.addItems(["","AB","BC","CA","3-Phase"])
        self.phasetype.currentIndexChanged.connect(self.phaseselect)
        self.phasetype.move(460,170)
        self.phasetype.resize(70,20)

        self.wiretype = QtGui.QComboBox(self)
        self.wiretype.addItems(["","TW - Copper","UF - Copper","RHW - Copper","THW - Copper","THWN - Copper","RHH - Copper","THHN - Copper","THHW - Copper","XHH - Copper","XHHW - Copper","TW - Aluminum","UF - Aluminum","RHW - Aluminum","THW - Aluminum","THWN - Aluminum","RHH - Aluminum","THHN - Aluminum","THHW - Aluminum","XHH - Aluminum","XHHW - Aluminum"])
        self.wiretype.currentIndexChanged.connect(self.wireselect)
        self.wiretype.move(130,200)
        self.wiretype.resize(120,20)
        self.conduittype = QtGui.QComboBox(self)
        self.conduittype.addItems(["","EMT","ENMT","FMC","IMC","Liquidtight FNMC","Liquidtight FMC","RMC","Rigid PVC"])
        self.conduittype.currentIndexChanged.connect(self.conduitselect)
        self.conduittype.move(410,200)
        self.conduittype.resize(120,20)
        self.compinput = QtGui.QPushButton("Generate",self)
        self.compinput.clicked.connect(self.computedata)
        self.compinput.move(580,700)
        
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.move(50,280)
        self.table.setHorizontalHeaderLabels(['         Ckt. No.        ','         Qty         ','          Load Description           ', '            Rating          '])
        self.table.resize(600,400)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        self.outputpanelcommercial = paneloutputcommercial(self)
        self.commercialdiagram = diagramcommercial(self)
        
    def computedata(self,ax):
         global wireflag,groundtype,phaseflag,wiredisp,conduitdisp,areaflag
         dlag=0
         directory=str(self.n2.text())
         if not os.path.exists(directory):
             os.makedirs(directory)
         panelboard=str(self.l3.text())
       
         
         unitarea=str(self.n5.text())
         
         demandfactor=str(self.l5.text())
         if demandfactor=="":
             self.l19.setText("Please input demand factor.")
         else:
             try:
                 demandfactor=float(self.l5.text())
                 dflag=1
             except:
                 self.l19.setText("Invalid input for demand factor.")
         pathtarget=directory+"/"+panelboard+".csv"
         try:
             df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','Ampere','WireSize','GroundSize','ConduitSize'],skiprows=1)
             np_df = df.as_matrix()
         except:
             self.l19.setText("Project doesn't exist.")
         if wireflag==0:
                 self.l19.setText("Please select type of wire.")
         elif conduitflag==0:
             self.l19.setText("Please select type of conduit.")
         
         if wireflag!=0 and conduitflag!=0 and demandfactor!="" and dflag==1:
             
             df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
             np_df = df.as_matrix()
             dflighting=df[df.Lighting != 0]
             np_dflighting=dflighting.as_matrix()
             print np_dflighting
             lightingtotal=0
             itx=0
             for i in xrange(len(np_dflighting)):
                 lighting=np_dflighting[itx][3]
                 lightingtotal=lightingtotal+lighting
                 itx=itx+1
             print lightingtotal 
             Itab=0
             Itbc=0
             Itac=0
             Itabc=0
             itx=0
             vatotal=0
             for i in xrange(len(np_df)):
                 vatotal=vatotal+np_df[itx][3]
                 Itab=Itab+np_df[itx][10]
                 Itbc=Itbc+np_df[itx][11]
                 Itac=Itac+np_df[itx][12]
                 Itabc=Itabc+np_df[itx][13]
                 itx=itx+1
             Ih=[Itab,Itbc,Itac]
             Ih=sorted(Ih)
             Ih=Ih[2]
             print "Ih: "+str(Ih)
             It=Itabc+math.sqrt(3)*Ih

             
             try:    
                 dfmotor=df[df.Motor != 0]
                 dfmotor = dfmotor.sort_values(['AB'], ascending=[False])
                 np_dfmotor=dfmotor.as_matrix()
                 abmotor=np_dfmotor[0][10]
                 
                 dfmotor=df[df.Motor != 0]
                 dfmotor = dfmotor.sort_values(['BC'], ascending=[False])
                 np_dfmotor=dfmotor.as_matrix()
                 bcmotor=np_dfmotor[0][11]
                 
                 dfmotor=df[df.Motor != 0]
                 dfmotor = dfmotor.sort_values(['CA'], ascending=[False])
                 np_dfmotor=dfmotor.as_matrix()
                 acmotor=np_dfmotor[0][12]
                 
                 dfmotor=df[df.Motor != 0]
                 dfmotor = dfmotor.sort_values(['3-Phase'], ascending=[False])
                 np_dfmotor=dfmotor.as_matrix()
                 abcmotor=np_dfmotor[0][13]
                 Imh=[abmotor,bcmotor,acmotor,abcmotor]
                 Imh=sorted(Imh)
                 highestmotor=Imh[3]
                 Icb=It+1.5*highestmotor
                 Iwire=It+0.25*highestmotor
                 print "Highest AB Motor(A): "+str(abmotor)
                 print "Highest BC Motor(A): "+str(bcmotor)
                 print "Highest AC Motor(A): "+str(acmotor)
                 print "Highest ABC Motor(A): "+str(abcmotor)
                 print "Highest Rated Motor(A): "+str(highestmotor)
                 
             except:
                 Icb=It
                 Iwire=It
                 highestmotor=0
             
             print "Itab: "+str(Itab)
             print "Itbc: "+str(Itbc)
             print "Itac: "+str(Itac)
             print "Itabc: "+str(Itabc)
             print "Icb: "+str(Icb)
             print "Iwire: "+str(Iwire)
             atdata="ATParse.csv"
             dfat=pd.read_csv(atdata,names=['AT','Low','High'],skiprows=1)
             np_dfat = dfat.as_matrix()
             
             atcnt=0
             for i in xrange(len(np_dfat)):
                   
                   if Icb>np_dfat[atcnt][1] and Icb<=np_dfat[atcnt][2]:
                         amperetrip=np_dfat[atcnt][0]
                         print "AT: "+str(amperetrip)
                   atcnt=atcnt+1
                   
             try:
                 self.l19.setText("")
                 afdata="AFParse.csv"
                 dfaf=pd.read_csv(afdata,names=['AF','AT'],skiprows=1)
                 afout=np.where(dfaf["AT"] == amperetrip)
                 np_dfaf = dfaf.as_matrix()
                 
                 afout=afout[0][0]
                 afout=np_dfaf[afout][0]
                 print "AF: "+str(afout)
             except:
                 afout="Out of Range"
                 print "Adjust AF Table: Out of Range"
                 self.l19.setText("Adjust AF Table: Out of Range")
             wiredata="MainWireParse.csv"
             dfwire=pd.read_csv(wiredata,names=['Size','A','B','C','D','E','F'],skiprows=1)
             np_dfwire = dfwire.as_matrix()
             wireat=Iwire
             if wireflag==1:
                 
                 if wireat<=405:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][1] and wireat<=np_dfwire[wirecnt+1][1]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>405 and wireat<=445:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>445:
                     wireatout=wireat
                     while wireatout>445:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][1] and wireatout<=np_dfwire[wirecnt+1][1]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==2:
                 
                 if wireat<=485:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][2] and wireat<=np_dfwire[wirecnt+1][2]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>485 and wireat<=540:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>540:
                     wireatout=wireat
                     while wireatout>540:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][2] and wireatout<=np_dfwire[wirecnt+1][2]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==3:
                 
                 if wireat<=515:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][3] and wireat<=np_dfwire[wirecnt+1][3]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>515 and wireat<=580:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>580:
                     wireatout=wireat
                     while wireatout>580:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][3] and wireatout<=np_dfwire[wirecnt+1][3]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==4:
                 
                 if wireat<=335:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][4] and wireat<=np_dfwire[wirecnt+1][4]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>335 and wireat<=370:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>370:
                     wireatout=wireat
                     while wireatout>370:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][4] and wireatout<=np_dfwire[wirecnt+1][4]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==5:
                 
                 if wireat<=405:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][5] and wireat<=np_dfwire[wirecnt+1][5]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>405 and wireat<=440:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>440:
                     wireatout=wireat
                     while wireatout>440:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][5] and wireatout<=np_dfwire[wirecnt+1][5]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             elif wireflag==6:
                 
                 if wireat<=460:
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireat>np_dfwire[wirecnt][6] and wireat<=np_dfwire[wirecnt+1][6]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
                 elif wireat>460 and wireat<=495:
                     wiresize=np_dfwire[wirecnt+1][0]
                     print "Wire Size:"+str(wiresize)
                 elif wireat>495:
                     wireatout=wireat
                     while wireatout>495:
                         if wireset<2:
                             wireset=wireset+1
                         wireatout=wireat/wireset
                         wireset=wireset+1
                     print "AT: "+str(wireatout)
                     wirecnt=0
                     for i in xrange(len(np_dfwire)-1):
                         
                            if wireatout>np_dfwire[wirecnt][6] and wireatout<=np_dfwire[wirecnt+1][6]:
                             
                                 wiresize=np_dfwire[wirecnt+1][0]
                                 print "Wire Size:"+str(wiresize)
                             
                            wirecnt=wirecnt+1
             grounddata="groundwire.csv"
             dfground=pd.read_csv(grounddata,names=['AT','Copper','Aluminum'],skiprows=1)
          
             if groundtype==0:
                 np_dfground = dfground.as_matrix()
                 groundcnt=0
                 groundat=Iwire
                 for i in xrange(len(np_dfground)-1):
                     
                        if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                         
                             groundsize=np_dfground[groundcnt+1][1]
                             print "Ground Wire: "+str(groundsize)
                         
                        groundcnt=groundcnt+1
             elif groundtype==1:
                 np_dfground = dfground.as_matrix()
                 groundcnt=0
                 groundat=amperetrip
                 for i in xrange(len(np_dfground)-1):
                     
                        if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                         
                             groundsize=np_dfground[groundcnt+1][2]
                             print "Ground Wire: "+str(groundsize)
                         
                        groundcnt=groundcnt+1
             totalwire=3
             try:
                 self.l19.setText("")
                 if conduitflag==1:
                    conduitrange=10
                    if emtflag==1:
                        pathwire="conduit_csv/emt_A.csv"
                    elif emtflag==2:
                        pathwire="conduit_csv/emt_B.csv"
                    elif emtflag==3:
                        pathwire="conduit_csv/emt_C.csv"
                    elif emtflag==4:
                        pathwire="conduit_csv/emt_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                     
                 elif conduitflag==2:
                    conduitrange=6
                    if entflag==1:
                        pathwire="conduit_csv/ent_A.csv"
                    elif entflag==2:
                        pathwire="conduit_csv/ent_B.csv"
                    elif entflag==3:
                        pathwire="conduit_csv/ent_C.csv"
                    elif entflag==4:
                        pathwire="conduit_csv/ent_D.csv"
                    elif entflag==5:
                        pathwire="conduit_csv/ent_E.csv"
                            
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F'],skiprows=1)
                    
                 elif conduitflag==3:
                    conduitrange=10
                    if fmcflag==1:
                        pathwire="conduit_csv/fmc_A.csv"
                    elif fmcflag==2:
                        pathwire="conduit_csv/fmc_B.csv"
                    elif fmcflag==3:
                        pathwire="conduit_csv/fmc_C.csv"
                    elif fmcflag==4:
                        pathwire="conduit_csv/fmc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)  
                 elif conduitflag==4:
                    conduitrange=10
                    if imcflag==1:
                        pathwire="conduit_csv/imc_A.csv"
                    elif imcflag==2:
                        pathwire="conduit_csv/imc_B.csv"
                    elif imcflag==3:
                        pathwire="conduit_csv/imc_C.csv"
                    elif imcflag==4:
                        pathwire="conduit_csv/imc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                 elif conduitflag==5:
                    conduitrange=7
                    if lfnmcflag==1:
                        pathwire="conduit_csv/lfnmc_A.csv"
                    elif lfnmcflag==2:
                        pathwire="conduit_csv/lfnmc_B.csv"
                    elif lfnmcflag==3:
                        pathwire="conduit_csv/lfnmc_C.csv"
                    elif lfnmcflag==4:
                        pathwire="conduit_csv/lfnmc_D.csv"
                    
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G'],skiprows=1)
                 elif conduitflag==6:
                    conduitrange=10
                    if lfmcflag==1:
                        pathwire="conduit_csv/lfmc_A.csv"
                    elif lfmcflag==2:
                        pathwire="conduit_csv/lfmc_B.csv"
                    elif lfmcflag==3:
                        pathwire="conduit_csv/lfmc_C.csv"
                    elif lfmcflag==4:
                        pathwire="conduit_csv/lfmc_D.csv"
                    elif lfmcflag==5:
                        pathwire="conduit_csv/lfmc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                 elif conduitflag==7:
                    conduitrange=12
                    if rmcflag==1:
                        pathwire="conduit_csv/rmc_A.csv"
                    elif rmcflag==2:
                        pathwire="conduit_csv/rmc_B.csv"
                    elif rmcflag==3:
                        pathwire="conduit_csv/rmc_C.csv"
                    elif rmcflag==4:
                        pathwire="conduit_csv/rmc_D.csv"
                    elif rmcflag==5:
                        pathwire="conduit_csv/rmc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                 elif conduitflag==8:
                    conduitrange=12
                    if rpvcflag==1:
                        pathwire="conduit_csv/rpvc_A.csv"
                    elif rpvcflag==2:
                        pathwire="conduit_csv/rpvc_B.csv"
                    elif rpvcflag==3:
                        pathwire="conduit_csv/rpvc_C.csv"
                    elif rpvcflag==4:
                        pathwire="conduit_csv/rpvc_D.csv"
                    elif rpvcflag==5:
                        pathwire="conduit_csv/rpvc_E.csv"
                    dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                 
                 print pathwire
                 
                 wireid=np.where(dfw["Output"] == wiresize)
                 np_dfw = dfw.as_matrix()
                 wireid=wireid[0][0]
             except:
                 self.l19.setText("Wire Size Out of Range on Selected Type of Wire and Conduit.")
         
             conduitcnt=1
             for i in xrange(10): 
                    try:
                        
                        
                        if np_dfw[wireid][conduitcnt]!=np_dfw[wireid][conduitcnt+1] and totalwire>np_dfw[wireid][conduitcnt]:
                            if totalwire>np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                 
                                 conduitsize=np_dfw[0][conduitcnt+1]
                                 
                        elif totalwire<=np_dfw[wireid][1]:
                            conduitsize=np_dfw[0][1]
                            
                        else:
                             if totalwire>=np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                 
                                 conduitsize=np_dfw[0][conduitcnt+1]
                                 
                    except:
                         print ""
                    conduitcnt=conduitcnt+1
             print "Conduit Size: "+str(conduitsize) 
             pathsave="outputdata.csv"

             columns = ['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory']
             df = pd.DataFrame(columns=columns)
             df = df.append({'Panel':pathtarget,'AT':amperetrip,'AF':afout, 'Sets':1,'WireSize':wiresize,'TypeWire':wiredisp,'GroundingWire':groundsize,'Conduit':conduitsize,'ConduitType':conduitdisp,'Directory':directory}, ignore_index=True)

             df.to_csv(pathsave,  index = False)
             pathmp=directory+"/mpout.csv"

             columns = ['DemandFactor','Area','Wireflag','Areaflag']
             df = pd.DataFrame(columns=columns)
             df = df.append({'DemandFactor':demandfactor,'Area':unitarea,'Wireflag':wireflag,'Areaflag':areaflag}, ignore_index=True)

             df.to_csv(pathmp,  index = False)


             pathmain=str(self.n2.text())+"/mainpanel.csv"
             if os.path.exists(pathmain):
                 
                 df=pd.read_csv(pathmain,names=['Circuit','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','AB',
                                                  'BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting','HRM','Subflag'],skiprows=1)
                 np_df = df.as_matrix()
                 df = df.append({'Circuit':len(np_df)+1, 'LoadDescription':panelboard,'Rating':vatotal,'Voltage':230,'Wireset':1,
                                         'Wirenumber':4,'AT':amperetrip,'AF':afout,'AB':Itab,'BC':Itbc,'CA':Itac,'3-Phase':Itabc,
                                         'WireSize':wiresize,'GroundSize':groundsize,'ConduitSize':conduitsize,'Lighting':lightingtotal,'HRM':highestmotor,'Subflag':0}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print df
             else:
                 columns = ['Circuit','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting','HRM','Subflag']
                 df = pd.DataFrame(columns=columns)
                 np_df = df.as_matrix()
                 
                 df = df.append({'Circuit':len(np_df)+1, 'LoadDescription':panelboard,'Rating':vatotal,'Voltage':230,'Wireset':1,
                                         'Wirenumber':4,'AT':amperetrip,'AF':afout,'AB':Itab,'BC':Itbc,'CA':Itac,'3-Phase':Itabc,
                                         'WireSize':wiresize,'GroundSize':groundsize,'ConduitSize':conduitsize,'Lighting':lightingtotal,'HRM':highestmotor,'Subflag':0}, ignore_index=True)
                 df.to_csv(pathmain,  index = False)
                 print df
             
             
             self.accept()
             self.close()
             self.outputpanelcommercial.exec_()

                     
    def adddata(self,cx):
          global airconflag,ampflag,unitflag,specflag,ampere,appliancesflag,wireflag,groundtype,emtflag,entflag,fmcflag,imcflag,lfnmcflag,lfmcflag,rmcflag,rpvcflag,conduitflag,phaseflag,otherflag,dryerflag,wiredisp,conduitdisp,spareflag,spaceflag
          directory=str(self.n2.text())
          if directory!="":
                 if not os.path.exists(directory):
                     os.makedirs(directory)
          
          panelboard=str(self.l3.text())
          pathtarget=directory+"/"+panelboard+".csv"
          loadname=str(self.l10.text())
          rating=str(self.l12.text())
          quantity=str(self.l14.text())
          if directory=="":
             self.l19.setText("Indicate project name.")
          elif panelboard=="":
             self.l19.setText("Indicate panel board.")
          elif ampflag==0:
             self.l19.setText("Please select type of load.")
          elif specflag==0 and ampflag!=1:
             self.l19.setText("Please select specific load.")
          elif loadname=="":
             self.l19.setText("Indicate load name.")
          elif rating=="":
             self.l19.setText("Input rating.")
            
          elif quantity=="":
             self.l19.setText("Input quantity.")
          elif wireflag==0:
             self.l19.setText("Please select type of wire.")
          elif conduitflag==0:
             self.l19.setText("Please select type of conduit.")
          elif phaseflag==0:
             self.l19.setText("Please select type of phase.") 
          if rating!="":
             try:
                 rating=float(self.l12.text())
             except:
                 self.l19.setText("Invalid input for rating.")     
          if quantity!="":
             try:    
                 quantity=int(self.l14.text())
             except:
                 self.l19.setText("Invalid input for quantity.")
          
          
          
          
          if wireflag!=0 and conduitflag!=0 and phaseflag!=0:###
              if otherflag!=3:
                 #try:  
                     voltage=230
      
                     wireset=1
                     if phaseflag==1 or phaseflag==2 or phaseflag==3:
                          wirenumber=3
                     elif phaseflag==4:
                         wirenumber=4
                     totalwire=wireset*wirenumber    
                     self.l19.setText("")
                     
                     
                     if ampflag==1:
                          typeflag=0
                          lightingflag=1
                          if specflag==1:
                              ampere=0
                          else:
                             if unitflag==1:
                                 rating=float(self.l12.text())
                             elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                             quantity=float(self.l14.text())
                             ampere=(rating*quantity)/230
                     elif ampflag==2:
                         typeflag=0
                         lightingflag=0
                         if unitflag==1:
                             rating=float(self.l12.text())
                         elif unitflag==2:
                             rating=float(self.l12.text())*1000
                         quantity=float(self.l14.text())
                         pathid="cookingappliance.csv"
                         df=pd.read_csv(pathid,names=['Qty','A','B','C'],skiprows=1)
                         if ((df['Qty'] == quantity)).any()==True:
                             cookid=np.where(df["Qty"] == quantity)
                             np_df = df.as_matrix()
                             numid=cookid[0][0]
                             A=float(np_df[numid][1])/100
                             B=float(np_df[numid][2])/100
                             C=float(np_df[numid][3])/100
                         
                             if rating<3500 and quantity<=60:
                                 ampere=((rating*quantity)/230)*A
                             elif rating>=3500 and rating<=8750 and quantity<=60:
                                 ampere=((rating*quantity)/230)*B
                             elif rating>8750 and quantity<26:
                                 ampere=((rating*quantity)/230)*C
                             elif rating>8750 and quantity>=26 and quantity<41:
                                 ampere=((1000*quantity+15000)/230)
                             elif rating>8750 and quantity<61 and quantity>=41:
                                 ampere=((750*quantity+25000)/230)
                         else:
                             if rating<3500 and quantity>=61:
                                 ampere=((rating*quantity)/230)*0.3
                             elif rating>=3500 and rating<=8750 and quantity>=61:
                                 ampere=((rating*quantity)/230)*0.16
                             elif rating>8750 and quantity>=61:
                                 ampere=((750*quantity+25000)/230)
                                     
                             
                     elif ampflag==3:
                         typeflag=1
                         lightingflag=0
                         if phaseflag==1 or phaseflag==2 or phaseflag==3:
                             pathid="motorload.csv"
                         elif phaseflag==4:
                             pathid="motorloadtri.csv"
                         df=pd.read_csv(pathid,names=['Motor','Ampere','VA'],skiprows=1)
                         ratingmotor=self.l12.text()
                         if unitflag==1:
                             if ((df['Motor'] == ratingmotor)).any()==True:
                                 
                                 motorid=np.where(df["Motor"] == ratingmotor)
                                 np_df = df.as_matrix()
                                 numid=motorid[0][0]
                                 ampere=float(np_df[numid][1])
                                 rating=float(np_df[numid][2])
                             else:
                                 ampere="Out of Range"
                         elif unitflag==2:
                             rating=float(self.l12.text())
                             if phaseflag==1 or phaseflag==2 or phaseflag==3:
                                 ampere=(rating)/230
                             elif phaseflag==4:
                                 ampere=(rating)/(math.sqrt(3)*230)
                             
                             
                     elif ampflag==4:
                          typeflag=0
                          lightingflag=0
                          if appliancesflag==1:
                              rating=180
                              quantity=float(self.l14.text())
                              ampere=(rating*quantity)/230
                          elif appliancesflag==0:
                             if unitflag==1:
                                 rating=float(self.l12.text())
                             elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                             quantity=float(self.l14.text())
                             ampere=(rating*quantity)/230
                     elif ampflag==5:
                          typeflag=0
                          lightingflag=0
                          if otherflag==1:
                             if unitflag==1:
                                 rating=float(self.l12.text())
                             elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                             ampere=(rating*quantity)/230
                          elif otherflag==2:
                             if unitflag==1:
                                 rating=float(self.l12.text())
                             elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                             ampere=(rating*quantity)/(math.sqrt(3)*230)
                          elif otherflag==3:
                              ampere=0
                          elif otherflag==4:
                             if unitflag==1:
                                 rating=float(self.l12.text())
                             elif unitflag==2:
                                 rating=float(self.l12.text())*1000
                             if phaseflag==1 or phaseflag==2 or phaseflag==3:
                                 ampere=(rating*quantity)/230
                             elif phaseflag==4:
                                 ampere=(rating*quantity)/(math.sqrt(3)*230)
                     elif ampflag==6:
                          typeflag=0
                          lightingflag=0
                          rating=float(self.l12.text())
                          if dryerflag==1:
                             if phaseflag==1 or phaseflag==2 or phaseflag==3:
                                 ampere=(rating*quantity)/230
                             elif phaseflag==4:
                                 ampere=(rating*quantity)/(math.sqrt(3)*230)
                          elif dryerflag==2:
                              if phaseflag==1 or phaseflag==2 or phaseflag==3:
                                  if quantity>=1 and quantity<=4:
                                      ampere=((rating*quantity)/230)*1
                                  elif quantity==5:
                                      ampere=((rating*quantity)/230)*0.85
                                  elif quantity==6:
                                      ampere=((rating*quantity)/230)*0.75
                                  elif quantity==7:
                                      ampere=((rating*quantity)/230)*0.65
                                  elif quantity==8:
                                      ampere=((rating*quantity)/230)*0.60
                                  elif quantity==9:
                                      ampere=((rating*quantity)/230)*0.55
                                  elif quantity==10:
                                      ampere=((rating*quantity)/230)*0.50
                                  elif quantity==11:
                                      ampere=((rating*quantity)/230)*0.47
                                  elif quantity>=12 and quantity<=22:
                                      ampere=((rating*quantity)/230)*(47-(quantity-11))*0.01
                                  elif quantity==23:
                                      ampere=((rating*quantity)/230)*0.35
                                  elif quantity>=24 and quantity<=42:
                                      ampere=((rating*quantity)/230)*(0.5*(quantity-23))*0.01
                                  elif quantity>=43:
                                      ampere=((rating*quantity)/230)*0.25
                              elif phaseflag==4:
                                  if quantity>=1 and quantity<=4:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*1
                                  elif quantity==5:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.85
                                  elif quantity==6:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.75
                                  elif quantity==7:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.65
                                  elif quantity==8:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.60
                                  elif quantity==9:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.55
                                  elif quantity==10:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.50
                                  elif quantity==11:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.47
                                  elif quantity>=12 and quantity<=22:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*(47-(quantity-11))*0.01
                                  elif quantity==23:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.35
                                  elif quantity>=24 and quantity<=42:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*(0.5*(quantity-23))*0.01
                                  elif quantity>=43:
                                      ampere=((rating*quantity)/(math.sqrt(3)*230))*0.25
                              
                              
                              
                     else:
                         ampere=0
                     ampere=round(ampere, 2)
                     if phaseflag==1:
                         ab=ampere
                         bc=0
                         ac=0
                         abc=0
                     elif phaseflag==2:
                         ab=0
                         bc=ampere
                         ac=0
                         abc=0
                     elif phaseflag==3:
                         ab=0
                         bc=0
                         ac=ampere
                         abc=0
                     elif phaseflag==4:
                         ab=0
                         bc=0
                         ac=0
                         abc=ampere
                     
                     if typeflag==1:
                         wireat=ampere*1.25
                         atampere=ampere*2.5
                     else:    
                         wireat=ampere/0.8
                         atampere=ampere/0.8
                     
                     print "Wire Reference: "+str(wireat)
                     print "AT Reference: "+str(atampere)
                     atdata="ATParse.csv"
                     dfat=pd.read_csv(atdata,names=['AT','Low','High'],skiprows=1)
                     np_dfat = dfat.as_matrix()
                     atcnt=0
                     for i in xrange(len(np_dfat)):
                           if atampere>np_dfat[atcnt][1] and atampere<=np_dfat[atcnt][2]:
                                 amperetrip=np_dfat[atcnt][0]
                                 
                           atcnt=atcnt+1
                     wiredata="WireParse.csv"
                     dfwire=pd.read_csv(wiredata,names=['Size','A','B','C','D','E','F'],skiprows=1)
                     np_dfwire = dfwire.as_matrix()
                     if airconflag==1 and ampflag==3 and amperetrip<=30:
                                                    amperetrip=30
                     print "AT: "+str(amperetrip)

                     
                     if wireflag==1:
                         
                         if wireat<=405:
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireat>np_dfwire[wirecnt][1] and wireat<=np_dfwire[wirecnt+1][1]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                         elif wireat>405 and wireat<=445:
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         elif wireat>445:
                             wireatout=wireat
                             while wireatout>445:
                                 if wireset<2:
                                     wireset=wireset+1
                                 wireatout=wireat/wireset
                                 wireset=wireset+1
                             print "AT: "+str(wireatout)
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireatout>np_dfwire[wirecnt][1] and wireatout<=np_dfwire[wirecnt+1][1]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                     elif wireflag==2:
                         
                         if wireat<=485:
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireat>np_dfwire[wirecnt][2] and wireat<=np_dfwire[wirecnt+1][2]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                         elif wireat>485 and wireat<=540:
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         elif wireat>540:
                             wireatout=wireat
                             while wireatout>540:
                                 if wireset<2:
                                     wireset=wireset+1
                                 wireatout=wireat/wireset
                                 wireset=wireset+1
                             print "AT: "+str(wireatout)
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireatout>np_dfwire[wirecnt][2] and wireatout<=np_dfwire[wirecnt+1][2]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                     elif wireflag==3:
                         
                         if wireat<=515:
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireat>np_dfwire[wirecnt][3] and wireat<=np_dfwire[wirecnt+1][3]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                         elif wireat>515 and wireat<=580:
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         elif wireat>580:
                             wireatout=wireat
                             while wireatout>580:
                                 if wireset<2:
                                     wireset=wireset+1
                                 wireatout=wireat/wireset
                                 wireset=wireset+1
                             print "AT: "+str(wireatout)
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireatout>np_dfwire[wirecnt][3] and wireatout<=np_dfwire[wirecnt+1][3]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                     elif wireflag==4:
                         
                         if wireat<=335:
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireat>np_dfwire[wirecnt][4] and wireat<=np_dfwire[wirecnt+1][4]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                         elif wireat>335 and wireat<=370:
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         elif wireat>370:
                             wireatout=wireat
                             while wireatout>370:
                                 if wireset<2:
                                     wireset=wireset+1
                                 wireatout=wireat/wireset
                                 wireset=wireset+1
                             print "AT: "+str(wireatout)
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireatout>np_dfwire[wirecnt][4] and wireatout<=np_dfwire[wirecnt+1][4]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                     elif wireflag==5:
                         
                         if wireat<=405:
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireat>np_dfwire[wirecnt][5] and wireat<=np_dfwire[wirecnt+1][5]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                         elif wireat>405 and wireat<=440:
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         elif wireat>440:
                             wireatout=wireat
                             while wireatout>440:
                                 if wireset<2:
                                     wireset=wireset+1
                                 wireatout=wireat/wireset
                                 wireset=wireset+1
                             print "AT: "+str(wireatout)
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireatout>np_dfwire[wirecnt][5] and wireatout<=np_dfwire[wirecnt+1][5]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                     elif wireflag==6:
                         
                         if wireat<=460:
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireat>np_dfwire[wirecnt][6] and wireat<=np_dfwire[wirecnt+1][6]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                         elif wireat>460 and wireat<=495:
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         elif wireat>495:
                             wireatout=wireat
                             while wireatout>495:
                                 if wireset<2:
                                     wireset=wireset+1
                                 wireatout=wireat/wireset
                                 wireset=wireset+1
                             print "AT: "+str(wireatout)
                             wirecnt=0
                             for i in xrange(len(np_dfwire)-1):
                                 
                                    if wireatout>np_dfwire[wirecnt][6] and wireatout<=np_dfwire[wirecnt+1][6]:
                                     
                                         wiresize=np_dfwire[wirecnt+1][0]
                                         print "Wire Size:"+str(wiresize)
                                     
                                    wirecnt=wirecnt+1
                     try:
                         self.l19.setText("")
                         afdata="AFParse.csv"
                         dfaf=pd.read_csv(afdata,names=['AF','AT'],skiprows=1)
                         afout=np.where(dfaf["AT"] == amperetrip)
                         np_dfaf = dfaf.as_matrix()
                         
                         afout=afout[0][0]
                         afout=np_dfaf[afout][0]
                         print "AF: "+str(afout)
                     except:
                         afout="Out of Range"
                         print "Adjust AF Table: Out of Range"
                         self.l19.setText("Adjust AF Table: Out of Range")
                         
                     grounddata="groundwire.csv"
                     dfground=pd.read_csv(grounddata,names=['AT','Copper','Aluminum'],skiprows=1)
                     
           
                     if groundtype==0:
                         np_dfground = dfground.as_matrix()
                         groundcnt=0
                         groundat=amperetrip
                         for i in xrange(len(np_dfground)-1):
                             
                                if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                                 
                                     groundsize=np_dfground[groundcnt+1][1]
                                     print "Ground Wire: "+str(groundsize)
                                 
                                groundcnt=groundcnt+1
                     elif groundtype==1:
                         np_dfground = dfground.as_matrix()
                         groundcnt=0
                         groundat=amperetrip
                         for i in xrange(len(np_dfground)-1):
                             
                                if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                                 
                                     groundsize=np_dfground[groundcnt+1][2]
                                     print "Ground Wire: "+str(groundsize)
                                 
                                groundcnt=groundcnt+1
                     
                     if conduitflag==1:
                        conduitrange=10
                        if emtflag==1:
                            pathwire="conduit_csv/emt_A.csv"
                        elif emtflag==2:
                            pathwire="conduit_csv/emt_B.csv"
                        elif emtflag==3:
                            pathwire="conduit_csv/emt_C.csv"
                        elif emtflag==4:
                            pathwire="conduit_csv/emt_D.csv"
                        
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                         
                     elif conduitflag==2:
                        conduitrange=6
                        if entflag==1:
                            pathwire="conduit_csv/ent_A.csv"
                        elif entflag==2:
                            pathwire="conduit_csv/ent_B.csv"
                        elif entflag==3:
                            pathwire="conduit_csv/ent_C.csv"
                        elif entflag==4:
                            pathwire="conduit_csv/ent_D.csv"
                        elif entflag==5:
                            pathwire="conduit_csv/ent_E.csv"
                                
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F'],skiprows=1)
                        
                     elif conduitflag==3:
                        conduitrange=10
                        if fmcflag==1:
                            pathwire="conduit_csv/fmc_A.csv"
                        elif fmcflag==2:
                            pathwire="conduit_csv/fmc_B.csv"
                        elif fmcflag==3:
                            pathwire="conduit_csv/fmc_C.csv"
                        elif fmcflag==4:
                            pathwire="conduit_csv/fmc_D.csv"
                        
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)  
                     elif conduitflag==4:
                        conduitrange=10
                        if imcflag==1:
                            pathwire="conduit_csv/imc_A.csv"
                        elif imcflag==2:
                            pathwire="conduit_csv/imc_B.csv"
                        elif imcflag==3:
                            pathwire="conduit_csv/imc_C.csv"
                        elif imcflag==4:
                            pathwire="conduit_csv/imc_D.csv"
                        
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                     elif conduitflag==5:
                        conduitrange=7
                        if lfnmcflag==1:
                            pathwire="conduit_csv/lfnmc_A.csv"
                        elif lfnmcflag==2:
                            pathwire="conduit_csv/lfnmc_B.csv"
                        elif lfnmcflag==3:
                            pathwire="conduit_csv/lfnmc_C.csv"
                        elif lfnmcflag==4:
                            pathwire="conduit_csv/lfnmc_D.csv"
                        
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G'],skiprows=1)
                     elif conduitflag==6:
                        conduitrange=10
                        if lfmcflag==1:
                            pathwire="conduit_csv/lfmc_A.csv"
                        elif lfmcflag==2:
                            pathwire="conduit_csv/lfmc_B.csv"
                        elif lfmcflag==3:
                            pathwire="conduit_csv/lfmc_C.csv"
                        elif lfmcflag==4:
                            pathwire="conduit_csv/lfmc_D.csv"
                        elif lfmcflag==5:
                            pathwire="conduit_csv/lfmc_E.csv"
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                     elif conduitflag==7:
                        conduitrange=12
                        if rmcflag==1:
                            pathwire="conduit_csv/rmc_A.csv"
                        elif rmcflag==2:
                            pathwire="conduit_csv/rmc_B.csv"
                        elif rmcflag==3:
                            pathwire="conduit_csv/rmc_C.csv"
                        elif rmcflag==4:
                            pathwire="conduit_csv/rmc_D.csv"
                        elif rmcflag==5:
                            pathwire="conduit_csv/rmc_E.csv"
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                     elif conduitflag==8:
                        conduitrange=12
                        if rpvcflag==1:
                            pathwire="conduit_csv/rpvc_A.csv"
                        elif rpvcflag==2:
                            pathwire="conduit_csv/rpvc_B.csv"
                        elif rpvcflag==3:
                            pathwire="conduit_csv/rpvc_C.csv"
                        elif rpvcflag==4:
                            pathwire="conduit_csv/rpvc_D.csv"
                        elif rpvcflag==5:
                            pathwire="conduit_csv/rpvc_E.csv"
                        dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
                     
                     print pathwire
                     wireid=np.where(dfw["Output"] == wiresize)
                     np_dfw = dfw.as_matrix()
                     wireid=wireid[0][0]
                 
                     conduitcnt=1
                     for i in xrange(conduitrange): 
                            try:
                                
                                
                                if np_dfw[wireid][conduitcnt]!=np_dfw[wireid][conduitcnt+1] and totalwire>np_dfw[wireid][conduitcnt]:
                                    if totalwire>np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                         
                                         conduitsize=np_dfw[0][conduitcnt+1]
                                         
                                elif totalwire<=np_dfw[wireid][1]:
                                    conduitsize=np_dfw[0][1]
                                    
                                else:
                                     if totalwire>=np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                                         
                                         conduitsize=np_dfw[0][conduitcnt+1]
                                         
                            except:
                                 print ""
                            conduitcnt=conduitcnt+1
                     print "Conduit Size: "+str(conduitsize)
                     if ampflag==5 and spareflag==1:

                             conduitsize=0
                             groundsize=0
                             wiresize=0
                     if ampflag==5 and spaceflag==1:
                             conduitsize=0
                             groundsize=0
                             wiresize=0
                             ab=0
                             bc=0
                             ac=0
                             abc=0
                             rating=0
                             amperetrip=0
                             afout=0
                             wirenumber=0
                             wireset=0
                     if os.path.exists(pathtarget):
                         
                         df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
                         np_df = df.as_matrix()
                         df = df.append({'Circuit':len(np_df)+1, 'Quantity':quantity, 'LoadDescription':loadname,'Rating':rating,'Voltage':230,'Wireset':wireset,
                                         'Wirenumber':wirenumber,'AT':amperetrip,'AF':afout,'Motor':typeflag,'AB':ab,'BC':bc,'CA':ac,'3-Phase':abc,'WireSize':wiresize,
                                         'GroundSize':groundsize,'ConduitSize':conduitsize,'Lighting':lightingflag}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         print df
                     else:
                         
                         columns = ['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting']
                         df = pd.DataFrame(columns=columns)
                         np_df = df.as_matrix()
                         
                         df = df.append({'Circuit':len(np_df)+1, 'Quantity':quantity, 'LoadDescription':loadname,'Rating':rating,'Voltage':230,'Wireset':wireset,
                                         'Wirenumber':wirenumber,'AT':amperetrip,'AF':afout,'Motor':typeflag,'AB':ab,'BC':bc,'CA':ac,'3-Phase':abc,
                                         'WireSize':wiresize,'GroundSize':groundsize,'ConduitSize':conduitsize,'Lighting':lightingflag}, ignore_index=True)
                         df.to_csv(pathtarget,  index = False)
                         print df
                     
                     cnt=0
                     np_df = df.as_matrix()
                     self.table.setRowCount(len(np_df))
                     for i in xrange(len(np_df)):
                         self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(int(cnt+1))))
                         self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][1]))))
                         self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])))
                         self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])))
                         cnt=cnt+1
                     columns = ['Wire Type','Conduit Type']
                     pathhistory="history.csv"
                     df = pd.DataFrame(columns=columns)
                     np_df = df.as_matrix()
                     df = df.append({'Wire Type':wiredisp,'Conduit Type':conduitdisp}, ignore_index=True)
                     df.to_csv(pathhistory,  index = False)
             #except:
                   #self.l19.setText("Please fill up all required information.")
              else:
                 if os.path.exists(pathtarget):
                     
                     df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
                     np_df = df.as_matrix()
                     df = df.append({'Circuit':len(np_df)+1, 'Quantity':quantity, 'LoadDescription':loadname,'Rating':0,'Voltage':230,'Wireset':0,'Wirenumber':0,'AT':0,'AF':0,'Motor':0,'AB':0,'BC':0,'CA':0,'3-Phase':0,'WireSize':0,'GroundSize':0,'ConduitSize':0,'Lighting':0}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                 else:
                     
                     columns = ['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting']
                     df = pd.DataFrame(columns=columns)
                     np_df = df.as_matrix()
                     
                     df = df.append({'Circuit':len(np_df)+1, 'Quantity':quantity, 'LoadDescription':loadname,'Rating':0,'Voltage':230,'Wireset':0,'Wirenumber':0,'AT':0,'AF':0,'Motor':0,'AB':0,'BC':0,'CA':0,'3-Phase':0,'WireSize':0,'GroundSize':0,'ConduitSize':0,'Lighting':0}, ignore_index=True)
                     df.to_csv(pathtarget,  index = False)
                     print df
                 
                 cnt=0
                 np_df = df.as_matrix()
                 self.table.setRowCount(len(np_df))
                 for i in xrange(len(np_df)):
                     self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(int(cnt+1))))
                     self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][1]))))
                     self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])))
                     self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])))
                     cnt=cnt+1
            
    def deletedata(self,dx):
         directory=str(self.n2.text())
         if not os.path.exists(directory):
             os.makedirs(directory)
         panelboard=str(self.l3.text())
         pathtarget=directory+"/"+panelboard+".csv"
         x=0
         indexes = self.table.selectionModel().selectedRows()
         for index in sorted(indexes):
            print index.row()
         df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
         df.drop(index.row(), inplace=True)
         df = df.reset_index(drop=True)
         df.to_csv(pathtarget,  index = False)
         np_df = df.as_matrix()
         cnt=0
         print np_df
         
         columns = ['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting']
         df = pd.DataFrame(columns=columns)
         for i in xrange(len(np_df)):
             
             df = df.append({'Circuit':cnt+1, 'Quantity':np_df[cnt][1], 'LoadDescription':np_df[cnt][2],'Rating':np_df[cnt][3],'Voltage':np_df[cnt][4],'Wireset':np_df[cnt][5],'Wirenumber':np_df[cnt][6],'AT':np_df[cnt][7],
                             'AF':np_df[cnt][8],'Motor':np_df[cnt][9],'AB':np_df[cnt][10],'BC':np_df[cnt][11],'CA':np_df[cnt][12],'3-Phase':np_df[cnt][13],'WireSize':np_df[cnt][14],'GroundSize':np_df[cnt][15],
                             'ConduitSize':np_df[cnt][16],'Lighting':np_df[cnt][17]}, ignore_index=True)
             cnt=cnt+1
         df.to_csv(pathtarget,  index = False)
         cnt=0
         np_df = df.as_matrix()
         self.table.setRowCount(len(np_df))
         for i in xrange(len(np_df)):
             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(int(cnt+1))))
             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][1]))))
             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])))
             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])))
             cnt=cnt+1
    def loaddata(self,dx):
         try:
             self.l19.setText("")
             panelboard=str(self.l3.text())
             directory=str(self.n2.text())
             if not os.path.exists(directory):
                 os.makedirs(directory)
             panelboard=str(self.l3.text())
             pathtarget=directory+"/"+panelboard+".csv"
             df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
             np_df = df.as_matrix()
             self.table.setRowCount(len(np_df))
             cnt=0
             for i in xrange(len(np_df)):
                 self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+"            "+str(int(cnt+1))+"             "))
                 self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][1]))))
                 self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])))
                 self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])))
                 cnt=cnt+1
             
         except:
             self.l19.setText("File doesn't exist.")
    def typeselect(self,ex):
        global ampflag,specflag,otherflag
        self.specload.clear()
        self.unitload.clear()
        if ex==1:
            ampflag=1
            self.specload.addItems([])
            self.unitload.addItems(["VA","kW"])
            otherflag=1
            specflag=0
        elif ex==2:
            ampflag=4
            self.specload.addItems(["","General Purpose Receptacle","Special Purpose Receptacle",])
            self.unitload.addItems(["VA","kW"])
            specflag=0
        elif ex==3:
            ampflag=2
            
            self.specload.addItems(["","Microwave","Dishwasher","Electric range","Electric griller","Refrigerator","Cooking equipment"])
            self.unitload.addItems(["VA","kW"])
        elif ex==4:
            ampflag=6
            self.specload.addItems(["","Washing machine","Electric Dryer"])
            self.unitload.addItems(["VA"])
        elif ex==5:
            ampflag=3
            self.specload.addItems(["","Other Motor","Air conditioning units","Water pump","Compressor"])
            self.unitload.addItems(["HP","VA"])
        elif ex==6:
            ampflag=5
            self.specload.addItems(["","Specific Load","1-Phase Transformer","3-Phase Transformer","Spare","Space"])
            self.unitload.addItems(["VA","kW"])
            
        
    def loadselect(self,fx):
        global unitflag
        if fx==0:
            unitflag=1
        elif fx==1:
            unitflag=2
    def specselect(self,gx):
        global specflag,appliancesflag,otherflag,dryerflag,spareflag,spaceflag,airconflag
 
        if gx==1:
           appliancesflag=1
        elif gx==2:
           specflag=1
           appliancesflag=0
           airconflag=1
        elif gx==3:
           specflag=1
        else:
           airconflag=0 	
           specflag=0
           appliancesflag=0
        if  gx==1 or gx==4:
            otherflag=4
        elif gx==2:
            otherflag=1
        elif gx==3 :
            otherflag=2
       
        elif gx==5:
            otherflag=3
            
        if gx==4:
            spareflag=1
        else:
            spareflag=0
        if gx==5:
            spaceflag=1
        else:
            spaceflag=0
        if  gx==1:
            dryerflag=1
        elif gx==2:
            dryerflag=2
            
    
            
    def wireselect(self,hx):
        global wireflag,groundtype,emtflag,entflag,fmcflag,imcflag,lfnmcflag,lfmcflag,rmcflag,rpvcflag,wiredisp
        if hx==1 or hx==2:
            wireflag=1
        elif hx==3 or hx==4 or hx==5:
            wireflag=2
        elif hx==6 or hx==7 or hx==8 or hx==9 or hx==10:
            wireflag=3
        elif hx==11 or hx==12:
            wireflag=4
        elif hx==13 or hx==14 or hx==15:
            wireflag=5
        elif hx==16 or hx==17 or hx==18 or hx==19 or hx==20:
            wireflag=6
        if hx==1 or hx==2 or hx==3 or hx==4 or hx==5 or hx==6 or hx==7 or hx==8 or hx==9 or hx==10:
            groundtype=0
        elif hx==11 or hx==12 or hx==13 or hx==14 or hx==15 or hx==16 or hx==17 or hx==18 or hx==19 or hx==20:
            groundtype=1
        if hx==3 or hx==13 or hx==6 or hx==16:#RHW - RHH
            emtflag=1
            entflag=1
            fmcflag=1
            imcflag=1
            lfnmcflag=1
            lfmcflag=1
            rmcflag=1
            rpvcflag=1
        elif hx==1 or hx==11:#TW
            emtflag=2
            entflag=2
            fmcflag=2
            imcflag=2
            lfnmcflag=2
            lfmcflag=2
            rmcflag=2
            rpvcflag=2
        elif hx==8 or hx==18 or hx==4 or hx==14:#THHW - THW
            entflag=3
            fmcflag=2
            imcflag=2
            lfnmcflag=2
            lfmcflag=3
            rmcflag=3
            rpvcflag=3
        elif hx==7 or hx==17 or hx==5 or hx==15:#THHN - THWN
            emtflag=3
            entflag=4
            fmcflag=3
            imcflag=3
            lfnmcflag=3
            lfmcflag=4
            rmcflag=4
            rpvcflag=4
        
        elif hx==9 or hx==19 or hx==10 or hx==20:#XHH - XHHW
            emtflag=4
            entflag=5
            fmcflag=4
            imcflag=4
            lfnmcflag=4
            lfmcflag=5
            rmcflag=5
            rpvcflag=5
        if hx==1:
            wiredisp="TW"
        elif hx==2:
            wiredisp="UF"
        elif hx==3:
            wiredisp="RHW"
        elif hx==4:
            wiredisp="THW"
        elif hx==5:
            wiredisp="THWN"
        elif hx==6:
            wiredisp="RHH"
        elif hx==7:
            wiredisp="THHN"
        elif hx==8:
            wiredisp="THHW"
        elif hx==9:
            wiredisp="XHH"
        elif hx==10:
            wiredisp="XHHW"        
      
        
    def conduitselect(self,ix):
        global conduitflag,conduitdisp
        if ix==1:
            conduitflag=1
            conduitdisp="EMT"
        elif ix==2:
            conduitflag=2
            conduitdisp="ENMT"
        elif ix==3:
            conduitflag=3
            conduitdisp="FMC"
        elif ix==4:
            conduitflag=4
            conduitdisp="IMC"
        elif ix==5:
            conduitflag=5
            conduitdisp="FNMC"
        elif ix==6:
            conduitflag=6
            conduitdisp="FMC"
        elif ix==7:
            conduitflag=7
            conduitdisp="RMC"
        elif ix==8:
            conduitflag=8
            conduitdisp="RPVC"
            conduitflag=8
    
            
    def phaseselect(self,jx):
        global phaseflag
        if jx==1:
            phaseflag=1
        elif jx==2:
            phaseflag=2
        elif jx==3:
            phaseflag=3
        elif jx==4:
            phaseflag=4
    def unitselect(self,kx):
        global areaflag
        if kx==0:
            areaflag=0
        elif kx==1:
            areaflag=1
        elif kx==2:
            areaflag=2
        elif kx==3:
            areaflag=3
        elif kx==4:
            areaflag=4
        elif kx==5:
            areaflag=5
        elif kx==6:
            areaflag=6
        elif kx==7:
            areaflag=7
        elif kx==8:
            areaflag=8
        elif kx==9:
            areaflag=9
        elif kx==10:
            areaflag=10
        elif kx==11:
            areaflag=11
        elif kx==12:
            areaflag=12
        elif kx==13:
            areaflag=13
        elif kx==13:
            areaflag=13
        elif kx==14:
            areaflag=14
        elif kx==15:
            areaflag=15
        elif kx==16:
            areaflag=16
        elif kx==17:
            areaflag=17
        elif kx==18:
            areaflag=18
        
            
                

        
class paneloutputcommercial(QtGui.QDialog):
    def __init__(self,parent=None):
        super(paneloutputcommercial, self).__init__(parent)
        
        self.setWindowTitle("THREE PHASE LOAD SCHEDULE")
        self.setGeometry(20,20,1500,780)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(16)
        self.table.move(120,50)
        self.table.setHorizontalHeaderLabels(['Ckt. No.       ','       Load Description      ','     V    ','       VA     ','AB','BC','CA','3-Phase','AT','AF','Sets','Wire Size','Ground Wire','Wire Type','Conduit','Conduit Type'])
        self.table.resize(1200,400)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        self.tablediag = QtGui.QTableWidget(self)
        self.tablediag.setColumnCount(8)
        self.tablediag.move(120,500)
        self.tablediag.setHorizontalHeaderLabels(['Main Feeder AT                           ','Main Feeder AF                ','Sets                 ','Wire Size                ',
                                                  'Grounding Wire               ','Wire Type               ','Conduit         ','Conduit Type               '])
        self.tablediag.resize(1200,100)
        self.tablediag.resizeColumnsToContents()
        self.tablediag.verticalHeader().setVisible(0)
        self.commercialdiagram = diagramcommercial(self)
        #self.panelmain = mainpanel(self)
        self.displayinput = QtGui.QPushButton("Diagram",self)
        self.displayinput.clicked.connect(self.displaydata)
        self.displayinput.move(410,700)
        self.updateinput = QtGui.QPushButton("Display",self)
        self.updateinput.clicked.connect(self.updatedata)
        self.updateinput.move(310,700)
        font10 = QtGui.QFont("Helvetica", 10)
        self.dt=QtGui.QLabel("Disclaimer: The data from this software must only be for verification purposes.",self)
        self.dt.move(10,730)
        self.dt.setFont(font10)
        self.dx=QtGui.QLabel("It is based from the PEC 2009 provisions that are considered minimum requirements necessary for safety.",self)
        self.dx.move(10,750)
        self.dx.setFont(font10)
        self.lt=QtGui.QLabel("Minimum Lighting Load: ",self)
        self.lt.move(10,650)
        self.lt.resize(210,30)
        self.lt.setFont(font10)
        self.lto=QtGui.QLabel(self)
        self.lto.move(250,650)
        self.lto.resize(100,30)
        self.lto.setFont(font10)
    def displaydata(self):
        self.commercialdiagram.exec_()
        self.close()
        #self.panelmain.exec_()
        #python = sys.executable
        #os.execl(python, python, * sys.argv)
        
        self.close()
    def updatedata(self):
        pathsave="outputdata.csv"
        dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
        np_dfo = dfo.as_matrix()
        pathtarget=str(np_dfo[0][0])
        wiretype=str(np_dfo[0][6])
        conduittype=str(np_dfo[0][8])
                            
        pathhistory="history.csv"
        dfh=pd.read_csv(pathhistory,names=['Wire Type','Conduit Type'],skiprows=1)
        np_dfh = dfh.as_matrix()
        
        df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
        np_df = df.as_matrix()
        itx=0
        pathsave="outputdata.csv"
        dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
        np_dfo = dfo.as_matrix()
        pathmp=str(np_dfo[0][9])+"/mpout.csv"
        dfmp=pd.read_csv(pathmp,names=['DemandFactor','Area','Wireflag','Areaflag'],skiprows=1)
        np_dfmp = dfmp.as_matrix()
        unitarea=float(np_dfmp[0][1])
        areaflag=float(np_dfmp[0][2])
        
        dflighting=df[df.Lighting != 0]
        np_dflighting=dflighting.as_matrix()
        print np_dflighting
        lightingtotal=0
        for i in xrange(len(np_dflighting)):
             lighting=np_dflighting[itx][3]
             lightingtotal=lightingtotal+lighting
             itx=itx+1
        self.lto.setText(str(lightingtotal))  
        if unitarea!="" and areaflag!=0:
             unitarea=float(np_dfmp[0][1])
             if areaflag==1:
                 vasq=8
             elif areaflag==2:
                 vasq=28
             elif areaflag==3:
                 vasq=24
             elif areaflag==4:
                 vasq=8
             elif areaflag==5:
                 vasq=16
             elif areaflag==6:
                 vasq=16
             elif areaflag==7:
                 vasq=24
             elif areaflag==8:
                 vasq=4
             elif areaflag==9:
                 vasq=16
             elif areaflag==10:
                 vasq=16
             elif areaflag==11:
                 vasq=12
             elif areaflag==12:
                 vasq=28
             elif areaflag==13:
                 vasq=16
             elif areaflag==14:
                 vasq=24
             elif areaflag==15:
                 vasq=24
             elif areaflag==16:
                 vasq=8
             elif areaflag==17:
                 vasq=4
             elif areaflag==18:
                 vasq=2
         
             if areaflag!=0:
                 vaunit=unitarea*vasq
               
                 if lightingtotal>=vaunit:
                    self.lto.setText(str(lightingtotal))
                    self.lto.setStyleSheet('color: green')
                 elif lightingtotal<vaunit:
                    self.lto.setText(str(lightingtotal))
                    self.lto.setStyleSheet('color: red')
             else:
                 self.lto.setText("No Input")
                 self.lto.setStyleSheet('color: red')
                
        df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
        np_df = df.as_matrix()
        self.table.setRowCount(len(np_df))
        self.tablediag.setRowCount(1)
        self.tablediag.setItem(0, 0, QtGui.QTableWidgetItem(""+str(np_dfo[0][1])))
        self.tablediag.setItem(0, 1, QtGui.QTableWidgetItem(""+str(np_dfo[0][2])))
        self.tablediag.setItem(0, 2, QtGui.QTableWidgetItem(""+str(int(np_dfo[0][3]))))
        self.tablediag.setItem(0, 3, QtGui.QTableWidgetItem(" 3 - "+str(np_dfo[0][4])))
        self.tablediag.setItem(0, 5, QtGui.QTableWidgetItem(""+wiretype))
        self.tablediag.setItem(0, 7, QtGui.QTableWidgetItem(""+conduittype))
        self.tablediag.setItem(0, 4, QtGui.QTableWidgetItem(" 1 - "+str(np_dfo[0][5])))
        self.tablediag.setItem(0, 6, QtGui.QTableWidgetItem(""+str(np_dfo[0][7])))
        cnt=0
        for i in xrange(len(np_df)):
             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+"            "+str(int(np_df[cnt][0]))+"          "))
             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])))
             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][4])))
             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])))
             self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][10])))
             self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(np_df[cnt][11])))
             self.table.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(np_df[cnt][12])))
             self.table.setItem(cnt, 7, QtGui.QTableWidgetItem(""+str(np_df[cnt][13])))
             self.table.setItem(cnt, 8, QtGui.QTableWidgetItem(""+str(np_df[cnt][7])))
             self.table.setItem(cnt, 9, QtGui.QTableWidgetItem(""+str(np_df[cnt][8])))
             self.table.setItem(cnt, 10, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][5]))))
             self.table.setItem(cnt, 11, QtGui.QTableWidgetItem(" 3 - "+str(np_df[cnt][14])))
             self.table.setItem(cnt, 12, QtGui.QTableWidgetItem(" 1 - "+str(np_df[cnt][15])))
             
             self.table.setItem(cnt, 14, QtGui.QTableWidgetItem(""+str(np_df[cnt][16])))
             if np_df[cnt][16]!=0:
                 self.table.setItem(cnt, 13, QtGui.QTableWidgetItem(""+str(np_dfh[0][0])))
                 self.table.setItem(cnt, 15, QtGui.QTableWidgetItem(""+str(np_dfh[0][1])))
             else:
                 self.table.setItem(cnt, 13, QtGui.QTableWidgetItem(""+"----"))
                 self.table.setItem(cnt, 15, QtGui.QTableWidgetItem(""+"----"))
             
             cnt=cnt+1
        

######################################################################Main Panel###################################################################################
class mainpanel(QtGui.QDialog):
    def __init__(self,parent=None):
        super(mainpanel, self).__init__(parent)
        self.setWindowTitle("Main Panel")
        self.setGeometry(20,20,950,760)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(16)
        self.table.move(50,50)
        self.table.setHorizontalHeaderLabels(['Ckt. No.','       Load Description      ','     V    ','       VA     ','AB','BC','CA','3-Phase','AT','AF','Sets','Wire Size','Ground Wire','Wire Type','Conduit','Conduit Type'])
        self.table.resize(890,400)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        self.tablediag = QtGui.QTableWidget(self)
        self.tablediag.setColumnCount(8)
        self.tablediag.move(50,500)
        self.tablediag.setHorizontalHeaderLabels(['Main Feeder AT                           ','Main Feeder AF                ','Sets                 ','Wire Size                ',
                                                  'Grounding Wire               ','Wire Type               ','Conduit         ','Conduit Type               '])
        self.tablediag.resize(750,100)
        self.tablediag.resizeColumnsToContents()
        self.tablediag.verticalHeader().setVisible(0)
        self.l19=QtGui.QLabel(self)
        self.l19.move(10,735)
        self.l19.resize(500,30)
        
        self.maindiagram = diagrammain(self)

        self.displayinput = QtGui.QPushButton("Diagram",self)
        self.displayinput.clicked.connect(self.displaydata)
        self.displayinput.move(410,700)
        self.updateinput = QtGui.QPushButton("Display",self)
        self.updateinput.clicked.connect(self.updatedata)
        self.updateinput.move(310,700)
        self.conduittype = QtGui.QComboBox(self)
        self.conduittype.addItems(["","EMT","ENMT","FMC","IMC","Liquidtight FNMC","Liquidtight FMC","RMC","Rigid PVC"])
        self.conduittype.currentIndexChanged.connect(self.conduitselect)
        self.conduittype.move(50,700)
        self.conduittype.resize(120,20)
        self.wiretype = QtGui.QComboBox(self)
        self.wiretype.addItems(["","TW - Copper","UF - Copper","RHW - Copper","THW - Copper","THWN - Copper","RHH - Copper","THHN - Copper","THHW - Copper","XHH - Copper","XHHW - Copper","TW - Aluminum","UF - Aluminum","RHW - Aluminum","THW - Aluminum","THWN - Aluminum","RHH - Aluminum","THHN - Aluminum","THHW - Aluminum","XHH - Aluminum","XHHW - Aluminum"])
        self.wiretype.currentIndexChanged.connect(self.wireselect)
        self.wiretype.move(150,700)
        self.wiretype.resize(120,20)
        self.spareinput = QtGui.QPushButton("Add Spare",self)
        self.spareinput.clicked.connect(self.sparedata)
        self.spareinput.move(210,600)
        self.spaceinput = QtGui.QPushButton("Add Space",self)
        self.spaceinput.clicked.connect(self.spacedata)
        self.spaceinput.move(310,600)
    def displaydata(self):
        self.maindiagram.exec_()
        #self.panelmain.exec_()
        #python = sys.executable
        #os.execl(python, python, * sys.argv)
        self.close()
    def sparedata(self):
         pathsave="outputdata.csv"
         dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
         np_dfo = dfo.as_matrix()
         pathtarget=str(np_dfo[0][0])
         pathtarget=pathtarget.split("/")
         pathtarget=str(pathtarget[0])+"/mainpanel.csv"
         df=pd.read_csv(pathtarget,names=['Circuit','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','AB',
                                              'BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting','HRM','Subflag'],skiprows=1)
         np_df = df.as_matrix()
         
         dfspare=df[df.AT != 0]
         dfspare = dfspare.sort_values(['AT'], ascending=[True])
         np_dfspare=dfspare.as_matrix()
         atspare=np_dfspare[0][6]
          
         
         df = df.append({'Circuit':len(np_df)+1, 'LoadDescription':"Spare",'Rating':0,'Voltage':230,'Wireset':0,
                                     'Wirenumber':0,'AT':atspare,'AF':0,'AB':0,'BC':0,'CA':0,'3-Phase':0,
                                     'WireSize':0,'GroundSize':0,'ConduitSize':0,'Lighting':0,'HRM':0,'Subflag':1}, ignore_index=True)
         df.to_csv(pathtarget,  index = False)
    def spacedata(self):
         pathsave="outputdata.csv"
         dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
         np_dfo = dfo.as_matrix()
         pathtarget=str(np_dfo[0][0])
         pathtarget=pathtarget.split("/")
         pathtarget=str(pathtarget[0])+"/mainpanel.csv"
         df=pd.read_csv(pathtarget,names=['Circuit','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','AB',
                                              'BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting','HRM','Subflag'],skiprows=1)
         np_df = df.as_matrix()
         df = df.append({'Circuit':len(np_df)+1, 'LoadDescription':"Space",'Rating':0,'Voltage':230,'Wireset':0,
                                     'Wirenumber':0,'AT':0,'AF':0,'AB':0,'BC':0,'CA':0,'3-Phase':0,
                                     'WireSize':0,'GroundSize':0,'ConduitSize':0,'Lighting':0,'HRM':0,'Subflag':2}, ignore_index=True)
         df.to_csv(pathtarget,  index = False)
    def conduitselect(self,ix):
            global conduitflag,conduitdisp
            if ix==1:
                conduitflag=1
                conduitdisp="EMT"
            elif ix==2:
                conduitflag=2
                conduitdisp="ENMT"
            elif ix==3:
                conduitflag=3
                conduitdisp="FMC"
            elif ix==4:
                conduitflag=4
                conduitdisp="IMC"
            elif ix==5:
                conduitflag=5
                conduitdisp="FNMC"
            elif ix==6:
                conduitflag=6
                conduitdisp="FMC"
            elif ix==7:
                conduitflag=7
                conduitdisp="RMC"
            elif ix==8:
                conduitflag=8
                conduitdisp="RPVC"
                conduitflag=8   
    def updatedata(self):
         global conduitflag,conduitdisp,wireflag,groundtype,emtflag,entflag,fmcflag,imcflag,lfnmcflag,lfmcflag,rmcflag,rpvcflag,wiredisp
         pathsave="outputdata.csv"
         dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
         np_dfo = dfo.as_matrix()
         pathtarget=str(np_dfo[0][9])+"/mainpanel.csv"
         wiretype=str(np_dfo[0][6])
         conduittype=str(np_dfo[0][8])
         pathmp=str(np_dfo[0][9])+"/mpout.csv"                   
         pathhistory="history.csv"
         wireset=1
         wirenumber=4
         totalwire=wireset*wirenumber
         dfh=pd.read_csv(pathhistory,names=['Wire Type','Conduit Type'],skiprows=1)
         np_dfh = dfh.as_matrix()
         dfmp=pd.read_csv(pathmp,names=['DemandFactor','Area','Wireflag'],skiprows=1)
         np_dfmp = dfmp.as_matrix()
         demandfactor=float(np_dfmp[0][0])
         unitarea=float(np_dfmp[0][1])
         df=pd.read_csv(pathtarget,names=['Circuit','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting','HRM','Subflag'],skiprows=1)
         np_df = df.as_matrix()
         self.table.setRowCount(len(np_df))
        
         cnt=0
         for i in xrange(len(np_df)):
             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][0]))))
             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])))
             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])))
             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])))
             self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][8])))
             self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(np_df[cnt][9])))
             self.table.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(np_df[cnt][10])))
             self.table.setItem(cnt, 7, QtGui.QTableWidgetItem(""+str(np_df[cnt][11])))
             self.table.setItem(cnt, 8, QtGui.QTableWidgetItem(""+str(np_df[cnt][6])))
             self.table.setItem(cnt, 9, QtGui.QTableWidgetItem(""+str(np_df[cnt][7])))
             self.table.setItem(cnt, 10, QtGui.QTableWidgetItem(""+str(int(np_df[cnt][4]))))
             self.table.setItem(cnt, 11, QtGui.QTableWidgetItem(" 3 - "+str(np_df[cnt][12])))
             self.table.setItem(cnt, 12, QtGui.QTableWidgetItem(" 1 - "+str(np_df[cnt][13])))
             
             self.table.setItem(cnt, 14, QtGui.QTableWidgetItem(""+str(np_df[cnt][14])))
             if np_df[cnt][15]!=0:
                 self.table.setItem(cnt, 13, QtGui.QTableWidgetItem(""+str(np_dfh[0][0])))
                 self.table.setItem(cnt, 15, QtGui.QTableWidgetItem(""+str(np_dfh[0][1])))
             else:
                 self.table.setItem(cnt, 13, QtGui.QTableWidgetItem(""+"----"))
                 self.table.setItem(cnt, 15, QtGui.QTableWidgetItem(""+"----"))
             
             cnt=cnt+1
         dfmotor = df.sort_values(['HRM'], ascending=[False])
         np_dfmotor=dfmotor.as_matrix()
         highestmotor=np_dfmotor[0][16]     
         itx=0
         lightingtotal=0
         for i in xrange(len(np_df)):
                 lighting=np_df[itx][15]
                 lightingtotal=lightingtotal+lighting
                 itx=itx+1
         print lightingtotal
         Itab=0
         Itbc=0
         Itac=0
         Itabc=0
         itx=0
         vatotal=0
         for i in xrange(len(np_df)):
             vatotal=vatotal+np_df[itx][3]
             Itab=Itab+np_df[itx][10]
             Itbc=Itbc+np_df[itx][11]
             Itac=Itac+np_df[itx][12]
             Itabc=Itabc+np_df[itx][13]
             itx=itx+1
         Ih=[Itab,Itbc,Itac]
         Ih=sorted(Ih)
         Ih=Ih[2]
         print "Ih: "+str(Ih)
         It=Itabc+math.sqrt(3)*Ih
         Icb=It+1.5*highestmotor
         print "Highest Motor: "+str(highestmotor)
         print "Icb: "+str(Icb)
         
         Iwire=It+0.25*highestmotor
         atdata="ATParse.csv"
         dfat=pd.read_csv(atdata,names=['AT','Low','High'],skiprows=1)
         np_dfat = dfat.as_matrix()
         
         atcnt=0
         for i in xrange(len(np_dfat)):
               
               if Icb>np_dfat[atcnt][1] and Icb<=np_dfat[atcnt][2]:
                     amperetrip=np_dfat[atcnt][0]
                     
                     print "AT: "+str(amperetrip)
               
               atcnt=atcnt+1
              
         try:
             self.l19.setText("")
             afdata="AFParse.csv"
             dfaf=pd.read_csv(afdata,names=['AF','AT'],skiprows=1)
             afout=np.where(dfaf["AT"] == amperetrip)
             np_dfaf = dfaf.as_matrix()
             
             afout=afout[0][0]
             afout=np_dfaf[afout][0]
             print "AF: "+str(afout)
         except:
             afout="Out of Range"
             print "Adjust AF Table: Out of Range"
             self.l19.setText("Adjust AF Table: Out of Range")
         wiredata="MainWireParse.csv"
         dfwire=pd.read_csv(wiredata,names=['Size','A','B','C','D','E','F'],skiprows=1)
         np_dfwire = dfwire.as_matrix()
         wireat=Iwire
         if wireflag==1:
             
             if wireat<=405:
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireat>np_dfwire[wirecnt][1] and wireat<=np_dfwire[wirecnt+1][1]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
             elif wireat>405 and wireat<=445:
                 wiresize=np_dfwire[wirecnt+1][0]
                 print "Wire Size:"+str(wiresize)
             elif wireat>445:
                 wireatout=wireat
                 while wireatout>445:
                     if wireset<2:
                         wireset=wireset+1
                     wireatout=wireat/wireset
                     wireset=wireset+1
                 print "AT: "+str(wireatout)
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireatout>np_dfwire[wirecnt][1] and wireatout<=np_dfwire[wirecnt+1][1]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
         elif wireflag==2:
             
             if wireat<=485:
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireat>np_dfwire[wirecnt][2] and wireat<=np_dfwire[wirecnt+1][2]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
             elif wireat>485 and wireat<=540:
                 wiresize=np_dfwire[wirecnt+1][0]
                 print "Wire Size:"+str(wiresize)
             elif wireat>540:
                 wireatout=wireat
                 while wireatout>540:
                     if wireset<2:
                         wireset=wireset+1
                     wireatout=wireat/wireset
                     wireset=wireset+1
                 print "AT: "+str(wireatout)
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireatout>np_dfwire[wirecnt][2] and wireatout<=np_dfwire[wirecnt+1][2]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
         elif wireflag==3:
             
             if wireat<=515:
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireat>np_dfwire[wirecnt][3] and wireat<=np_dfwire[wirecnt+1][3]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
             elif wireat>515 and wireat<=580:
                 wiresize=np_dfwire[wirecnt+1][0]
                 print "Wire Size:"+str(wiresize)
             elif wireat>580:
                 wireatout=wireat
                 while wireatout>580:
                     if wireset<2:
                         wireset=wireset+1
                     wireatout=wireat/wireset
                     wireset=wireset+1
                 print "AT: "+str(wireatout)
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireatout>np_dfwire[wirecnt][3] and wireatout<=np_dfwire[wirecnt+1][3]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
         elif wireflag==4:
             
             if wireat<=335:
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireat>np_dfwire[wirecnt][4] and wireat<=np_dfwire[wirecnt+1][4]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
             elif wireat>335 and wireat<=370:
                 wiresize=np_dfwire[wirecnt+1][0]
                 print "Wire Size:"+str(wiresize)
             elif wireat>370:
                 wireatout=wireat
                 while wireatout>370:
                     if wireset<2:
                         wireset=wireset+1
                     wireatout=wireat/wireset
                     wireset=wireset+1
                 print "AT: "+str(wireatout)
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireatout>np_dfwire[wirecnt][4] and wireatout<=np_dfwire[wirecnt+1][4]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
         elif wireflag==5:
             
             if wireat<=405:
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireat>np_dfwire[wirecnt][5] and wireat<=np_dfwire[wirecnt+1][5]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
             elif wireat>405 and wireat<=440:
                 wiresize=np_dfwire[wirecnt+1][0]
                 print "Wire Size:"+str(wiresize)
             elif wireat>440:
                 wireatout=wireat
                 while wireatout>440:
                     if wireset<2:
                         wireset=wireset+1
                     wireatout=wireat/wireset
                     wireset=wireset+1
                 print "AT: "+str(wireatout)
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireatout>np_dfwire[wirecnt][5] and wireatout<=np_dfwire[wirecnt+1][5]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
         elif wireflag==6:
             
             if wireat<=460:
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireat>np_dfwire[wirecnt][6] and wireat<=np_dfwire[wirecnt+1][6]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
             elif wireat>460 and wireat<=495:
                 wiresize=np_dfwire[wirecnt+1][0]
                 print "Wire Size:"+str(wiresize)
             elif wireat>495:
                 wireatout=wireat
                 while wireatout>495:
                     if wireset<2:
                         wireset=wireset+1
                     wireatout=wireat/wireset
                     wireset=wireset+1
                 print "AT: "+str(wireatout)
                 wirecnt=0
                 for i in xrange(len(np_dfwire)-1):
                     
                        if wireatout>np_dfwire[wirecnt][6] and wireatout<=np_dfwire[wirecnt+1][6]:
                         
                             wiresize=np_dfwire[wirecnt+1][0]
                             print "Wire Size:"+str(wiresize)
                         
                        wirecnt=wirecnt+1
         grounddata="groundwire.csv"
         dfground=pd.read_csv(grounddata,names=['AT','Copper','Aluminum'],skiprows=1)
      
         if groundtype==0:
             np_dfground = dfground.as_matrix()
             groundcnt=0
             groundat=Iwire
             for i in xrange(len(np_dfground)-1):
                 
                    if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                     
                         groundsize=np_dfground[groundcnt+1][1]
                         print "Ground Wire: "+str(groundsize)
                     
                    groundcnt=groundcnt+1
         elif groundtype==1:
             np_dfground = dfground.as_matrix()
             groundcnt=0
             groundat=amperetrip
             for i in xrange(len(np_dfground)-1):
                 
                    if groundat>np_dfground[groundcnt][0] and groundat<=np_dfground[groundcnt+1][0]:
                     
                         groundsize=np_dfground[groundcnt+1][2]
                         print "Ground Wire: "+str(groundsize)
                     
                    groundcnt=groundcnt+1
         totalwire=3
         try:
             self.l19.setText("")
             if conduitflag==1:
                conduitrange=10
                if emtflag==1:
                    pathwire="conduit_csv/emt_A.csv"
                elif emtflag==2:
                    pathwire="conduit_csv/emt_B.csv"
                elif emtflag==3:
                    pathwire="conduit_csv/emt_C.csv"
                elif emtflag==4:
                    pathwire="conduit_csv/emt_D.csv"
                
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
                 
             elif conduitflag==2:
                conduitrange=6
                if entflag==1:
                    pathwire="conduit_csv/ent_A.csv"
                elif entflag==2:
                    pathwire="conduit_csv/ent_B.csv"
                elif entflag==3:
                    pathwire="conduit_csv/ent_C.csv"
                elif entflag==4:
                    pathwire="conduit_csv/ent_D.csv"
                elif entflag==5:
                    pathwire="conduit_csv/ent_E.csv"
                        
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F'],skiprows=1)
                
             elif conduitflag==3:
                conduitrange=10
                if fmcflag==1:
                    pathwire="conduit_csv/fmc_A.csv"
                elif fmcflag==2:
                    pathwire="conduit_csv/fmc_B.csv"
                elif fmcflag==3:
                    pathwire="conduit_csv/fmc_C.csv"
                elif fmcflag==4:
                    pathwire="conduit_csv/fmc_D.csv"
                
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)  
             elif conduitflag==4:
                conduitrange=10
                if imcflag==1:
                    pathwire="conduit_csv/imc_A.csv"
                elif imcflag==2:
                    pathwire="conduit_csv/imc_B.csv"
                elif imcflag==3:
                    pathwire="conduit_csv/imc_C.csv"
                elif imcflag==4:
                    pathwire="conduit_csv/imc_D.csv"
                
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
             elif conduitflag==5:
                conduitrange=7
                if lfnmcflag==1:
                    pathwire="conduit_csv/lfnmc_A.csv"
                elif lfnmcflag==2:
                    pathwire="conduit_csv/lfnmc_B.csv"
                elif lfnmcflag==3:
                    pathwire="conduit_csv/lfnmc_C.csv"
                elif lfnmcflag==4:
                    pathwire="conduit_csv/lfnmc_D.csv"
                
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G'],skiprows=1)
             elif conduitflag==6:
                conduitrange=10
                if lfmcflag==1:
                    pathwire="conduit_csv/lfmc_A.csv"
                elif lfmcflag==2:
                    pathwire="conduit_csv/lfmc_B.csv"
                elif lfmcflag==3:
                    pathwire="conduit_csv/lfmc_C.csv"
                elif lfmcflag==4:
                    pathwire="conduit_csv/lfmc_D.csv"
                elif lfmcflag==5:
                    pathwire="conduit_csv/lfmc_E.csv"
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J'],skiprows=1)
             elif conduitflag==7:
                conduitrange=12
                if rmcflag==1:
                    pathwire="conduit_csv/rmc_A.csv"
                elif rmcflag==2:
                    pathwire="conduit_csv/rmc_B.csv"
                elif rmcflag==3:
                    pathwire="conduit_csv/rmc_C.csv"
                elif rmcflag==4:
                    pathwire="conduit_csv/rmc_D.csv"
                elif rmcflag==5:
                    pathwire="conduit_csv/rmc_E.csv"
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
             elif conduitflag==8:
                conduitrange=12
                if rpvcflag==1:
                    pathwire="conduit_csv/rpvc_A.csv"
                elif rpvcflag==2:
                    pathwire="conduit_csv/rpvc_B.csv"
                elif rpvcflag==3:
                    pathwire="conduit_csv/rpvc_C.csv"
                elif rpvcflag==4:
                    pathwire="conduit_csv/rpvc_D.csv"
                elif rpvcflag==5:
                    pathwire="conduit_csv/rpvc_E.csv"
                dfw=pd.read_csv(pathwire,names=['Output','A','B','C','D','E','F','G','H','I','J','K','L'],skiprows=1)
             
             print pathwire
             
             wireid=np.where(dfw["Output"] == wiresize)
             np_dfw = dfw.as_matrix()
             wireid=wireid[0][0]
         except:
             self.l19.setText("Wire Size Out of Range on Selected Type of Wire and Conduit.")
     
         conduitcnt=1
         for i in xrange(10): 
                try:
                    
                    
                    if np_dfw[wireid][conduitcnt]!=np_dfw[wireid][conduitcnt+1] and totalwire>np_dfw[wireid][conduitcnt]:
                        if totalwire>np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                             
                             conduitsize=np_dfw[0][conduitcnt+1]
                             
                    elif totalwire<=np_dfw[wireid][1]:
                        conduitsize=np_dfw[0][1]
                        
                    else:
                         if totalwire>=np_dfw[wireid][conduitcnt] and totalwire<=np_dfw[wireid][conduitcnt+1]:
                             
                             conduitsize=np_dfw[0][conduitcnt+1]
                             
                except:
                     print ""
                conduitcnt=conduitcnt+1
         print "Conduit Size: "+str(conduitsize) 
         
         
         self.tablediag.setRowCount(1)

         self.tablediag.setItem(0, 0, QtGui.QTableWidgetItem(""+str(amperetrip)))
         self.tablediag.setItem(0, 1, QtGui.QTableWidgetItem(""+str(afout)))
         self.tablediag.setItem(0, 2, QtGui.QTableWidgetItem(""+"1"))
         self.tablediag.setItem(0, 3, QtGui.QTableWidgetItem(" 3 - "+str(wiresize)))
         self.tablediag.setItem(0, 4, QtGui.QTableWidgetItem(" 1 - "+str(groundsize)))
         self.tablediag.setItem(0, 5, QtGui.QTableWidgetItem(""+wiredisp))
         self.tablediag.setItem(0, 6, QtGui.QTableWidgetItem(""+str(conduitsize)))
         self.tablediag.setItem(0, 7, QtGui.QTableWidgetItem(""+conduitdisp))
    def wireselect(self,hx):
        global wireflag,groundtype,emtflag,entflag,fmcflag,imcflag,lfnmcflag,lfmcflag,rmcflag,rpvcflag,wiredisp
        if hx==1 or hx==2:
            wireflag=1
        elif hx==3 or hx==4 or hx==5:
            wireflag=2
        elif hx==6 or hx==7 or hx==8 or hx==9 or hx==10:
            wireflag=3
        elif hx==11 or hx==12:
            wireflag=4
        elif hx==13 or hx==14 or hx==15:
            wireflag=5
        elif hx==16 or hx==17 or hx==18 or hx==19 or hx==20:
            wireflag=6
        if hx==1 or hx==2 or hx==3 or hx==4 or hx==5 or hx==6 or hx==7 or hx==8 or hx==9 or hx==10:
            groundtype=0
        elif hx==11 or hx==12 or hx==13 or hx==14 or hx==15 or hx==16 or hx==17 or hx==18 or hx==19 or hx==20:
            groundtype=1
        if hx==3 or hx==13 or hx==6 or hx==16:#RHW - RHH
            emtflag=1
            entflag=1
            fmcflag=1
            imcflag=1
            lfnmcflag=1
            lfmcflag=1
            rmcflag=1
            rpvcflag=1
        elif hx==1 or hx==11:#TW
            emtflag=2
            entflag=2
            fmcflag=2
            imcflag=2
            lfnmcflag=2
            lfmcflag=2
            rmcflag=2
            rpvcflag=2
        elif hx==8 or hx==18 or hx==4 or hx==14:#THHW - THW
            entflag=3
            fmcflag=2
            imcflag=2
            lfnmcflag=2
            lfmcflag=3
            rmcflag=3
            rpvcflag=3
        elif hx==7 or hx==17 or hx==5 or hx==15:#THHN - THWN
            emtflag=3
            entflag=4
            fmcflag=3
            imcflag=3
            lfnmcflag=3
            lfmcflag=4
            rmcflag=4
            rpvcflag=4
        
        elif hx==9 or hx==19 or hx==10 or hx==20:#XHH - XHHW
            emtflag=4
            entflag=5
            fmcflag=4
            imcflag=4
            lfnmcflag=4
            lfmcflag=5
            rmcflag=5
            rpvcflag=5
        if hx==1:
            wiredisp="TW"
        elif hx==2:
            wiredisp="UF"
        elif hx==3:
            wiredisp="RHW"
        elif hx==4:
            wiredisp="THW"
        elif hx==5:
            wiredisp="THWN"
        elif hx==6:
            wiredisp="RHH"
        elif hx==7:
            wiredisp="THHN"
        elif hx==8:
            wiredisp="THHW"
        elif hx==9:
            wiredisp="XHH"
        elif hx==10:
            wiredisp="XHHW"     

         
class diagramcommercial(QtGui.QDialog):
    def __init__(self,parent=None):
        super(diagramcommercial, self).__init__(parent)
        self.setWindowTitle("THREE PHASE SYSTEM PB DIAGRAM")
        self.setGeometry(20,20,942,760)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        font10 = QtGui.QFont("Helvetica", 10)
        self.panelmain = mainpanel(self)
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame.resize(800,700)
        self.frame.move(85,10)
        self.frame.setStyleSheet(" border-image: url(tpbg.png);");
        
        self.frame1 = QtGui.QFrame(self)
        self.frame1.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame1.resize(500,80)
        self.frame1.move(42,145)
        
        self.frame3 = QtGui.QFrame(self)
        self.frame3.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame3.resize(500,80)
        self.frame3.move(42,175)
        self.frame5 = QtGui.QFrame(self)
        self.frame5.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame5.resize(500,80)
        self.frame5.move(42,205)
        self.frame7 = QtGui.QFrame(self)
        self.frame7.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame7.resize(500,80)
        self.frame7.move(42,235)
        self.frame9 = QtGui.QFrame(self)
        self.frame9.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame9.resize(500,80)
        self.frame9.move(42,265)
        self.frame11 = QtGui.QFrame(self)
        self.frame11.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame11.resize(500,80)
        self.frame11.move(42,295)
        self.frame13 = QtGui.QFrame(self)
        self.frame13.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame13.resize(500,80)
        self.frame13.move(42,325)
        self.frame15 = QtGui.QFrame(self)
        self.frame15.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame15.resize(500,80)
        self.frame15.move(42,355)
        self.frame17 = QtGui.QFrame(self)
        self.frame17.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame17.resize(500,80)
        self.frame17.move(42,385)
        self.frame19 = QtGui.QFrame(self)
        self.frame19.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame19.resize(500,80)
        self.frame19.move(42,415)
        self.frame21 = QtGui.QFrame(self)
        self.frame21.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame21.resize(500,80)
        self.frame21.move(42,445)
        self.frame23 = QtGui.QFrame(self)
        self.frame23.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame23.resize(500,80)
        self.frame23.move(42,465)
        self.frame25 = QtGui.QFrame(self)
        self.frame25.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame25.resize(500,80)
        self.frame25.move(42,495)
        self.frame27 = QtGui.QFrame(self)
        self.frame27.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame27.resize(500,80)
        self.frame27.move(42,525)
        self.frame29 = QtGui.QFrame(self)
        self.frame29.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame29.resize(500,80)
        self.frame29.move(42,555)
        
        self.frame2 = QtGui.QFrame(self)
        self.frame2.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame2.resize(500,80)
        self.frame2.move(430,145)
        self.frame4 = QtGui.QFrame(self)
        self.frame4.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame4.resize(500,80)
        self.frame4.move(430,175)
        self.frame6 = QtGui.QFrame(self)
        self.frame6.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame6.resize(500,80)
        self.frame6.move(430,205)
        self.frame8 = QtGui.QFrame(self)
        self.frame8.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame8.resize(500,80)
        self.frame8.move(430,235)
        self.frame10 = QtGui.QFrame(self)
        self.frame10.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame10.resize(500,80)
        self.frame10.move(430,265)
        self.frame12 = QtGui.QFrame(self)
        self.frame12.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame12.resize(500,80)
        self.frame12.move(430,295)
        self.frame14 = QtGui.QFrame(self)
        self.frame14.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame14.resize(500,80)
        self.frame14.move(430,325)
        self.frame16 = QtGui.QFrame(self)
        self.frame16.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame16.resize(500,80)
        self.frame16.move(430,355)
        self.frame18 = QtGui.QFrame(self)
        self.frame18.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame18.resize(500,80)
        self.frame18.move(430,385)
        self.frame20 = QtGui.QFrame(self)
        self.frame20.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame20.resize(500,80)
        self.frame20.move(430,415)
        self.frame22 = QtGui.QFrame(self)
        self.frame22.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame22.resize(500,80)
        self.frame22.move(430,445)
        self.frame24 = QtGui.QFrame(self)
        self.frame24.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame24.resize(500,80)
        self.frame24.move(430,465)
        self.frame26 = QtGui.QFrame(self)
        self.frame26.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame26.resize(500,80)
        self.frame26.move(430,495)
        self.frame28 = QtGui.QFrame(self)
        self.frame28.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame28.resize(500,80)
        self.frame28.move(430,525)
        self.frame30 = QtGui.QFrame(self)
        self.frame30.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame30.resize(500,80)
        self.frame30.move(430,555)
        
        #self.frame1.setStyleSheet(" border-image: url(tpleftAB.png);");
        #self.frame2.setStyleSheet(" border-image: url(tpleftABC.png);");
        #self.frame3.setStyleSheet(" border-image: url(tpleftspare.png);");
        #self.frame4.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame5.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame6.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame7.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame8.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame9.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame10.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame11.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame12.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame13.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame14.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame15.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame16.setStyleSheet(" border-image: url(tprightABC.png);");
        #self.frame17.setStyleSheet(" border-image: url(tprightspare.png);");
        #self.frame18.setStyleSheet(" border-image: url(tprightCA.png);");
        #self.frame19.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame20.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame21.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame22.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame23.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame24.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame25.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame26.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame27.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame28.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame29.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame30.setStyleSheet(" border-image: url(tprightBC.png);");
        self.displayinput = QtGui.QPushButton("Display",self)
        self.displayinput.clicked.connect(self.displaydata)
        self.displayinput.move(410,700)
        self.maininput = QtGui.QPushButton("Main Panel",self)
        self.maininput.clicked.connect(self.maindata)
        self.maininput.move(500,700)
        #self.maindiagram = diagrammain(self)
        self.a1=QtGui.QLabel(self)
        self.a1.move(150,150)
        self.a1.setFont(font10)
        self.a3=QtGui.QLabel(self)
        self.a3.move(150,180)
        self.a3.setFont(font10)
        self.a5=QtGui.QLabel(self)
        self.a5.move(150,210)
        self.a5.setFont(font10)
        self.a7=QtGui.QLabel(self)
        self.a7.move(150,240)
        self.a7.setFont(font10)
        self.a9=QtGui.QLabel(self)
        self.a9.move(150,270)
        self.a9.setFont(font10)
        self.a11=QtGui.QLabel(self)
        self.a11.move(150,300)
        self.a11.setFont(font10)
        self.a13=QtGui.QLabel(self)
        self.a13.move(150,330)
        self.a13.setFont(font10)
        self.a15=QtGui.QLabel(self)
        self.a15.move(150,360)
        self.a15.setFont(font10)
        self.a17=QtGui.QLabel(self)
        self.a17.move(150,390)
        self.a17.setFont(font10)
        self.a19=QtGui.QLabel(self)
        self.a19.move(150,420)
        self.a19.setFont(font10)
        self.a21=QtGui.QLabel(self)
        self.a21.move(150,450)
        self.a21.setFont(font10)
        self.a23=QtGui.QLabel(self)
        self.a23.move(150,480)
        self.a23.setFont(font10)
        self.a25=QtGui.QLabel(self)
        self.a25.move(150,510)
        self.a25.setFont(font10)
        self.a27=QtGui.QLabel(self)
        self.a27.move(150,540)
        self.a27.setFont(font10)
        self.a29=QtGui.QLabel(self)
        self.a29.move(150,570)
        self.a29.setFont(font10)
        
        self.a2=QtGui.QLabel(self)
        self.a2.move(800,150)
        self.a2.setFont(font10)
        self.a4=QtGui.QLabel(self)
        self.a4.move(800,180)
        self.a4.setFont(font10)
        self.a6=QtGui.QLabel(self)
        self.a6.move(800,210)
        self.a6.setFont(font10)
        self.a8=QtGui.QLabel(self)
        self.a8.move(800,240)
        self.a8.setFont(font10)
        self.a10=QtGui.QLabel(self)
        self.a10.move(800,270)
        self.a10.setFont(font10)
        self.a12=QtGui.QLabel(self)
        self.a12.move(800,300)
        self.a12.setFont(font10)
        self.a14=QtGui.QLabel(self)
        self.a14.move(800,330)
        self.a14.setFont(font10)
        self.a16=QtGui.QLabel(self)
        self.a16.move(800,360)
        self.a16.setFont(font10)
        self.a18=QtGui.QLabel(self)
        self.a18.move(800,390)
        self.a18.setFont(font10)
        self.a20=QtGui.QLabel(self)
        self.a20.move(800,420)
        self.a20.setFont(font10)
        self.a22=QtGui.QLabel(self)
        self.a22.move(800,450)
        self.a22.setFont(font10)
        self.a24=QtGui.QLabel(self)
        self.a24.move(800,480)
        self.a24.setFont(font10)
        self.a26=QtGui.QLabel(self)
        self.a26.move(800,510)
        self.a26.setFont(font10)
        self.a28=QtGui.QLabel(self)
        self.a28.move(800,540)
        self.a28.setFont(font10)
        self.a30=QtGui.QLabel(self)
        self.a30.move(800,570)
        self.a30.setFont(font10)
        
        self.b1=QtGui.QLabel(self)
        self.b1.move(250,150)
        self.b1.setFont(font10)
        self.b3=QtGui.QLabel(self)
        self.b3.move(250,180)
        self.b3.setFont(font10)
        self.b5=QtGui.QLabel(self)
        self.b5.move(250,210)
        self.b5.setFont(font10)
        self.b7=QtGui.QLabel(self)
        self.b7.move(250,240)
        self.b7.setFont(font10)
        self.b9=QtGui.QLabel(self)
        self.b9.move(250,270)
        self.b9.setFont(font10)
        self.b11=QtGui.QLabel(self)
        self.b11.move(250,300)
        self.b11.setFont(font10)
        self.b13=QtGui.QLabel(self)
        self.b13.move(250,330)
        self.b13.setFont(font10)
        self.b15=QtGui.QLabel(self)
        self.b15.move(250,360)
        self.b15.setFont(font10)
        self.b17=QtGui.QLabel(self)
        self.b17.move(250,390)
        self.b17.setFont(font10)
        self.b19=QtGui.QLabel(self)
        self.b19.move(250,420)
        self.b19.setFont(font10)
        self.b21=QtGui.QLabel(self)
        self.b21.move(250,450)
        self.b21.setFont(font10)
        self.b23=QtGui.QLabel(self)
        self.b23.move(250,480)
        self.b23.setFont(font10)
        self.b25=QtGui.QLabel(self)
        self.b25.move(250,510)
        self.b25.setFont(font10)
        self.b27=QtGui.QLabel(self)
        self.b27.move(250,540)
        self.b27.setFont(font10)
        self.b29=QtGui.QLabel(self)
        self.b29.move(250,570)
        self.b29.setFont(font10)
        
        self.b2=QtGui.QLabel(self)
        self.b2.move(700,150)
        self.b2.setFont(font10)
        self.b4=QtGui.QLabel(self)
        self.b4.move(700,180)
        self.b4.setFont(font10)
        self.b6=QtGui.QLabel(self)
        self.b6.move(700,210)
        self.b6.setFont(font10)
        self.b8=QtGui.QLabel(self)
        self.b8.move(700,240)
        self.b8.setFont(font10)
        self.b10=QtGui.QLabel(self)
        self.b10.move(700,270)
        self.b10.setFont(font10)
        self.b12=QtGui.QLabel(self)
        self.b12.move(700,300)
        self.b12.setFont(font10)
        self.b14=QtGui.QLabel(self)
        self.b14.move(700,330)
        self.b14.setFont(font10)
        self.b16=QtGui.QLabel(self)
        self.b16.move(700,360)
        self.b16.setFont(font10)
        self.b18=QtGui.QLabel(self)
        self.b18.move(700,390)
        self.b18.setFont(font10)
        self.b20=QtGui.QLabel(self)
        self.b20.move(700,420)
        self.b20.setFont(font10)
        self.b22=QtGui.QLabel(self)
        self.b22.move(700,450)
        self.b22.setFont(font10)
        self.b24=QtGui.QLabel(self)
        self.b24.move(700,480)
        self.b24.setFont(font10)
        self.b26=QtGui.QLabel(self)
        self.b26.move(700,510)
        self.b26.setFont(font10)
        self.b28=QtGui.QLabel(self)
        self.b28.move(700,540)
        self.b28.setFont(font10)
        self.b30=QtGui.QLabel(self)
        self.b30.move(700,570)
        self.b30.setFont(font10)
        
    def maindata(self):
         self.panelmain.exec_()
         self.close
    def displaydata(self):
         pathsave="outputdata.csv"
         dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
         np_dfo = dfo.as_matrix()
         pathtarget=str(np_dfo[0][0])
         df=pd.read_csv(pathtarget,names=['Circuit','Quantity','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting'],skiprows=1)
         np_df = df.as_matrix()
         itx=0
         mod=1
         for i in xrange(len(np_df)):
             if np_df[itx][10]>0 and np_df[itx][11]==0 and np_df[itx][12]==0 and np_df[itx][13]==0 and mod%2!=0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tpleftAB.png);")'
                 disp = disp.replace("'", "")
                 print "Left AB"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]>0 and np_df[itx][12]==0 and np_df[itx][13]==0 and mod%2!=0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tpleftBC.png);")'
                 disp = disp.replace("'", "")
                 print "Left BC"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]==0 and np_df[itx][12]>0 and np_df[itx][13]==0 and mod%2!=0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tpleftCA.png);")'
                 disp = disp.replace("'", "")
                 print "Left CA"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]==0 and np_df[itx][12]==0 and np_df[itx][13]>0 and mod%2!=0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tpleftABC.png);")'
                 disp = disp.replace("'", "")
                 print "Left ABC"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]==0 and np_df[itx][12]==0 and np_df[itx][13]==0 and mod%2!=0 and np_df[itx][16]==0:
                 disp='setStyleSheet(" border-image: url(tpleftspace.png);")'
                 disp = disp.replace("'", "")
                 print "Left Space"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]!=0 and mod%2!=0 and np_df[itx][16]==0 or np_df[itx][11]!=0 and mod%2!=0 and np_df[itx][16]==0 or np_df[itx][12]!=0  and mod%2!=0 and np_df[itx][16]==0 or np_df[itx][13]!=0 and mod%2!=0 and np_df[itx][16]==0:
                 disp='setStyleSheet(" border-image: url(tpleftspare.png);")'
                 disp = disp.replace("'", "")
                 print "Left Spare"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]>0 and np_df[itx][11]==0 and np_df[itx][12]==0 and np_df[itx][13]==0 and mod%2==0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tprightAB.png);")'
                 disp = disp.replace("'", "")
                 print "Right AB"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]>0 and np_df[itx][12]==0 and np_df[itx][13]==0 and mod%2==0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tprightBC.png);")'
                 disp = disp.replace("'", "")
                 print "Right BC"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]==0 and np_df[itx][12]>0 and np_df[itx][13]==0 and mod%2==0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tprightCA.png);")'
                 disp = disp.replace("'", "")
                 print "Right CA"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]==0 and np_df[itx][12]==0 and np_df[itx][13]>0 and mod%2==0 and np_df[itx][16]!=0:
                 disp='setStyleSheet(" border-image: url(tprightABC.png);")'
                 disp = disp.replace("'", "")
                 print "Right ABC"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]==0 and np_df[itx][11]==0 and np_df[itx][12]==0 and np_df[itx][13]==0 and mod%2==0 and np_df[itx][16]==0:
                 disp='setStyleSheet(" border-image: url(tprightspace.png);")'
                 disp = disp.replace("'", "")
                 print "Right Space"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][10]!=0 and mod%2==0 and np_df[itx][16]==0 or np_df[itx][11]!=0 and mod%2==0 and np_df[itx][16]==0 or np_df[itx][12]!=0  and mod%2==0 and np_df[itx][16]==0 or np_df[itx][13]!=0 and mod%2==0 and np_df[itx][16]==0:
                 disp='setStyleSheet(" border-image: url(tprightspare.png);")'
                 disp = disp.replace("'", "")
                 print "Right Spare"
                 exec("self.frame%d.%s" % (i + 1, disp));
             disp='setText(str('+str(np_df[itx][7])+'))'
             disp = disp.replace("'", "")
             exec("self.a%d.%s" % (i + 1, disp));

             print np_df[itx][7]
             disp='setText(str('+str(np_df[itx][7])+'))'
             disp = disp.replace("'", "")
             resdisp='resize(100,30)'
             resdisp = resdisp.replace("'", "")
             loaddisp='setText("'+str(np_df[itx][2])+'")'
             loaddisp = loaddisp.replace("'", "")
             exec("self.a%d.%s" % (i + 1, disp));
             exec("self.a%d.%s" % (i + 1, resdisp));
             exec("self.b%d.%s" % (i + 1, loaddisp));
             exec("self.b%d.%s" % (i + 1, resdisp)); 
             itx=itx+1
             mod=mod+1
         if len(np_df)%2!=0:
             disp='setStyleSheet(" border-image: url(sprightspare.png);")'
             disp = disp.replace("'", "")
             exec("self.frame%d.%s" % (len(np_df) + 1, disp));
             print "Right Spare"
             resdisp='resize(100,30)'
             resdisp = resdisp.replace("'", "")
             loaddisp='setText("Spare")'
             loaddisp = loaddisp.replace("'", "")
             exec("self.b%d.%s" % (len(np_df) + 1, loaddisp));
             exec("self.b%d.%s" % (len(np_df) + 1, resdisp));
             
            
        
class diagrammain(QtGui.QDialog):
    def __init__(self,parent=None):
        super(diagrammain, self).__init__(parent)
        self.setWindowTitle("THREE PHASE SYSTEM MAIN PANEL DIAGRAM")
        self.setGeometry(20,20,942,760)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        font10 = QtGui.QFont("Helvetica", 10)
 
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame.resize(800,700)
        self.frame.move(85,10)
        self.frame.setStyleSheet(" border-image: url(tpbg.png);");
        
        self.frame1 = QtGui.QFrame(self)
        self.frame1.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame1.resize(500,80)
        self.frame1.move(42,145)
        
        self.frame3 = QtGui.QFrame(self)
        self.frame3.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame3.resize(500,80)
        self.frame3.move(42,175)
        self.frame5 = QtGui.QFrame(self)
        self.frame5.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame5.resize(500,80)
        self.frame5.move(42,205)
        self.frame7 = QtGui.QFrame(self)
        self.frame7.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame7.resize(500,80)
        self.frame7.move(42,235)
        self.frame9 = QtGui.QFrame(self)
        self.frame9.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame9.resize(500,80)
        self.frame9.move(42,265)
        self.frame11 = QtGui.QFrame(self)
        self.frame11.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame11.resize(500,80)
        self.frame11.move(42,295)
        self.frame13 = QtGui.QFrame(self)
        self.frame13.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame13.resize(500,80)
        self.frame13.move(42,325)
        self.frame15 = QtGui.QFrame(self)
        self.frame15.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame15.resize(500,80)
        self.frame15.move(42,355)
        self.frame17 = QtGui.QFrame(self)
        self.frame17.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame17.resize(500,80)
        self.frame17.move(42,385)
        self.frame19 = QtGui.QFrame(self)
        self.frame19.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame19.resize(500,80)
        self.frame19.move(42,415)
        self.frame21 = QtGui.QFrame(self)
        self.frame21.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame21.resize(500,80)
        self.frame21.move(42,445)
        self.frame23 = QtGui.QFrame(self)
        self.frame23.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame23.resize(500,80)
        self.frame23.move(42,465)
        self.frame25 = QtGui.QFrame(self)
        self.frame25.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame25.resize(500,80)
        self.frame25.move(42,495)
        self.frame27 = QtGui.QFrame(self)
        self.frame27.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame27.resize(500,80)
        self.frame27.move(42,525)
        self.frame29 = QtGui.QFrame(self)
        self.frame29.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame29.resize(500,80)
        self.frame29.move(42,555)
        
        self.frame2 = QtGui.QFrame(self)
        self.frame2.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame2.resize(500,80)
        self.frame2.move(430,145)
        self.frame4 = QtGui.QFrame(self)
        self.frame4.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame4.resize(500,80)
        self.frame4.move(430,175)
        self.frame6 = QtGui.QFrame(self)
        self.frame6.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame6.resize(500,80)
        self.frame6.move(430,205)
        self.frame8 = QtGui.QFrame(self)
        self.frame8.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame8.resize(500,80)
        self.frame8.move(430,235)
        self.frame10 = QtGui.QFrame(self)
        self.frame10.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame10.resize(500,80)
        self.frame10.move(430,265)
        self.frame12 = QtGui.QFrame(self)
        self.frame12.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame12.resize(500,80)
        self.frame12.move(430,295)
        self.frame14 = QtGui.QFrame(self)
        self.frame14.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame14.resize(500,80)
        self.frame14.move(430,325)
        self.frame16 = QtGui.QFrame(self)
        self.frame16.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame16.resize(500,80)
        self.frame16.move(430,355)
        self.frame18 = QtGui.QFrame(self)
        self.frame18.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame18.resize(500,80)
        self.frame18.move(430,385)
        self.frame20 = QtGui.QFrame(self)
        self.frame20.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame20.resize(500,80)
        self.frame20.move(430,415)
        self.frame22 = QtGui.QFrame(self)
        self.frame22.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame22.resize(500,80)
        self.frame22.move(430,445)
        self.frame24 = QtGui.QFrame(self)
        self.frame24.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame24.resize(500,80)
        self.frame24.move(430,465)
        self.frame26 = QtGui.QFrame(self)
        self.frame26.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame26.resize(500,80)
        self.frame26.move(430,495)
        self.frame28 = QtGui.QFrame(self)
        self.frame28.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame28.resize(500,80)
        self.frame28.move(430,525)
        self.frame30 = QtGui.QFrame(self)
        self.frame30.setFrameStyle(QtGui.QFrame.NoFrame);
        self.frame30.resize(500,80)
        self.frame30.move(430,555)
        
        #self.frame1.setStyleSheet(" border-image: url(tpleftAB.png);");
        #self.frame2.setStyleSheet(" border-image: url(tpleftABC.png);");
        #self.frame3.setStyleSheet(" border-image: url(tpleftspare.png);");
        #self.frame4.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame5.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame6.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame7.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame8.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame9.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame10.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame12.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame16.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame20.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame24.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame28.setStyleSheet(" border-image: url(tpleftBC.png);");
        #self.frame2.setStyleSheet(" border-image: url(tprightABC.png);");
        #self.frame4.setStyleSheet(" border-image: url(tprightspare.png);");
        #self.frame6.setStyleSheet(" border-image: url(tprightCA.png);");
        #self.frame8.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame10.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame12.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame14.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame16.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame18.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame20.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame22.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame24.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame26.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame28.setStyleSheet(" border-image: url(tprightBC.png);");
        #self.frame30.setStyleSheet(" border-image: url(tprightBC.png);");
        self.displayinput = QtGui.QPushButton("Diagram",self)
        self.displayinput.clicked.connect(self.displaydata)
        self.displayinput.move(410,700)
        
        
        
        self.a1=QtGui.QLabel(self)
        self.a1.move(150,150)
        self.a1.setFont(font10)
        self.a3=QtGui.QLabel(self)
        self.a3.move(150,180)
        self.a3.setFont(font10)
        self.a5=QtGui.QLabel(self)
        self.a5.move(150,210)
        self.a5.setFont(font10)
        self.a7=QtGui.QLabel(self)
        self.a7.move(150,240)
        self.a7.setFont(font10)
        self.a9=QtGui.QLabel(self)
        self.a9.move(150,270)
        self.a9.setFont(font10)
        self.a11=QtGui.QLabel(self)
        self.a11.move(150,300)
        self.a11.setFont(font10)
        self.a13=QtGui.QLabel(self)
        self.a13.move(150,330)
        self.a13.setFont(font10)
        self.a15=QtGui.QLabel(self)
        self.a15.move(150,360)
        self.a15.setFont(font10)
        self.a17=QtGui.QLabel(self)
        self.a17.move(150,390)
        self.a17.setFont(font10)
        self.a19=QtGui.QLabel(self)
        self.a19.move(150,420)
        self.a19.setFont(font10)
        self.a21=QtGui.QLabel(self)
        self.a21.move(150,450)
        self.a21.setFont(font10)
        self.a23=QtGui.QLabel(self)
        self.a23.move(150,480)
        self.a23.setFont(font10)
        self.a25=QtGui.QLabel(self)
        self.a25.move(150,510)
        self.a25.setFont(font10)
        self.a27=QtGui.QLabel(self)
        self.a27.move(150,540)
        self.a27.setFont(font10)
        self.a29=QtGui.QLabel(self)
        self.a29.move(150,570)
        self.a29.setFont(font10)
        
        self.a2=QtGui.QLabel(self)
        self.a2.move(800,150)
        self.a2.setFont(font10)
        self.a4=QtGui.QLabel(self)
        self.a4.move(800,180)
        self.a4.setFont(font10)
        self.a6=QtGui.QLabel(self)
        self.a6.move(800,210)
        self.a6.setFont(font10)
        self.a8=QtGui.QLabel(self)
        self.a8.move(800,240)
        self.a8.setFont(font10)
        self.a10=QtGui.QLabel(self)
        self.a10.move(800,270)
        self.a10.setFont(font10)
        self.a12=QtGui.QLabel(self)
        self.a12.move(800,300)
        self.a12.setFont(font10)
        self.a14=QtGui.QLabel(self)
        self.a14.move(800,330)
        self.a14.setFont(font10)
        self.a16=QtGui.QLabel(self)
        self.a16.move(800,360)
        self.a16.setFont(font10)
        self.a18=QtGui.QLabel(self)
        self.a18.move(800,390)
        self.a18.setFont(font10)
        self.a20=QtGui.QLabel(self)
        self.a20.move(800,420)
        self.a20.setFont(font10)
        self.a22=QtGui.QLabel(self)
        self.a22.move(800,450)
        self.a22.setFont(font10)
        self.a24=QtGui.QLabel(self)
        self.a24.move(800,480)
        self.a24.setFont(font10)
        self.a26=QtGui.QLabel(self)
        self.a26.move(800,510)
        self.a26.setFont(font10)
        self.a28=QtGui.QLabel(self)
        self.a28.move(800,540)
        self.a28.setFont(font10)
        self.a30=QtGui.QLabel(self)
        self.a30.move(800,570)
        self.a30.setFont(font10)
        
        self.b1=QtGui.QLabel(self)
        self.b1.move(250,150)
        self.b1.setFont(font10)
        self.b3=QtGui.QLabel(self)
        self.b3.move(250,180)
        self.b3.setFont(font10)
        self.b5=QtGui.QLabel(self)
        self.b5.move(250,210)
        self.b5.setFont(font10)
        self.b7=QtGui.QLabel(self)
        self.b7.move(250,240)
        self.b7.setFont(font10)
        self.b9=QtGui.QLabel(self)
        self.b9.move(250,270)
        self.b9.setFont(font10)
        self.b11=QtGui.QLabel(self)
        self.b11.move(250,300)
        self.b11.setFont(font10)
        self.b13=QtGui.QLabel(self)
        self.b13.move(250,330)
        self.b13.setFont(font10)
        self.b15=QtGui.QLabel(self)
        self.b15.move(250,360)
        self.b15.setFont(font10)
        self.b17=QtGui.QLabel(self)
        self.b17.move(250,390)
        self.b17.setFont(font10)
        self.b19=QtGui.QLabel(self)
        self.b19.move(250,420)
        self.b19.setFont(font10)
        self.b21=QtGui.QLabel(self)
        self.b21.move(250,450)
        self.b21.setFont(font10)
        self.b23=QtGui.QLabel(self)
        self.b23.move(250,480)
        self.b23.setFont(font10)
        self.b25=QtGui.QLabel(self)
        self.b25.move(250,510)
        self.b25.setFont(font10)
        self.b27=QtGui.QLabel(self)
        self.b27.move(250,540)
        self.b27.setFont(font10)
        self.b29=QtGui.QLabel(self)
        self.b29.move(250,570)
        self.b29.setFont(font10)
        
        self.b2=QtGui.QLabel(self)
        self.b2.move(700,150)
        self.b2.setFont(font10)
        self.b4=QtGui.QLabel(self)
        self.b4.move(700,180)
        self.b4.setFont(font10)
        self.b6=QtGui.QLabel(self)
        self.b6.move(700,210)
        self.b6.setFont(font10)
        self.b8=QtGui.QLabel(self)
        self.b8.move(700,240)
        self.b8.setFont(font10)
        self.b10=QtGui.QLabel(self)
        self.b10.move(700,270)
        self.b10.setFont(font10)
        self.b12=QtGui.QLabel(self)
        self.b12.move(700,300)
        self.b12.setFont(font10)
        self.b14=QtGui.QLabel(self)
        self.b14.move(700,330)
        self.b14.setFont(font10)
        self.b16=QtGui.QLabel(self)
        self.b16.move(700,360)
        self.b16.setFont(font10)
        self.b18=QtGui.QLabel(self)
        self.b18.move(700,390)
        self.b18.setFont(font10)
        self.b20=QtGui.QLabel(self)
        self.b20.move(700,420)
        self.b20.setFont(font10)
        self.b22=QtGui.QLabel(self)
        self.b22.move(700,450)
        self.b22.setFont(font10)
        self.b24=QtGui.QLabel(self)
        self.b24.move(700,480)
        self.b24.setFont(font10)
        self.b26=QtGui.QLabel(self)
        self.b26.move(700,510)
        self.b26.setFont(font10)
        self.b28=QtGui.QLabel(self)
        self.b28.move(700,540)
        self.b28.setFont(font10)
        self.b30=QtGui.QLabel(self)
        self.b30.move(700,570)
        self.b30.setFont(font10)
    
    def displaydata(self):
         pathsave="outputdata.csv"
         dfo=pd.read_csv(pathsave,names=['Panel','AT','AF', 'Sets','WireSize','GroundingWire','TypeWire','Conduit','ConduitType','Directory'],skiprows=1)
         np_dfo = dfo.as_matrix()
         pathtarget=str(np_dfo[0][0])
         pathtarget=pathtarget.split("/")
         pathtarget=str(pathtarget[0])+"/mainpanel.csv"
         df=pd.read_csv(pathtarget,names=['Circuit','LoadDescription', 'Rating','Voltage','Wireset','Wirenumber','AT','AF','Motor','AB','BC','CA','3-Phase','WireSize','GroundSize','ConduitSize','Lighting','HRM','Subflag'],skiprows=1)
         np_df = df.as_matrix()
         itx=0
         mod=1
         for i in xrange(len(np_df)):
             if np_df[itx][17]==0 and mod%2!=0 and np_df[itx][14]!=0:
                 disp='setStyleSheet(" border-image: url(tpleftABC.png);")'
                 disp = disp.replace("'", "")
                 print "Left ABC"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][17]==2 and mod%2!=0 and np_df[itx][14]==0:
                 disp='setStyleSheet(" border-image: url(tpleftspace.png);")'
                 disp = disp.replace("'", "")
                 print "Left Space"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][17]==1 and mod%2!=0 and np_df[itx][14]==0:
                 disp='setStyleSheet(" border-image: url(tpleftspare.png);")'
                 disp = disp.replace("'", "")
                 print "Left Spare"
                 exec("self.frame%d.%s" % (i + 1, disp));
                 
             elif np_df[itx][17]==0 and mod%2==0 and np_df[itx][14]!=0:
                 disp='setStyleSheet(" border-image: url(tprightABC.png);")'
                 disp = disp.replace("'", "")
                 print "Right ABC"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][17]==2  and mod%2==0 and np_df[itx][14]==0:
                 disp='setStyleSheet(" border-image: url(tprightspace.png);")'
                 disp = disp.replace("'", "")
                 print "Right Space"
                 exec("self.frame%d.%s" % (i + 1, disp));
             elif np_df[itx][17]==1  and mod%2==0 and np_df[itx][14]==0:
                 disp='setStyleSheet(" border-image: url(tprightspare.png);")'
                 disp = disp.replace("'", "")
                 print "Right Spare"
                 exec("self.frame%d.%s" % (i + 1, disp));
             disp='setText(str('+str(np_df[itx][6])+'))'
             disp = disp.replace("'", "")
             exec("self.a%d.%s" % (i + 1, disp));

             print np_df[itx][7]
             disp='setText(str('+str(np_df[itx][6])+'))'
             disp = disp.replace("'", "")
             resdisp='resize(100,30)'
             resdisp = resdisp.replace("'", "")
             loaddisp='setText("'+str(np_df[itx][1])+'")'
             loaddisp = loaddisp.replace("'", "")
             exec("self.a%d.%s" % (i + 1, disp));
             exec("self.a%d.%s" % (i + 1, resdisp));
             exec("self.b%d.%s" % (i + 1, loaddisp));
             exec("self.b%d.%s" % (i + 1, resdisp)); 
             itx=itx+1
             mod=mod+1
         if len(np_df)%2!=0:
             disp='setStyleSheet(" border-image: url(sprightspare.png);")'
             disp = disp.replace("'", "")
             exec("self.frame%d.%s" % (len(np_df) + 1, disp));
             print "Right Spare"
             resdisp='resize(100,30)'
             resdisp = resdisp.replace("'", "")
             loaddisp='setText("Spare")'
             loaddisp = loaddisp.replace("'", "")
             exec("self.b%d.%s" % (len(np_df) + 1, loaddisp));
             exec("self.b%d.%s" % (len(np_df) + 1, resdisp));         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
