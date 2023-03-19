import os
import cv2
import numpy as np
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import tensorflow as tf
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import time
import adafruit_dht
from board import *
import pymeanshift as pms
from colorthief import ColorThief
sys.setrecursionlimit(40000)
import pandas as pd
from datetime import datetime

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.models import model_from_yaml

class Main(QtWidgets.QMainWindow):

        def __init__(self):
            super().__init__()

            self.initUI()
        def initUI(self):
                global captureflag,model,flag,liveflag,cap,DHT_SENSOR,DHT_PIN,recflag,stime,timeinterval
                yaml_file = open('/home/pi/Desktop/model.yaml', 'r')
                loaded_model_yaml = yaml_file.read()
                yaml_file.close()
                model = model_from_yaml(loaded_model_yaml)
                # load weights into new model
                model.load_weights("/home/pi/Desktop/model.h5")
                print("Loaded model from disk")
                model.compile(optimizer='adam', loss='mse')
                timeinterval=5*60 #in secs
                stime=time.time()
                recflag=0
                cap=cv2.VideoCapture(0)
                cap.set(3,640)
                cap.set(4,480)
                time.sleep(0.1)
                DHT_PIN = D4
                DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)

                
                liveflag=0
                flag=0
                captureflag=0
                self.timer = QtCore.QTimer(self)
                self.timer.timeout.connect(self.Loop)
                self.timer.start()

                

                self.i1=QtWidgets.QLabel(self)
                self.i1.setGeometry(10,50,300,300) #Image Size (X Location, Y Location, X Size, Y Size
                self.disp=QtGui.QPixmap("/home/pi/Desktop/blackscreen.png")
                self.disp=self.disp.scaledToHeight(180)
                self.i1.setScaledContents(True);
                self.i1.setPixmap(self.disp)

                self.i2=QtWidgets.QLabel(self)
                self.i2.setGeometry(400,50,300,300) #Image Size (X Location, Y Location, X Size, Y Size
                self.disp=QtGui.QPixmap("/home/pi/Desktop/blackscreen.png")
                self.disp=self.disp.scaledToHeight(180)
                self.i2.setScaledContents(True);
                self.i2.setPixmap(self.disp)
            
                self.analyzebutton = QtWidgets.QPushButton("Capture Banana",self)
                self.analyzebutton.clicked.connect(self.analyzedata)
                self.analyzebutton.move(300,420)
                
                self.autobutton = QtWidgets.QPushButton("Record Banana",self)
                self.autobutton.clicked.connect(self.recorddata)
                self.autobutton.move(190,420)

                self.browsebutton = QtWidgets.QPushButton("Load Banana",self)
                self.browsebutton.clicked.connect(self.browsedata)
                self.browsebutton.move(410,420)
                
                self.gatherbutton = QtWidgets.QPushButton("Data",self)
                self.gatherbutton.clicked.connect(self.gatherdata)
                self.gatherbutton.move(660,420)
                
                
                self.r1=QtWidgets.QLabel("Banana Type: ",self)
                
                self.r1.move(50,350)
                self.r1.resize(800,30)
                
                self.r2=QtWidgets.QLabel("Ripeness Stage",self)
                
                self.r2.move(300,350)
                self.r2.resize(800,60)
                
                
                
                self.r4=QtWidgets.QLabel("Temperature: ",self)
                
                self.r4.move(50,365)
                self.r4.resize(800,30)
                
                self.r5=QtWidgets.QLabel("Humidity: ",self)
                
                self.r5.move(50,380)
                self.r5.resize(800,30)
                
                self.r6=QtWidgets.QLabel("RGB: ",self)
                
                self.r6.move(50,395)
                self.r6.resize(200,30)
                
                self.a1=QtWidgets.QLineEdit(self)
                self.a1.move(550,420)
        
                self.setGeometry(0,20,800,480) #GUI Size (X Location, Y Location, X Size, Y Size
                self.show()
        def gatherdata(self):
            if not os.path.exists('/home/pi/Desktop/Data/'):
                os.makedirs('/home/pi/Desktop/Data/')
            folder="/home/pi/Desktop/Data/"+str(self.a1.text())
            if not os.path.exists(folder):
                os.makedirs(folder)
            path, dirs, files = next(os.walk(folder))
            file_count = len(files)
            ret, frame = cap.read()
            cv2.imwrite("/home/pi/Desktop/Data/"+str(self.a1.text())+"/"+str(file_count)+".png",frame)
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                frame.strides[0], QtGui.QImage.Format_RGB888)
            image=image.scaledToHeight(360)
            self.i2.setPixmap(QtGui.QPixmap.fromImage(image))
        def recorddata(self):
            global recflag
            if recflag==0:
                print("Start")
                recflag=1
            elif recflag==1:
                print("Stop")
                recflag=0
        def browsedata(self):
                global dirpath,model
                
                #try:
                if True:
                    dirpath = os.getcwd()
                    dirpath = dirpath.replace('\\' , '/')
                    dirpath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', dirpath)
                                  
                    
                    
                    image_path   = dirpath[0]
                    print(image_path)
                    img = cv2.imread(image_path)
                    MODEL_NAME = 'banana_model'
                    CWD_PATH = os.getcwd()+'/Desktop'
                    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
                    PATH_TO_LABELS = os.path.join(CWD_PATH,'labeldata','label_map.pbtxt')
                    NUM_CLASSES = 3
                    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
                    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
                    category_index = label_map_util.create_category_index(categories)
                    detection_graph = tf.Graph()
                    with detection_graph.as_default():
                        od_graph_def = tf.compat.v1.GraphDef()
                        with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                            serialized_graph = fid.read()
                            od_graph_def.ParseFromString(serialized_graph)
                            tf.import_graph_def(od_graph_def, name='')
                        sess = tf.compat.v1.Session(graph=detection_graph)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    time.sleep(1)
                    frame = img.copy()
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_expanded = np.expand_dims(frame_rgb, axis=0)

                    (boxes, scores, classes, num) = sess.run(
                        [detection_boxes, detection_scores, detection_classes, num_detections],
                        feed_dict={image_tensor: frame_expanded})
                    cthreshold=0.8
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8,
                        min_score_thresh=cthreshold)
                    if True:
                    ######################################################
                        category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS)
                        #Create indexes list of element with a score > 0.5
                        indexes = [k for k,v in enumerate(scores[0]) if (v >float(cthreshold))]

                        #Number of entities
                        num_entities = len(indexes)

                        #Extract the class id
                        def itemgetter(*items):
                            if len(items) == 1:
                                item = items[0]
                                def g(obj):
                                    return obj[item]
                            else:
                                def g(obj):
                                    return tuple(obj[item] for item in items)
                            return g
                        class_id = itemgetter(*indexes)(classes[0])
                        scores = itemgetter(*indexes)(scores[0])
                        print(class_id)
                        print(scores)
                        #Convert the class id in their name
                        class_names = []
                        if num_entities == 1:
                                  class_names.append(category_index[class_id]['name'])
                                  class_name = str(class_names)
                        else:
                                  for i in range(0, len(indexes)):
                                          class_names.append(category_index[class_id[i]]['name'])
                        print(class_names)
                    #######################################################  
                    self.r1.setText("Banana Type: "+str(class_names[0]))
                    image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                frame.strides[0], QtGui.QImage.Format_RGB888)
                    image=image.scaledToHeight(360)
                    self.i2.setPixmap(QtGui.QPixmap.fromImage(image))    
                    #cv2.imshow('Object detector', frame)
                    def get_dominant_color(image, k=4, image_processing_size = None):
                        
                        #resize image if new dims provided
                        if image_processing_size is not None:
                            image = cv2.resize(image, image_processing_size, 
                                                interpolation = cv2.INTER_AREA)
                        
                        #reshape the image to be a list of pixels
                        image = image.reshape((image.shape[0] * image.shape[1], 3))

                        #cluster and assign labels to the pixels 
                        clt = KMeans(n_clusters = k)
                        labels = clt.fit_predict(image)

                        #count labels to find most popular
                        label_counts = Counter(labels)

                        #subset out most popular centroid
                        dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

                        return list(dominant_color)    
                    
                    lowerrange = np.array([0,0,0])
                    upperrange = np.array([160,160,160])
                    
                    mask = cv2.inRange(img, lowerrange, upperrange)
                    
                    mask = cv2.bitwise_not(mask)
                    output =  cv2.connectedComponentsWithStats(mask)
                    num_labels = output[0]-1
                    labels = output[1]
                    stats = output[2]
                    centroids = output[3]
                    sizes = stats[1:, -1]
                    min_size = 1000 #Change
                    #max_size = 10000000000 #Change
                    mask = np.zeros((labels.shape))
                    z=0
                    for i in range(0, num_labels):
                           
                           if sizes[i] >= min_size:
                                mask[labels == i + 1] = 255
                                
                                #print("Area("+str(z)+"):"+str(sizes[i]))
                                z=z+1
                    kernel = np.ones((5,5),np.uint8)
                    mask=cv2.dilate(mask,kernel,iterations = 1)
                    mask = cv2.convertScaleAbs(mask)
                    _,contours, _ = cv2.findContours(mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

                    # Find object with the biggest bounding box
                    mx = (0,0,0,0)      # biggest bounding box so far
                    mx_area = 0
                    for cont in contours:
                            x,y,w,h = cv2.boundingRect(cont)
                            area = w*h
                            if area > mx_area:
                                mx = x,y,w,h
                                mx_area = area
                    x,y,w,h = mx
                    altimg=img.copy()
                    (alt_seg, labels_image, number_regions) = pms.segment(altimg, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
                    alt_seg = cv2.bitwise_and(alt_seg,alt_seg,mask = mask)
                    
                    cv2.imwrite("/home/pi/Desktop/mask.png",mask)
                    #img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
                    cv2.imwrite("segmento.png",segmented_image)
                    segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
                    cv2.imwrite("/home/pi/Desktop/segment.png",segmented_image)   
                    color_thief = ColorThief('/home/pi/Desktop/segment.png')
                    dominant_color = color_thief.get_color(quality=1)
                    print(dominant_color)
                    def bincount_app(a):
                            a2D = a.reshape(-1,a.shape[-1])
                            col_range = (256, 256, 256) # generically : a2D.max(0)+1
                            a1D = np.ravel_multi_index(a2D.T, col_range)
                            return np.unravel_index(np.bincount(a1D).argmax(), col_range)
                    print(bincount_app(segmented_image))
                    channels = cv2.mean(segmented_image)
                    
                    (B, G, R) = cv2.split(alt_seg)
                    nzcountB = np.count_nonzero(B)
                    nzcountG = np.count_nonzero(G)
                    nzcountR = np.count_nonzero(R)
                    cB=float(np.sum(B))/float(nzcountB)
                    cG=float(np.sum(G))/float(nzcountG)
                    cR=float(np.sum(R))/float(nzcountR)

                    ##############################################
                    # load YAML and create model
                    if True:
                        

                        def find_nearest(array, value):
                            array = np.asarray(array)
                            idx = (np.abs(array - value)).argmin()
                            
                            return idx
                        df=pd.read_csv("/home/pi/Desktop/datatime.csv",names=["Time","Temperature","Humidity","Red","Green","Blue"],skiprows=1)
                        #print(df)

                        np_df = df.values
                        temperature = np_df[:,1]
                        humidity = np_df[:,2]
                        red = np_df[:,3]
                        green=np_df[:,4]
                        blue=np_df[:,5]

                        temperature = temperature.reshape((len(temperature), 1))
                        humidity = humidity.reshape((len(humidity), 1))
                        red = red.reshape((len(red), 1))
                        green = green.reshape((len(green), 1))
                        blue = blue.reshape((len(blue), 1))

                        mdata = np.hstack((temperature,humidity,red,green,blue))
                        ldata=np_df[:,0]

                        
                        redi=cR
                        greeni=cG
                        bluei=cB

                        x_input = np.array([[redi, greeni, bluei]])
                        n_steps_in, n_steps_out = 1, 1
                        n_features = x_input.shape[1]
                        x_input = x_input.reshape((1, n_steps_in, n_features))
                        yhat = model.predict(x_input, verbose=0)
                        x_input = np.array([[redi, greeni, bluei]])
                        redindex=find_nearest(red, x_input[0][0])
                        greenindex=find_nearest(green, x_input[0][1])
                        blueindex=find_nearest(blue, x_input[0][2])

                        #print(redindex+2)
                        #print(greenindex+2)
                        #print(blueindex+2)
                        averageindex=int(float(redindex+greenindex+blueindex+6)/float(3))
                        stage2pred=int((float((338-averageindex)*5)/float(60))/float(24))
                        stage3pred=int((float((847-averageindex)*5)/float(60))/float(24))
                        stage4pred=int((float((1385-averageindex)*5)/float(60))/float(24))
                        stage5pred=int((float((1767-averageindex)*5)/float(60))/float(24))
                        stage6pred=int((float((2227-averageindex)*5)/float(60))/float(24))
                        stage7pred=int((float((2482-averageindex)*5)/float(60))/float(24))

                        stage2predmin=float((338-averageindex)*5)
                        stage3predmin=float((847-averageindex)*5)
                        stage4predmin=float((1385-averageindex)*5)
                        stage5predmin=float((1767-averageindex)*5)
                        stage6predmin=float((2227-averageindex)*5)
                        stage7predmin=float((2482-averageindex)*5)

                        print("Stage 2: "+str(stage2pred)+" estimated days or "+str(stage2predmin)+" minutes.")
                        print("Stage 3: "+str(stage3pred)+" estimated days or "+str(stage3predmin)+" minutes.")
                        print("Stage 4: "+str(stage4pred)+" estimated days or "+str(stage4predmin)+" minutes.")
                        print("Stage 5: "+str(stage5pred)+" estimated days or "+str(stage5predmin)+" minutes.")
                        print("Stage 6: "+str(stage6pred)+" estimated days or "+str(stage6predmin)+" minutes.")
                        print("Stage 7: "+str(stage7pred)+" estimated days or "+str(stage7predmin)+" minutes.")

    

                    resultout="Ripeness Stage\nStage 2:"+str(stage2pred)+" days/"+str(stage2predmin)+" minutes"+"    Stage 3: "+str(stage3pred)+" days/"+str(stage3predmin)+" minutes\n"+"Stage 4: "+str(stage4pred)+" days/"+str(stage4predmin)+" minutes"+"    Stage 5: "+str(stage5pred)+" days/"+str(stage5predmin)+" minutes\n"+"Stage 6: "+str(stage6pred)+" days/"+str(stage6predmin)+" minutes"+"    Stage 7: "+str(stage7pred)+" days/"+str(stage7predmin)+" minutes"
                    self.r2.setText(resultout)
                    ##############################################
                    rgbres = np.array([(cR, cG, cB)])    
                    print(rgbres)
                    
                    self.r6.setText("RGB: Mean("+str(int(cR))+","+str(int(cG))+","+str(int(cB))+")")
                    #frame=segmented_image.copy()
                    #image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                    #        frame.strides[0], QtGui.QImage.Format_RGB888)
                    #image=image.scaledToHeight(360)
                    #self.i2.setPixmap(QtGui.QPixmap.fromImage(image))
                    
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    #image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                    #            frame.strides[0], QtGui.QImage.Format_RGB888)
                    #image=image.scaledToHeight(360)
                    #self.i2.setPixmap(QtGui.QPixmap.fromImage(image))        
                #except:
                    #print("Load Cancelled")
        def analyzedata(self):
                global captureflag,recflag
                captureflag=1
                recflag=1
                     
        def Loop(self):     
                global captureflag,flag,cap,liveflag,DHT_SENSOR,DHT_PIN,stime,timeinterval,temperature,humidity
                
                try:
                    temperature = DHT_SENSOR.temperature
                    humidity = DHT_SENSOR.humidity    
                    self.r4.setText("Temperature: "+str(temperature)+"°C")
                    self.r5.setText("Humidity: "+str(humidity))
                except:
                    print("")
                
                if recflag==1:
                    if captureflag==1:
                        captureflag=0
                        recflag=0
                    def get_dominant_color(image, k=4, image_processing_size = None):
                        
                        #resize image if new dims provided
                        if image_processing_size is not None:
                            image = cv2.resize(image, image_processing_size, 
                                                interpolation = cv2.INTER_AREA)
                        
                        #reshape the image to be a list of pixels
                        image = image.reshape((image.shape[0] * image.shape[1], 3))

                        #cluster and assign labels to the pixels 
                        clt = KMeans(n_clusters = k)
                        labels = clt.fit_predict(image)

                        #count labels to find most popular
                        label_counts = Counter(labels)

                        #subset out most popular centroid
                        dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

                        return list(dominant_color)    
                    ret, frame = cap.read()
                    img=frame.copy()
                    
                    MODEL_NAME = 'banana_model'
                    CWD_PATH = os.getcwd()+'/Desktop'
                    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
                    PATH_TO_LABELS = os.path.join(CWD_PATH,'labeldata','label_map.pbtxt')
                    NUM_CLASSES = 3
                    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
                    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
                    category_index = label_map_util.create_category_index(categories)
                    detection_graph = tf.Graph()
                    with detection_graph.as_default():
                        od_graph_def = tf.compat.v1.GraphDef()
                        with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                            serialized_graph = fid.read()
                            od_graph_def.ParseFromString(serialized_graph)
                            tf.import_graph_def(od_graph_def, name='')
                        sess = tf.compat.v1.Session(graph=detection_graph)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    time.sleep(1)
                    frame = img.copy()
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_expanded = np.expand_dims(frame_rgb, axis=0)

                    (boxes, scores, classes, num) = sess.run(
                        [detection_boxes, detection_scores, detection_classes, num_detections],
                        feed_dict={image_tensor: frame_expanded})
                    cthreshold=0.8
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8,
                        min_score_thresh=cthreshold)
                    if True:
                    ######################################################
                        category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS)
                        #Create indexes list of element with a score > 0.5
                        indexes = [k for k,v in enumerate(scores[0]) if (v >float(cthreshold))]

                        #Number of entities
                        num_entities = len(indexes)

                        #Extract the class id
                        def itemgetter(*items):
                            if len(items) == 1:
                                item = items[0]
                                def g(obj):
                                    return obj[item]
                            else:
                                def g(obj):
                                    return tuple(obj[item] for item in items)
                            return g
                        class_id = itemgetter(*indexes)(classes[0])
                        scores = itemgetter(*indexes)(scores[0])
                        print(class_id)
                        print(scores)
                        #Convert the class id in their name
                        class_names = []
                        if num_entities == 1:
                                  class_names.append(category_index[class_id]['name'])
                                  class_name = str(class_names)
                        else:
                                  for i in range(0, len(indexes)):
                                          class_names.append(category_index[class_id[i]]['name'])
                        print(class_names)
                    #######################################################  
                    self.r1.setText("Banana Type: "+str(class_names[0]))
                    image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                frame.strides[0], QtGui.QImage.Format_RGB888)
                    image=image.scaledToHeight(360)
                    self.i2.setPixmap(QtGui.QPixmap.fromImage(image))    
                    #cv2.imshow('Object detector', frame)
                    def get_dominant_color(image, k=4, image_processing_size = None):
                        
                        #resize image if new dims provided
                        if image_processing_size is not None:
                            image = cv2.resize(image, image_processing_size, 
                                                interpolation = cv2.INTER_AREA)
                        
                        #reshape the image to be a list of pixels
                        image = image.reshape((image.shape[0] * image.shape[1], 3))

                        #cluster and assign labels to the pixels 
                        clt = KMeans(n_clusters = k)
                        labels = clt.fit_predict(image)

                        #count labels to find most popular
                        label_counts = Counter(labels)

                        #subset out most popular centroid
                        dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

                        return list(dominant_color)    
                    
                    lowerrange = np.array([0,0,0])
                    upperrange = np.array([160,160,160])
                    
                    mask = cv2.inRange(img, lowerrange, upperrange)
                    
                    mask = cv2.bitwise_not(mask)
                    output =  cv2.connectedComponentsWithStats(mask)
                    num_labels = output[0]-1
                    labels = output[1]
                    stats = output[2]
                    centroids = output[3]
                    sizes = stats[1:, -1]
                    min_size = 1000 #Change
                    #max_size = 10000000000 #Change
                    mask = np.zeros((labels.shape))
                    z=0
                    for i in range(0, num_labels):
                           
                           if sizes[i] >= min_size:
                                mask[labels == i + 1] = 255
                                
                                #print("Area("+str(z)+"):"+str(sizes[i]))
                                z=z+1
                    kernel = np.ones((5,5),np.uint8)
                    mask=cv2.dilate(mask,kernel,iterations = 1)
                    mask = cv2.convertScaleAbs(mask)
                    _,contours, _ = cv2.findContours(mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

                    # Find object with the biggest bounding box
                    mx = (0,0,0,0)      # biggest bounding box so far
                    mx_area = 0
                    for cont in contours:
                            x,y,w,h = cv2.boundingRect(cont)
                            area = w*h
                            if area > mx_area:
                                mx = x,y,w,h
                                mx_area = area
                    x,y,w,h = mx
                    altimg=img.copy()
                    (alt_seg, labels_image, number_regions) = pms.segment(altimg, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
                    alt_seg = cv2.bitwise_and(alt_seg,alt_seg,mask = mask)
                    
                    cv2.imwrite("/home/pi/Desktop/mask.png",mask)
                    #img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    (segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=3, 
                                                              range_radius=3, min_density=25)
                    cv2.imwrite("segmento.png",segmented_image)
                    segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
                    cv2.imwrite("/home/pi/Desktop/segment.png",segmented_image)   
                    color_thief = ColorThief('/home/pi/Desktop/segment.png')
                    dominant_color = color_thief.get_color(quality=1)
                    print(dominant_color)
                    def bincount_app(a):
                            a2D = a.reshape(-1,a.shape[-1])
                            col_range = (256, 256, 256) # generically : a2D.max(0)+1
                            a1D = np.ravel_multi_index(a2D.T, col_range)
                            return np.unravel_index(np.bincount(a1D).argmax(), col_range)
                    print(bincount_app(segmented_image))
                    channels = cv2.mean(segmented_image)
                    
                    (B, G, R) = cv2.split(alt_seg)
                    nzcountB = np.count_nonzero(B)
                    nzcountG = np.count_nonzero(G)
                    nzcountR = np.count_nonzero(R)
                    cB=float(np.sum(B))/float(nzcountB)
                    cG=float(np.sum(G))/float(nzcountG)
                    cR=float(np.sum(R))/float(nzcountR)

                    ##############################################
                    # load YAML and create model
                    if True:
                        

                        def find_nearest(array, value):
                            array = np.asarray(array)
                            idx = (np.abs(array - value)).argmin()
                            
                            return idx
                        df=pd.read_csv("/home/pi/Desktop/datatime.csv",names=["Time","Temperature","Humidity","Red","Green","Blue"],skiprows=1)
                        #print(df)

                        np_df = df.values
                        temperature = np_df[:,1]
                        humidity = np_df[:,2]
                        red = np_df[:,3]
                        green=np_df[:,4]
                        blue=np_df[:,5]

                        temperature = temperature.reshape((len(temperature), 1))
                        humidity = humidity.reshape((len(humidity), 1))
                        red = red.reshape((len(red), 1))
                        green = green.reshape((len(green), 1))
                        blue = blue.reshape((len(blue), 1))

                        mdata = np.hstack((temperature,humidity,red,green,blue))
                        ldata=np_df[:,0]

                        
                        redi=cR
                        greeni=cG
                        bluei=cB

                        x_input = np.array([[redi, greeni, bluei]])
                        n_steps_in, n_steps_out = 1, 1
                        n_features = x_input.shape[1]
                        x_input = x_input.reshape((1, n_steps_in, n_features))
                        yhat = model.predict(x_input, verbose=0)
                        x_input = np.array([[redi, greeni, bluei]])
                        redindex=find_nearest(red, x_input[0][0])
                        greenindex=find_nearest(green, x_input[0][1])
                        blueindex=find_nearest(blue, x_input[0][2])

                        #print(redindex+2)
                        #print(greenindex+2)
                        #print(blueindex+2)
                        averageindex=int(float(redindex+greenindex+blueindex+6)/float(3))
                        stage2pred=int((float((338-averageindex)*5)/float(60))/float(24))
                        stage3pred=int((float((847-averageindex)*5)/float(60))/float(24))
                        stage4pred=int((float((1385-averageindex)*5)/float(60))/float(24))
                        stage5pred=int((float((1767-averageindex)*5)/float(60))/float(24))
                        stage6pred=int((float((2227-averageindex)*5)/float(60))/float(24))
                        stage7pred=int((float((2482-averageindex)*5)/float(60))/float(24))

                        stage2predmin=float((338-averageindex)*5)
                        stage3predmin=float((847-averageindex)*5)
                        stage4predmin=float((1385-averageindex)*5)
                        stage5predmin=float((1767-averageindex)*5)
                        stage6predmin=float((2227-averageindex)*5)
                        stage7predmin=float((2482-averageindex)*5)

                        print("Stage 2: "+str(stage2pred)+" estimated days or "+str(stage2predmin)+" minutes.")
                        print("Stage 3: "+str(stage3pred)+" estimated days or "+str(stage3predmin)+" minutes.")
                        print("Stage 4: "+str(stage4pred)+" estimated days or "+str(stage4predmin)+" minutes.")
                        print("Stage 5: "+str(stage5pred)+" estimated days or "+str(stage5predmin)+" minutes.")
                        print("Stage 6: "+str(stage6pred)+" estimated days or "+str(stage6predmin)+" minutes.")
                        print("Stage 7: "+str(stage7pred)+" estimated days or "+str(stage7predmin)+" minutes.")

    

                    resultout="Ripeness Stage\nStage 2:"+str(stage2pred)+" days/"+str(stage2predmin)+" minutes"+"    Stage 3: "+str(stage3pred)+" days/"+str(stage3predmin)+" minutes\n"+"Stage 4: "+str(stage4pred)+" days/"+str(stage4predmin)+" minutes"+"    Stage 5: "+str(stage5pred)+" days/"+str(stage5predmin)+" minutes\n"+"Stage 6: "+str(stage6pred)+" days/"+str(stage6predmin)+" minutes"+"    Stage 7: "+str(stage7pred)+" days/"+str(stage7predmin)+" minutes"
                    self.r2.setText(resultout)
                    ##############################################
                    rgbres = np.array([(cR, cG, cB)])    
                    print(rgbres)
                    
                    self.r6.setText("RGB: Mean("+str(int(cR))+","+str(int(cG))+","+str(int(cB))+")")
                    
                    
                    
                if liveflag==1:
                    
                  try:
                    
                    ret, frame = cap.read()
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                    image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                        frame.strides[0], QtGui.QImage.Format_RGB888)
                    image=image.scaledToHeight(360)
                    self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
                  except:
                      print("Data Loss")
                QtCore.QCoreApplication.processEvents()
def main():

    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


