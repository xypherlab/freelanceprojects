from PyQt4 import QtGui, QtCore
import sys
import time
import os
import cv2
import numpy as np
import pyaudio
import wave
import threading
import subprocess
import librosa
from scipy.io import wavfile
import matplotlib.pyplot as plt
from mss import mss
from moviepy.editor import VideoFileClip, clips_array, vfx
import serial
import datetime
import shutil
ser=serial.Serial('COM7',9600,timeout=1) #Change Serial Communication Port
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global flag,stopflag,filename
        ser.write("90,")
        filename = "inputvideo"	
        stopflag=0
        flag=0
        centralwidget = QtGui.QWidget(self) 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
    
        self.startbutton = QtGui.QPushButton("Record",self)
        self.startbutton.clicked.connect(self.start)
        self.startbutton.move(130,80)
        self.stopbutton = QtGui.QPushButton("Stop",self)
        self.stopbutton.clicked.connect(self.stop)
        self.stopbutton.move(130,120)
        
        
        self.setGeometry(0,20,320,240)
        
    def start(self):
        global flag
        flag=1
    def stop(self):
        global stopflag
        stopflag=1
        
 
    def Loop(self):
        global flag,stopflag,filename
        if flag==1:
            flag=0
            
            file_manager(filename)
            
            start_AVrecording(filename)
            print "Recording"
        if stopflag==1:
            stopflag=0
            audio_thread.stop() 
            frame_counts = video_thread.frame_counts
            elapsed_time = time.time() - video_thread.start_time
            recorded_fps = frame_counts / elapsed_time
            print "total frames " + str(frame_counts)
            print "elapsed time " + str(elapsed_time)
            print "recorded fps " + str(recorded_fps)
            video_thread.stop() 

            while threading.active_count() > 1:
                    time.sleep(1)
            y, sr = librosa.load('temp_audio.wav')
            fs, data = wavfile.read('temp_audio.wav')
            data = np.asarray(data, dtype=np.int16)
            wavfile.write('originalsignal.wav',fs,data)
            S_full, phase = librosa.magphase(librosa.stft(y))



            S_filter = librosa.decompose.nn_filter(S_full,
                                                   aggregate=np.median,
                                                   metric='cosine',
                                                   width=int(librosa.time_to_frames(2, sr=sr)))


            S_filter = np.minimum(S_full, S_filter)

            margin_i, margin_v = 2, 10
            power = 2

            mask_i = librosa.util.softmask(S_filter,
                                           margin_i * (S_full - S_filter),
                                           power=power)

            mask_v = librosa.util.softmask(S_full - S_filter,
                                           margin_v * S_filter,
                                           power=power)


            S_foreground = mask_v * S_full

            S_full, phase = librosa.magphase(librosa.stft(y))
            D_foreground = S_foreground * phase
            y_foreground = librosa.istft(D_foreground)
            librosa.output.write_wav("temp_audio.wav", y_foreground, sr)
            clip1 = VideoFileClip("temp_video.avi")
            clip2 = VideoFileClip("screen.avi")
            final_clip = clips_array([[clip1, clip2]])
            final_clip.write_videofile("temp_video.mp4")
            src_dir = "temp_video.mp4"
            dst_dir = "temp_video.avi"

            video_cap = cv2.VideoCapture(src_dir)
            
            fps = video_cap.get(cv2.CAP_PROP_FPS)
            size = (int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),   
                    int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))   
            video_writer = cv2.VideoWriter(dst_dir, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size) 

            success, frame = video_cap.read()
            while success:
                video_writer.write(frame)
                success, frame = video_cap.read()
            if abs(recorded_fps - 6) >= 0.01:   
                                                                                    
                    print "Re-encoding"
                    cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.avi -pix_fmt yuv420p -r 6 temp_video2.avi"
                    subprocess.call(cmd, shell=True)
            
                    print "Muxing"
                    cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.avi -pix_fmt yuv420p " + filename + ".avi"
                    subprocess.call(cmd, shell=True)
            
            else:
                    
                    print "Normal recording/nMuxing"
                    cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p " + filename + ".avi"
                    subprocess.call(cmd, shell=True)

                    print ".."
            print "Done"
            src_dir = "C:/Users/ADMIN/Desktop/Workspace/Lecture Capture System/inputvideo.avi" #Program Directory
            dropboxdir="C:/Users/ADMIN/Dropbox/" #Dropbox Directory
            now = datetime.datetime.now()
            data=str(now)
            date=data.split(" ")[0]
            timepost=data.split(" ")[1]
            timepost=timepost.split(".")[0]
            timepost=timepost.replace(":", "-")
            videoname=str(date)+"_"+str(timepost)
            dst_dir = dropboxdir+videoname+".avi"
            print dst_dir
            def copy_rename(old_file_name, new_file_name):
                src_dir= os.curdir
                dst_dir= os.path.join(os.curdir , "subfolder")
                src_file = os.path.join(src_dir, old_file_name)
                shutil.copy(src_file,dst_dir)
                
                dst_file = os.path.join(dst_dir, old_file_name)
                new_dst_file_name = os.path.join(dst_dir, new_file_name)
                os.rename(dst_file, new_dst_file_name)
            copy_rename(src_dir,dst_dir)
            
            fs, data1 = wavfile.read('temp_audio.wav')
            fs, data2 = wavfile.read('originalsignal.wav')
            #Disable
            plt.figure(1)
            plt.subplot(211)
            plt.plot(data1)
            plt.subplot(212)
            plt.plot(2*data1)
            
            plt.figure(1)
            plt.subplot(211)
            plt.plot(data2, 's')
            ax = plt.gca()
            ax.set_xticklabels([])
            plt.show()
            #Disable
