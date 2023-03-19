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
        global flag,frameposition,stackflag,startflag,stepcnt,remarkdisp
        remarkdisp=""
        stepcnt=0
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
        
        pygame.display.set_caption("Golf Posture")

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
        self.i1.setGeometry(200,60,250,230)
        self.disp=QtGui.QPixmap("blackscreen.png")
        self.disp=self.disp.scaledToHeight(180)
        self.i1.setPixmap(self.disp)   
        #
        #Image Display Right
        self.i2=QtGui.QLabel(self)
        self.i2.setGeometry(550,60,250,230)
        self.dispa=QtGui.QPixmap("blackscreen.png")
        self.dispa=self.disp.scaledToHeight(180)
        self.i2.setPixmap(self.dispa)
        #
        #Register Menu
        self.registermenu = QtGui.QPushButton("Register",self)
        self.registermenu.clicked.connect(self.registerfunc)
        self.registermenu.move(400,280)
        self.registermenu.resize(200,50)
        #
        #Analyze Menu
        self.analyzemenu = QtGui.QPushButton("Analyze",self)
        self.analyzemenu.clicked.connect(self.analyzefunc)
        self.analyzemenu.move(400,350)
        self.analyzemenu.resize(200,50)
        #
        #Back Menu
        self.backmenu = QtGui.QPushButton("Back",self)
        self.backmenu.clicked.connect(self.backfunc)
        self.backmenu.move(800,700)
        #
        
        #Step Button
        self.stepbutton = QtGui.QPushButton("Step",self)
        self.stepbutton.clicked.connect(self.step)
        self.stepbutton.move(350,600)
        #
        #Register Step
        self.registerbutton = QtGui.QPushButton("Register",self)
        self.registerbutton.clicked.connect(self.register)
        self.registerbutton.move(400,580)
        self.registerbutton.resize(200,50)
        #
        #Delete Step
        self.deletebutton = QtGui.QPushButton("Delete",self)
        self.deletebutton.clicked.connect(self.delete)
        self.deletebutton.move(400,650)
        self.deletebutton.resize(200,50)
        #
        #
        #Scan Button
        self.scanbutton = QtGui.QPushButton("Scan",self)
        self.scanbutton.clicked.connect(self.scan)
        self.scanbutton.move(200,600)
        #

        #Play Button
        self.playbutton = QtGui.QPushButton("Play",self)
        self.playbutton.clicked.connect(self.play)
        self.playbutton.move(500,600)
        #
        #Stop Button
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(650,600)
        #
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.move(50,330)
        
        self.table.setHorizontalHeaderLabels(['Steps','Body','Right Arm','Right Leg','Left Arm', 'Left Leg'])
        self.table.resize(860,250)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        #Tolerance Registration
        self.status=QtGui.QLabel("",self)
        self.status.move(20,720)
        self.status.resize(600,30)

        self.remark=QtGui.QLabel("---",self)
        self.remark.move(20,680)
        self.remark.resize(600,30)

        
        self.t1=QtGui.QLabel("NS Tolerance: ",self)
        self.t1.move(220,300)
        self.t1.resize(200,30)
        self.t2=QtGui.QLineEdit(self)
        self.t2.move(370,300)
        self.t2.resize(50,30)

        

        self.t17=QtGui.QLabel("RSE Tolerance: ",self)
        self.t17.move(220,350)
        self.t17.resize(200,30)
        self.t18=QtGui.QLineEdit(self)
        self.t18.move(370,350)
        self.t18.resize(50,30)

        self.t3=QtGui.QLabel("REW Tolerance: ",self)
        self.t3.move(220,400)
        self.t3.resize(200,30)
        self.t4=QtGui.QLineEdit(self)
        self.t4.move(370,400)
        self.t4.resize(50,30)

        self.t5=QtGui.QLabel("RHK Tolerance: ",self)
        self.t5.move(220,450)
        self.t5.resize(200,30)
        self.t6=QtGui.QLineEdit(self)
        self.t6.move(370,450)
        self.t6.resize(50,30)

        self.t7=QtGui.QLabel("RKA Tolerance: ",self)
        self.t7.move(220,500)
        self.t7.resize(200,30)
        self.t8=QtGui.QLineEdit(self)
        self.t8.move(370,500)
        self.t8.resize(50,30)

        self.t9=QtGui.QLabel("LSE Tolerance: ",self)
        self.t9.move(520,350)
        self.t9.resize(200,30)
        self.t10=QtGui.QLineEdit(self)
        self.t10.move(670,350)
        self.t10.resize(50,30)

        self.t11=QtGui.QLabel("LEW Tolerance: ",self)
        self.t11.move(520,400)
        self.t11.resize(200,30)
        self.t12=QtGui.QLineEdit(self)
        self.t12.move(670,400)
        self.t12.resize(50,30)

        self.t13=QtGui.QLabel("LHK Tolerance: ",self)
        self.t13.move(520,450)
        self.t13.resize(200,30)
        self.t14=QtGui.QLineEdit(self)
        self.t14.move(670,450)
        self.t14.resize(50,30)

        self.t15=QtGui.QLabel("LKA Tolerance: ",self)
        self.t15.move(520,500)
        self.t15.resize(200,30)
        self.t16=QtGui.QLineEdit(self)
        self.t16.move(670,500)
        self.t16.resize(50,30)
        
        #Visibility
        self.i1.setVisible(0)
        self.i2.setVisible(0)
        self.stepbutton.setVisible(0)
        self.registerbutton.setVisible(0)
        self.deletebutton.setVisible(0)
        self.scanbutton.setVisible(0)
        self.playbutton.setVisible(0)
        self.stopbutton.setVisible(0)
        self.table.setVisible(0)
        self.backmenu.setVisible(0)
        self.t1.setVisible(0)
        self.t2.setVisible(0)
        self.t3.setVisible(0)
        self.t4.setVisible(0)
        self.t5.setVisible(0)
        self.t6.setVisible(0)
        self.t7.setVisible(0)
        self.t8.setVisible(0)
        self.t9.setVisible(0)
        self.t10.setVisible(0)
        self.t11.setVisible(0)
        self.t12.setVisible(0)
        self.t13.setVisible(0)
        self.t14.setVisible(0)
        self.t15.setVisible(0)
        self.t16.setVisible(0)
        self.t17.setVisible(0)
        self.t18.setVisible(0)
    def registerfunc(self):
        self.analyzemenu.setVisible(0)
        self.registermenu.setVisible(0)
        self.i1.setVisible(1)
        self.i2.setVisible(1)
        self.registerbutton.setVisible(1)
        self.backmenu.setVisible(1)
        self.t1.setVisible(1)
        self.t2.setVisible(1)
        self.t3.setVisible(1)
        self.t4.setVisible(1)
        self.t5.setVisible(1)
        self.t6.setVisible(1)
        self.t7.setVisible(1)
        self.t8.setVisible(1)
        self.t9.setVisible(1)
        self.t10.setVisible(1)
        self.t11.setVisible(1)
        self.t12.setVisible(1)
        self.t13.setVisible(1)
        self.t14.setVisible(1)
        self.t15.setVisible(1)
        self.t16.setVisible(1)
        self.t17.setVisible(1)
        self.t18.setVisible(1)
        self.deletebutton.setVisible(1)
    def analyzefunc(self):
        self.analyzemenu.setVisible(0)
        self.registermenu.setVisible(0)
        self.i1.setVisible(1)
        self.i2.setVisible(1)
        self.stepbutton.setVisible(1)
        self.scanbutton.setVisible(1)
        self.table.setVisible(1)
        self.playbutton.setVisible(1)
        self.stopbutton.setVisible(1)
        self.backmenu.setVisible(1)
        trackdata=np.load('trackdata.npy')
        self.status.setText("A total of "+str(len(trackdata))+" steps for analysis.")
    def backfunc(self):
        self.analyzemenu.setVisible(1)
        self.registermenu.setVisible(1)
        self.i1.setVisible(0)
        self.i2.setVisible(0)
        self.stepbutton.setVisible(0)
        self.registerbutton.setVisible(0)
        self.scanbutton.setVisible(0)
        self.playbutton.setVisible(0)
        self.stopbutton.setVisible(0)
        self.table.setVisible(0)
        self.backmenu.setVisible(0)
        self.t1.setVisible(0)
        self.t2.setVisible(0)
        self.t3.setVisible(0)
        self.t4.setVisible(0)
        self.t5.setVisible(0)
        self.t6.setVisible(0)
        self.t7.setVisible(0)
        self.t8.setVisible(0)
        self.t9.setVisible(0)
        self.t10.setVisible(0)
        self.t11.setVisible(0)
        self.t12.setVisible(0)
        self.t13.setVisible(0)
        self.t14.setVisible(0)
        self.t15.setVisible(0)
        self.t16.setVisible(0)
        self.t17.setVisible(0)
        self.t18.setVisible(0)
        self.deletebutton.setVisible(0)
        self.status.setText("")
    def stop(self):
        global flag,frameposition
        frameposition=0
        flag=0
        
    def delete(self):
        global flag,frameposition
        frameposition=0
        flag=0
        os.remove("trackdata.npy")
        self.status.setText("Data deleted.")
    def play(self):
        subprocess.Popen([os.path.join("C:/", "VideoLAN", "VLC", "vlc.exe"),os.path.join("demo.mp4")])
        
    def scan(self):
        global flag,frameposition,startflag
        frameposition=0
        flag=1
        startflag=1
    def register(self):     
        global flag
        flag=2
    def step(self):
        global flag
        self.status.setText("Searching for body to track...")
        flag=3
        
        
        
        
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
        global flag,frameposition,stackflag,startflag,stepcnt,remarkdisp
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

                    
                    joint_points_depth = self._kinect.body_joints_to_depth_space(joints)
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_Head].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_Head].y)
                    z =  22000/(x*y)
                    print("Head - X: "+str(joint_points[PyKinectV2.JointType_Head].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_Head].y)+" Z: "+str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_Neck].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_Neck].y)
                    z =  22000/(x*y)
                    print("Neck - X: "+str(joint_points[PyKinectV2.JointType_Neck].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_Neck].y) +" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_SpineMid].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_SpineMid].y)
                    z =  22000/(x*y)
                    print("Spine Mid - X: "+str(joint_points[PyKinectV2.JointType_SpineMid].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_SpineMid].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_SpineShoulder].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_SpineShoulder].y)
                    z =  22000/(x*y)
                    print("Spine Shoulder - X: "+str(joint_points[PyKinectV2.JointType_SpineShoulder].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_SpineShoulder].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_SpineBase].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_SpineBase].y)
                    z =  22000/(x*y)
                    print("Spine Base - X: "+str(joint_points[PyKinectV2.JointType_SpineBase].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_SpineBase].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_ShoulderRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_ShoulderRight].y)
                    z =  22000/(x*y)
                    print("Shoulder Right - X: "+str(joint_points[PyKinectV2.JointType_ShoulderRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_ShoulderRight].y)+" Z: "+ str(z))##
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_ElbowRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_ElbowRight].y)
                    z =  22000/(x*y)
                    print("Elbow Right - X: "+str(joint_points[PyKinectV2.JointType_ElbowRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_ElbowRight].y)+" Z: "+ str(z))##
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_HandRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_HandRight].y)
                    z =  22000/(x*y)
                    print("Hand Right - X: "+str(joint_points[PyKinectV2.JointType_HandRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_HandRight].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_HandTipRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_HandTipRight].y)
                    z =  22000/(x*y)
                    print("Hand Tip Right - X: "+str(joint_points[PyKinectV2.JointType_HandTipRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_HandTipRight].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_WristRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_WristRight].y)
                    z =  22000/(x*y)
                    print("Wrist Right - X: "+str(joint_points[PyKinectV2.JointType_WristRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_WristRight].y)+" Z: "+ str(z))##
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_ThumbRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_ThumbRight].y)
                    z =  22000/(x*y)
                    print("Thumb Right - X: "+str(joint_points[PyKinectV2.JointType_ThumbRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_ThumbRight].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_ShoulderLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_ShoulderLeft].y)
                    z =  22000/(x*y)
                    print("Shoulder Left - X: "+str(joint_points[PyKinectV2.JointType_ShoulderLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_ShoulderLeft].y)+" Z: "+ str(z))##
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_ElbowLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_ElbowLeft].y)
                    z =  22000/(x*y)
                    print("Elbow Left - X: "+str(joint_points[PyKinectV2.JointType_ElbowLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_ElbowLeft].y)+" Z: "+ str(z))##
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_HandLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_HandLeft].y)
                    z =  22000/(x*y)
                    print("Hand Left - X: "+str(joint_points[PyKinectV2.JointType_HandLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_HandLeft].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_HandTipLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_HandTipLeft].y)
                    z =  22000/(x*y)
                    print("Hand Tip Left - X: "+str(joint_points[PyKinectV2.JointType_HandTipLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_HandTipLeft].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_WristLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_WristLeft].y)
                    z =  22000/(x*y)
                    print("Wrist Left - X: "+str(joint_points[PyKinectV2.JointType_WristLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_WristLeft].y)+" Z: "+ str(z))##
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_ThumbLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_ThumbLeft].y)
                    z =  22000/(x*y)
                    print("Thumb Left - X: "+str(joint_points[PyKinectV2.JointType_ThumbLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_ThumbLeft].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_HipRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_HipRight].y)
                    z =  22000/(x*y)
                    print("Hip Right - X: "+str(joint_points[PyKinectV2.JointType_HipRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_HipRight].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_KneeRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_KneeRight].y)
                    z =  22000/(x*y)
                    print("Knee Right - X: "+str(joint_points[PyKinectV2.JointType_KneeRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_KneeRight].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_AnkleRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_AnkleRight].y)
                    z =  22000/(x*y)
                    print("Ankle Right - X: "+str(joint_points[PyKinectV2.JointType_AnkleRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_AnkleRight].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_FootRight].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_FootRight].y)
                    z =  22000/(x*y)
                    print("Foot Right - X: "+str(joint_points[PyKinectV2.JointType_FootRight].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_FootRight].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_HipLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_HipLeft].y)
                    z =  22000/(x*y)
                    print("Hip Left - X: "+str(joint_points[PyKinectV2.JointType_HipLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_HipLeft].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_KneeLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_KneeLeft].y)
                    z =  22000/(x*y)
                    print("Knee Left - X: "+str(joint_points[PyKinectV2.JointType_KneeLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_KneeLeft].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_AnkleLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_AnkleLeft].y)
                    z =  22000/(x*y)
                    print("Ankle Left - X: "+str(joint_points[PyKinectV2.JointType_AnkleLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_AnkleLeft].y)+" Z: "+ str(z))
                    ##
                    x= int(joint_points_depth[PyKinectV2.JointType_FootLeft].x)
                    y= int(joint_points_depth[PyKinectV2.JointType_FootLeft].y)
                    z =  22000/(x*y)
                    print("Foot Left - X: "+str(joint_points[PyKinectV2.JointType_FootLeft].x) +" Y: "+ str(joint_points[PyKinectV2.JointType_FootLeft].y)+" Z: "+ str(z))


                    
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
        elif flag==3:
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

                    #
                    
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
                    frameposition=0
                    flag=0
                    
                    
                    trackdata=np.load('trackdata.npy')
                    
                    if stepcnt<=len(trackdata)-1:
                        #Step
                        print("Analyzing Steps....")
                        
                        
                        #Slope Setting for First Step
                        tolerancens=trackdata[stepcnt,9]
                        tolerancerse=trackdata[stepcnt,10]
                        tolerancerew=trackdata[stepcnt,11]
                        tolerancerhk=trackdata[stepcnt,12]
                        tolerancerka=trackdata[stepcnt,13]
                        tolerancelse=trackdata[stepcnt,14]
                        tolerancelew=trackdata[stepcnt,15]
                        tolerancelhk=trackdata[stepcnt,16]
                        tolerancelka=trackdata[stepcnt,17]
                        ns=trackdata[stepcnt,0]
                        rse=trackdata[stepcnt,1]
                        rew=trackdata[stepcnt,2]
                        rhk=trackdata[stepcnt,3]
                        rka=trackdata[stepcnt,4]
                        lse=trackdata[stepcnt,5]
                        lew=trackdata[stepcnt,6]
                        lhk=trackdata[stepcnt,7]
                        lka=trackdata[stepcnt,8]
                        stepcnt=stepcnt+1
                        #Body
                        if mNS<=ns+tolerancens and mNS>=ns-tolerancens:
                            print("NS is correct")
                            nsflag=True
                        else:
                            print("NS is incorrect")
                            nsflag=False
                        #####################      
                        if mRSE<=rse+tolerancerse and mRSE>=rse-tolerancerse:
                            print("RSE is correct")
                            rseflag=True
                        else:
                            print("RSE is incorrect")
                            rseflag=False
                            
                        if mREW<=rew+tolerancerew and mREW>=rew-tolerancerew:
                            print("REW is correct")
                            rewflag=True
                        else:
                            print("REW is incorrect")
                            rewflag=False
                            
                        #Right Arm
                        if rseflag==True and rseflag==True:
                            rarmflag=True
                            print(rarmflag)
                        else:
                            rarmflag=False
                            print(rarmflag)
                        #####################    
                        if mRHK<=rhk+tolerancerhk and mRHK>=rhk-tolerancerhk:
                            print("RHK is correct")
                            rhkflag=True
                        else:
                            print("RHK is incorrect")
                            rhkflag=False

                            
                        if mRKA<=rka+tolerancerka and mRKA>=rka-tolerancerka:
                            print("RKA is correct")
                            rkaflag=True
                        else:
                            print("RKA is incorrect")
                            rkaflag=False
                            
                        #Right Leg
                        if rhkflag==True and rkaflag==True:
                            rlegflag=True
                            print(rlegflag)
                        else:
                            rlegflag=False
                            print(rlegflag)
                        #####################    
                        if mLSE<=lse+tolerancerka and mLSE>=lse-tolerancerka:
                            print("LSE is correct")
                            lseflag=True
                        else:
                            print("LSE is incorrect")
                            lseflag=False
                            
                        if mLEW<=lew+tolerancelew and mLEW>=lew-tolerancelew:
                            print("LEW is correct")
                            lewflag=True
                        else:
                            print("LEW is incorrect")
                            lewflag=False
                        #Left Arm
                        if lewflag==True and lseflag==True:
                            larmflag=True
                            print(larmflag)
                        else:
                            larmflag=False
                            print(larmflag)
                        #####################    
                        if mLHK<=lhk+tolerancelhk and mLHK>=lhk-tolerancelhk:
                            print("LHK is correct")
                            lhkflag=True
                        else:
                            print("LHK is incorrect")
                            lhkflag=False
                        if mLKA<=lka+tolerancelka and mLKA>=lka-tolerancelka:
                            print("LKA is correct")
                            lkaflag=True
                        else:
                            print("LKA is incorrect")
                            lkaflag=False
                        #Left Leg
                        if lkaflag==True and lhkflag==True:
                            llegflag=True
                            print(llegflag)
                        else:
                            llegflag=False
                            print(llegflag)
                        #####################
                        print("####Result####")
                        print(nsflag)
                        print(rarmflag)
                        print(rlegflag)
                        print(larmflag)
                        print(llegflag)
                        print("##############")

                        
                        
                        if stackflag==1:
                            #if os.path.isfile('resultdata.npy'):
                               
                            result=np.array([[nsflag,rarmflag,rlegflag,larmflag,llegflag,str(stepcnt)]])
                            np.save('resultdata.npy',result)
                            stackflag=0
                            print(result.shape)
                            print(result)
                            remarkdisp="Step 1: "
                            if nsflag==False:
                                remarkdisp=remarkdisp+"Body -"
                            if rarmflag==False:
                                remarkdisp=remarkdisp+"Right Arm -"
                            if rlegflag==False:
                                remarkdisp=remarkdisp+"Right Leg -"
                            if larmflag==False:
                                remarkdisp=remarkdisp+"Left Arm -"
                            if llegflag==False:
                                remarkdisp=remarkdisp+"Left Leg -"
                            if nsflag==False or rarmflag==False or rlegflag==False or larmflag==False or llegflag==False:
                                remarkdisp=remarkdisp+" is slightly off, needs more improvement. "
                            
                        elif stackflag==0:
                            stackdata=np.load('resultdata.npy')
                            result=np.array([[nsflag,rarmflag,rlegflag,larmflag,llegflag,str(stepcnt)]])
                            result=np.vstack([stackdata,result])
                            np.save('resultdata.npy',result)
                            print(result.shape)
                            print(result)
                            remarkdisp=" - Step "+str(stepcnt)+": "
                            if nsflag==False:
                                remarkdisp=remarkdisp+"Body -"
                            if rarmflag==False:
                                remarkdisp=remarkdisp+"Right Arm -"
                            if rlegflag==False:
                                remarkdisp=remarkdisp+"Right Leg -"
                            if larmflag==False:
                                remarkdisp=remarkdisp+"Left Arm -"
                            if llegflag==False:
                                remarkdisp=remarkdisp+"Left Leg -"
                            if nsflag==False or rarmflag==False or rlegflag==False or larmflag==False or llegflag==False:
                                remarkdisp=remarkdisp+" is slightly off, needs more improvement. "
                        self.remark.setText(remarkdisp)
                        print(remarkdisp)
                        self.table.setRowCount(len(result))
                        cnt=0
                        for i in range(len(result)):
                             
                             self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(result[cnt,5])+""))
                             self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(result[cnt,0])+""))
                             self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(result[cnt,1])+""))
                             self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(result[cnt,2])+""))
                             self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(result[cnt,3])+""))
                             self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(result[cnt,4])+""))
                             cnt=cnt+1
                        if stepcnt==len(trackdata):     
                            self.stepbutton.setText("Again")
                            remarkdisp=""
                    else:
                        stepcnt=0
                        stackflag=1
                        
                        cnt=0
                        result=np.load('resultdata.npy')
                        for i in range(len(result)):
                            self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""))
                            self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""))
                            self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""))
                            self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""))
                            self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""))
                            self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""))
                            cnt=cnt+1
                        os.remove("resultdata.npy")
                        self.stepbutton.setText("Step")
                        
                        
                        self.remark.setText(remarkdisp)
                        print("Done....")
                    flag=0    
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
        elif flag==2:
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
                    print("mNS="+str(mNS))#Neck to Spine
                    print("mRSE="+str(mRSE)) #Right Shoulder to Right Elbow
                    print("mREW="+str(mREW)) #Right Elbow to Right Wrist
                    print("mRHK="+str(mRHK)) #Right Hip to Right Knee
                    print("mRKA="+str(mRKA)) #Right Knee to Right Ankle
                    print("mLSE="+str(mLSE)) #Left Shoulder to Left Elbow   
                    print("mLEW="+str(mLEW)) #Left Elbow to Left Wrist
                    print("mLHK="+str(mLHK)) #Left Hip to Left Knee
                    print("mLKA="+str(mLKA)) #Left Knee to Left Ankle   
                    print("Frame: "+str(frameposition))

                  
                    tolerancens=float(self.t2.text())
                    tolerancerse=float(self.t4.text())
                    tolerancerew=float(self.t6.text())
                    tolerancerhk=float(self.t8.text())
                    tolerancerka=float(self.t10.text())
                    tolerancelse=float(self.t12.text())
                    tolerancelew=float(self.t14.text())
                    tolerancelhk=float(self.t16.text())
                    tolerancelka=float(self.t18.text())
                    if os.path.isfile('trackdata.npy'):
                        stackdata=np.load('trackdata.npy')
                        
                        
                        trackdata=np.array([mNS,mRSE,mREW,mRHK,mRKA,mLSE,mLEW,mLHK,mLKA,tolerancens,tolerancerse,tolerancerew,tolerancerhk,tolerancerka,tolerancelse,tolerancelew,tolerancelhk,tolerancelka])
                        trackdata=np.vstack([trackdata,stackdata])
                        np.save('trackdata.npy',trackdata)
                        print(trackdata.shape)
                        print(trackdata)
                        self.status.setText("Step "+str(len(trackdata))+" added. A total of "+str(len(trackdata))+" steps registered.")
                    else:
                        stackdata=np.array([mNS,mRSE,mREW,mRHK,mRKA,mLSE,mLEW,mLHK,mLKA,tolerancens,tolerancerse,tolerancerew,tolerancerhk,tolerancerka,tolerancelse,tolerancelew,tolerancelhk,tolerancelka])
                        np.save('trackdata.npy',stackdata)
                        print(stackdata)
                        self.status.setText("Step 1 added. A total of 1 steps registered.")
                    
                    flag=0
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
