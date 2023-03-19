import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
from threading import Thread
import time
import pandas as pd
from datetime import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
sys.path.append('..')

from object_detection.utils import label_map_util

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=10):
        # initialize the camera and stream
	    self.camera = PiCamera()
	    self.camera.resolution = resolution
	    self.camera.framerate = framerate
	    self.rawCapture = PiRGBArray(self.camera, size=resolution)
	    self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

	    self.frame = None
	    self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

   
    def update(self):

        for f in self.stream:

            self.frame = f.array
            self.rawCapture.truncate(0)

            if self.stopped:
               self.stream.close()
               self.rawCapture.close()
               self.camera.close()
               return 
    def read(self):
	
        return self.frame

    def stop(self):
	
        self.stopped = True
# Name of the directory containing the object detection module we're using
#MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
MODEL_NAME = 'defect_model'
# Grab path to current working directory
CWD_PATH = os.getcwd()+'/Desktop'
# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'labeldata','labelmap.pbtxt')
#PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt')

# Number of classes the object detector can identify
#NUM_CLASSES = 90
NUM_CLASSES = 6
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
# Load the Tensorflow model into memory.
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
videostream = VideoStream(resolution=(640,480),framerate=10).start()
time.sleep(1)
while True:

    if GPIO.input(23):    
        print("Processing...")
        frame1=videostream.read()
        frame = frame1.copy()
        image=frame.copy()
        imgwidth=image.shape[0]
        imglength=image.shape[1]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)

        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})
        
        if True:
                        thresholdset=0.5
                        ######################################################
                        category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS)
                        #Create indexes list of element with a score > 0.5
                        indexes = [k for k,v in enumerate(scores[0]) if (v > thresholdset)]

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
                        boxes=boxes[0]
                        
                        print(len(class_names))
                        try:
                                print(scores[len(class_names)-1])
                        except:
                                scores=[scores]
                                print(scores[len(class_names)-1])
                        #######################################################
                        #try:
                        if True:
                                scaledmeasurement=10
                                minordefect=0
                                majordefect=0
                                criticaldefect=0
                                minordefect=0
                                majordefect=0
                                criticaldefect=0
                                microcrack=0
                                broken=0
                                bruise=0
                                dirty=0
                                check=0
                                chip=0
                                totaldefect=0                                
                                for i in range(len(class_names)):
                                    print(i)
                                    if scores is None or scores[i] > thresholdset:
                                        
                                        print(boxes[i])
                                        print(imgwidth)
                                        print(imglength)
                                        ymin=boxes[i][0]*imgwidth
                                        xmin=boxes[i][1]*imglength
                                        ymax=boxes[i][2]*imgwidth
                                        xmax=boxes[i][3]*imglength
                                        x=int(xmin)
                                        y=int(ymin)
                                        w=int(xmax)
                                        h=int(ymax)
                                        print(str(x)+","+str(y)+","+str(w)+","+str(h))
                                        width=abs((ymax-ymin)/ymax)*scaledmeasurement
                                        length=abs((xmax-xmin)/xmax)*scaledmeasurement
                                        print("X: "+str(width)+" m")
                                        print("Y: "+str(length)+" m")
                                        print(class_names[i])
                                        print(scores[i])
                                        disptext=str(class_names[i])+": "+"{:.2f}".format(scores[i]*100)+"%"
                                        xmt="H: "+"{:.2f}".format(width)+"m"
                                        ymt="W: "+"{:.2f}".format(length)+"m"
                                        
                                        
                                        if str(class_names[i])=="Broken":
                                                colorb=(0,255,0)
                                                criticaldefect=criticaldefect+1
                                                broken=broken+1
                                                totaldefect=totaldefect+1
                                        elif str(class_names[i])=="Bruise":
                                                colorb=(255,0,0)
                                                majordefect=majordefect+1
                                                bruise=bruise+1
                                                totaldefect=totaldefect+1
                                        elif str(class_names[i])=="Check":
                                                colorb=(0,0,255)
                                                majordefect=majordefect+1
                                                check=check+1
                                                totaldefect=totaldefect+1
                                        elif str(class_names[i])=="Dirty":
                                                colorb=(255,255,0)
                                                minordefect=minordefect+1
                                                dirty=dirty+1
                                                
                                                totaldefect=totaldefect+1
                                        elif str(class_names[i])=="Chip":
                                                colorb=(0,255,255)
                                                majordefect=majordefect+1
                                                chip=chip+1
                                                totaldefect=totaldefect+1
                                        elif str(class_names[i])=="Micro_Crack":
                                                colorb=(255,0,255)
                                                minordefect=minordefect+1
                                                microcrack=microcrack+1
                                                totaldefect=totaldefect+1
                                        image=cv2.rectangle(image,(x,y),(w,h),colorb,1)
                                        cv2.putText(image,disptext,(x,y-25),cv2.FONT_HERSHEY_SIMPLEX, 0.4, colorb, 1)
                                        cv2.putText(image,xmt,(x-70,y+int((h-y)/2)),cv2.FONT_HERSHEY_SIMPLEX, 0.4, colorb, 1)
                                        cv2.putText(image,ymt,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.4, colorb, 1)
                                        
                        #except:
                                #print("No Detection")
                        timehour=str(datetime.today().strftime("%I:%M:%S %p"))
                        timedate=str(datetime.today().strftime("%m-%d-%Y "))
                                
                        pathtarget="/home/pi/ShareFile/defectdataB.csv"
                        if os.path.exists(pathtarget):
                                    df=pd.read_csv(pathtarget,names=['Date','Time','Micro_Crack','Dirty','Bruise','Check','Chip','Broken','Total'],skiprows=1)
                                    np_df = df.values
                                    df.loc[0,'Date']=timedate
                                    df.loc[0,'Time']=timehour
                                    df.loc[0,'Micro_Crack']=microcrack
                                    df.loc[0,'Dirty']=dirty
                                    df.loc[0,'Broken']=broken
                                    df.loc[0,'Bruise']=bruise
                                    df.loc[0,'Chip']=chip
                                    df.loc[0,'Check']=check
                                    df.loc[0,'Total']=totaldefect

                                    
                                    #df = df.append({'Date':timedate,'Time':timehour,'Micro_Crack':microcrack,'Dirty':dirty,'Bruise':bruise,'Check':check,'Chip':chip,'Broken':broken,'Total':totaldefect}, ignore_index=True)
                                    df.to_csv(pathtarget,  index = False)
                        else:
                                    columns = ['Date','Time','Micro_Crack','Dirty','Bruise','Check','Chip','Broken','Total']
                                    df = pd.DataFrame(columns=columns)
                                    np_df = df.values
                                    #df=df.set_value(0, 'Date', timedate)
                                    df = df.append({'Date':timedate,'Time':timehour,'Micro_Crack':microcrack,'Dirty':dirty,'Bruise':bruise,'Check':check,'Chip':chip,'Broken':broken,'Total':totaldefect}, ignore_index=True)
                                    df.to_csv(pathtarget,  index = False)      
                        cv2.imwrite("/home/pi/ShareFile/output.png",cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                        #cv2.imshow('Object detector', image)
                        
                        # Press 'q' to quit
                        #if cv2.waitKey(1) == ord('q'):
                            #break

        

#cv2.destroyAllWindows()
videostream.stop()
