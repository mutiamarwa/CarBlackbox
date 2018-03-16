#File name : modcamdepan.py
#Source code module for Raspberry Pi Camera that being used as front camera.

#Import library
from picamera import PiCamera
from picamera import Color
from shutil import copyfile
import datetime
import time

class CamDepan(object):
    def __init__(self):
        #Pi Camera initialization
        res_vertical= 1280
        res_horizontal= 720
        PiCamera.resolution = (res_vertical, res_horizontal)
            
        #Time configuration for Pi Camera 'night mode'
        jam = datetime.now.hour()
                
        #Pi Camera mode configuration
        PiCamera.exposure_mode = 'antishake'
        if ((jam < 6) and (jam > 18)) :
            PiCamera.brightness = 60
            PiCamera.contrast = 30
            PiCamera.sharpness = 65
            PiCamera.exposure_mode = 'night'

    def start_record(self, localtime):
            #Start recording process with Pi Camera
            file_name = "/home/pi/Desktop/fix/datafrontcam/Video_Depan_%s.h264" % (localtime)
            PiCamera.start_recording(file_name)
            init_time = time.time()
            
    def record(self, localtime):
            #Initialization for next recording session
            rec_time = time.time()
            if ((rec_time - init_time) > 60) :
                    PiCamera.stop_recording()
                    last_file_name = file_name
                    file_name = "/home/pi/Desktop/fix/datafrontcam/Video_Depan_%s.h264" % (localtime)
                    PiCamera.start_recording(NamaFile)
                    init_time = time.time()
