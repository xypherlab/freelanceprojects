from __future__ import division
import os
import cv2
import numpy as np
import sys
import pickle
import time
from keras_frcnn import config
from keras import backend as K
from keras.layers import Input
from keras.models import Model
from keras_frcnn import roi_helpers
from PyQt4 import QtGui, QtCore
import pandas as pd
sys.setrecursionlimit(40000)

class Main(QtGui.QMainWindow):
        def __init__(self):
                QtGui.QMainWindow.__init__(self)
                self.initUI()

        def initUI(self):
                global config_output_filename,img_path,C,flag,cap
                global model_rpn,model_classifier_only,model_classifier,bbox_threshold,class_mapping,class_to_color
                flag=0
                
                centralwidget = QtGui.QWidget(self) 
                self.timer = QtCore.QTimer(self)
                self.timer.timeout.connect(self.Loop)
                self.timer.start()

                self.setGeometry(0,20,1100,480)

                self.i1=QtGui.QLabel(self)
                self.i1.setGeometry(50,50,400,200)
                self.disp=QtGui.QPixmap("blackscreen.png")
                self.disp=self.disp.scaledToHeight(180)
                self.i1.setPixmap(self.disp)

                
                config_output_filename = "config.pickle" ##########################

                with open(config_output_filename, 'rb') as f_in:
                        C = pickle.load(f_in)

                if C.network == 'resnet50':
                        import keras_frcnn.resnet as nn
                elif C.network == 'vgg':
                        import keras_frcnn.vgg as nn

                # turn off any data augmentation at test time
                C.use_horizontal_flips = False
                C.use_vertical_flips = False
                C.rot_90 = False

                

        

                class_mapping = C.class_mapping

                if 'bg' not in class_mapping:
                        class_mapping['bg'] = len(class_mapping)

                class_mapping = {v: k for k, v in class_mapping.items()}
                print(class_mapping)
                class_to_color = {class_mapping[v]: np.random.randint(0, 255, 3) for v in class_mapping}
                C.num_rois = int(32) #####################

                if C.network == 'resnet50':
                        num_features = 1024
                elif C.network == 'vgg':
                        num_features = 512

                if K.image_dim_ordering() == 'th':
                        input_shape_img = (3, None, None)
                        input_shape_features = (num_features, None, None)
                else:
                        input_shape_img = (None, None, 3)
                        input_shape_features = (None, None, num_features)


                img_input = Input(shape=input_shape_img)
                roi_input = Input(shape=(C.num_rois, 4))
                feature_map_input = Input(shape=input_shape_features)

                # define the base network (resnet here, can be VGG, Inception, etc)
                shared_layers = nn.nn_base(img_input, trainable=True)

                # define the RPN, built on the base layers
                num_anchors = len(C.anchor_box_scales) * len(C.anchor_box_ratios)
                rpn_layers = nn.rpn(shared_layers, num_anchors)

                classifier = nn.classifier(feature_map_input, roi_input, C.num_rois, nb_classes=len(class_mapping), trainable=True)

                model_rpn = Model(img_input, rpn_layers)
                model_classifier_only = Model([feature_map_input, roi_input], classifier)

                model_classifier = Model([feature_map_input, roi_input], classifier)

                print('Loading weights from {}'.format(C.model_path))
                model_rpn.load_weights(C.model_path, by_name=True)
                model_classifier.load_weights(C.model_path, by_name=True)

                model_rpn.compile(optimizer='sgd', loss='mse')
                model_classifier.compile(optimizer='sgd', loss='mse')

                all_imgs = []

                classes = {}

                bbox_threshold = 0.8

                visualise = True
                self.tablegarbage = QtGui.QTableWidget(self)
                self.tablegarbage.setColumnCount(2)
                self.tablegarbage.move(450,50)
                self.tablegarbage.setHorizontalHeaderLabels(['   Type of Garbage   ','     Number of Garbage      '])

                self.tablegarbage.resize(580,200)
                self.tablegarbage.resizeColumnsToContents()
                self.tablegarbage.verticalHeader().setVisible(0)
                self.tablegarbage.setRowCount(4)

                self.tablegarbage.setItem(0, 0, QtGui.QTableWidgetItem("Plastic"))
                self.tablegarbage.setItem(1, 0, QtGui.QTableWidgetItem("Glass"))
                self.tablegarbage.setItem(2, 0, QtGui.QTableWidgetItem("Cans"))
                self.tablegarbage.setItem(3, 0, QtGui.QTableWidgetItem("Polystyrene"))
                self.tablegarbage.setItem(4, 0, QtGui.QTableWidgetItem("Rubber"))
                self.tablegarbage.setItem(5, 0, QtGui.QTableWidgetItem("Diaper"))



                self.tablelocation = QtGui.QTableWidget(self)
                self.tablelocation.setColumnCount(2)
                self.tablelocation.move(20,250)
                self.tablelocation.setHorizontalHeaderLabels(['       Latitude      ','      Longitude     '])

                self.tablelocation.resize(410,80)
                self.tablelocation.resizeColumnsToContents()
                self.tablelocation.verticalHeader().setVisible(0)
                self.tablelocation.setRowCount(1)

                self.scanbutton = QtGui.QPushButton("Scan",self)
                self.scanbutton.clicked.connect(self.scanvideo)
                self.scanbutton.move(400,390)

                self.browsebutton = QtGui.QPushButton("Browse",self)
                self.browsebutton.clicked.connect(self.browsedata)
                self.browsebutton.move(510,390)
        def browsedata(self):
            global dirpath,csvpath
            dirpath = os.getcwd()
            dirpath = dirpath.replace('\\' , '/')
            dirpath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', dirpath)
            csvpath = dirpath
            splitpath=dirpath.split("/")
           
            dirpath=""
            for i in range(len(splitpath)-1):
                   dirpath=dirpath+splitpath[i]+"/"              
            
            print(dirpath)       
        def scanvideo(self):
                global flag
                flag=1
        def Loop(self):
            global config_output_filename,img_path,C,flag,cap,dirpath,csvpath
            global model_rpn,model_classifier_only,model_classifier,bbox_threshold,class_mapping,class_to_color

            
            
            if flag==1: 
                        
                def format_img_size(img, C):
                                """ formats the image size based on config """
                                img_min_side = float(C.im_size)
                                (height,width,_) = img.shape
                                        
                                if width <= height:
                                        ratio = img_min_side/width
                                        new_height = int(ratio * height)
                                        new_width = int(img_min_side)
                                else:
                                        ratio = img_min_side/height
                                        new_width = int(ratio * width)
                                        new_height = int(img_min_side)
                                img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                                return img, ratio	

                def format_img_channels(img, C):
                        """ formats the image channels based on config """
                        img = img[:, :, (2, 1, 0)]
                        img = img.astype(np.float32)
                        img[:, :, 0] -= C.img_channel_mean[0]
                        img[:, :, 1] -= C.img_channel_mean[1]
                        img[:, :, 2] -= C.img_channel_mean[2]
                        img /= C.img_scaling_factor
                        img = np.transpose(img, (2, 0, 1))
                        img = np.expand_dims(img, axis=0)
                        return img

                def format_img(img, C):
                        """ formats an image for model prediction based on config """
                        img, ratio = format_img_size(img, C)
                        img = format_img_channels(img, C)
                        return img, ratio

                # Method to transform the coordinates of the bounding box to its original size
                def get_real_coordinates(ratio, x1, y1, x2, y2):

                        real_x1 = int(round(x1 // ratio))
                        real_y1 = int(round(y1 // ratio))
                        real_x2 = int(round(x2 // ratio))
                        real_y2 = int(round(y2 // ratio))

                        return (real_x1, real_y1, real_x2 ,real_y2)
                
                
                st = time.time()
                #filepath = "vlcsnap-2020-08-22-15h27m10s526.png"

                #img = cv2.imread(filepath)
                #ret, img = cap.read()
                #print("Image Captured")
                videocount=1
                
              
                directory=dirpath+"video/"
                list = os.listdir(directory)
                video_number = len(list)
                plasticcount=0
                glasscount=0
                cancount=0
                polystyrenecount=0
                rubbercount=0
                diapercount=0
                
                plasticout=0
                glassout=0
                canout=0
                polystyreneout=0
                rubberout=0
                diaperout=0

                
                for j in range(video_number):
                        #videopath=directory+str(j+1)+".avi"
                        videopath=directory+str(j+1)+".wmv"
                        cap = cv2.VideoCapture(videopath) 

                        if (cap.isOpened()== False):  
                                  print("Error opening video  file")
                                  videopath=directory+str(j+1)+".avi"
                                  cap = cv2.VideoCapture(videopath)
                        property_id = int(cv2.CAP_PROP_FRAME_COUNT) 
                        length = int(cv2.VideoCapture.get(cap, property_id))
                        print("Frames: "+str(length))
                        zcount=0
                        cap.set(1, zcount)
                        flagbreak=0
                        verifyflag=0
                        frameskip=10 ######################Frame Skip##############################
                        skipsecond=3 ##############################################################
                        numberofverification=3 ######################Number of Corrects##############################
                        while(cap.isOpened()):
                          try:
                                  if flagbreak==1:
                                         zcount=zcount+frameskip*3*2
                                         cap.set(1, zcount)
                                         verifyflag=0
                                         flagbreak=0
                                         ret, img = cap.read()
                                         imgblank=img.copy()
                                         frame = cv2.cvtColor(imgblank, cv2.COLOR_BGR2RGB)
                                         image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                                frame.strides[0], QtGui.QImage.Format_RGB888)
                                         image=image.scaledToHeight(180)
                                         self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
                                  ret, img = cap.read()
                                  imgblank=img.copy()
                                  #cv2.imwrite("inputdispblank.png",img)
                                  if ret == True:
                                        zcount=zcount+1
                                        print("Frame: "+str(zcount))
                                        print("Frame Captured")
                                        X, ratio = format_img(img, C)

                                        if K.image_dim_ordering() == 'tf':
                                                X = np.transpose(X, (0, 2, 3, 1))

                                        # get the feature maps and output from the RPN
                                        [Y1, Y2, F] = model_rpn.predict(X)
                                        

                                        R = roi_helpers.rpn_to_roi(Y1, Y2, C, K.image_dim_ordering(), overlap_thresh=0.7)

                                        # convert from (x1,y1,x2,y2) to (x,y,w,h)
                                        R[:, 2] -= R[:, 0]
                                        R[:, 3] -= R[:, 1]

                                        # apply the spatial pyramid pooling to the proposed regions
                                        bboxes = {}
                                        probs = {}

                                        for jk in range(R.shape[0]//C.num_rois + 1):
                                                ROIs = np.expand_dims(R[C.num_rois*jk:C.num_rois*(jk+1), :], axis=0)
                                                if ROIs.shape[1] == 0:
                                                        break

                                                if jk == R.shape[0]//C.num_rois:
                                                        #pad R
                                                        curr_shape = ROIs.shape
                                                        target_shape = (curr_shape[0],C.num_rois,curr_shape[2])
                                                        ROIs_padded = np.zeros(target_shape).astype(ROIs.dtype)
                                                        ROIs_padded[:, :curr_shape[1], :] = ROIs
                                                        ROIs_padded[0, curr_shape[1]:, :] = ROIs[0, 0, :]
                                                        ROIs = ROIs_padded

                                                [P_cls, P_regr] = model_classifier_only.predict([F, ROIs])

                                                for ii in range(P_cls.shape[1]):

                                                        if np.max(P_cls[0, ii, :]) < bbox_threshold or np.argmax(P_cls[0, ii, :]) == (P_cls.shape[2] - 1):
                                                                continue

                                                        cls_name = class_mapping[np.argmax(P_cls[0, ii, :])]

                                                        if cls_name not in bboxes:
                                                                bboxes[cls_name] = []
                                                                probs[cls_name] = []

                                                        (x, y, w, h) = ROIs[0, ii, :]

                                                        cls_num = np.argmax(P_cls[0, ii, :])
                                                        try:
                                                                (tx, ty, tw, th) = P_regr[0, ii, 4*cls_num:4*(cls_num+1)]
                                                                tx /= C.classifier_regr_std[0]
                                                                ty /= C.classifier_regr_std[1]
                                                                tw /= C.classifier_regr_std[2]
                                                                th /= C.classifier_regr_std[3]
                                                                x, y, w, h = roi_helpers.apply_regr(x, y, w, h, tx, ty, tw, th)
                                                        except:
                                                                pass
                                                        bboxes[cls_name].append([C.rpn_stride*x, C.rpn_stride*y, C.rpn_stride*(x+w), C.rpn_stride*(y+h)])
                                                        probs[cls_name].append(np.max(P_cls[0, ii, :]))

                                        all_dets = []

                                        for key in bboxes:
                                                bbox = np.array(bboxes[key])

                                                new_boxes, new_probs = roi_helpers.non_max_suppression_fast(bbox, np.array(probs[key]), overlap_thresh=0.5)
                                                for jk in range(new_boxes.shape[0]):
                                                        (x1, y1, x2, y2) = new_boxes[jk,:]

                                                        (real_x1, real_y1, real_x2, real_y2) = get_real_coordinates(ratio, x1, y1, x2, y2)

                                                        cv2.rectangle(img,(real_x1, real_y1), (real_x2, real_y2), (int(class_to_color[key][0]), int(class_to_color[key][1]), int(class_to_color[key][2])),2)

                                                        textLabel = '{}: {}'.format(key,int(100*new_probs[jk]))
                                                        all_dets.append((key,100*new_probs[jk]))

                                                        (retval,baseLine) = cv2.getTextSize(textLabel,cv2.FONT_HERSHEY_COMPLEX,1,1)
                                                        textOrg = (real_x1, real_y1-0)

                                                        cv2.rectangle(img, (textOrg[0] - 5, textOrg[1]+baseLine - 5), (textOrg[0]+retval[0] + 5, textOrg[1]-retval[1] - 5), (0, 0, 0), 2)
                                                        cv2.rectangle(img, (textOrg[0] - 5,textOrg[1]+baseLine - 5), (textOrg[0]+retval[0] + 5, textOrg[1]-retval[1] - 5), (255, 255, 255), -1)
                                                        cv2.putText(img, textLabel, textOrg, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 1)

                                        #print('Elapsed time = {}'.format(time.time() - st))
                                        print(all_dets)
                                        print(len(all_dets))
                                        garbagecounter=0
                                        if len(all_dets)==0:
                                                zcount=zcount+frameskip
                                                cap.set(1, zcount)
                                                ret, img = cap.read()
                                                imgblank=img.copy()
                                                frame = cv2.cvtColor(imgblank, cv2.COLOR_BGR2RGB)
                                                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                                        frame.strides[0], QtGui.QImage.Format_RGB888)
                                                image=image.scaledToHeight(180)
                                                self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
                                        for i in range(len(all_dets)):
                                                print(all_dets[i][0])
                                                print(all_dets[i][1])
                                                if float(all_dets[i][1])>=90:
                                                        garbagecounter=garbagecounter+1
                                                
                                                if garbagecounter==len(all_dets):
                                                        print("Found Object") 
                                                        verifyflag=verifyflag+1
                                                        #cv2.imwrite("inputdisp.png",img)
                                                        #self.disp=QtGui.QPixmap("inputdisp.png")
                                                        #self.disp=self.disp.scaledToHeight(180)
                                                        #self.i1.setPixmap(self.disp)


                                                        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                                        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                                                frame.strides[0], QtGui.QImage.Format_RGB888)
                                                        image=image.scaledToHeight(180)
                                                        self.i1.setPixmap(QtGui.QPixmap.fromImage(image))     
                                                else:
                                                        
                                                        #self.disp=QtGui.QPixmap("inputdispblank.png")
                                                        #self.disp=self.disp.scaledToHeight(180)
                                                        #self.i1.setPixmap(self.disp)
                                                        frame = cv2.cvtColor(imgblank, cv2.COLOR_BGR2RGB)
                                                        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 
                                                                frame.strides[0], QtGui.QImage.Format_RGB888)
                                                        image=image.scaledToHeight(180)
                                                        self.i1.setPixmap(QtGui.QPixmap.fromImage(image))
                                                if verifyflag==numberofverification:
                                                        if all_dets[i][0]=="Plastic":
                                                                plasticcount=plasticcount+1
                                                                plasticout=plasticout+1
                                                        elif all_dets[i][0]=="Glass_Bottle":
                                                                glasscount=glasscount+1
                                                                glassout=glassout+1
                                                        elif all_dets[i][0]=="Can":
                                                                cancount=cancount+1
                                                                canout=canout+1
                                                        elif all_dets[i][0]=="Polystyrene":
                                                                polystyrenecount=polystyrenecount+1
                                                                polystyreneout=polystyreneout+1
                                                        elif all_dets[i][0]=="Rubber":
                                                                plasticcount=plasticcount+1
                                                                plasticout=plasticout+1
                                                                #rubbercount=rubbercount+1
                                                                #rubberout=rubberout+1
                                                        elif all_dets[i][0]=="Diaper":
                                                                plasticcount=plasticcount+1
                                                                plasticout=plasticout+1
                                                                #diapercount=diapercount+1
                                                                #diaperout=diaperout+1
                                                        pathmain=csvpath
                                                        if os.path.exists(pathmain):
                                                                 
                                                                df=pd.read_csv(pathmain,names=["routename","startx","starty","endx","endy"],skiprows=1)
                                                                np_df = df.values
                                                                x1=np_df[0][1]
                                                                y1=np_df[0][2]
                                                                x2=np_df[0][3]
                                                                y2=np_df[0][4]
                                                        percent=float(zcount/length)
                                                        print("Percent: "+str(percent))
                                                        xo="{:.6f}".format(x1+percent*(x2-x1))
                                                        yo="{:.6f}".format(y1+percent*(y2-y1))
                                                        print(xo+","+yo)
                                                        flagbreak=1
                                                        #verifyflag=0
                                                        pathoutput=pathmain.strip(".csv")
                                                        pathoutput=pathoutput+"output.csv"
                                                        if os.path.exists(pathoutput):
                                                             df=pd.read_csv(pathoutput,names=["Route","Latitude","Longitude","Plastic","Glass","Can","Polystyrene"],skiprows=1)   
                                                             #df=pd.read_csv(pathoutput,names=["Route","Latitude","Longitude","Plastic","Glass","Can","Polystyrene","Rubber","Diaper"],skiprows=1)
                                                             np_df = df.values
                                                             df = df.append({"Route":j+1,"Latitude":xo,"Longitude":yo,"Plastic":plasticout,"Glass":glassout,"Can":canout,"Polystyrene":polystyreneout}, ignore_index=True)
                                                             #df = df.append({"Route":j+1,"Latitude":xo,"Longitude":yo,"Plastic":plasticout,"Glass":glassout,"Can":canout,"Polystyrene":polystyreneout,"Rubber":rubberout,"Diaper":diaperout}, ignore_index=True)   
                                                             df.to_csv(pathoutput,  index = False)
                                                             
                                                        else:
                                                             #columns = ["Route","Latitude","Longitude","Plastic","Glass","Can","Polystyrene","Rubber","Diaper"]
                                                             columns = ["Route","Latitude","Longitude","Plastic","Glass","Can","Polystyrene"]
                                                             df = pd.DataFrame(columns=columns)
                                                             np_df = df.values
                                                             df = df.append({"Route":j+1,"Latitude":xo,"Longitude":yo,"Plastic":plasticout,"Glass":glassout,"Can":canout,"Polystyrene":polystyreneout}, ignore_index=True)
                                                             #df = df.append({"Route":j+1,"Latitude":xo,"Longitude":yo,"Plastic":plasticout,"Glass":glassout,"Can":canout,"Polystyrene":polystyreneout,"Rubber":rubberout,"Diaper":diaperout}, ignore_index=True)
                                                             df.to_csv(pathoutput,  index = False)
                                                        plasticout=0
                                                        glassout=0
                                                        canout=0
                                                        polystyreneout=0
                                                        rubberout=0
                                                        diaperout=0
                                                        self.tablelocation.setItem(0, 0, QtGui.QTableWidgetItem("        "+str(xo)))
                                                        self.tablelocation.setItem(0, 1, QtGui.QTableWidgetItem("        "+str(yo)))
                                                        zcount=zcount+frameskip*3*1
                                                        cap.set(1, zcount)
                                        QtGui.QApplication.processEvents()
                                        #cv2.imshow('img', img)
                                        #cv2.waitKey(0)
                                        
                                        # cv2.imwrite('./results_imgs/{}.png'.format(idx),img)
                                  else:  
                                            break
                          except:
                                  break
                        
                       
                        
                        
                        self.tablegarbage.setItem(0, 1, QtGui.QTableWidgetItem("        "+str(plasticcount)))
                        self.tablegarbage.setItem(1, 1, QtGui.QTableWidgetItem("        "+str(glasscount)))
                        self.tablegarbage.setItem(2, 1, QtGui.QTableWidgetItem("        "+str(cancount)))
                        self.tablegarbage.setItem(3, 1, QtGui.QTableWidgetItem("        "+str(polystyrenecount)))
                        self.tablegarbage.setItem(4, 1, QtGui.QTableWidgetItem("        "+str(rubbercount)))
                        self.tablegarbage.setItem(5, 1, QtGui.QTableWidgetItem("        "+str(diapercount)))
                        flag=0
                        print("Done")
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
