import sys
from PyQt4 import QtGui, QtCore
import time
import os

from heapq import heappush, heappop # for priority queue
import math
import random
import serial
ser=serial.Serial('COM4',115200,timeout=1)
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()
       
        self._bodies = None
    def initUI(self):
        global flag,locflag,xB,yB,xA,yA
        xA=0
        yA=0
        xB=0
        yB=0
        locflag=0
        flag=0
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.setGeometry(0,20,1200,800)
        #Node A
        self.tilemap1 = QtGui.QPushButton(self)
        self.tilemap1.clicked.connect(self.tilemapfunc1)
        self.tilemap1.move(100,100)
        self.tilemap1.resize(100,100)
        

        self.tilemap2 = QtGui.QPushButton(self)
        self.tilemap2.clicked.connect(self.tilemapfunc2)
        self.tilemap2.move(200,100)
        self.tilemap2.resize(100,100)
        

        self.tilemap3 = QtGui.QPushButton(self)
        self.tilemap3.clicked.connect(self.tilemapfunc3)
        self.tilemap3.move(300,100)
        self.tilemap3.resize(100,100)
        

        self.tilemap4 = QtGui.QPushButton(self)
        self.tilemap4.clicked.connect(self.tilemapfunc4)
        self.tilemap4.move(100,200)
        self.tilemap4.resize(100,100)
        

        self.tilemap5 = QtGui.QPushButton(self)
        self.tilemap5.clicked.connect(self.tilemapfunc5)
        self.tilemap5.move(300,200)
        self.tilemap5.resize(100,100)
        

        self.tilemap6 = QtGui.QPushButton(self)
        self.tilemap6.clicked.connect(self.tilemapfunc6)
        self.tilemap6.move(100,300)
        self.tilemap6.resize(100,100)
       

        self.tilemap7 = QtGui.QPushButton(self)
        self.tilemap7.clicked.connect(self.tilemapfunc7)
        self.tilemap7.move(200,300)
        self.tilemap7.resize(100,100)
        

        self.tilemap8 = QtGui.QPushButton(self)
        self.tilemap8.clicked.connect(self.tilemapfunc8)
        self.tilemap8.move(300,300)
        self.tilemap8.resize(100,100)
        

        self.tilemap9 = QtGui.QPushButton(self)
        self.tilemap9.clicked.connect(self.tilemapfunc9)
        self.tilemap9.move(100,400)
        self.tilemap9.resize(100,100)
       

        self.tilemap10 = QtGui.QPushButton(self)
        self.tilemap10.clicked.connect(self.tilemapfunc10)
        self.tilemap10.move(300,400)
        self.tilemap10.resize(100,100)
        

        self.tilemap11 = QtGui.QPushButton(self)
        self.tilemap11.clicked.connect(self.tilemapfunc11)
        self.tilemap11.move(100,500)
        self.tilemap11.resize(100,100)
        

        self.tilemap12 = QtGui.QPushButton(self)
        self.tilemap12.clicked.connect(self.tilemapfunc12)
        self.tilemap12.move(200,500)
        self.tilemap12.resize(100,100)
        

        self.tilemap13 = QtGui.QPushButton(self)
        self.tilemap13.clicked.connect(self.tilemapfunc13)
        self.tilemap13.move(300,500)
        self.tilemap13.resize(100,100)
        #Node B
        self.tilemap14 = QtGui.QPushButton(self)
        self.tilemap14.clicked.connect(self.tilemapfunc14)
        self.tilemap14.move(400,100)
        self.tilemap14.resize(100,100)
        

        self.tilemap15 = QtGui.QPushButton(self)
        self.tilemap15.clicked.connect(self.tilemapfunc15)
        self.tilemap15.move(500,100)
        self.tilemap15.resize(100,100)
        

        self.tilemap16 = QtGui.QPushButton(self)
        self.tilemap16.clicked.connect(self.tilemapfunc16)
        self.tilemap16.move(600,100)
        self.tilemap16.resize(100,100)
        

        self.tilemap17 = QtGui.QPushButton(self)
        self.tilemap17.clicked.connect(self.tilemapfunc17)
        self.tilemap17.move(400,200)
        self.tilemap17.resize(100,100)
        

        self.tilemap18 = QtGui.QPushButton(self)
        self.tilemap18.clicked.connect(self.tilemapfunc18)
        self.tilemap18.move(600,200)
        self.tilemap18.resize(100,100)
        

        self.tilemap19 = QtGui.QPushButton(self)
        self.tilemap19.clicked.connect(self.tilemapfunc19)
        self.tilemap19.move(400,300)
        self.tilemap19.resize(100,100)
       

        self.tilemap20 = QtGui.QPushButton(self)
        self.tilemap20.clicked.connect(self.tilemapfunc20)
        self.tilemap20.move(500,300)
        self.tilemap20.resize(100,100)
        

        self.tilemap21 = QtGui.QPushButton(self)
        self.tilemap21.clicked.connect(self.tilemapfunc21)
        self.tilemap21.move(600,300)
        self.tilemap21.resize(100,100)
        

        self.tilemap22 = QtGui.QPushButton(self)
        self.tilemap22.clicked.connect(self.tilemapfunc22)
        self.tilemap22.move(400,400)
        self.tilemap22.resize(100,100)
       

        self.tilemap23 = QtGui.QPushButton(self)
        self.tilemap23.clicked.connect(self.tilemapfunc23)
        self.tilemap23.move(600,400)
        self.tilemap23.resize(100,100)
        

        self.tilemap24 = QtGui.QPushButton(self)
        self.tilemap24.clicked.connect(self.tilemapfunc24)
        self.tilemap24.move(400,500)
        self.tilemap24.resize(100,100)
        

        self.tilemap25 = QtGui.QPushButton(self)
        self.tilemap25.clicked.connect(self.tilemapfunc25)
        self.tilemap25.move(500,500)
        self.tilemap25.resize(100,100)
        

        self.tilemap26 = QtGui.QPushButton(self)
        self.tilemap26.clicked.connect(self.tilemapfunc26)
        self.tilemap26.move(600,500)
        self.tilemap26.resize(100,100)

       
        
    def tilemapfunc1(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=0
        yB=0
        print("A1")
        

    def tilemapfunc2(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=1
        yB=0
        print("A2")
        
    def tilemapfunc3(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=2
        yB=0
        print("A3")
        
    def tilemapfunc4(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=0
        yB=1
        print("A4")
        

    def tilemapfunc5(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=2
        yB=1
        print("A5")
        

    def tilemapfunc6(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=0
        yB=2
        print("A6")
        
    def tilemapfunc7(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=1
        yB=2
        print("A7")
        
            
    def tilemapfunc8(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=2
        yB=2
        print("A8")
        

    def tilemapfunc9(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=0
        yB=3
        print("A9")
        

    def tilemapfunc10(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=2
        yB=3
        print("A10")
        i

    def tilemapfunc11(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=0
        yB=4
        print("A11")
        

    def tilemapfunc12(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=1
        yB=4
        print("A12")
        
    def tilemapfunc13(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=2
        yB=4
        print("A13")

    def tilemapfunc14(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=3
        yB=0
        print("A14")
    def tilemapfunc15(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=4
        yB=0
        print("A15")
    def tilemapfunc16(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=5
        yB=0
        print("A16")
    def tilemapfunc17(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=3
        yB=1
        print("A17")
    def tilemapfunc18(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=5
        yB=1
        print("A18")
    def tilemapfunc19(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=3
        yB=2
        print("A19")
    def tilemapfunc20(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=4
        yB=2
        print("A20")
    def tilemapfunc21(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=5
        yB=2
        print("A21")
    def tilemapfunc22(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=3
        yB=3
        print("A22")
    def tilemapfunc23(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=5
        yB=3
        print("A23")
    def tilemapfunc24(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=3
        yB=4
        print("A24")
    def tilemapfunc25(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=4
        yB=4
        print("A25")
    def tilemapfunc26(self):
        global flag,locflag,xB,yB
        locflag=1
        xB=5
        yB=4
        print("A26")    


    
    def Loop(self):
        global locflag,xB,yB,xA,yA
        class node:
            xPos = 0 
            yPos = 0
            distance = 0 
            priority = 0 
            def __init__(self, xPos, yPos, distance, priority): 
                self.xPos = xPos
                self.yPos = yPos
                self.distance = distance
                self.priority = priority
            def __lt__(self, other): 
                return self.priority < other.priority
            def updatePriority(self, xDest, yDest):
                self.priority = self.distance + self.estimate(xDest, yDest) * 10 # A*
            
            def nextMove(self, dirs, d): 
                if dirs == 8 and d % 2 != 0:
                    self.distance += 14
                else:
                    self.distance += 10
            
            def estimate(self, xDest, yDest):
                xd = xDest - self.xPos
                yd = yDest - self.yPos
                
                d = math.sqrt(xd * xd + yd * yd)
                
                return(d)
        
        def pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB):
            closed_nodes_map = [] 
            open_nodes_map = []
            dir_map = [] 
            row = [0] * n
            for i in range(m): 
                closed_nodes_map.append(list(row))
                open_nodes_map.append(list(row))
                dir_map.append(list(row))

            pq = [[], []] 
            pqi = 0 
            
            n0 = node(xA, yA, 0, 0) 
            n0.updatePriority(xB, yB) 
            heappush(pq[pqi], n0)
            open_nodes_map[int(yA)][int(xA)] = n0.priority 

            
            while len(pq[pqi]) > 0:
                
                n1 = pq[pqi][0] 
                n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
                x = n0.xPos
                y = n0.yPos
                heappop(pq[pqi]) 
                open_nodes_map[int(y)][int(x)] = 0
                closed_nodes_map[int(y)][int(x)] = 1 

                
                if x == xB and y == yB:
                    
                    path = ''
                    while not (x == xA and y == yA):
                        j = int(dir_map[int(y)][int(x)])
                        c = str(int((j + dirs / 2) % dirs)) 
                        path = c + path
                        x += dx[j]
                        y += dy[j]
                    return path

                
                for i in range(dirs):
                    xdx = x + dx[i]
                    ydy = y + dy[i]
                    if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                            or the_map[int(ydy)][int(xdx)] == 1 or closed_nodes_map[int(ydy)][int(xdx)] == 1):
                        
                        m0 = node(xdx, ydy, n0.distance, n0.priority)
                        m0.nextMove(dirs, i)
                        m0.updatePriority(xB, yB)
                        
                        if open_nodes_map[int(ydy)][int(xdx)] == 0:
                            open_nodes_map[int(ydy)][int(xdx)] = m0.priority
                            heappush(pq[pqi], m0)
                            
                            dir_map[int(ydy)][int(xdx)] = (i + dirs / 2) % dirs
                        elif open_nodes_map[int(ydy)][int(xdx)] > m0.priority:
                            
                            open_nodes_map[int(ydy)][int(xdx)] = m0.priority
                            
                            dir_map[int(ydy)][int(xdx)] = (i + dirs / 2) % dirs
                            
                            while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                                heappush(pq[1 - pqi], pq[pqi][0])
                                heappop(pq[pqi])
                            heappop(pq[pqi])
                            
                            if len(pq[pqi]) > len(pq[1 - pqi]):
                                pqi = 1 - pqi
                            while len(pq[pqi]) > 0:
                                heappush(pq[1-pqi], pq[pqi][0])
                                heappop(pq[pqi])       
                            pqi = 1 - pqi
                            heappush(pq[pqi], m0) 
            return ''
        #try:
        if True:
            lightsensor=str(ser.readline())
            
            lightdata=lightsensor.split("'")[1]
            lightdata=lightdata.split(",")[0]
            print(lightdata)
            if lightdata=="A1":
                xA=0
                yA=0
                locflag=1
            elif lightdata=="A2":
                xA=1
                yA=0
                locflag=1
            elif lightdata=="A3":
                xA=2
                yA=0
                locflag=1
            elif lightdata=="A4":
                xA=0
                yA=1
                locflag=1
            elif lightdata=="A5":
                xA=1
                yA=1
                locflag=1
            elif lightdata=="A6":
                xA=0
                yA=2
                locflag=1
            elif lightdata=="A7":
                xA=1
                yA=2
                locflag=1
            elif lightdata=="A8":
                xA=2
                yA=2
                locflag=1
            elif lightdata=="A9":
                xA=0
                yA=3
                locflag=1
            elif lightdata=="A10":
                xA=2
                yA=3
                locflag=1
            elif lightdata=="A11":
                xA=0
                yA=4
                locflag=1
            elif lightdata=="A12":
                xA=1
                yA=4
                locflag=1
            elif lightdata=="A13":
                xA=2
                yA=4
                locflag=1

            elif lightdata=="A14":
                xA=3
                yA=0
                locflag=1
            elif lightdata=="A15":
                xA=4
                yA=0
                locflag=1
            elif lightdata=="A16":
                xA=5
                yA=0
                locflag=1
            elif lightdata=="A17":
                xA=3
                yA=1
                locflag=1
            elif lightdata=="A18":
                xA=5
                yA=1
                locflag=1
            elif lightdata=="A19":
                xA=3
                yA=2
                locflag=1
            elif lightdata=="A20":
                xA=4
                yA=2
                locflag=1
            elif lightdata=="A21":
                xA=5
                yA=2
                locflag=1
            elif lightdata=="A22":
                xA=3
                yA=3
                locflag=1
            elif lightdata=="A23":
                xA=5
                yA=3
                locflag=1
            elif lightdata=="A24":
                xA=3
                yA=4
                locflag=1
            elif lightdata=="A25":
                xA=4
                yA=4
                locflag=1
            elif lightdata=="A26":
                xA=5
                yA=4
                locflag=1
        #except:
        #    print("No Serial Data")
        if locflag==1:
            dirs = 4 
            if dirs == 4:
                dx = [1, 0, -1, 0]
                dy = [0, 1, 0, -1]
            elif dirs == 8:
                dx = [1, 1, 0, -1, -1, -1, 0, 1]
                dy = [0, 1, 1, 1, 0, -1, -1, -1]

            n = 6 
            m = 5 
            the_map = []
            row = [0] * n
            for i in range(m): 
                the_map.append(list(row))




            #Obstacle Input
            the_map[1][1] = 1
            the_map[3][1] = 1
            the_map[1][4] = 1
            the_map[3][4] = 1

            #xA=0
            #yA=0
            #xB=1
            #yB=4
            #xA = int(xA)
            #yA = int(yA)
            #xB = int(xB)
            #yB = int(yB)

            
            # print ("Debug: Starting the_map is ", the_map)
            print ('Map size (X,Y): ', n, m)
            print ('Start: ', xA, yA)
            print ('Finish: ', xB, yB)
            t = time.time()
            route = pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB)
            print ('Time to generate the route (seconds): ', time.time() - t)
            print ('Route:')
            print (route)
            #print ("Debug: Ending the_map is ")
            #print (the_map)

            # mark the route on the map
            if len(route) > 0:
                x = int(xA)
                y = int(yA)
                the_map[y][x] = 2
                for i in range(len(route)):
                    #print("Debug pt 1", i, len(route), route[i])
                    if (route[i] != "."): # Not needed - removed "."'s from ending routes
                        j = int(route[i])
                        x += dx[j]
                        y += dy[j]
                        #print("Debug pt 2", x, y, the_map[y][x])
                        the_map[y][x] = 3 # Problems here!
                the_map[y][x] = 4
            #print("Debug: Map with route is:")
            #print (the_map)
            #input('Debug - Press Enter...')

            # display the map with the route added

            for y in range(m):
                
                for x in range(n):
                    #print("y="+str(y))
                    #print("x="+str(x))
                    xy = the_map[y][x]
                    
                    if xy == 0:
                        print ('.',end=" ") # space
                        if x==0 and y==0:
                            self.tilemap1.setStyleSheet("QPushButton { background-color: white }")
                        elif x==1 and y==0:
                            self.tilemap2.setStyleSheet("QPushButton { background-color: white }")
                        elif x==2 and y==0:
                            self.tilemap3.setStyleSheet("QPushButton { background-color: white }")
                        elif x==0 and y==1:
                            self.tilemap4.setStyleSheet("QPushButton { background-color: white }")
                        elif x==2 and y==1:
                            self.tilemap5.setStyleSheet("QPushButton { background-color: white }")
                        elif x==0 and y==2:
                            self.tilemap6.setStyleSheet("QPushButton { background-color: white }")
                        elif x==1 and y==2:
                            self.tilemap7.setStyleSheet("QPushButton { background-color: white }")
                        elif x==2 and y==2:
                            self.tilemap8.setStyleSheet("QPushButton { background-color: white }")
                        elif x==0 and y==3:
                            self.tilemap9.setStyleSheet("QPushButton { background-color: white }")
                        elif x==2 and y==3:
                            self.tilemap10.setStyleSheet("QPushButton { background-color: white }")
                        elif x==0 and y==4:
                            self.tilemap11.setStyleSheet("QPushButton { background-color: white }")
                        elif x==1 and y==4:
                            self.tilemap12.setStyleSheet("QPushButton { background-color: white }")
                        elif x==2 and y==4:
                            self.tilemap13.setStyleSheet("QPushButton { background-color: white }")

                        elif x==3 and y==0:
                            self.tilemap14.setStyleSheet("QPushButton { background-color: white }")
                        elif x==4 and y==0:
                            self.tilemap15.setStyleSheet("QPushButton { background-color: white }")
                        elif x==5 and y==0:
                            self.tilemap16.setStyleSheet("QPushButton { background-color: white }")
                        elif x==3 and y==1:
                            self.tilemap17.setStyleSheet("QPushButton { background-color: white }")
                        elif x==5 and y==1:
                            self.tilemap18.setStyleSheet("QPushButton { background-color: white }")
                        elif x==3 and y==2:
                            self.tilemap19.setStyleSheet("QPushButton { background-color: white }")
                        elif x==4 and y==2:
                            self.tilemap20.setStyleSheet("QPushButton { background-color: white }")
                        elif x==5 and y==2:
                            self.tilemap21.setStyleSheet("QPushButton { background-color: white }")
                        elif x==3 and y==3:
                            self.tilemap22.setStyleSheet("QPushButton { background-color: white }")
                        elif x==5 and y==3:
                            self.tilemap23.setStyleSheet("QPushButton { background-color: white }")
                        elif x==3 and y==4:
                            self.tilemap24.setStyleSheet("QPushButton { background-color: white }")
                        elif x==4 and y==4:
                            self.tilemap25.setStyleSheet("QPushButton { background-color: white }")
                        elif x==5 and y==4:
                            self.tilemap26.setStyleSheet("QPushButton { background-color: white }") 
                    elif xy == 1:
                        print ('O',end=" ") # obstacle
                        if x==0 and y==0:
                            self.tilemap1.setStyleSheet("QPushButton { background-color: black }")
                        elif x==1 and y==0:
                            self.tilemap2.setStyleSheet("QPushButton { background-color: black }")
                        elif x==2 and y==0:
                            self.tilemap3.setStyleSheet("QPushButton { background-color: black }")
                        elif x==0 and y==1:
                            self.tilemap4.setStyleSheet("QPushButton { background-color: black }")
                        elif x==2 and y==1:
                            self.tilemap5.setStyleSheet("QPushButton { background-color: black }")
                        elif x==0 and y==2:
                            self.tilemap6.setStyleSheet("QPushButton { background-color: black }")
                        elif x==1 and y==2:
                            self.tilemap7.setStyleSheet("QPushButton { background-color: black }")
                        elif x==2 and y==2:
                            self.tilemap8.setStyleSheet("QPushButton { background-color: black }")
                        elif x==0 and y==3:
                            self.tilemap9.setStyleSheet("QPushButton { background-color: black }")
                        elif x==2 and y==3:
                            self.tilemap10.setStyleSheet("QPushButton { background-color: black }")
                        elif x==0 and y==4:
                            self.tilemap11.setStyleSheet("QPushButton { background-color: black }")
                        elif x==1 and y==4:
                            self.tilemap12.setStyleSheet("QPushButton { background-color: black }")
                        elif x==2 and y==4:
                            self.tilemap13.setStyleSheet("QPushButton { background-color: black }")
                        elif x==3 and y==0:
                            self.tilemap14.setStyleSheet("QPushButton { background-color: black }")
                        elif x==4 and y==0:
                            self.tilemap15.setStyleSheet("QPushButton { background-color: black }")
                        elif x==5 and y==0:
                            self.tilemap16.setStyleSheet("QPushButton { background-color: black }")
                        elif x==3 and y==1:
                            self.tilemap17.setStyleSheet("QPushButton { background-color: black }")
                        elif x==5 and y==1:
                            self.tilemap18.setStyleSheet("QPushButton { background-color: black }")
                        elif x==3 and y==2:
                            self.tilemap19.setStyleSheet("QPushButton { background-color: black }")
                        elif x==4 and y==2:
                            self.tilemap20.setStyleSheet("QPushButton { background-color: black }")
                        elif x==5 and y==2:
                            self.tilemap21.setStyleSheet("QPushButton { background-color: black }")
                        elif x==3 and y==3:
                            self.tilemap22.setStyleSheet("QPushButton { background-color: black }")
                        elif x==5 and y==3:
                            self.tilemap23.setStyleSheet("QPushButton { background-color: black }")
                        elif x==3 and y==4:
                            self.tilemap24.setStyleSheet("QPushButton { background-color: black }")
                        elif x==4 and y==4:
                            self.tilemap25.setStyleSheet("QPushButton { background-color: black }")
                        elif x==5 and y==4:
                            self.tilemap26.setStyleSheet("QPushButton { background-color: black }") 
                    elif xy == 2:
                        print ('S',end=" ") # start
                        if x==0 and y==0:
                            self.tilemap1.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==1 and y==0:
                            self.tilemap2.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==2 and y==0:
                            self.tilemap3.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==0 and y==1:
                            self.tilemap4.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==2 and y==1:
                            self.tilemap5.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==0 and y==2:
                            self.tilemap6.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==1 and y==2:
                            self.tilemap7.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==2 and y==2:
                            self.tilemap8.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==0 and y==3:
                            self.tilemap9.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==2 and y==3:
                            self.tilemap10.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==0 and y==4:
                            self.tilemap11.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==1 and y==4:
                            self.tilemap12.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==2 and y==4:
                            self.tilemap13.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==3 and y==0:
                            self.tilemap14.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==4 and y==0:
                            self.tilemap15.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==5 and y==0:
                            self.tilemap16.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==3 and y==1:
                            self.tilemap17.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==5 and y==1:
                            self.tilemap18.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==3 and y==2:
                            self.tilemap19.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==4 and y==2:
                            self.tilemap20.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==5 and y==2:
                            self.tilemap21.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==3 and y==3:
                            self.tilemap22.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==5 and y==3:
                            self.tilemap23.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==3 and y==4:
                            self.tilemap24.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==4 and y==4:
                            self.tilemap25.setStyleSheet("QPushButton { background-color: blue }")
                        elif x==5 and y==4:
                            self.tilemap26.setStyleSheet("QPushButton { background-color: blue }") 
                    elif xy == 3:
                        print ('R',end=" ") # route
                        
                        if x==0 and y==0:
                            self.tilemap1.setStyleSheet("background-image: url('image.png');")
                        elif x==1 and y==0:
                            self.tilemap2.setStyleSheet("background-image: url('image.png');")
                        elif x==2 and y==0:
                            self.tilemap3.setStyleSheet("background-image: url('image.png');")
                        elif x==0 and y==1:
                            self.tilemap4.setStyleSheet("background-image: url('image.png');")
                        elif x==2 and y==1:
                            self.tilemap5.setStyleSheet("background-image: url('image.png');")
                        elif x==0 and y==2:
                            self.tilemap6.setStyleSheet("background-image: url('image.png');")
                        elif x==1 and y==2:
                            self.tilemap7.setStyleSheet("background-image: url('image.png');")
                        elif x==2 and y==2:
                            self.tilemap8.setStyleSheet("background-image: url('image.png');")
                        elif x==0 and y==3:
                            self.tilemap9.setStyleSheet("background-image: url('image.png');")
                        elif x==2 and y==3:
                            self.tilemap10.setStyleSheet("background-image: url('image.png');")
                        elif x==0 and y==4:
                            self.tilemap11.setStyleSheet("background-image: url('image.png');")
                        elif x==1 and y==4:
                            self.tilemap12.setStyleSheet("background-image: url('image.png');")
                        elif x==2 and y==4:
                            self.tilemap13.setStyleSheet("background-image: url('image.png');")
                        elif x==3 and y==0:
                            self.tilemap14.setStyleSheet("background-image: url('image.png');")
                        elif x==4 and y==0:
                            self.tilemap15.setStyleSheet("background-image: url('image.png');")
                        elif x==5 and y==0:
                            self.tilemap16.setStyleSheet("background-image: url('image.png');")
                        elif x==3 and y==1:
                            self.tilemap17.setStyleSheet("background-image: url('image.png');")
                        elif x==5 and y==1:
                            self.tilemap18.setStyleSheet("background-image: url('image.png');")
                        elif x==3 and y==2:
                            self.tilemap19.setStyleSheet("background-image: url('image.png');")
                        elif x==4 and y==2:
                            self.tilemap20.setStyleSheet("background-image: url('image.png');")
                        elif x==5 and y==2:
                            self.tilemap21.setStyleSheet("background-image: url('image.png');")
                        elif x==3 and y==3:
                            self.tilemap22.setStyleSheet("background-image: url('image.png');")
                        elif x==5 and y==3:
                            self.tilemap23.setStyleSheet("background-image: url('image.png');")
                        elif x==3 and y==4:
                            self.tilemap24.setStyleSheet("background-image: url('image.png');")
                        elif x==4 and y==4:
                            self.tilemap25.setStyleSheet("background-image: url('image.png');")
                        elif x==5 and y==4:
                            self.tilemap26.setStyleSheet("background-image: url('image.png');") 
                    elif xy == 4:
                        
                        print ('F',end=" ") # finish
                        if x==0 and y==0:
                            self.tilemap1.setStyleSheet("QPushButton { background-color: red }")
                        elif x==1 and y==0:
                            self.tilemap2.setStyleSheet("QPushButton { background-color: red }")
                        elif x==2 and y==0:
                            self.tilemap3.setStyleSheet("QPushButton { background-color: red }")
                        elif x==0 and y==1:
                            self.tilemap4.setStyleSheet("QPushButton { background-color: red }")
                        elif x==2 and y==1:
                            self.tilemap5.setStyleSheet("QPushButton { background-color: red }")
                        elif x==0 and y==2:
                            self.tilemap6.setStyleSheet("QPushButton { background-color: red }")
                        elif x==1 and y==2:
                            self.tilemap7.setStyleSheet("QPushButton { background-color: red }")
                        elif x==2 and y==2:
                            self.tilemap8.setStyleSheet("QPushButton { background-color: red }")
                        elif x==0 and y==3:
                            self.tilemap9.setStyleSheet("QPushButton { background-color: red }")
                        elif x==2 and y==3:
                            self.tilemap10.setStyleSheet("QPushButton { background-color: red }")
                        elif x==0 and y==4:
                            self.tilemap11.setStyleSheet("QPushButton { background-color: red }")
                        elif x==1 and y==4:
                            self.tilemap12.setStyleSheet("QPushButton { background-color: red }")
                        elif x==2 and y==4:
                            self.tilemap13.setStyleSheet("QPushButton { background-color: red }")
                        elif x==3 and y==0:
                            self.tilemap14.setStyleSheet("QPushButton { background-color: red }")
                        elif x==4 and y==0:
                            self.tilemap15.setStyleSheet("QPushButton { background-color: red }")
                        elif x==5 and y==0:
                            self.tilemap16.setStyleSheet("QPushButton { background-color: red }")
                        elif x==3 and y==1:
                            self.tilemap17.setStyleSheet("QPushButton { background-color: red }")
                        elif x==5 and y==1:
                            self.tilemap18.setStyleSheet("QPushButton { background-color: red }")
                        elif x==3 and y==2:
                            self.tilemap19.setStyleSheet("QPushButton { background-color: red }")
                        elif x==4 and y==2:
                            self.tilemap20.setStyleSheet("QPushButton { background-color: red }")
                        elif x==5 and y==2:
                            self.tilemap21.setStyleSheet("QPushButton { background-color: red }")
                        elif x==3 and y==3:
                            self.tilemap22.setStyleSheet("QPushButton { background-color: red }")
                        elif x==5 and y==3:
                            self.tilemap23.setStyleSheet("QPushButton { background-color: red }")
                        elif x==3 and y==4:
                            self.tilemap24.setStyleSheet("QPushButton { background-color: red }")
                        elif x==4 and y==4:
                            self.tilemap25.setStyleSheet("QPushButton { background-color: red }")
                        elif x==5 and y==4:
                            self.tilemap26.setStyleSheet("QPushButton { background-color: red }") 
                print ()
           
            locflag=0
      
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
