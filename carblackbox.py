#Filename : carblackbox.py
#Deskripsi : Perekaman data untuk ditulis di file utama dan file prioritas apabila trigger ditekan.
#Created by : Hans Christian, Mutia Marwa, Gregorius Henry
#Last Modified : 28 February 2018

#import library
import math
import time
import datetime
import RPi.GPIO as GPIO
import os
from shutil import copyfile
from cbaccel import Accel
from cbobd import Obd
from cbgps import Gps
from cbcamdepan import CamDepan

if __name__ == '__main__':
    #Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin GPIO 16 sebagai input (PUSHBUTTON APABILA KECELAKAAN)
    GPIO.setup(26,GPIO.OUT) #Pin GPIO 26 sebagai output (LED menyala apabila terjadi penulisan file saat tombol ditekan)

    GPIO.output(26,False) # Inisialisasi awal LED mati

    # Waktu saat ini
    temptime_init=time.time()
    localtime=time.asctime(time.localtime(time.time()))

    Gps.config_ublox()

    #Template penamaan file
    namafile_accel="/home/pi/Desktop/Result/Normal/Accelero_%s.txt" % (localtime)
    namafile_accel_priority="/home/pi/Desktop/Result/Priority/PRIORITY_Accelero_%s.txt" %(localtime)
    namafile_obd="/home/pi/Desktop/Result/Normal/OBD_%s .txt" % (localtime)
    namafile_priority_obd="/home/pi/Desktop/Result/Priority/PRIORITY_OBD_%s .txt" % (localtime)
    namafile_gps="/home/pi/Desktop/Result/Normal/GPS_%s.txt" % (localtime)
    namafile_priority_gps="/home/pi/Desktop/Result/Priority/PRIORITY_GPS_%s.txt" %(localtime)

    #Buka file untuk menulis data akselerasi
    file_accel=open(namafile,"w")
    file_obd=open(namafile_obd,"w")
    file_gps=open(namafile_gps,"w")
    file_gps.write("datetime,latitude,longitude,altitude,course,speed,sat\n")

    #Array waktu. Panjang array 300 untuk menyimpan data 30 detik
    array_time= [''] * 300


    #start picamera
    #namafile_frontcamera= "Video_Depan_%s.h264" % (localtime)
    namafile_frontcamera= "Video_Depan_%s" % (localtime)
    camera.start_recording("/home/pi/Desktop/Result/Normal/%s.h264" % (namafile_frontcamera))
    camtime_init=time.time()

    copycurrentfile=0
    copyforwardfile=0
    namafile_frontcamera_previous=namafile_frontcamera
