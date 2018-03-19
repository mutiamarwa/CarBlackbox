#File name : modcambelakang.py
#Source code module for Logitech Webcam that being used as back camera.

#Import library
import os
import time

class CamBelakang(object) :
    def __init__(self):
        #Aspect configuration
        brightness = 65
        contrast = 30
        sharpness = 65
    
    def start_record(self):
        #Start to record
        os.system("cd Desktop/fix/databackcam")
        os.system("ffmpeg -f video4linux2 -input_format mjpeg -t 60 -s 1080x720 -i /dev/video0 -c:v copy Video_Belakang_%s.h264" % (localtime))
    
    def start_render(self):
        
