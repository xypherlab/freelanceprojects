from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import sys
from PyQt4 import QtGui, QtCore
import time
import os
import numpy as np
import ctypes
import _ctypes
import pygame
import cv2
if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread
import subprocess
# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()
       
        self._bodies = None
    def initUI(self):
        global flag,frameposition,stackflag,startflag
        flag=0
        frameposition=0
        stackflag=1
        pygame.init()
        startflag=1
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        
        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.setGeometry(0,20,1000,750)
        #Video Display Left
        self.i1=QtGui.QLabel(self)
        self.i1.setGeometry(50,60,230,200)
       
        #
        #Image Display Right
        self.i2=QtGui.QLabel(self)
        self.i2.setGeometry(550,60,230,200)
        
        #
        #Left Button
        self.leftbutton = QtGui.QPushButton("Left Hand",self)
        self.leftbutton.clicked.connect(self.left)
        self.leftbutton.move(450,280)
        #
        #Right Button
        self.rightbutton = QtGui.QPushButton("Right Hand",self)
        self.rightbutton.clicked.connect(self.right)
        self.rightbutton.move(250,280)
        #
        
        #
        #Stop Button
        self.scanbutton = QtGui.QPushButton("Scan",self)
        self.scanbutton.clicked.connect(self.scan)
        self.scanbutton.move(50,280)
        #

        #Play Button
        self.playbutton = QtGui.QPushButton("Play",self)
        self.playbutton.clicked.connect(self.play)
        self.playbutton.move(650,280)
        #
        #Play Button
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(850,280)
        #
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.move(50,330)
        self.table.setHorizontalHeaderLabels(['                 ','First Step','Second Step','Third Step', 'Fourth Step', 'Throw Step'])
        self.table.resize(860,250)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
      
        
    def stop(self):
        global flag,frameposition
        frameposition=0
        flag=0
        os.remove("trackdata.npy")
    def play(self):
        subprocess.call(['C:/Program Files/VideoLAN/VLC/vlc.exe', 'demo.mp4'])
    def scan(self):
        global flag,frameposition,startflag
        frameposition=0
        flag=1
        startflag=1
        
    def left(self):
        global flag,frameposition,stackflag
        frameposition=0
        flag=0
        stackflag=1
        print("Analyzing Data  for Left Hand....")
        trackdata=np.load('trackdata.npy')
        posdiv=int((len(trackdata)-len(trackdata)%5)/5)
        print(posdiv)
        pos1=(posdiv-1)*(1)
        pos2=(posdiv*2-1)*(1)
        pos3=(posdiv*3-1)*(1)
        pos4=(posdiv*4-1)*(1)
        pos5=(posdiv*5-1)*(1)
        #First Step
        mNS1=trackdata[pos1,0]
        mRSE1=trackdata[pos1,1]
        mREW1=trackdata[pos1,2]
        mRHK1=trackdata[pos1,3]
        mRKA1=trackdata[pos1,4]
        mLSE1=trackdata[pos1,5]
        mLEW1=trackdata[pos1,6]
        mLHK1=trackdata[pos1,7]
        mLKA1=trackdata[pos1,8]
        #Slope Setting for First Step
        tolerancens1=1
        tolerancerse1=1
        tolerancerew1=1
        tolerancerhk1=1
        tolerancerka1=1
        tolerancelse1=1
        tolerancelew1=1
        tolerancelhk1=1
        tolerancelka1=1
        ns1=9.8
        rse1=9.45
        rew1=0.12
        rhk1=-14.52
        rka1=-13.32
        lse1=-1.83
        lew1=11
        lhk1=12
        lka1=13
        if mNS1<=ns1+tolerancens1 and mNS1>=ns1-tolerancens1:
            print("NS1 is correct")
            ns1flag=True
        else:
            print("NS1 is incorrect")
            ns1flag=False
        if mRSE1<=rse1+tolerancerse1 and mRSE1>=rse1-tolerancerse1:
            print("RSE1 is correct")
            rse1flag=True
        else:
            print("RSE1 is incorrect")
            rse1flag=False
        if mREW1<=rew1+tolerancerew1 and mREW1>=rew1-tolerancerew1:
            print("REW1 is correct")
            rew1flag=True
        else:
            print("REW1 is incorrect")
            rew1flag=False
        #Right Arm
        if rse1flag==True and rse1flag==True:
            rarm1flag=True
            print(rarm1flag)
        else:
            rarm1flag=False
            print(rarm1flag)
            
        if mRHK1<=rhk1+tolerancerhk1 and mRHK1>=rhk1-tolerancerhk1:
            print("RHK1 is correct")
            rhk1flag=True
        else:
            print("RHK1 is incorrect")
            rhk1flag=False
        if mRKA1<=rka1+tolerancerka1 and mRKA1>=rka1-tolerancerka1:
            print("RKA1 is correct")
            rka1flag=True
        else:
            print("RKA1 is incorrect")
            rka1flag=False
        #Right Leg
        if rhk1flag==True and rka1flag==True:
            rleg1flag=True
            print(rleg1flag)
        else:
            rleg1flag=False
            print(rleg1flag)
            
        if mLSE1<=lse1+tolerancerka1 and mLSE1>=lse1-tolerancerka1:
            print("LSE1 is correct")
            lse1flag=True
        else:
            print("LSE1 is incorrect")
            lse1flag=False
        if mLEW1<=lew1+tolerancelew1 and mLEW1>=lew1-tolerancelew1:
            print("LEW1 is correct")
            lew1flag=True
        else:
            print("LEW1 is incorrect")
            lew1flag=False
        #Left Arm
        if lew1flag==True and lse1flag==True:
            larm1flag=True
            print(larm1flag)
        else:
            larm1flag=False
            print(larm1flag)
            
        if mLHK1<=lhk1+tolerancelhk1 and mLHK1>=lhk1-tolerancelhk1:
            print("LHK1 is correct")
            lhk1flag=True
        else:
            print("LHK1 is incorrect")
            lhk1flag=False
        if mLKA1<=lka1+tolerancelka1 and mLKA1>=lka1-tolerancelka1:
            print("LKA1 is correct")
            lka1flag=True
        else:
            print("LKA1 is incorrect")
            lka1flag=False
        #Left Leg
        if lka1flag==True and lhk1flag==True:
            lleg1flag=True
            print(lleg1flag)
        else:
            lleg1flag=False
            print(lleg1flag)
        print("####Result####")
        print(ns1flag)
        print(rarm1flag)
        print(rleg1flag)
        print(larm1flag)
        print(lleg1flag)
        print("##############")
        #Second Step
        mNS2=trackdata[pos2,0]
        mRSE2=trackdata[pos2,1]
        mREW2=trackdata[pos2,2]
        mRHK2=trackdata[pos2,3]
        mRKA2=trackdata[pos2,4]
        mLSE2=trackdata[pos2,5]
        mLEW2=trackdata[pos2,6]
        mLHK2=trackdata[pos2,7]
        mLKA2=trackdata[pos2,8]
        #Slope Setting for Second Step
        tolerancens2=1
        tolerancerse2=1
        tolerancerew2=1
        tolerancerhk2=1
        tolerancerka2=1
        tolerancelse2=1
        tolerancelew2=1
        tolerancelhk2=1
        tolerancelka2=1
        ns2=9.8
        rse2=9.45
        rew2=0.12
        rhk2=-14.52
        rka2=-13.32
        lse2=-1.83
        lew2=11
        lhk2=12
        lka2=13
        if mNS2<=ns2+tolerancens2 and mNS2>=ns2-tolerancens2:
            print("NS2 is correct")
            ns2flag=True
        else:
            print("NS2 is incorrect")
            ns2flag=False
        if mRSE2<=rse2+tolerancerse2 and mRSE2>=rse2-tolerancerse2:
            print("RSE2 is correct")
            rse2flag=True
        else:
            print("RSE2 is incorrect")
            rse2flag=False
        if mREW2<=rew2+tolerancerew2 and mREW2>=rew2-tolerancerew2:
            print("REW2 is correct")
            rew2flag=True
        else:
            print("REW2 is incorrect")
            rew2flag=False
        #Right Arm
        if rse2flag==True and rse2flag==True:
            rarm2flag=True
            print(rarm2flag)
        else:
            rarm2flag=False
            print(rarm2flag)
            
        if mRHK2<=rhk2+tolerancerhk2 and mRHK2>=rhk2-tolerancerhk2:
            print("RHK2 is correct")
            rhk2flag=True
        else:
            print("RHK2 is incorrect")
            rhk2flag=False
        if mRKA2<=rka2+tolerancerka2 and mRKA2>=rka2-tolerancerka2:
            print("RKA2 is correct")
            rka2flag=True
        else:
            print("RKA2 is incorrect")
            rka2flag=False
        #Right Leg
        if rhk2flag==True and rka2flag==True:
            rleg2flag=True
            print(rleg2flag)
        else:
            rleg2flag=False
            print(rleg2flag)
            
        if mLSE2<=lse2+tolerancerka2 and mLSE2>=lse2-tolerancerka2:
            print("LSE2 is correct")
            lse2flag=True
        else:
            print("LSE2 is incorrect")
            lse2flag=False
        if mLEW2<=lew2+tolerancelew2 and mLEW2>=lew2-tolerancelew2:
            print("LEW2 is correct")
            lew2flag=True
        else:
            print("LEW2 is incorrect")
            lew2flag=False
        #Left Arm
        if lew2flag==True and lse2flag==True:
            larm2flag=True
            print(larm2flag)
        else:
            larm2flag=False
            print(larm2flag)
            
        if mLHK2<=lhk2+tolerancelhk2 and mLHK2>=lhk2-tolerancelhk2:
            print("LHK2 is correct")
            lhk2flag=True
        else:
            print("LHK2 is incorrect")
            lhk2flag=False
        if mLKA2<=lka2+tolerancelka2 and mLKA2>=lka2-tolerancelka2:
            print("LKA2 is correct")
            lka2flag=True
        else:
            print("LKA2 is incorrect")
            lka2flag=False
        #Left Leg
        if lka2flag==True and lhk2flag==True:
            lleg2flag=True
            print(lleg2flag)
        else:
            lleg2flag=False
            print(lleg2flag)
        print("####Result####")
        print(ns2flag)
        print(rarm2flag)
        print(rleg2flag)
        print(larm2flag)
        print(lleg2flag)
        print("##############")
        #Third Step
        mNS3=trackdata[pos3,0]
        mRSE3=trackdata[pos3,1]
        mREW3=trackdata[pos3,2]
        mRHK3=trackdata[pos3,3]
        mRKA3=trackdata[pos3,4]
        mLSE3=trackdata[pos3,5]
        mLEW3=trackdata[pos3,6]
        mLHK3=trackdata[pos3,7]
        mLKA3=trackdata[pos3,8]
        #Slope Setting for Third Step
        tolerancens3=1
        tolerancerse3=1
        tolerancerew3=1
        tolerancerhk3=1
        tolerancerka3=1
        tolerancelse3=1
        tolerancelew3=1
        tolerancelhk3=1
        tolerancelka3=1
        ns3=9.8
        rse3=9.45
        rew3=0.12
        rhk3=-14.52
        rka3=-13.32
        lse3=-1.83
        lew3=11
        lhk3=12
        lka3=13
        if mNS3<=ns3+tolerancens3 and mNS3>=ns3-tolerancens3:
            print("NS3 is correct")
            ns3flag=True
        else:
            print("NS3 is incorrect")
            ns3flag=False
        if mRSE3<=rse3+tolerancerse3 and mRSE3>=rse3-tolerancerse3:
            print("RSE3 is correct")
            rse3flag=True
        else:
            print("RSE3 is incorrect")
            rse3flag=False
        if mREW3<=rew3+tolerancerew3 and mREW3>=rew3-tolerancerew3:
            print("REW3 is correct")
            rew3flag=True
        else:
            print("REW3 is incorrect")
            rew3flag=False
        #Right Arm
        if rse3flag==True and rse3flag==True:
            rarm3flag=True
            print(rarm3flag)
        else:
            rarm3flag=False
            print(rarm3flag)
            
        if mRHK3<=rhk3+tolerancerhk3 and mRHK3>=rhk3-tolerancerhk3:
            print("RHK3 is correct")
            rhk3flag=True
        else:
            print("RHK3 is incorrect")
            rhk3flag=False
        if mRKA3<=rka3+tolerancerka3 and mRKA3>=rka3-tolerancerka3:
            print("RKA3 is correct")
            rka3flag=True
        else:
            print("RKA3 is incorrect")
            rka3flag=False
        #Right Leg
        if rhk3flag==True and rka3flag==True:
            rleg3flag=True
            print(rleg3flag)
        else:
            rleg3flag=False
            print(rleg3flag)
            
        if mLSE3<=lse3+tolerancerka3 and mLSE3>=lse3-tolerancerka3:
            print("LSE3 is correct")
            lse3flag=True
        else:
            print("LSE3 is incorrect")
            lse3flag=False
        if mLEW3<=lew3+tolerancelew3 and mLEW3>=lew3-tolerancelew3:
            print("LEW3 is correct")
            lew3flag=True
        else:
            print("LEW3 is incorrect")
            lew3flag=False
        #Left Arm
        if lew3flag==True and lse3flag==True:
            larm3flag=True
            print(larm3flag)
        else:
            larm3flag=False
            print(larm3flag)
            
        if mLHK3<=lhk3+tolerancelhk3 and mLHK3>=lhk3-tolerancelhk3:
            print("LHK3 is correct")
            lhk3flag=True
        else:
            print("LHK3 is incorrect")
            lhk3flag=False
        if mLKA3<=lka3+tolerancelka3 and mLKA3>=lka3-tolerancelka3:
            print("LKA3 is correct")
            lka3flag=True
        else:
            print("LKA3 is incorrect")
            lka3flag=False
        #Left Leg
        if lka3flag==True and lhk3flag==True:
            lleg3flag=True
            print(lleg3flag)
        else:
            lleg3flag=False
            print(lleg3flag)
        print("####Result####")
        print(ns3flag)
        print(rarm3flag)
        print(rleg3flag)
        print(larm3flag)
        print(lleg3flag)
        print("##############")
        #Fourth Step
        mNS4=trackdata[pos4,0]
        mRSE4=trackdata[pos4,1]
        mREW4=trackdata[pos4,2]
        mRHK4=trackdata[pos4,3]
        mRKA4=trackdata[pos4,4]
        mLSE4=trackdata[pos4,5]
        mLEW4=trackdata[pos4,6]
        mLHK4=trackdata[pos4,7]
        mLKA4=trackdata[pos4,8]
        #Slope Setting for Fourth Step
        tolerancens4=1
        tolerancerse4=1
        tolerancerew4=1
        tolerancerhk4=1
        tolerancerka4=1
        tolerancelse4=1
        tolerancelew4=1
        tolerancelhk4=1
        tolerancelka4=1
        ns4=9.8
        rse4=9.45
        rew4=0.12
        rhk4=-14.52
        rka4=-13.32
        lse4=-1.83
        lew4=11
        lhk4=12
        lka4=13
        if mNS4<=ns4+tolerancens4 and mNS4>=ns4-tolerancens4:
            print("NS4 is correct")
            ns4flag=True
        else:
            print("NS4 is incorrect")
            ns4flag=False
        if mRSE4<=rse4+tolerancerse4 and mRSE4>=rse4-tolerancerse4:
            print("RSE4 is correct")
            rse4flag=True
        else:
            print("RSE4 is incorrect")
            rse4flag=False
        if mREW4<=rew4+tolerancerew4 and mREW4>=rew4-tolerancerew4:
            print("REW4 is correct")
            rew4flag=True
        else:
            print("REW4 is incorrect")
            rew4flag=False
        #Right Arm
        if rse4flag==True and rse4flag==True:
            rarm4flag=True
            print(rarm4flag)
        else:
            rarm4flag=False
            print(rarm4flag)
            
        if mRHK4<=rhk4+tolerancerhk4 and mRHK4>=rhk4-tolerancerhk4:
            print("RHK4 is correct")
            rhk4flag=True
        else:
            print("RHK4 is incorrect")
            rhk4flag=False
        if mRKA4<=rka4+tolerancerka4 and mRKA4>=rka4-tolerancerka4:
            print("RKA4 is correct")
            rka4flag=True
        else:
            print("RKA4 is incorrect")
            rka4flag=False
        #Right Leg
        if rhk4flag==True and rka4flag==True:
            rleg4flag=True
            print(rleg4flag)
        else:
            rleg4flag=False
            print(rleg4flag)
            
        if mLSE4<=lse4+tolerancerka4 and mLSE4>=lse4-tolerancerka4:
            print("LSE4 is correct")
            lse4flag=True
        else:
            print("LSE4 is incorrect")
            lse4flag=False
        if mLEW4<=lew4+tolerancelew4 and mLEW4>=lew4-tolerancelew4:
            print("LEW4 is correct")
            lew4flag=True
        else:
            print("LEW4 is incorrect")
            lew4flag=False
        #Left Arm
        if lew4flag==True and lse4flag==True:
            larm4flag=True
            print(larm4flag)
        else:
            larm4flag=False
            print(larm4flag)
            
        if mLHK4<=lhk4+tolerancelhk4 and mLHK4>=lhk4-tolerancelhk4:
            print("LHK4 is correct")
            lhk4flag=True
        else:
            print("LHK4 is incorrect")
            lhk4flag=False
        if mLKA4<=lka4+tolerancelka4 and mLKA4>=lka4-tolerancelka4:
            print("LKA4 is correct")
            lka4flag=True
        else:
            print("LKA4 is incorrect")
            lka4flag=False
        #Left Leg
        if lka4flag==True and lhk4flag==True:
            lleg4flag=True
            print(lleg4flag)
        else:
            lleg4flag=False
            print(lleg4flag)
        print("####Result####")
        print(ns4flag)
        print(rarm4flag)
        print(rleg4flag)
        print(larm4flag)
        print(lleg4flag)
        print("##############")
        #Throw Step
        mNS5=trackdata[pos5,0]
        mRSE5=trackdata[pos5,1]
        mREW5=trackdata[pos5,2]
        mRHK5=trackdata[pos5,3]
        mRKA5=trackdata[pos5,4]
        mLSE5=trackdata[pos5,5]
        mLEW5=trackdata[pos5,6]
        mLHK5=trackdata[pos5,7]
        mLKA5=trackdata[pos5,8]
        #Slope Setting for Fifth Step
        tolerancens5=1
        tolerancerse5=1
        tolerancerew5=1
        tolerancerhk5=1
        tolerancerka5=1
        tolerancelse5=1
        tolerancelew5=1
        tolerancelhk5=1
        tolerancelka5=1
        ns5=9.8
        rse5=9.45
        rew5=0.12
        rhk5=-14.52
        rka5=-13.32
        lse5=-1.83
        lew5=11
        lhk5=12
        lka5=13
        if mNS5<=ns5+tolerancens5 and mNS5>=ns5-tolerancens5:
            print("NS5 is correct")
            ns5flag=True
        else:
            print("NS5 is incorrect")
            ns5flag=False
        if mRSE5<=rse5+tolerancerse5 and mRSE5>=rse5-tolerancerse5:
            print("RSE5 is correct")
            rse5flag=True
        else:
            print("RSE5 is incorrect")
            rse5flag=False
        if mREW5<=rew5+tolerancerew5 and mREW5>=rew5-tolerancerew5:
            print("REW5 is correct")
            rew5flag=True
        else:
            print("REW5 is incorrect")
            rew5flag=False
        #Right Arm
        if rse5flag==True and rse5flag==True:
            rarm5flag=True
            print(rarm5flag)
        else:
            rarm5flag=False
            print(rarm5flag)
            
        if mRHK5<=rhk5+tolerancerhk5 and mRHK5>=rhk5-tolerancerhk5:
            print("RHK5 is correct")
            rhk5flag=True
        else:
            print("RHK5 is incorrect")
            rhk5flag=False
        if mRKA5<=rka5+tolerancerka5 and mRKA5>=rka5-tolerancerka5:
            print("RKA5 is correct")
            rka5flag=True
        else:
            print("RKA5 is incorrect")
            rka5flag=False
        #Right Leg
        if rhk5flag==True and rka5flag==True:
            rleg5flag=True
            print(rleg5flag)
        else:
            rleg5flag=False
            print(rleg5flag)
            
        if mLSE5<=lse5+tolerancerka5 and mLSE5>=lse5-tolerancerka5:
            print("LSE5 is correct")
            lse5flag=True
        else:
            print("LSE5 is incorrect")
            lse5flag=False
        if mLEW5<=lew5+tolerancelew5 and mLEW5>=lew5-tolerancelew5:
            print("LEW5 is correct")
            lew5flag=True
        else:
            print("LEW5 is incorrect")
            lew5flag=False
        #Left Arm
        if lew5flag==True and lse5flag==True:
            larm5flag=True
            print(larm5flag)
        else:
            larm5flag=False
            print(larm5flag)
            
        if mLHK5<=lhk5+tolerancelhk5 and mLHK5>=lhk5-tolerancelhk5:
            print("LHK5 is correct")
            lhk5flag=True
        else:
            print("LHK5 is incorrect")
            lhk5flag=False
        if mLKA5<=lka5+tolerancelka5 and mLKA5>=lka5-tolerancelka5:
            print("LKA5 is correct")
            lka5flag=True
        else:
            print("LKA5 is incorrect")
            lka5flag=False
        #Left Leg
        if lka5flag==True and lhk5flag==True:
            lleg5flag=True
            print(lleg5flag)
        else:
            lleg5flag=False
            print(lleg5flag)
        print("####Result####")
        print(ns5flag)
        print(rarm5flag)
        print(rleg5flag)
        print(larm5flag)
        print(lleg5flag)
        print("##############")
        cnt=0
        result=np.array([["Body","Right Arm","Right Leg","Left Arm","Left Leg"],[ns1flag,rarm1flag,rleg1flag,larm1flag,lleg1flag],[ns2flag,rarm2flag,rleg2flag,larm2flag,lleg2flag], [ns3flag,rarm3flag,rleg3flag,larm3flag,lleg3flag], [ns4flag,rarm4flag,rleg4flag,larm4flag,lleg4flag], [ns5flag,rarm5flag,rleg5flag,larm5flag,lleg5flag]])
        print(result)
        self.table.setRowCount(5)
        for i in range(5):
             print(result[0,cnt])
             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+result[0,cnt]+""))
             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+result[1,cnt]+""))
             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+result[2,cnt]+""))
             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+result[3,cnt]+""))
             self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""+result[4,cnt]+""))
             self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""+result[5,cnt]+""))
             cnt=cnt+1
             
        
        os.remove("trackdata.npy")
    def right(self):
        global flag,frameposition,stackflag
        frameposition=0
        flag=0
        stackflag=1
        print("Analyzing Data for Right Hand....")
        trackdata=np.load('trackdata.npy')
        posdiv=int((len(trackdata)-len(trackdata)%5)/5)
        print(posdiv)
        pos1=(posdiv-1)*(1)
        pos2=(posdiv*2-1)*(1)
        pos3=(posdiv*3-1)*(1)
        pos4=(posdiv*4-1)*(1)
        pos5=(posdiv*5-1)*(1)
        
        #First Step
        mNS1=trackdata[pos1,0]
        mRSE1=trackdata[pos1,1]
        mREW1=trackdata[pos1,2]
        mRHK1=trackdata[pos1,3]
        mRKA1=trackdata[pos1,4]
        mLSE1=trackdata[pos1,5]
        mLEW1=trackdata[pos1,6]
        mLHK1=trackdata[pos1,7]
        mLKA1=trackdata[pos1,8]
        #Slope Setting for First Step
        tolerancens1=1
        tolerancerse1=1
        tolerancerew1=1
        tolerancerhk1=1
        tolerancerka1=1
        tolerancelse1=1
        tolerancelew1=1
        tolerancelhk1=1
        tolerancelka1=1
        ns1=9.8
        rse1=9.45
        rew1=0.12
        rhk1=-14.52
        rka1=-13.32
        lse1=-1.83
        lew1=11
        lhk1=12
        lka1=13
        if mNS1<=ns1+tolerancens1 and mNS1>=ns1-tolerancens1:
            print("NS1 is correct")
            ns1flag=True
        else:
            print("NS1 is incorrect")
            ns1flag=False
        if mRSE1<=rse1+tolerancerse1 and mRSE1>=rse1-tolerancerse1:
            print("RSE1 is correct")
            rse1flag=True
        else:
            print("RSE1 is incorrect")
            rse1flag=False
        if mREW1<=rew1+tolerancerew1 and mREW1>=rew1-tolerancerew1:
            print("REW1 is correct")
            rew1flag=True
        else:
            print("REW1 is incorrect")
            rew1flag=False
        #Right Arm
        if rse1flag==True and rse1flag==True:
            rarm1flag=True
            print(rarm1flag)
        else:
            rarm1flag=False
            print(rarm1flag)
            
        if mRHK1<=rhk1+tolerancerhk1 and mRHK1>=rhk1-tolerancerhk1:
            print("RHK1 is correct")
            rhk1flag=True
        else:
            print("RHK1 is incorrect")
            rhk1flag=False
        if mRKA1<=rka1+tolerancerka1 and mRKA1>=rka1-tolerancerka1:
            print("RKA1 is correct")
            rka1flag=True
        else:
            print("RKA1 is incorrect")
            rka1flag=False
        #Right Leg
        if rhk1flag==True and rka1flag==True:
            rleg1flag=True
            print(rleg1flag)
        else:
            rleg1flag=False
            print(rleg1flag)
            
        if mLSE1<=lse1+tolerancerka1 and mLSE1>=lse1-tolerancerka1:
            print("LSE1 is correct")
            lse1flag=True
        else:
            print("LSE1 is incorrect")
            lse1flag=False
        if mLEW1<=lew1+tolerancelew1 and mLEW1>=lew1-tolerancelew1:
            print("LEW1 is correct")
            lew1flag=True
        else:
            print("LEW1 is incorrect")
            lew1flag=False
        #Left Arm
        if lew1flag==True and lse1flag==True:
            larm1flag=True
            print(larm1flag)
        else:
            larm1flag=False
            print(larm1flag)
            
        if mLHK1<=lhk1+tolerancelhk1 and mLHK1>=lhk1-tolerancelhk1:
            print("LHK1 is correct")
            lhk1flag=True
        else:
            print("LHK1 is incorrect")
            lhk1flag=False
        if mLKA1<=lka1+tolerancelka1 and mLKA1>=lka1-tolerancelka1:
            print("LKA1 is correct")
            lka1flag=True
        else:
            print("LKA1 is incorrect")
            lka1flag=False
        #Left Leg
        if lka1flag==True and lhk1flag==True:
            lleg1flag=True
            print(lleg1flag)
        else:
            lleg1flag=False
            print(lleg1flag)
        print("####Result####")
        print(ns1flag)
        print(rarm1flag)
        print(rleg1flag)
        print(larm1flag)
        print(lleg1flag)
        print("##############")
        #Second Step
        mNS2=trackdata[pos2,0]
        mRSE2=trackdata[pos2,1]
        mREW2=trackdata[pos2,2]
        mRHK2=trackdata[pos2,3]
        mRKA2=trackdata[pos2,4]
        mLSE2=trackdata[pos2,5]
        mLEW2=trackdata[pos2,6]
        mLHK2=trackdata[pos2,7]
        mLKA2=trackdata[pos2,8]
        #Slope Setting for Second Step
        tolerancens2=1
        tolerancerse2=1
        tolerancerew2=1
        tolerancerhk2=1
        tolerancerka2=1
        tolerancelse2=1
        tolerancelew2=1
        tolerancelhk2=1
        tolerancelka2=1
        ns2=9.8
        rse2=9.45
        rew2=0.12
        rhk2=-14.52
        rka2=-13.32
        lse2=-1.83
        lew2=11
        lhk2=12
        lka2=13
        if mNS2<=ns2+tolerancens2 and mNS2>=ns2-tolerancens2:
            print("NS2 is correct")
            ns2flag=True
        else:
            print("NS2 is incorrect")
            ns2flag=False
        if mRSE2<=rse2+tolerancerse2 and mRSE2>=rse2-tolerancerse2:
            print("RSE2 is correct")
            rse2flag=True
        else:
            print("RSE2 is incorrect")
            rse2flag=False
        if mREW2<=rew2+tolerancerew2 and mREW2>=rew2-tolerancerew2:
            print("REW2 is correct")
            rew2flag=True
        else:
            print("REW2 is incorrect")
            rew2flag=False
        #Right Arm
        if rse2flag==True and rse2flag==True:
            rarm2flag=True
            print(rarm2flag)
        else:
            rarm2flag=False
            print(rarm2flag)
            
        if mRHK2<=rhk2+tolerancerhk2 and mRHK2>=rhk2-tolerancerhk2:
            print("RHK2 is correct")
            rhk2flag=True
        else:
            print("RHK2 is incorrect")
            rhk2flag=False
        if mRKA2<=rka2+tolerancerka2 and mRKA2>=rka2-tolerancerka2:
            print("RKA2 is correct")
            rka2flag=True
        else:
            print("RKA2 is incorrect")
            rka2flag=False
        #Right Leg
        if rhk2flag==True and rka2flag==True:
            rleg2flag=True
            print(rleg2flag)
        else:
            rleg2flag=False
            print(rleg2flag)
            
        if mLSE2<=lse2+tolerancerka2 and mLSE2>=lse2-tolerancerka2:
            print("LSE2 is correct")
            lse2flag=True
        else:
            print("LSE2 is incorrect")
            lse2flag=False
        if mLEW2<=lew2+tolerancelew2 and mLEW2>=lew2-tolerancelew2:
            print("LEW2 is correct")
            lew2flag=True
        else:
            print("LEW2 is incorrect")
            lew2flag=False
        #Left Arm
        if lew2flag==True and lse2flag==True:
            larm2flag=True
            print(larm2flag)
        else:
            larm2flag=False
            print(larm2flag)
            
        if mLHK2<=lhk2+tolerancelhk2 and mLHK2>=lhk2-tolerancelhk2:
            print("LHK2 is correct")
            lhk2flag=True
        else:
            print("LHK2 is incorrect")
            lhk2flag=False
        if mLKA2<=lka2+tolerancelka2 and mLKA2>=lka2-tolerancelka2:
            print("LKA2 is correct")
            lka2flag=True
        else:
            print("LKA2 is incorrect")
            lka2flag=False
        #Left Leg
        if lka2flag==True and lhk2flag==True:
            lleg2flag=True
            print(lleg2flag)
        else:
            lleg2flag=False
            print(lleg2flag)
        print("####Result####")
        print(ns2flag)
        print(rarm2flag)
        print(rleg2flag)
        print(larm2flag)
        print(lleg2flag)
        print("##############")
        #Third Step
        mNS3=trackdata[pos3,0]
        mRSE3=trackdata[pos3,1]
        mREW3=trackdata[pos3,2]
        mRHK3=trackdata[pos3,3]
        mRKA3=trackdata[pos3,4]
        mLSE3=trackdata[pos3,5]
        mLEW3=trackdata[pos3,6]
        mLHK3=trackdata[pos3,7]
        mLKA3=trackdata[pos3,8]
        #Slope Setting for Third Step
        tolerancens3=1
        tolerancerse3=1
        tolerancerew3=1
        tolerancerhk3=1
        tolerancerka3=1
        tolerancelse3=1
        tolerancelew3=1
        tolerancelhk3=1
        tolerancelka3=1
        ns3=9.8
        rse3=9.45
        rew3=0.12
        rhk3=-14.52
        rka3=-13.32
        lse3=-1.83
        lew3=11
        lhk3=12
        lka3=13
        if mNS3<=ns3+tolerancens3 and mNS3>=ns3-tolerancens3:
            print("NS3 is correct")
            ns3flag=True
        else:
            print("NS3 is incorrect")
            ns3flag=False
        if mRSE3<=rse3+tolerancerse3 and mRSE3>=rse3-tolerancerse3:
            print("RSE3 is correct")
            rse3flag=True
        else:
            print("RSE3 is incorrect")
            rse3flag=False
        if mREW3<=rew3+tolerancerew3 and mREW3>=rew3-tolerancerew3:
            print("REW3 is correct")
            rew3flag=True
        else:
            print("REW3 is incorrect")
            rew3flag=False
        #Right Arm
        if rse3flag==True and rse3flag==True:
            rarm3flag=True
            print(rarm3flag)
        else:
            rarm3flag=False
            print(rarm3flag)
            
        if mRHK3<=rhk3+tolerancerhk3 and mRHK3>=rhk3-tolerancerhk3:
            print("RHK3 is correct")
            rhk3flag=True
        else:
            print("RHK3 is incorrect")
            rhk3flag=False
        if mRKA3<=rka3+tolerancerka3 and mRKA3>=rka3-tolerancerka3:
            print("RKA3 is correct")
            rka3flag=True
        else:
            print("RKA3 is incorrect")
            rka3flag=False
        #Right Leg
        if rhk3flag==True and rka3flag==True:
            rleg3flag=True
            print(rleg3flag)
        else:
            rleg3flag=False
            print(rleg3flag)
            
        if mLSE3<=lse3+tolerancerka3 and mLSE3>=lse3-tolerancerka3:
            print("LSE3 is correct")
            lse3flag=True
        else:
            print("LSE3 is incorrect")
            lse3flag=False
        if mLEW3<=lew3+tolerancelew3 and mLEW3>=lew3-tolerancelew3:
            print("LEW3 is correct")
            lew3flag=True
        else:
            print("LEW3 is incorrect")
            lew3flag=False
        #Left Arm
        if lew3flag==True and lse3flag==True:
            larm3flag=True
            print(larm3flag)
        else:
            larm3flag=False
            print(larm3flag)
            
        if mLHK3<=lhk3+tolerancelhk3 and mLHK3>=lhk3-tolerancelhk3:
            print("LHK3 is correct")
            lhk3flag=True
        else:
            print("LHK3 is incorrect")
            lhk3flag=False
        if mLKA3<=lka3+tolerancelka3 and mLKA3>=lka3-tolerancelka3:
            print("LKA3 is correct")
            lka3flag=True
        else:
            print("LKA3 is incorrect")
            lka3flag=False
        #Left Leg
        if lka3flag==True and lhk3flag==True:
            lleg3flag=True
            print(lleg3flag)
        else:
            lleg3flag=False
            print(lleg3flag)
        print("####Result####")
        print(ns3flag)
        print(rarm3flag)
        print(rleg3flag)
        print(larm3flag)
        print(lleg3flag)
        print("##############")
        #Fourth Step
        mNS4=trackdata[pos4,0]
        mRSE4=trackdata[pos4,1]
        mREW4=trackdata[pos4,2]
        mRHK4=trackdata[pos4,3]
        mRKA4=trackdata[pos4,4]
        mLSE4=trackdata[pos4,5]
        mLEW4=trackdata[pos4,6]
        mLHK4=trackdata[pos4,7]
        mLKA4=trackdata[pos4,8]
        #Slope Setting for Fourth Step
        tolerancens4=1
        tolerancerse4=1
        tolerancerew4=1
        tolerancerhk4=1
        tolerancerka4=1
        tolerancelse4=1
        tolerancelew4=1
        tolerancelhk4=1
        tolerancelka4=1
        ns4=9.8
        rse4=9.45
        rew4=0.12
        rhk4=-14.52
        rka4=-13.32
        lse4=-1.83
        lew4=11
        lhk4=12
        lka4=13
        if mNS4<=ns4+tolerancens4 and mNS4>=ns4-tolerancens4:
            print("NS4 is correct")
            ns4flag=True
        else:
            print("NS4 is incorrect")
            ns4flag=False
        if mRSE4<=rse4+tolerancerse4 and mRSE4>=rse4-tolerancerse4:
            print("RSE4 is correct")
            rse4flag=True
        else:
            print("RSE4 is incorrect")
            rse4flag=False
        if mREW4<=rew4+tolerancerew4 and mREW4>=rew4-tolerancerew4:
            print("REW4 is correct")
            rew4flag=True
        else:
            print("REW4 is incorrect")
            rew4flag=False
        #Right Arm
        if rse4flag==True and rse4flag==True:
            rarm4flag=True
            print(rarm4flag)
        else:
            rarm4flag=False
            print(rarm4flag)
            
        if mRHK4<=rhk4+tolerancerhk4 and mRHK4>=rhk4-tolerancerhk4:
            print("RHK4 is correct")
            rhk4flag=True
        else:
            print("RHK4 is incorrect")
            rhk4flag=False
        if mRKA4<=rka4+tolerancerka4 and mRKA4>=rka4-tolerancerka4:
            print("RKA4 is correct")
            rka4flag=True
        else:
            print("RKA4 is incorrect")
            rka4flag=False
        #Right Leg
        if rhk4flag==True and rka4flag==True:
            rleg4flag=True
            print(rleg4flag)
        else:
            rleg4flag=False
            print(rleg4flag)
            
        if mLSE4<=lse4+tolerancerka4 and mLSE4>=lse4-tolerancerka4:
            print("LSE4 is correct")
            lse4flag=True
        else:
            print("LSE4 is incorrect")
            lse4flag=False
        if mLEW4<=lew4+tolerancelew4 and mLEW4>=lew4-tolerancelew4:
            print("LEW4 is correct")
            lew4flag=True
        else:
            print("LEW4 is incorrect")
            lew4flag=False
        #Left Arm
        if lew4flag==True and lse4flag==True:
            larm4flag=True
            print(larm4flag)
        else:
            larm4flag=False
            print(larm4flag)
            
        if mLHK4<=lhk4+tolerancelhk4 and mLHK4>=lhk4-tolerancelhk4:
            print("LHK4 is correct")
            lhk4flag=True
        else:
            print("LHK4 is incorrect")
            lhk4flag=False
        if mLKA4<=lka4+tolerancelka4 and mLKA4>=lka4-tolerancelka4:
            print("LKA4 is correct")
            lka4flag=True
        else:
            print("LKA4 is incorrect")
            lka4flag=False
        #Left Leg
        if lka4flag==True and lhk4flag==True:
            lleg4flag=True
            print(lleg4flag)
        else:
            lleg4flag=False
            print(lleg4flag)
        print("####Result####")
        print(ns4flag)
        print(rarm4flag)
        print(rleg4flag)
        print(larm4flag)
        print(lleg4flag)
        print("##############")
        #Throw Step
        mNS5=trackdata[pos5,0]
        mRSE5=trackdata[pos5,1]
        mREW5=trackdata[pos5,2]
        mRHK5=trackdata[pos5,3]
        mRKA5=trackdata[pos5,4]
        mLSE5=trackdata[pos5,5]
        mLEW5=trackdata[pos5,6]
        mLHK5=trackdata[pos5,7]
        mLKA5=trackdata[pos5,8]
        #Slope Setting for Fifth Step
        tolerancens5=1
        tolerancerse5=1
        tolerancerew5=1
        tolerancerhk5=1
        tolerancerka5=1
        tolerancelse5=1
        tolerancelew5=1
        tolerancelhk5=1
        tolerancelka5=1
        ns5=9.8
        rse5=9.45
        rew5=0.12
        rhk5=-14.52
        rka5=-13.32
        lse5=-1.83
        lew5=11
        lhk5=12
        lka5=13
        if mNS5<=ns5+tolerancens5 and mNS5>=ns5-tolerancens5:
            print("NS5 is correct")
            ns5flag=True
        else:
            print("NS5 is incorrect")
            ns5flag=False
        if mRSE5<=rse5+tolerancerse5 and mRSE5>=rse5-tolerancerse5:
            print("RSE5 is correct")
            rse5flag=True
        else:
            print("RSE5 is incorrect")
            rse5flag=False
        if mREW5<=rew5+tolerancerew5 and mREW5>=rew5-tolerancerew5:
            print("REW5 is correct")
            rew5flag=True
        else:
            print("REW5 is incorrect")
            rew5flag=False
        #Right Arm
        if rse5flag==True and rse5flag==True:
            rarm5flag=True
            print(rarm5flag)
        else:
            rarm5flag=False
            print(rarm5flag)
            
        if mRHK5<=rhk5+tolerancerhk5 and mRHK5>=rhk5-tolerancerhk5:
            print("RHK5 is correct")
            rhk5flag=True
        else:
            print("RHK5 is incorrect")
            rhk5flag=False
        if mRKA5<=rka5+tolerancerka5 and mRKA5>=rka5-tolerancerka5:
            print("RKA5 is correct")
            rka5flag=True
        else:
            print("RKA5 is incorrect")
            rka5flag=False
        #Right Leg
        if rhk5flag==True and rka5flag==True:
            rleg5flag=True
            print(rleg5flag)
        else:
            rleg5flag=False
            print(rleg5flag)
            
        if mLSE5<=lse5+tolerancerka5 and mLSE5>=lse5-tolerancerka5:
            print("LSE5 is correct")
            lse5flag=True
        else:
            print("LSE5 is incorrect")
            lse5flag=False
        if mLEW5<=lew5+tolerancelew5 and mLEW5>=lew5-tolerancelew5:
            print("LEW5 is correct")
            lew5flag=True
        else:
            print("LEW5 is incorrect")
            lew5flag=False
        #Left Arm
        if lew5flag==True and lse5flag==True:
            larm5flag=True
            print(larm5flag)
        else:
            larm5flag=False
            print(larm5flag)
            
        if mLHK5<=lhk5+tolerancelhk5 and mLHK5>=lhk5-tolerancelhk5:
            print("LHK5 is correct")
            lhk5flag=True
        else:
            print("LHK5 is incorrect")
            lhk5flag=False
        if mLKA5<=lka5+tolerancelka5 and mLKA5>=lka5-tolerancelka5:
            print("LKA5 is correct")
            lka5flag=True
        else:
            print("LKA5 is incorrect")
            lka5flag=False
        #Left Leg
        if lka5flag==True and lhk5flag==True:
            lleg5flag=True
            print(lleg5flag)
        else:
            lleg5flag=False
            print(lleg5flag)
        print("####Result####")
        print(ns5flag)
        print(rarm5flag)
        print(rleg5flag)
        print(larm5flag)
        print(lleg5flag)
        print("##############")
        cnt=0
        result=np.array([["Body","Right Arm","Right Leg","Left Arm","Left Leg"],[ns1flag,rarm1flag,rleg1flag,larm1flag,lleg1flag],[ns2flag,rarm2flag,rleg2flag,larm2flag,lleg2flag], [ns3flag,rarm3flag,rleg3flag,larm3flag,lleg3flag], [ns4flag,rarm4flag,rleg4flag,larm4flag,lleg4flag], [ns5flag,rarm5flag,rleg5flag,larm5flag,lleg5flag]])
        print(result)
        self.table.setRowCount(5)
        for i in range(5):
             print(result[0,cnt])
             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+result[0,cnt]+""))
             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+result[1,cnt]+""))
             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+result[2,cnt]+""))
             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+result[3,cnt]+""))
             self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""+result[4,cnt]+""))
             self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""+result[5,cnt]+""))
             cnt=cnt+1
             
        
        os.remove("trackdata.npy")
        
    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);##Neck
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);##Spine Base
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);##Shoulder to Elbow
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);##Elbow to Wrist
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);##Shoulder to Elbow
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);##Elbow to Wrist
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);##Hip to Knee
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);##Knee to Ankle
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);##Hip to Knee
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);##Knee to Ankle
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

        
    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()
    def draw_bodyframe(body_frame, kinect, img):
        if body_frame is not None: 
            for i in range(0, kinect.max_body_count):
                body = body_frame.bodies[i]
                if body.is_tracked: 
                    joints = body.joints
                    joint_points = kinect.body_joints_to_depth_space(joints) # Convert joint coordinates to depth space 
                    joint2D = get_joint2D(joints, joint_points) # Convert to numpy array format
                    img = draw_joint2D(img, joint2D, colors_order[i])
                    img = draw_bone2D(img, joint2D, colors_order[i])
                    break # Add a break here

        return img
    def Loop(self):
        global flag,frameposition,stackflag,startflag
        if flag==1:
            frameposition=frameposition+1
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self._done = True

                elif event.type == pygame.VIDEORESIZE: 
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

 
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
    
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[0])
                    
                    
                    print(" ")
                    print(" ")

                    #print("Head - X: "+str(joint_points[PyKinectV2.JointType_Head].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_Head].y)
                    #print("Neck - X: "+str(joint_points[PyKinectV2.JointType_Neck].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_Neck].y)
                    
                    #print("Spine Mid - X: "+str(joint_points[PyKinectV2.JointType_SpineMid].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_SpineMid].y)
                    #print("Spine Shoulder - X: "+str(joint_points[PyKinectV2.JointType_SpineShoulder].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_SpineShoulder].y)
                    #print("Spine Base - X: "+str(joint_points[PyKinectV2.JointType_SpineBase].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_SpineBase].y)

                    #print("Shoulder Right - X: "+str(joint_points[PyKinectV2.JointType_ShoulderRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_ShoulderRight].y)##
                    #print("Elbow Right - X: "+str(joint_points[PyKinectV2.JointType_ElbowRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_ElbowRight].y)##
                    #print("Hand Right - X: "+str(joint_points[PyKinectV2.JointType_HandRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_HandRight].y)
                    #print("Hand Tip Right - X: "+str(joint_points[PyKinectV2.JointType_HandTipRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_HandTipRight].y)
                    #print("Wrist Right - X: "+str(joint_points[PyKinectV2.JointType_WristRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_WristRight].y)##
                    #print("Thumb Right - X: "+str(joint_points[PyKinectV2.JointType_ThumbRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_ThumbRight].y)
                    
                    #print("Shoulder Left - X: "+str(joint_points[PyKinectV2.JointType_ShoulderLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_ShoulderLeft].y)##
                    #print("Elbow Left - X: "+str(joint_points[PyKinectV2.JointType_ElbowLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_ElbowLeft].y)##
                    #print("Hand Left - X: "+str(joint_points[PyKinectV2.JointType_HandLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_HandLeft].y)
                    #print("Hand Tip Left - X: "+str(joint_points[PyKinectV2.JointType_HandTipLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_HandTipLeft].y)
                    #print("Wrist Left - X: "+str(joint_points[PyKinectV2.JointType_WristLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_WristLeft].y)##
                    #print("Thumb Left - X: "+str(joint_points[PyKinectV2.JointType_ThumbLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_ThumbLeft].y)
                    
                    #print("Hip Right - X: "+str(joint_points[PyKinectV2.JointType_HipRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_HipRight].y)
                    #print("Knee Right - X: "+str(joint_points[PyKinectV2.JointType_KneeRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_KneeRight].y)
                    #print("Ankle Right - X: "+str(joint_points[PyKinectV2.JointType_AnkleRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_AnkleRight].y)
                    #print("Foot Right - X: "+str(joint_points[PyKinectV2.JointType_FootRight].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_FootRight].y)
                
                    #print("Hip Left - X: "+str(joint_points[PyKinectV2.JointType_HipLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_HipLeft].y)
                    #print("Knee Left - X: "+str(joint_points[PyKinectV2.JointType_KneeLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_KneeLeft].y)
                    #print("Ankle Left - X: "+str(joint_points[PyKinectV2.JointType_AnkleLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_AnkleLeft].y)
                    #print("Foot Left - X: "+str(joint_points[PyKinectV2.JointType_FootLeft].x) ,"Y: "+ str(joint_points[PyKinectV2.JointType_FootLeft].y)


                    
                    
                    #Settings for Slope Reference
                    #s1=2
                    #s2=4
                    #s3=6
                    #s4=8
                    #s5=10
                    #Percentage Scoring based on Slope 
                    mNS=(float(joint_points[PyKinectV2.JointType_Neck].y)-float(joint_points[PyKinectV2.JointType_SpineBase].y))/(float(joint_points[PyKinectV2.JointType_Neck].x)-float(joint_points[PyKinectV2.JointType_SpineBase].x))
                    mRSE=(float(joint_points[PyKinectV2.JointType_ShoulderRight].y)-float(joint_points[PyKinectV2.JointType_ElbowRight].y))/(float(joint_points[PyKinectV2.JointType_ShoulderRight].x)-float(joint_points[PyKinectV2.JointType_ElbowRight].x))
                    mREW=(float(joint_points[PyKinectV2.JointType_ElbowRight].y)-float(joint_points[PyKinectV2.JointType_WristRight].y))/(float(joint_points[PyKinectV2.JointType_ElbowRight].x)-float(joint_points[PyKinectV2.JointType_WristRight].x))
                    mRHK=(float(joint_points[PyKinectV2.JointType_HipRight].y)-float(joint_points[PyKinectV2.JointType_KneeRight].y))/(float(joint_points[PyKinectV2.JointType_HipRight].x)-float(joint_points[PyKinectV2.JointType_KneeRight].x))
                    mRKA=(float(joint_points[PyKinectV2.JointType_KneeRight].y)-float(joint_points[PyKinectV2.JointType_AnkleRight].y))/(float(joint_points[PyKinectV2.JointType_KneeRight].x)-float(joint_points[PyKinectV2.JointType_AnkleRight].x)) 
                    mLSE=(float(joint_points[PyKinectV2.JointType_ShoulderLeft].y)-float(joint_points[PyKinectV2.JointType_ElbowLeft].y))/(float(joint_points[PyKinectV2.JointType_ShoulderLeft].x)-float(joint_points[PyKinectV2.JointType_ElbowLeft].x))
                    mLEW=(float(joint_points[PyKinectV2.JointType_ElbowLeft].y)-float(joint_points[PyKinectV2.JointType_WristLeft].y))/(float(joint_points[PyKinectV2.JointType_ElbowLeft].x)-float(joint_points[PyKinectV2.JointType_WristLeft].x))
                    mLHK=(float(joint_points[PyKinectV2.JointType_HipLeft].y)-float(joint_points[PyKinectV2.JointType_KneeLeft].y))/(float(joint_points[PyKinectV2.JointType_HipLeft].x)-float(joint_points[PyKinectV2.JointType_KneeLeft].x))
                    mLKA=(float(joint_points[PyKinectV2.JointType_KneeLeft].y)-float(joint_points[PyKinectV2.JointType_AnkleLeft].y))/(float(joint_points[PyKinectV2.JointType_KneeLeft].x)-float(joint_points[PyKinectV2.JointType_AnkleLeft].x))
                    print("mNS="+str(mNS))
                    print("mRSE="+str(mRSE))
                    print("mREW="+str(mREW))
                    print("mRHK="+str(mRHK))
                    print("mRKA="+str(mRKA))
                    print("mLSE="+str(mLSE))
                    print("mLEW="+str(mLEW))
                    print("mLHK="+str(mLHK))
                    print("mLKA="+str(mLKA))
                    print("Frame: "+str(frameposition))
                    if startflag==1:
                        print("3")
                        time.sleep(1)
                        print("2")
                        time.sleep(1)
                        print("1")
                        time.sleep(1)
                        startflag=0
                    if stackflag==1:
                        stackdata=np.array([mNS,mRSE,mREW,mRHK,mRKA,mLSE,mLEW,mLHK,mLKA])
                        np.save('trackdata.npy',stackdata)
                        print(stackdata)
                        stackflag=0
                    elif stackflag==0:
                        stackdata=np.load('trackdata.npy')
                        trackdata=np.array([mNS,mRSE,mREW,mRHK,mRKA,mLSE,mLEW,mLHK,mLKA])
                        trackdata=np.vstack([trackdata,stackdata])
                        np.save('trackdata.npy',trackdata)
                        print(trackdata.shape)
                        
                    #First Step
                    #if frameposition==30*s1:
                    #elif frameposition==60*s1:
                    #Second Step
                    #elif frameposition==30*s2:
                    #elif frameposition==60*s2:
                    #Third Step    
                    #elif frameposition==30*s3:
                    #elif frameposition==60*s3:
                    #Fourth Step
                    #elif frameposition==30*s4:
                    #elif frameposition==60*s4:
                    #Final Step
                    #elif frameposition==30*s5:
                    #elif frameposition==60*s5:
                        
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            view = pygame.surfarray.array3d(surface_to_draw)
            
            view = view.transpose([1, 0, 2])
            image=view.copy()
            image = QtGui.QImage(image, image.shape[1], image.shape[0], 
                       image.strides[0], QtGui.QImage.Format_RGB888)
            image=image.scaledToHeight(180)
            self.i1.setPixmap(QtGui.QPixmap.fromImage(image))

            
            image = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
            lowerrange = np.array([0,0,255])
            upperrange = np.array([0,0,255])
            mask = cv2.inRange(image, lowerrange, upperrange)
            mask = cv2.convertScaleAbs(mask)
            image = cv2.bitwise_and(image,image,mask = mask)
            
            image = QtGui.QImage(image, image.shape[1], image.shape[0], 
                       image.strides[0], QtGui.QImage.Format_RGB888)
            image=image.scaledToHeight(180)
            self.i2.setPixmap(QtGui.QPixmap.fromImage(image))
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            
      
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
