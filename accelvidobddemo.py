#Filename : accelero_button_10min.py
#Deskripsi : Perekaman data akselerasi untuk ditulis di file utama dan file prioritas apabila trigger ditekan.
#Penulisan di file utama untuk durasi 10 menit, penulisan di file priortas durasi 1 menit, 30s sebelum trigger dan 30s setelah trigger
#Created by : Hans Christian, Mutia Marwa, Gregorius Henry
#Last Modified : 28 February 2018

#import library
from picamera import PiCamera
from picamera import Color
import smbus
import math
import time
import datetime
import RPi.GPIO as GPIO
import os
import obd
import serial, pynmea2
import datetime
from pytz import timezone, utc
from timezonefinder import TimezoneFinder
from shutil import copyfile


#OBD
connection = obd.OBD()

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin GPIO 16 sebagai input (PUSHBUTTON APABILA KECELAKAAN)
GPIO.setup(26,GPIO.OUT) #Pin GPIO 26 sebagai output (LED menyala apabila terjadi penulisan file saat tombol ditekan)

GPIO.output(26,False) # Inisialisasi awal LED mati

# Power management registers pada accelerometer
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#Inisialisasi Pi Camera
camera=PiCamera()
camera.resolution = (1280,720)

now=datetime.datetime.now()
jam=now.hour
if ((jam>6)and(jam<18)):
    camera.start_preview()
    camera.exposure_mode = 'antishake'
    camera.annotate_text_size = 25
    camera.annotate_foreground = Color('black')
    camera.annotate_background = Color('white')
else:
#NIGHT MODE
    camera.brightness = 60
    camera.contrast = 30
    camera.sharpness = 65
    camera.exposure_mode = 'night'
    camera.start_preview()
    #camera.exposure_mode = 'nightpreview'

# Waktu saat ini
temptime_init=time.time()
localtime=time.asctime(time.localtime(time.time()))

#counter=1
#counter_priority=1

#inisialisasi variabel awal
temptime2=0
arraycount=0
arraycountGPS=0
priority_status=0

#configurasi gps ublox
def config_ublox():
    baud9600 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x80\x25\x00\x00\x07\x00\x07\x00\x00\x00\x00\x00\xE2\xE1\xB5\x62\x06\x00\x01\x00\x01\x08\x22'
    baud57600 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xE1\x00\x00\x07\x00\x07\x00\x00\x00\x00\x00\xE2\xE1\xB5\x62\x06\x00\x01\x00\x01\x08\x22'
    baud115200 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xc2\x01\x00\x07\x00\x07\x00\x00\x00\x00\x00\xc4\x96\xb5\x62\x06\x00\x01\x00\x01\x08\x22'
    
    rate1hz = b'\xB5\x62\x06\x08\x06\x00\xE8\x03\x01\x00\x01\x00\x00\x00'
    rate5hz = b'\xB5\x62\x06\x08\x06\x00\xC8\x00\x01\x00\x01\x00\x00\x00'
    rate10hz = b'\xB5\x62\x06\x08\x06\x00\x64\x00\x01\x00\x01\x00\x00\x00'
    
    ser = serial.Serial('/dev/ttyS0', 9600) # open serial to write to GPS
 
    # Disabling all NMEA sentences
    ser.write("$PUBX,40,GLL,0,0,0,0*5C\n")
    ser.write("$PUBX,40,GSA,0,0,0,0*4E\n")
    #ser.write("$PUBX,40,RMC,0,0,0,0*47\n")
    ser.write("$PUBX,40,GSV,0,0,0,0*59\n")
    ser.write("$PUBX,40,VTG,0,0,0,0*5E\n")
    #ser.write("$PUBX,40,GGA,0,0,0,0*5A\n");
    
    #Change rate and baudrate
    ser.write(rate10hz)
    #ser.write(baud115200)
    ser.close()
    print "config ublox done \n"

def checkgpsfix():
    data = sergps.readline()
    gpsfix = False
    while (gpsfix== False):
        if (data.startswith("$GPRMC")):
            msg = pynmea2.parse(data)
            gpsfix= msg.is_valid
            print gpsfix
    #return gpsfix

