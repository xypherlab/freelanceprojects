import os
import time
from picamera import PiCamera
import RPi.GPIO as GPIO

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
time.sleep(0.1)

print("Camera Shot")
time.sleep(2)
camera.capture('/home/pi/share/livefeed.png')
time.sleep(0.5)

