#File name : modcamdepan.py
#Source code module for Raspberry Pi Camera that being used as front camera.

#Import library
from picamera import PiCamera
from picamera import Color
from shutil import copyfile
import datetime
import time

class CamDepan(object):
    def __init__:
        #Pi Camera initialization
        res_vertical= 1280
        res_horizontal= 720
        PiCamera.resolution = (res_vertical, res_horizontal)
            
        #Time configuration for Pi Camera 'night mode'
        jam = datetime.now.hour()
                
        #Pi Camera mode configuration
        PiCamera.exposure_mode = 'antishake'
        if ((Jam < 6) and (Jam > 18)) :
            PiCamera.brightness = 60
            PiCamera.contrast = 30
            PiCamera.sharpness = 65
            PiCamera.exposure_mode = 'night'

    def camera_simpan(VarKopi) :
            if (VarKopi = 1) :
                    Sumber = NamaFileSebelum
                    Tujuan = "/home/pi/Desktop/fix/PRIORITY_datafrontcam/%s" % (NamaFileSebelum)
                    copyfile(Sumber, Tujuan)
                    return 0
            elif (VarKopi = 2) :
                    Sumber = NamaFileSebelum
                    Tujuan = "/home/pi/Desktop/fix/PRIORITY_datafrontcam/%s" % (NamaFileSebelum)
                    copyfile(Sumber, Tujuan)
                    return 1

    def camera_rekam_awal :
            #Start recording process with Pi Camera
            NamaFile = "/home/pi/Desktop/fix/datafrontcam/Video_Depan_%s.h264" % (localtime)
            PiCamera.start_recording(NamaFile)
            CamTimeAwal = time.time()
            
    def camera_rekam :
            #Initialization for next recording session
            CamTime = time.time()
            if ((CamTime - CamTimeAwal) > 60) :
                    PiCamera.stop_recording()
                    NamaFileSebelum = NamaFile
                    NamaFile = "/home/pi/Desktop/fix/datafrontcam/Video_Depan_%s.h264" % (localtime)
                    PiCamera.start_recording(NamaFile)
                    CamTimeAwal = time.time()
                    CamSimpan(VarKopi)

    def camera_prioritas :
            #Initial condition for the decisioning
            WaktuRekam = CamTime - CamTimeAwal
            
            #Condition when button pressed during the first 20 seconds of recording
            if (WaktuRekam < 20) :
                    Sumber = NamaFileSebelum
                    Tujuan = "/home/pi/Desktop/fix/PRIORITY_datafrontcam/%s" % (NamaFileSebelum)
                    copyfile(Sumber, Tujuan)
                    return 1
            #Condition when button pressed during the mid-recording session
            elif ((WaktuRekam >= 20) and (WaktuRekam < 40)) :
                    return 1
            #Condition when button pressed during the last 20 seconds of recording
            else:
                    return 2