def read_datetimegps():
    data = sergps.readline()
    if (data.startswith("$GPRMC")):
        msg = pynmea2.parse(data)
        gps_datetime = msg.datetime
        gprmcok = msg.is_valid
        if (gprmcok == 1):
            gps_lat = round(msg.latitude,5)
            gps_lon = round(msg.longitude,5)
            gps_tz = tf.timezone_at(lng=gps_lon, lat=gps_lat)
            tz = timezone(gps_tz)
            gps_datetime_aware = gps_datetime.replace(tzinfo=utc)
            gps_datetime_local = gps_datetime_aware.astimezone(tz)
            return str(gps_datetime_local.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4])
        else:
            return ''

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


config_ublox()
#open serial GPS
global sergps
sergps = serial.Serial('/dev/ttyS0',9600)
#inisialisasi variabel GPS
gprmcok = 0
gpggaok = 0
datalinegps = ''
tf = TimezoneFinder()
gps_lat = 0
gps_lon = 0
#checkgpsfix()
'''
if read_datetimegps()==''
    localtime = read_datetimegps()
'''
#print localtime 
    
#Template penamaan file
namafile="/home/pi/Desktop/Result/Normal/Accelero_%s.txt" % (localtime)
namafile_priority="/home/pi/Desktop/Result/Priority/PRIORITY_Accelero_%s.txt" %(localtime)
namafile_OBD="/home/pi/Desktop/Result/Normal/OBD_%s .txt" % (localtime)
namafile_priority_OBD="/home/pi/Desktop/Result/Priority/PRIORITY_OBD_%s .txt" % (localtime)
namafile_GPS="/home/pi/Desktop/Result/Normal/GPS_%s.txt" % (localtime)
namafile_priority_GPS="/home/pi/Desktop/Result/Priority/PRIORITY_GPS_%s.txt" %(localtime)

#Buka file untuk menulis data akselerasi
file=open(namafile,"w")
file_OBD=open(namafile_OBD,"w")
file_GPS=open(namafile_GPS,"w")
file_GPS.write("datetime,latitude,longitude,altitude,course,speed,sat\n")

