#File name : GPS.py
#Source code module for GPS device.

#Import library
import serial
import pynmea2
import datetime
from pytz import timezone, utc
from timezonefinder import TimezoneFinder

#configurasi gps ublox
def config_ublox :
    #Ublox configuration
    baud9600 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x80\x25\x00\x00\x07\x00\x07\x00\x00\x00\x00\x00\xE2\xE1\xB5\x62\x06\x00\x01\x00\x01\x08\x22'
    baud57600 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xE1\x00\x00\x07\x00\x07\x00\x00\x00\x00\x00\xE2\xE1\xB5\x62\x06\x00\x01\x00\x01\x08\x22'
    baud115200 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xc2\x01\x00\x07\x00\x07\x00\x00\x00\x00\x00\xc4\x96\xb5\x62\x06\x00\x01\x00\x01\x08\x22'
    
    rate1hz = b'\xB5\x62\x06\x08\x06\x00\xE8\x03\x01\x00\x01\x00\x00\x00'
    rate5hz = b'\xB5\x62\x06\x08\x06\x00\xC8\x00\x01\x00\x01\x00\x00\x00'
    rate10hz = b'\xB5\x62\x06\x08\x06\x00\x64\x00\x01\x00\x01\x00\x00\x00'
    
    #Opening serial to write to GPS
    ser = serial.Serial('/dev/ttyS0', 9600)
 
    # Disabling all NMEA sentences
    ser.write("$PUBX,40,GLL,0,0,0,0*5C\n")
    ser.write("$PUBX,40,GSA,0,0,0,0*4E\n")
    ser.write("$PUBX,40,GSV,0,0,0,0*59\n")
    ser.write("$PUBX,40,VTG,0,0,0,0*5E\n")
    
    #Change rate and baudrate
    ser.write(rate10hz)
    ser.close()

def checkgpsfix :
    data = ser.readline()
    gpsfix = false
    while (gpsfix == false) :
        if (data.startswith("$GPRMC")) :
            msg = pynmea2.parse(data)
            gpsfix = msg.is_valid

def read_datetimegps :
    data = ser.readline()
    if (data.startswith("$GPRMC")) :
        msg = pynmea2.parse(data)
        gps_datetime = msg.datetime
        gprmcok = msg.is_valid
        if (gprmcok == 1):
            gps_lat = round(msg.latitude,5)
            gps_lon = round(msg.longitude,5)
            gps_tz = tf.timezone_at(lng = gps_lon, lat = gps_lat)
            tz = timezone(gps_tz)
            gps_datetime_aware = gps_datetime.replace(tzinfo = utc)
            gps_datetime_local = gps_datetime_aware.astimezone(tz)
            return gps_datetime_local.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

def InitGPS:
    config_ublox()
    sergps = serial.Serial('/dev/ttyS0',9600)
    gprmcok = 0
    gpggaok = 0
    datalinegps = ''
    tf = TimezoneFinder()
    gps_lat = 0
    gps_lon = 0
    rategps = 1
    ArrayGPS=[''] * 30 * rategps
    
def BacaGPS(Counter) :
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
    
    #Array replacing process
    ArrayGPS[Counter]=datalinegps

def TulisGPS(file):
    file.write(datalinegps)
    file.write("\n")