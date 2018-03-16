#Filename : clicktosave.py
#Deskripsi : Program untuk mennyalin data dari direktori tertentu ke flash memory apabila tombol ditekan
#Created by : Hans Christian
#Last Modified : 23 February 2018

#import library

import RPi.GPIO as GPIO
import time
import shutil
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19,GPIO.OUT)
GPIO.output(19,False)

os.system ("sudo mount /dev/sda1 /media/usb")

if not os.path.exists(r'/media/usb'):
    os.makedirs (r'/media/usb')

source=os.listdir("/home/pi/Desktop/copysource")
newpath = r'/media/usb/copytarget/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

destination = "/media/usb/copytarget/"

while (1):
    GPIO.output(19,False)
    inputValue=GPIO.input(20)
    if (inputValue==False):
        GPIO.output(19,True)
        print("Button press")
        for files in source:
            if files.endswith(".txt") or files.endswith(".mp4"):
                shutil.copy(files,destination)
        os.system ("sudo umount /dev/sda1 /media/usb")
    else:
        time.sleep(0.1)
        
#shutil.copy2('/home/pi/Desktop/python/gps.txt', '/home/pi/Desktop/gps.txt')