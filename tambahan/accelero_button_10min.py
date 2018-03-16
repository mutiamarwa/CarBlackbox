#Filename : accelero_button_10min.py
#Deskripsi : Perekaman data akselerasi untuk ditulis di file utama dan file prioritas apabila trigger ditekan.
#Penulisan di file utama untuk durasi 10 menit, penulisan di file priortas durasi 1 menit, 30s sebelum trigger dan 30s setelah trigger
#Created by : Hans Christian, Mutia Marwa, Gregorius Henry
#Last Modified : 28 February 2018

#import library

import smbus
import math
import time
import RPi.GPIO as GPIO
import os

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin GPIO 18 sebagai input (PUSHBUTTON APABILA KECELAKAAN)
GPIO.setup(26,GPIO.OUT) #Pin GPIO 26 sebagai output (LED menyala apabila terjadi penulisan file saat tombol ditekan)

GPIO.output(26,False) # Inisialisasi awal LED mati

# Power management registers pada accelerometer
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Waktu saat ini
temptime_init=time.time()
localtime=time.asctime(time.localtime(time.time()))

#counter=1
#counter_priority=1

#inisialisasi variabel awal
temptime2=0
arraycount=0
priority_status=0

#fungsi pembacaan data akselerasi
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
bus.write_byte_data(address, 0x1c,0x10) #penulisan register untuk sensitivitas akselerometer

#Template penamaan file
namafile="/home/pi/Desktop/fix/dataaccelero/accel_button_10min_%s.txt" % (localtime)
namafile_priority="/home/pi/Desktop/fix/PRIORITY_dataaccelero/PRIORITY_accel_button_10min_%s.txt" %(localtime)

#Buka file untuk menulis data akselerasi
file=open(namafile,"w")

#Array akselerasi dan waktu. Panjang array 300 untuk menyimpan data 30 detik
arr_acc_x = [0] * 300
arr_acc_y = [0] * 300
arr_acc_z = [0] * 300
arr_time = [''] * 300

#Algoritma utama
while (1):
    localtime=time.asctime(time.localtime(time.time()))
    temptime=time.time()
    inputValue=GPIO.input(18)
    
    #Pembacaan data akselerasi
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
    
    #Penskalaan pembacaan data akselerasi
    accel_xout_scaled = round((accel_xout / 4096.0),5)
    accel_yout_scaled = round((accel_yout / 4096.0),5)
    accel_zout_scaled = round((accel_zout / 4096.0),5)
    
    print "Local current time :",localtime
    print "x_scaled: ", accel_xout_scaled
    print "y_scaled: ", accel_yout_scaled
    print "z_scaled: ", accel_zout_scaled
    
    #Penimpaan array
    if (arraycount<300):
        arr_time[arraycount]=localtime
        arr_acc_x[arraycount]=accel_xout_scaled
        arr_acc_y[arraycount]=accel_yout_scaled
        arr_acc_z[arraycount]=accel_zout_scaled
    else:
        arraycount=arraycount-300
        arr_time[arraycount]=localtime
        arr_acc_x[arraycount]=accel_xout_scaled
        arr_acc_y[arraycount]=accel_yout_scaled
        arr_acc_z[arraycount]=accel_zout_scaled
    
    #Apabila pushbutton ditekan, dilakukan penulisan file ke file utama dan file prioritas
    if (priority_status==1):
        file.write(localtime)
        file.write("\tX: ")
        file.write("%.5f\t"  % (accel_xout_scaled))
        file.write("Y: ")
        file.write("%.5f\t"  % (accel_yout_scaled))
        file.write("Z: ")
        file.write("%.5f\n"  % (accel_zout_scaled))
        
        file_priority.write(localtime)
        file_priority.write("\tX: ")
        file_priority.write("%.5f\t"  % (accel_xout_scaled))
        file_priority.write("Y: ")
        file_priority.write("%.5f\t"  % (accel_yout_scaled))
        file_priority.write("Z: ")
        file_priority.write("%.5f\n"  % (accel_zout_scaled))
        k=k+1
        
        #Handling untuk file prioritas
        if (k>=300):
            file_priority.close()
            #counter_priority=counter_priority+1
            namafile_priority="/home/pi/Desktop/fix/PRIORITY_accel_button_10min_%s.txt" %(localtime)
            priority_status=0
            # LED OFF
            GPIO.output(26,False)
            
    else:
        file.write(localtime)
        file.write("\tX: ")
        file.write("%.5f\t"  % (accel_xout_scaled))
        file.write("Y: ")
        file.write("%.5f\t"  % (accel_yout_scaled))
        file.write("Z: ")
        file.write("%.5f\n"  % (accel_zout_scaled))
    
    #Membuka file baru apabila waktu perekaman telah mencapai 10 menit
    if ((temptime-temptime_init)>600):
        file.close()
        #counter=counter+1
        namafile="/home/pi/Desktop/fix/accel_button_10min_%s.txt" % (localtime)
        file=open(namafile,"w")
        temptime_init=temptime
    
    #Trigger perekaman file prioritas apabila button ditekan atau pembacaan akselerasi melebihi 1g
    if ((inputValue==False) and ((temptime-temptime2)>3)) or (abs(arr_acc_x[arraycount]-arr_acc_x[arraycount-1])>1) or (abs(arr_acc_y[arraycount]-arr_acc_y[arraycount-1])>1) or (abs(arr_acc_z[arraycount]-arr_acc_z[arraycount-1])>1):
        priority_status=1
        
        # LED ON
        GPIO.output(26,True)
        
        k=0
        #Penulisan file prioritas
        file_priority=open(namafile_priority,"w")
        if ((inputValue==False) and ((temptime-temptime2)>3)):
            file_priority.write("Button pressed at ")
        else:
            file_priority.write("Crash at ")
        file_priority.write(localtime)
        file_priority.write("\n")
        
        i=0
        for i in range(299,0,-1):
            file_priority.write(arr_time[arraycount-i])
            file_priority.write("\tX: ")
            file_priority.write("%.5f\t"  % (arr_acc_x[arraycount-i]))
            file_priority.write("Y: ")
            file_priority.write("%.5f\t"  % (arr_acc_y[arraycount-i]))
            file_priority.write("Z: ")
            file_priority.write("%.5f\n"  % (arr_acc_z[arraycount-i]))
        
        print("Button press")
        temptime2=time.time()
    
    arraycount=arraycount+1
    time.sleep(0.1)