#Algoritma utama
while (1):
    localtime=time.asctime(time.localtime(time.time()))
    #localtime = read_datetimegps()
    temptime=time.time()
    camtime=time.time()
    inputValue=GPIO.input(16)   
    
    if (arraycount<300):
        Accel.read_data()
        Obd.read_data()
    else:
        arraycount=arraycount-300
        Accel.read_data()
        Obd.read_data()
            
    if (arraycountGPS<30):
        Gps.read_data()
    else:
        arraycountGPS=arraycountGPS-30
        Gps.read_data()
        
    #camera.annotate_text = "%s                               X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_yout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),str(response3.value.to("percent")),str(response4.value.to("percent")),str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
    camera.annotate_text = "%s                       X: %s  Y: %s  Z: %s\nRPM: %s rpm Speed: %s kph Throttle: %s %% Engine: %s %% Coolant: %s C\nLat: %s  Lon: %s" % (localtime,str(Accel.x_scaled), str(Accel.y_scaled),str(Accel.z_scaled),str(Obd.rpm.value),str(Obd.speed.value),str(Round(float(Obd.throttle.value),5)),str(Round(float(Obd.load.value),5)),str(Obd.coolant.value), str(Gps.lat), str(Gps.lon))
    
    #print "%s                               X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_yout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),str(response3.value.to("percent")),str(response4.value.to("percent")),str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
    print "%s                       X: %s  Y: %s  Z: %s\nRPM: %s rpm Speed: %s kph Throttle: %s %% Engine: %s %% Coolant: %s C\nLat: %s  Lon: %s" % (localtime,str(Accel.x_scaled), str(Accel.y_scaled),str(Accel.z_scaled),str(Obd.rpm.value),str(Obd.speed.value),str(Round(float(Obd.throttle.value),5)),str(Round(float(Obd.load.value),5)),str(Obd.coolant.value), str(Gps.lat), str(Gps.lon))
    
    #Apabila pushbutton ditekan, dilakukan penulisan file ke file utama dan file prioritas
    if (priority_status==1):
        Accel.write_data(file_accel,localtime)
        Obd.write_data(file_obd,localtime)
        Gps.write_data(file_gps,localtime)
	
	Accel.write_data(file_priority_accel,localtime)
        Obd.write_data(file_priority_obd,localtime)
        Gps.write_data(file_priority_gps,localtime)
	
        k=k+1
        
        #Handling untuk file prioritas
        if (k>=300):
            file_priority.close()
            file_priority_obd.close()
            file_priority_gps.close()
            #counter_priority=counter_priority+1
            namafile_priority_accel="/home/pi/Desktop/Result/Priority/PRIORITY_Accelero_%s.txt" %(localtime)
            namafile_priority_obd="/home/pi/Desktop/Result/Priority/PRIORITY_OBD_%s .txt" % (localtime)
            namafile_priority_gps="/home/pi/Desktop/Result/Priority/PRIORITY_GPS_%s.txt" %(localtime)
            priority_status=0
            # LED OFF
            GPIO.output(26,False)
            
    else:
        Accel.write_data(file_accel,localtime)
        Obd.write_data(file_obd,localtime)
        Gps.write_data(file_gps,localtime)

    
    #Membuka file baru apabila waktu perekaman telah mencapai 10 menit
    if ((temptime-temptime_init)>600):
        file.close()
        file_obd.close()
        file_gps.close()
        #counter=counter+1
        namafile_accel="/home/pi/Desktop/Result/Normal/Accelero_%s.txt" % (localtime)
        namafile_obd="/home/pi/Desktop/Result/Normal/OBD_%s .txt" % (localtime)
        namafile_gps="/home/pi/Desktop/Result/Normal/GPS_%s.txt" % (localtime)
        
        file_accel=open(namafile_accel,"w")
        file_obd=open(namafile_obd,"w")
        file_gps=open(namafile_gps,"w")
        file_gps.write("datetime,latitude,longitude,altitude,course,speed,sat\n")
        temptime_init=temptime
    
    #Buat file video baru kamera depan                 
    if ((camtime-camtime_init)>60):
        camera.stop_recording()
        namafile_frontcamera_previous=namafile_frontcamera
        namafile_frontcamera= "Video_Depan_%s" % (localtime)
        camera.start_recording("/home/pi/Desktop/Result/Normal/%s.h264" % (namafile_frontcamera))
        
        
        camtime_init=time.time()
        if (copycurrentfile==1):
            dest_file = namafile_frontcamera_previous
            source = "/home/pi/Desktop/Result/Normal/%s.h264" % (namafile_frontcamera_previous)
            destination = "/home/pi/Desktop/Result/Priority/PRIORITY_%s.h264" %(dest_file)
            copyfile(source,destination)
            copycurrentfile=0
        if (copyforwardfile==1):
            copycurrentfile=1
            copyforwardfile=0
                       
    #Trigger perekaman file prioritas apabila button ditekan atau pembacaan akselerasi melebihi 1g
    if ((inputValue==False) and ((temptime-temptime2)>3)) or (abs(Accel.array_x[arraycount]-Accel.array_x[arraycount-1])>2) or (abs(Accel.array_y[arraycount]-Accel.array_y[arraycount-1])>2) or (abs(Accel.array_z[arraycount]-Accel.array_z[arraycount-1])>2):
        priority_status=1
        
        # LED ON
        GPIO.output(26,True)
        
        k=0
        #Penulisan file prioritas
        file_priority_accel=open(namafile_priority,"w")
        file_priority_obd=open(namafile_priority_OBD,"w")
        file_priority_gps=open(namafile_priority_GPS,"w")
        if ((inputValue==False) and ((temptime-temptime2)>3)):
            file_priority_accel.write("Button pressed at ")
            file_priority_obd.write("Button pressed at ")
            file_priority_gps.write("Button pressed at ")
        else:
            file_priority_accel.write("Crash at ")
            file_priority_obd.write("Crash at ")
            file_priority_gps.write("Crash at ")
        file_priority_accel.write(localtime)
        file_priority_obd.write(localtime)
        file_priority_gps.write(localtime)
        file_priority_accel.write("\n")
        file_priority_obd.write("\n")
        file_priority_gps.write("\n")
        file_gps.write("datetime,latitude,longitude,altitude,course,speed,sat\n")
        
        i=0
        j=0
        for i in range(299,0,-1):
            Accel.write_array(file_priority_accel,arraycount-i,localtime)
            Obd.write_array(file_priority_obd,arraycount-i,localtime)
            
 
        for j in range (29, 0, -1):
            Gps.write_array(file_priority_gps,arraycountGPS-i,localtime)
	    
        print("Button press")
        temptime2=time.time()
        
        if ((camtime-camtime_init)<20):
            dest_file = namafile_frontcamera_previous
            source = "/home/pi/Desktop/Result/Normal/%s.h264" % (namafile_frontcamera_previous)
            destination = "/home/pi/Desktop/Result/Priority/PRIORITY_%s.h264" %(dest_file)
            copyfile(source,destination)
            copycurrentfile=1
        elif ((camtime-camtime_init)>=20) and ((camtime-camtime_init)<40) :
            copycurrentfile=1
        else:
            copycurrentfile=1
            copynextfile=1
            
    arraycountGPS=arraycountGPS+1
    arraycount=arraycount+1
    #time.sleep(0.1)
    #camera.wait_recording(0.1)