class MSSSource:
    def __init__(self):
        self.sct = mss()

    def frame(self):
        monitor = {'top': 0, 'left': 0, 'width': 1366, 'height': 768}
        im = np.array(self.sct.grab(monitor))
        im = np.flip(im[:, :, :3], 2) 
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) 
        return True, im

    def release(self):
        pass


class CapSource:
    def __init__(self):
        self.cap = cv2.VideoCapture(1) #Video ID

    def frame(self):
        return self.cap.read()

    def release(self):
        self.cap.release()
        
class VideoRecorder():
	
	def __init__(self):
		
		self.open = True
		self.device_index = 1 #Video ID
		self.fps = 30         
		self.fourcc = "MJPG"   
		self.frameSize = (640,480)
		self.video_filename = "temp_video.avi"
		self.video_cap = cv2.VideoCapture(self.device_index)
		self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
		self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
		self.frame_counts = 1
		self.start_time = time.time()

	
	def record(self):
                def cv2_clipped_zoom(img, zoom_factor):
                    
                    height, width = img.shape[:2] 
                    new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

                    y1, x1 = max(0, new_height - height) // 2, max(0, new_width - width) // 2
                    y2, x2 = y1 + height, x1 + width
                    bbox = np.array([y1,x1,y2,x2])
                    
                    bbox = (bbox / zoom_factor).astype(np.int)
                    y1, x1, y2, x2 = bbox
                    cropped_img = img[y1:y2, x1:x2]

                    resize_height, resize_width = min(new_height, height), min(new_width, width)
                    pad_height1, pad_width1 = (height - resize_height) // 2, (width - resize_width) //2
                    pad_height2, pad_width2 = (height - resize_height) - pad_height1, (width - resize_width) - pad_width1
                    pad_spec = [(pad_height1, pad_height2), (pad_width1, pad_width2)] + [(0,0)] * (img.ndim - 2)

                    result = cv2.resize(cropped_img, (resize_width, resize_height))
                    result = np.pad(result, pad_spec, mode='constant')
                    print zoom_factor
                    assert result.shape[0] == height and result.shape[1] == width
                    return result    
		timer_start = time.time()
		timer_current = 0
		
		fourcc = cv2.VideoWriter_fourcc(*'DIVX')
                out = cv2.VideoWriter('screen.avi', fourcc, 30.0, (640, 480))
                source = MSSSource()
                servodir=90
                print "Servo: "+str(servodir)                                            
                zoomflag=0
		while(self.open==True):
			ret, video_frame = self.video_cap.read()
			if (ret==True):
				
					resizefacedetect=cv2.resize(video_frame, (640, 480))#########Add Line 
					self.frame_counts += 1					
					face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
					gray = cv2.cvtColor(resizefacedetect, cv2.COLOR_BGR2GRAY) #########Replace
					faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                        for (x,y,w,h) in faces:
                                            bbimage = cv2.rectangle(resizefacedetect,(x,y),(x+w,y+h),(255,0,0),2)
                                            print "X: "+str(x)
                                        
                                            cv2.imshow('Face', bbimage) #Disable
                                            cv2.waitKey(1) #Disable
                                            servosign=320-x
                                            centerdistance=abs(320-x)
                                            print "Distance: "+str(centerdistance)
                                            if servosign<0  and centerdistance>30:
                                                servodir=servodir-2
                                            elif servosign>=0  and centerdistance>30:
                                                servodir=servodir+2
                                            if servodir<30:
                                                servodir=30
                                            elif servodir>150:
                                                servodir=150
                                            print "Servo: "+str(servodir)                                            
                                            ser.write(str(servodir)+",")
                                            zoomflag=1
                                        ret, video_frame = self.video_cap.read() 
                                        if (ret==True):
                                               
                                            if zoomflag==1:
                                                video_frame=cv2_clipped_zoom(video_frame,1.5)
                                            self.video_out.write(video_frame)
                                            cv2.imshow('video_frame', video_frame) #Disable
                                            cv2.waitKey(1) #Disable
                                            zoomflag=0
					
			else:
				break
			ret, frame = source.frame()
			frame = cv2.resize(frame, (640, 480)) 
                        if not ret:
                            break
                        out.write(frame)
                        cv2.imshow('Screen', frame) #Disable  
			if cv2.waitKey(1) & 0xFF == ord('q'): #Disable
                            break	 #Disable
	def stop(self):
		
		if self.open==True:
			
			self.open=False
			self.video_out.release()
			self.video_cap.release()
			cv2.destroyAllWindows()
			
		else: 
			pass

		
	def start(self):
		video_thread = threading.Thread(target=self.record)
		video_thread.start()





