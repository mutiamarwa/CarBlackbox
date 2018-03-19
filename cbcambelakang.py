#File name : modcambelakang.py
#Source code module for Logitech Webcam that being used as back camera.

#Import library
import os
import time
import datetime

class CamBelakang(object) :
    def __init__(self):
        #Aspect configuration
        brightness = 65
        contrast = 30
    
    def start_record(self):
        #Start to record
        os.system("cd Desktop/fix/databackcam")
        init_time = localtime
        os.system("ffmpeg -f video4linux2 -input_format mjpeg -t 60 -s 1080x720 -i /dev/video0 -c:v copy Video_Belakang_%s.h264" % (localtime))
    
    def start_render(self):
        #Time configuration for Logitech Webcam 'night mode'
        jam = datetime.now.hour()
        
        #Mode configuration for Logitech Webcam
        if ((jam < 6) and (jam > 18)) :
            os.system("ffmpeg -i Video_Belakang_%s.h264 -vf eq=brightness=%d:contrast=%d -c:a copy Video_Belakang_%s.h264" % (init_time, brightness, contrast, init_time))
