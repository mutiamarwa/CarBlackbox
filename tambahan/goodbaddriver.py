#Filename : accelero_button_10min.py
#Deskripsi : Perekaman data akselerasi untuk ditulis di file utama dan file prioritas apabila trigger ditekan.
#Penulisan di file utama untuk durasi 10 menit, penulisan di file priortas durasi 1 menit, 30s sebelum trigger dan 30s setelah trigger
#Created by : Hans Christian, Mutia Marwa, Gregorius Henry
#Last Modified : 28 February 2018

#import library

import smbus
import math
import time
import os
import obd

#OBD
connection = obd.OBD()

# Waktu saat ini
localtime=time.asctime(time.localtime(time.time()))

#inisialisasi variabel awal
arraycount=0
change_throttle=0
change_rpm=0
rpm_before=0
throttle_before=0
ratio_speed_rpm=0
ratio_throttle_rpm=0
i=0


#Array akselerasi dan waktu. Panjang array 300 untuk menyimpan data 30 detik
arr_throttle = [0] * 300
arr_rpm = [0] * 300

#Algoritma utama
while (1):
    localtime=time.asctime(time.localtime(time.time()))
    #Pembacaan data OBD
    cmd1 = obd.commands.RPM
    cmd2 = obd.commands.SPEED
    cmd3 = obd.commands.THROTTLE_POS
    cmd4 = obd.commands.ENGINE_LOAD
    
    #RETRIEVE DATA DARI OBD
    response1 = connection.query(cmd1)
    response2 = connection.query(cmd2)
    response3 = connection.query(cmd3)
    response4 = connection.query(cmd4)

    rpm = response1.value
    speed = response2.value
    throttle = response3.value
    load = response4.value

    print("RPM: ")
    print(response1.value.to("rpm"))
    print("Speed: ")
    print(response2.value.to("kph"))
    print("Throttle Position: ")
    print(response3.value.to("percent"))
    print("Engine Load: ")
    print(response4.value.to("percent"))

    arr_rpm[i]=rpm
    arr_throttle[i]=throttle

    change_rpm=abs(rpm-rpm_before)
    change_throttle=abs(throttle-throttle_before)

    ratio_speed_rpm = (speed/220)/(rpm/8000)
    ratio_throttle_rpm = (change_throttle/max(arr_throttle))/(change_rpm/max(arr_rpm))

    if (ratio_speed_rpm>0.9)and(ratio_speed_rpm<1.3)and(ratio_throttle_rpm>0.9)and(ratio_throttle_rpm<1.3)and(load>20)and(load<50):
        print('Good Driver')
    else:
        print('Bad Driver')

    rpm_before=rpm
    throttle_before=throttle

    if(i>=299):
        i=0
    else:
        i=i+1
    
    time.sleep(0.1)
    #camera.wait_recording(0.1)