#Array akselerasi dan waktu. Panjang array 300 untuk menyimpan data 30 detik
rategps = 1
arr_time= [''] * 300
arr_acc_x = [0] * 300
arr_acc_y = [0] * 300
arr_acc_z = [0] * 300
arr_rpm = [''] * 300
arr_speed = [''] * 300
arr_throttle = [''] * 300
arr_load = [''] * 300
arr_coolant = [''] * 300
arr_datagps = [''] * 30

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
    
    #Pembacaan data akselerasi
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
    
    #Penskalaan pembacaan data akselerasi
    accel_xout_scaled = round((accel_xout / 4096.0),5)
    accel_yout_scaled = round((accel_yout / 4096.0),5)
    accel_zout_scaled = round((accel_zout / 4096.0),5)

    
    #Pembacaan data GPS
    data = sergps.readline()
    #print data
    if (data.startswith("$GPRMC")):
        msggps = pynmea2.parse(data)
        #print repr(msg)
        gps_date = msggps.datestamp
        gps_time = msggps.timestamp
        gps_datetime = msggps.datetime
        #gps_datetime = gps_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        gps_lat = round(msggps.latitude,5)
        gps_lon = round(msggps.longitude,5)
        gps_tz = tf.timezone_at(lng=gps_lon, lat=gps_lat)
        gps_speed = msggps.spd_over_grnd
        gps_course = msggps.true_course
        gprmcok = msggps.is_valid
    elif data.startswith("$GPGGA"):
        msggps = pynmea2.parse(data)
        gps_alt = msggps.altitude
        gps_sats = msggps.num_sats
        gpggaok = msggps.is_valid
    else:
        pass
    
    if ((gprmcok == 1) and (gpggaok == 1 )):
        gps_tz = tf.timezone_at(lng=gps_lon, lat=gps_lat)
        tz = timezone(gps_tz)
        gps_datetime_aware = gps_datetime.replace(tzinfo=utc)
        gps_datetime_local = gps_datetime_aware.astimezone(tz)
        
        datalistgps = []
        #datalist.append(str(gps_datetime))
        datalistgps.append(localtime)
        datalistgps.append(str(gps_datetime_local.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]))
        #datalist.append(str(gps_tz))
        datalistgps.append(str(gps_lat))
        datalistgps.append(str(gps_lon))
        datalistgps.append(str(gps_alt))
        datalistgps.append(str(gps_course))
        datalistgps.append(str(gps_speed))
        datalistgps.append(str(gps_sats))
        #datalist.append(str(gprmcok))
        #datalist.append(str(gpggaok))
        datalinegps = ','.join(datalistgps)
        
    
    #Pembacaan data OBD
    cmd1 = obd.commands.RPM
    cmd2 = obd.commands.SPEED
    cmd3 = obd.commands.THROTTLE_POS
    cmd4 = obd.commands.ENGINE_LOAD
    cmd5 = obd.commands.COOLANT_TEMP
    
    #RETRIEVE DATA DARI OBD
    response1 = connection.query(cmd1)
    response2 = connection.query(cmd2)
    response3 = connection.query(cmd3)
    response4 = connection.query(cmd4)
    response5 = connection.query(cmd5)
    
    print "Local current time :",localtime
    print "x_scaled: ", accel_xout_scaled
    print "y_scaled: ", accel_yout_scaled
    print "z_scaled: ", accel_zout_scaled
    
    print("RPM: ")
    print(response1.value.to("rpm"))
    ##print("{} rpm", response1.value)
    print("Speed: ")
    print(response2.value.to("kph"))
    print("Throttle Position: ")
    print(response3.value.to("percent"))
    ##print("{} %", round(response3.value,2))
    print("Engine Load: ")
    print(response4.value.to("percent"))
    ##print("{} %", round(response4.value,2))
    print("Coolant Temperature: ")
    print(response5.value.to("celsius"))
    
    
    Throttle = str(round(float(response3.value),3))
    Engine_Load = str(round(float(response4.value),3))
    
    
    #camera.annotate_text = "%s                               X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_yout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),str(response3.value.to("percent")),str(response4.value.to("percent")),str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
    camera.annotate_text = "%s                       X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_zout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),Throttle,Engine_Load,str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
    
    #Penimpaan array
    #print "%s                               X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_yout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),str(response3.value.to("percent")),str(response4.value.to("percent")),str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
    print "%s                       X: %s  Y: %s  Z: %s\nRPM: %s  Speed: %s  Throttle: %s  Engine: %s  Coolant: %s\nLat: %s  Lon: %s" % (localtime,str(accel_xout_scaled), str(accel_yout_scaled),str(accel_zout_scaled),str(response1.value.to("rpm")),str(response2.value.to("kph")),Throttle,Engine_Load,str(response5.value.to("celsius")), str(gps_lat), str(gps_lon))
    
    
    if (arraycount<300):
        arr_time[arraycount]=localtime
        arr_acc_x[arraycount]=accel_xout_scaled
        arr_acc_y[arraycount]=accel_yout_scaled
        arr_acc_z[arraycount]=accel_zout_scaled
        
        arr_rpm[arraycount]=response1.value.to("rpm")
        arr_speed[arraycount]=response2.value.to("kph")
        arr_throttle[arraycount]=response3.value.to("percent")
        arr_load[arraycount]=response4.value.to("percent")
        arr_coolant[arraycount]=response5.value.to("celsius")
        
    else:
        arraycount=arraycount-300
        arr_time[arraycount]=localtime
        arr_acc_x[arraycount]=accel_xout_scaled
        arr_acc_y[arraycount]=accel_yout_scaled
        arr_acc_z[arraycount]=accel_zout_scaled
        
        arr_rpm[arraycount]=response1.value.to("rpm")
        arr_speed[arraycount]=response2.value.to("kph")
        arr_throttle[arraycount]=response3.value.to("percent")
        arr_load[arraycount]=response4.value.to("percent")
        arr_coolant[arraycount]=response5.value.to("celsius")
            
    if (arraycountGPS<30):
        if ((gprmcok == 1) and (gpggaok == 1 )):
            arr_datagps[arraycountGPS]=datalinegps
    else:
        arraycountGPS=arraycountGPS-30
        if ((gprmcok == 1) and (gpggaok == 1 )):
            arr_datagps[arraycountGPS]=datalinegps
    
    #Apabila pushbutton ditekan, dilakukan penulisan file ke file utama dan file prioritas
    if (priority_status==1):
        file.write(localtime)
        file.write("\tX: ")
        file.write("%.5f\t"  % (accel_xout_scaled))
        file.write("Y: ")
        file.write("%.5f\t"  % (accel_yout_scaled))
        file.write("Z: ")
        file.write("%.5f\n"  % (accel_zout_scaled))
        
        file_OBD.write(localtime)
        file_OBD.write("\tRPM: ")
        file_OBD.write(str(response1.value.to("rpm")))
        file_OBD.write("\tSpeed: ")
        file_OBD.write(str(response2.value.to("kph")))
        file_OBD.write("\tThrottle Position: ")
        file_OBD.write(str(response3.value.to("percent")))
        file_OBD.write("\tEngine Load: ")
        file_OBD.write(str(response4.value.to("percent")))
        file_OBD.write("\tCoolant Temperature: ")
        file_OBD.write(str(response5.value.to("celsius")))
        file_OBD.write("\n")
        
        if ((gprmcok == 1) and (gpggaok == 1 )):
            file_GPS.write(datalinegps)
            file_GPS.write("\n")
	
        file_priority.write(localtime)
        file_priority.write("\tX: ")
        file_priority.write("%.5f\t"  % (accel_xout_scaled))
        file_priority.write("Y: ")
        file_priority.write("%.5f\t"  % (accel_yout_scaled))
        file_priority.write("Z: ")
        file_priority.write("%.5f\n"  % (accel_zout_scaled))
        
        file_priority_OBD.write(localtime)
        file_priority_OBD.write("\tRPM: ")
        file_priority_OBD.write(str(response1.value.to("rpm")))
        file_priority_OBD.write("\tSpeed: ")
        file_priority_OBD.write(str(response2.value.to("kph")))
        file_priority_OBD.write("\tThrottle Position: ")
        file_priority_OBD.write(str(response3.value.to("percent")))
        file_priority_OBD.write("\tEngine Load: ")
        file_priority_OBD.write(str(response4.value.to("percent")))
        file_priority_OBD.write("\tCoolant Temperature: ")
        file_priority_OBD.write(str(response5.value.to("celsius")))
        file_priority_OBD.write("\n")
        
        if ((gprmcok == 1) and (gpggaok == 1 )):
            file_priority_GPS.write(datalinegps)
            file_priority_GPS.write("\n")
            gprmcok = 0
            gpggaok = 0
	
        k=k+1
        
        #Handling untuk file prioritas
        if (k>=300):
            file_priority.close()
            file_priority_OBD.close()
            file_priority_GPS.close()
            #counter_priority=counter_priority+1
            namafile_priority="/home/pi/Desktop/Result/Priority/PRIORITY_Accelero_%s.txt" %(localtime)
            namafile_priority_OBD="/home/pi/Desktop/Result/Priority/PRIORITY_OBD_%s .txt" % (localtime)
            namafile_priority_GPS="/home/pi/Desktop/Result/Priority/PRIORITY_GPS_%s.txt" %(localtime)
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
        
        file_OBD.write(localtime)
        file_OBD.write("\tRPM: ")
        file_OBD.write(str(response1.value.to("rpm")))
        file_OBD.write("\tSpeed: ")
        file_OBD.write(str(response2.value.to("kph")))
        file_OBD.write("\tThrottle Position: ")
        file_OBD.write(str(response3.value.to("percent")))
        file_OBD.write("\tEngine Load: ")
        file_OBD.write(str(response4.value.to("percent")))
        file_OBD.write("\tCoolant Temperature: ")
        file_OBD.write(str(response5.value.to("celsius")))
        file_OBD.write("\n")
        
        if ((gprmcok == 1) and (gpggaok == 1 )):
            file_GPS.write(datalinegps)
            file_GPS.write("\n")
            gprmcok = 0
            gpggaok = 0

    
    #Membuka file baru apabila waktu perekaman telah mencapai 10 menit
    if ((temptime-temptime_init)>600):
        file.close()
        file_OBD.close()
        file_GPS.close()
        #counter=counter+1
        namafile="/home/pi/Desktop/Result/Normal/Accelero_%s.txt" % (localtime)
        namafile_OBD="/home/pi/Desktop/Result/Normal/OBD_%s .txt" % (localtime)
        namafile_GPS="/home/pi/Desktop/Result/Normal/GPS_%s.txt" % (localtime)
        
        file=open(namafile,"w")
        file_OBD=open(namafile_OBD,"w")
        file_GPS=open(namafile_GPS,"w")
        file_GPS.write("datetime,latitude,longitude,altitude,course,speed,sat\n")
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
    if ((inputValue==False) and ((temptime-temptime2)>3)) or (abs(arr_acc_x[arraycount]-arr_acc_x[arraycount-1])>2) or (abs(arr_acc_y[arraycount]-arr_acc_y[arraycount-1])>2) or (abs(arr_acc_z[arraycount]-arr_acc_z[arraycount-1])>2):
        priority_status=1
        
        # LED ON
        GPIO.output(26,True)
        
        k=0
        #Penulisan file prioritas
        file_priority=open(namafile_priority,"w")
        file_priority_OBD=open(namafile_priority_OBD,"w")
        file_priority_GPS=open(namafile_priority_GPS,"w")
        if ((inputValue==False) and ((temptime-temptime2)>3)):
            file_priority.write("Button pressed at ")
            file_priority_OBD.write("Button pressed at ")
            file_priority_GPS.write("Button pressed at ")
        else:
            file_priority.write("Crash at ")
            file_priority_OBD.write("Crash at ")
            file_priority_GPS.write("Crash at ")
        file_priority.write(localtime)
        file_priority_OBD.write(localtime)
        file_priority_GPS.write(localtime)
        file_priority.write("\n")
        file_priority_OBD.write("\n")
        file_priority_GPS.write("\n")
        file_GPS.write("datetime,latitude,longitude,altitude,course,speed,sat\n")
        
        i=0
        j=0
        for i in range(299,0,-1):
            file_priority.write(arr_time[arraycount-i])
            file_priority.write("\tX: ")
            file_priority.write("%.5f\t"  % (arr_acc_x[arraycount-i]))
            file_priority.write("Y: ")
            file_priority.write("%.5f\t"  % (arr_acc_y[arraycount-i]))
            file_priority.write("Z: ")
            file_priority.write("%.5f\n"  % (arr_acc_z[arraycount-i]))
            
            file_priority_OBD.write(arr_time[arraycount-i])
            file_priority_OBD.write("\tRPM: ")
            file_priority_OBD.write("%s\t"  % (arr_rpm[arraycount-i]))
            file_priority_OBD.write("\tSpeed: ")
            file_priority_OBD.write("%s\t"  % (arr_speed[arraycount-i]))
            file_priority_OBD.write("\tThrottle: ")
            file_priority_OBD.write("%s\t"  % (arr_throttle[arraycount-i]))
            file_priority_OBD.write("\tLoad: ")
            file_priority_OBD.write("%s\t"  % (arr_load[arraycount-i]))
            file_priority_OBD.write("\tCoolant: ")
            file_priority_OBD.write("%s\t"  % (arr_coolant[arraycount-i]))
            file_priority_OBD.write("\n")
            
        for j in range (29, 0, -1):
            file_priority_GPS.write(arr_datagps[arraycountGPS-i])
            file_priority_GPS.write("\n")
	    
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


