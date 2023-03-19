from heapq import heappush, heappop # for priority queue
import math
import time
import random
#from termcolor import colored

class node:
    xPos = 0 
    yPos = 0
    distance = 0 # total distance already travelled to reach the node. This is "g"
    priority = 0 # priority = distance + remaining distance estimate, low is better. This is "f"
    def __init__(self, xPos, yPos, distance, priority): # Node Constructor
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority
    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority
    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10 # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self, dirs, d): # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10
    # Estimation function for the remaining distance to the goal. This is "h"
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Euclidian Distance
        d = math.sqrt(xd * xd + yd * yd)
        # Manhattan distance
        # d = abs(xd) + abs(yd)
        # Chebyshev distance
        # d = max(abs(xd), abs(yd))
        return(d)

# A-star algorithm.
# The path "route" returned will be a string of digits of directions.
def pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB):
    closed_nodes_map = [] # map of closed (tried-out) nodes = non-leaf nodes
    open_nodes_map = [] # map of open (not-yet-tried) nodes = leaf nodes
    dir_map = [] # map of dirs
    row = [0] * n
    for i in range(m): # create 2d arrays
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-expanded) nodes
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0) # calls init in node class
    n0.updatePriority(xB, yB) # first time it's all heuristic guess on dist
    heappush(pq[pqi], n0)
    open_nodes_map[int(yA)][int(xA)] = n0.priority # mark it on the open nodes map

    # A* search itself:
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[int(y)][int(x)] = 0
        closed_nodes_map[int(y)][int(x)] = 1 # mark it on the closed nodes map

        # quit searching when the goal is reached
        # If n0.estimate(xB, yB) == 0:
        if x == xB and y == yB:
            # generate the path from finish to start
            # by following the rules: "dirs" = 4 means straight only, "dirs" = 8 means also diagonally
            path = ''
            while not (x == xA and y == yA):
                j = int(dir_map[int(y)][int(x)])
                c = str(int((j + dirs / 2) % dirs)) # tricky use of "dirs" value
                path = c + path
                x += dx[j]
                y += dy[j]
            return path

        # Else generate moves (child nodes) in all possible dirs and continue
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or the_map[int(ydy)][int(xdx)] == 1 or closed_nodes_map[int(ydy)][int(xdx)] == 1):
                # generate a child node
                m0 = node(xdx, ydy, n0.distance, n0.priority)
                m0.nextMove(dirs, i)
                m0.updatePriority(xB, yB)
                # if it is not in the open list then add into that
                if open_nodes_map[int(ydy)][int(xdx)] == 0:
                    open_nodes_map[int(ydy)][int(xdx)] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    dir_map[int(ydy)][int(xdx)] = (i + dirs / 2) % dirs
                elif open_nodes_map[int(ydy)][int(xdx)] > m0.priority:
                    # update the priority
                    open_nodes_map[int(ydy)][int(xdx)] = m0.priority
                    # update the parent direction
                    dir_map[int(ydy)][int(xdx)] = (i + dirs / 2) % dirs
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])       
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return '' # if no route found

# MAIN
dirs = 4 # number of possible directions to move on the map
if dirs == 4:
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
elif dirs == 8:
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

n = 3 # horizontal size of the map
m = 5 # vertical size of the map
the_map = []
row = [0] * n
for i in range(m): # create empty map
    the_map.append(list(row))




#Obstacle Input
the_map[1][1] = 1
the_map[3][1] = 1

xA=1
yA=0
xB=1
yB=4
xA = int(xA)
yA = int(yA)
xB = int(xB)
yB = int(yB)
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
        elif xy == 1:
            print ('O',end=" ") # obstacle
        elif xy == 2:
            print ('S',end=" ") # start
        elif xy == 3:
            print ('R',end=" ") # route
        elif xy == 4:
            print ('F',end=" ") # finish
    print ()

