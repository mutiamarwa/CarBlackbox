#Filename : killprocess.py
#Deskripsi : Program untuk reset dan menghentikan seluruh proses yang berjalan apabila tombol ditekan
#Created by : Hans Christian
#Last Modified : 23 February 2018

import RPi.GPIO as GPIO
import time
import os
import subprocess

#Setting GPIO untuk pushbutton
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#KALO UDAH ADA PUSHBUTTON GANTI PIN BUAT INPUTNYA
#GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while (1):
    inputValue=GPIO.input(21)
    #inputValue=GPIO.input(16)
    if (inputValue==False):
        print("Button press")
        #SYNTAX YANG AKAN DI-KILL
        os.system("pkill -9 -f accelero_button_10min.py")
        os.system("pkill -9 -f clicktosave.py")
        os.system("pkill -9 -f killprocess.py")       
        time.sleep(0.2)
    else:
        time.sleep(0.2)