class AudioRecorder():

    def __init__(self):
        
        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "temp_audio.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []


    def record(self):
        
        self.stream.start_stream()
        while(self.open == True):
            data = self.stream.read(self.frames_per_buffer) 
            self.audio_frames.append(data)
            if self.open==False:
                break
        
            
    def stop(self):
       
        if self.open==True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
               
            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()
        
        pass
    
    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()


	


def start_AVrecording(filename):
				
	global video_thread
	global audio_thread
	
	video_thread = VideoRecorder()
	audio_thread = AudioRecorder()

	audio_thread.start()
	video_thread.start()

	return filename




def start_video_recording(filename):
				
	global video_thread
	
	video_thread = VideoRecorder()
	video_thread.start()

	return filename
	

def start_audio_recording(filename):
				
	global audio_thread
	
	audio_thread = AudioRecorder()
	audio_thread.start()

	return filename



def file_manager(filename):

	local_path = os.getcwd()

	if os.path.exists(str(local_path) + "/temp_audio.wav"):
		os.remove(str(local_path) + "/temp_audio.wav")
	
	if os.path.exists(str(local_path) + "/temp_video.avi"):
		os.remove(str(local_path) + "/temp_video.avi")

	if os.path.exists(str(local_path) + "/temp_video2.avi"):
		os.remove(str(local_path) + "/temp_video2.avi")

	if os.path.exists(str(local_path) + "/" + filename + ".avi"):
		os.remove(str(local_path) + "/" + filename + ".avi")
		
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
