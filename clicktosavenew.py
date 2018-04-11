#Filename : clicktosave.py
#Deskripsi : Program untuk mennyalin data dari direktori tertentu ke flash memory apabila tombol ditekan
#Created by : Hans Christian
#Last Modified : 23 February 2018

#import library

import RPi.GPIO as GPIO
import time
import shutil
import os
import sys
import usb.core



GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19,GPIO.OUT)
GPIO.output(19,False)

source=os.listdir("/home/pi/Desktop/copysource")
destination = "/media/usb/copytarget"

dev = usb.core.find(find_all=True)
count=0
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
    count=count+1
print(count)


while (1):
    #localtimeread=time.localtime(time.time())
    waktu=time.strftime('%Y%m%d %H%M%S')
    #,localtime(time.time()))
    print (waktu)
    
    GPIO.output(19,False)
    inputValue=GPIO.input(20)
    dev = usb.core.find(find_all=True)
    count=0
    for cfg in dev:
        count=count+1
    print(count)
    if (inputValue==False) and (count>5):
        
        partitionsFile = open("/proc/partitions")
        lines = partitionsFile.readlines()[2:]#Skips the header lines
        for line in lines:
            words = [x.strip() for x in line.split()]
            minorNumber = int(words[1])
            deviceName = words[3]
            if minorNumber % 16 == 0:
                path = "/sys/class/block/" + deviceName
                if os.path.islink(path):
                    if os.path.realpath(path).find("/usb") > 0:
                        print "/dev/%s1" % deviceName
        
        GPIO.output(19,True)
        print("Button press")
        os.system ("sudo mount /dev/" +(deviceName)+ " /media/usb")
        if not os.path.exists(r'/media/usb'):
            os.makedirs (r'/media/usb')
        
        '''
        newpath = r'/media/usb/copytarget/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        '''
        
        shutil.copytree("/home/pi/Desktop/copysource" ,destination)
            
        '''
        for files in source:
            if files.endswith(".txt") or files.endswith(".mp4"):
                shutil.copy("/home/pi/Desktop/copysource/%s" %(files),"%s%s" %(destination,files))
        '''
       
        os.system ("sudo umount /dev/" +(deviceName)+ " /media/usb")
        os.system ("sudo eject /dev/" +(deviceName))
    else:
        time.sleep(0.1)
        
#shutil.copy2('/home/pi/Desktop/python/gps.txt', '/home/pi/Desktop/gps.txt')
        
        

# find USB devices
