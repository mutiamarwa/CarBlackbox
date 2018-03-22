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
from picamera import PiCamera
from picamera import Color

if __name__ == '__main__':
    #Setup GPIO
    accel=Accel()
    obd=Obd()
    gps=Gps()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin GPIO 16 sebagai input (PUSHBUTTON APABILA KECELAKAAN)
    GPIO.setup(26,GPIO.OUT) #Pin GPIO 26 sebagai output (LED menyala apabila terjadi penulisan file saat tombol ditekan)

    GPIO.output(26,False) # Inisialisasi awal LED mati

    gps.config_ublox
    
    # Waktu saat ini
    temptime_init=time.time()
    localtime=time.asctime(time.localtime(time.time()))

    #Template penamaan file
    namafile_accel="/home/pi/Desktop/Result/Normal/accelero_%s.txt" % (localtime)
    namafile_obd="/home/pi/Desktop/Result/Normal/obd_%s .txt" % (localtime)
    namafile_gps="/home/pi/Desktop/Result/Normal/gps_%s.txt" % (localtime)
    #Buka file untuk menulis data akselerasi
    file_accel=open(namafile_accel,"w")
    file_obd=open(namafile_obd,"w")
    file_gps=open(namafile_gps,"w")
    file_gps.write("datetime,latitude,longitude,altitude,course,speed,sat\n")
    
    #inisialisasi variabel awal
    temptime2=0
    arraycount=0
    arraycountgps=0
    priority_status=0
    #Array waktu. Panjang array 300 untuk menyimpan data 30 detik
    array_time= [''] * 300

    #Inisialisasi Pi Camera
    camera=PiCamera()
    camera.resolution = (1280,720)
    #start picamera
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
            accel.read_data(arraycount)
            obd.read_data(arraycount)
        else:
            arraycount=arraycount-300
            accel.read_data(arraycount)
            obd.read_data(arraycount)
                
        if (arraycountgps<30):
            gps.read_data(arraycount)
        else:
            arraycountgps=arraycountgps-30
            gps.read_data(arraycount)
        
        #camera.annotate_text = "%s                               X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_yout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),str(response3.value.to("percent")),str(response4.value.to("percent")),str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
        camera.annotate_text = "%s                       X: %s  Y: %s  Z: %s\nRPM: %s rpm Speed: %s kph Throttle: %s %% Engine: %s %% Coolant: %s C\nLat: %s  Lon: %s" % (localtime,str(accel.x_scaled), str(accel.y_scaled),str(accel.z_scaled),str(obd.rpm.value),str(obd.speed.value),str(round(float(obd.throttle.value),5)),str(round(float(obd.load.value),5)),str(obd.coolant.value), str(gps.lat), str(gps.lon))
        
        #print "%s                               X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_yout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),str(response3.value.to("percent")),str(response4.value.to("percent")),str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
        print "%s                       X: %s  Y: %s  Z: %s\nRPM: %s rpm Speed: %s kph Throttle: %s %% Engine: %s %% Coolant: %s C\nLat: %s  Lon: %s" % (localtime,str(accel.x_scaled), str(accel.y_scaled),str(accel.z_scaled),str(obd.rpm.value),str(obd.speed.value),str(round(float(obd.throttle.value),5)),str(round(float(obd.load.value),5)),str(obd.coolant.value), str(gps.lat), str(gps.lon))
        
        #Apabila pushbutton ditekan, dilakukan penulisan file ke file utama dan file prioritas
        if (priority_status==1):
            accel.write_data(file_accel,localtime)
            obd.write_data(file_obd,localtime)
            gps.write_data(file_gps,localtime)
            
            accel.write_data(file_priority_accel,localtime)
            obd.write_data(file_priority_obd,localtime)
            gps.write_data(file_priority_gps)
            
            k=k+1
            
            #Handling untuk file prioritas
            if (k>=300):
                file_priority.close()
                file_priority_obd.close()
                file_priority_gps.close()
                priority_status=0
                # LED OFF
                GPIO.output(26,False)
                
        else:
            accel.write_data(file_accel,localtime)
            obd.write_data(file_obd,localtime)
            gps.write_data(file_gps)

        
        #Membuka file baru apabila waktu perekaman telah mencapai 10 menit
        if ((temptime-temptime_init)>600):
            file.close()
            file_obd.close()
            file_gps.close()
            #counter=counter+1
            namafile_accel="/home/pi/Desktop/Result/Normal/accelero_%s.txt" % (localtime)
            namafile_obd="/home/pi/Desktop/Result/Normal/obd_%s .txt" % (localtime)
            namafile_gps="/home/pi/Desktop/Result/Normal/gps_%s.txt" % (localtime)
            
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
        if ((inputValue==False) and ((temptime-temptime2)>3)) or (abs(accel.array_x[arraycount]-accel.array_x[arraycount-1])>2) or (abs(accel.array_y[arraycount]-accel.array_y[arraycount-1])>2) or (abs(accel.array_z[arraycount]-accel.array_z[arraycount-1])>2):
            priority_status=1
            
            # LED ON
            GPIO.output(26,True)
            
            k=0
            #Penulisan file prioritas
            namafile_accel_priority="/home/pi/Desktop/Result/Priority/PRIORITY_accelero_%s.txt" %(localtime)
            namafile_priority_obd="/home/pi/Desktop/Result/Priority/PRIORITY_obd_%s .txt" % (localtime)
            namafile_priority_gps="/home/pi/Desktop/Result/Priority/PRIORITY_gps_%s.txt" %(localtime)
            file_priority_accel=open(namafile_priority,"w")
            file_priority_obd=open(namafile_priority_obd,"w")
            file_priority_gps=open(namafile_priority_gps,"w")
            if ((inputValue==False) and ((temptime-temptime2)>3)):
                file_priority_accel.write("Button pressed at %s\n" %(localtime))
                file_priority_obd.write("Button pressed at %s\n" %(localtime))
                file_priority_gps.write("Button pressed at %s\n" %(localtime))
            else:
                file_priority_accel.write("Crash at %s\n" %(localtime))
                file_priority_obd.write("Crash at %s\n" %(localtime))

            file_gps.write("datetime,latitude,longitude,altitude,course,speed,sat\n")
            
            i=0
            j=0
            for i in range(299,0,-1):
                accel.write_array(file_priority_accel,arraycount-i,array_time[arraycount-i])
                obd.write_array(file_priority_obd,arraycount-i,array_time[arraycount-i])
            for j in range (29, 0, -1):
                gps.write_array(file_priority_gps,arraycountgps-i,array_time[arraycount-i])
                
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
                
        arraycountgps=arraycountgps+1
        arraycount=arraycount+1
        #time.sleep(0.1)
        #camera.wait_recording(0.1)
