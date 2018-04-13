#File name : modgps.py
#Source code module for GPS device.

#Import library
import re
import array
import serial
import pynmea2
import datetime
from pytz import timezone, utc
from timezonefinder import TimezoneFinder
import array

# setup default GPS device (different on Raspberry Pi 3 and above)
def _get_rpi_revision():
    """Returns the version number from the revision line."""
    for line in open("/proc/cpuinfo"):
        if "Revision" in line:
            return re.sub('Revision\t: ([a-z0-9]+)\n', r'\1', line)


rpi_revision = _get_rpi_revision()
if (rpi_revision and
      (rpi_revision != 'Beta') and
      (int('0x'+rpi_revision, 16) >= 0xa02082)):
    # RPi 3 and above
    DEFAULT_GPS_DEVICE = '/dev/ttyS0'
else:
    # RPi 2 and below
    DEFAULT_GPS_DEVICE = '/dev/ttyAMA0'
	
class Gps(object):
    def __init__(self, device=DEFAULT_GPS_DEVICE):
        self.serialcom = serial.Serial(device,
                                       baudrate=9600,
                                       bytesize=8,
                                       parity='N',
                                       stopbits=1,
                                       timeout=0.5,
                                       rtscts=0)
        self.gprmc_status = 0
	self.gpgga_status = 0
	self.lat = 0
	self.lon = 0
	self.dataline = ''
	self.tf = TimezoneFinder()
	self.tzinfo = utc
	
	duration = 60/2 #minutes
	rate_gps = 10
	self.array_dataline=[''] * duration * rate_gps
	
    #configurasi gps ublox
    def config_ublox(self) :
        #Ublox configuration
        baud9600 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x80\x25\x00\x00\x07\x00\x07\x00\x00\x00\x00\x00\xE2\xE1\xB5\x62\x06\x00\x01\x00\x01\x08\x22'
        baud57600 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xE1\x00\x00\x07\x00\x07\x00\x00\x00\x00\x00\xE2\xE1\xB5\x62\x06\x00\x01\x00\x01\x08\x22'
        baud115200 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xc2\x01\x00\x07\x00\x07\x00\x00\x00\x00\x00\xc4\x96\xb5\x62\x06\x00\x01\x00\x01\x08\x22'
		
	rate1hz = b'\xB5\x62\x06\x08\x06\x00\xE8\x03\x01\x00\x01\x00\x00\x00'
	rate5hz = b'\xB5\x62\x06\x08\x06\x00\xC8\x00\x01\x00\x01\x00\x00\x00'
	#rate10hz = b'\xB5\x62\x06\x08\x06\x00\x64\x00\x01\x00\x01\x00\x00\x00'
	rate10hz = array.array('B',[0xB5,0x62,0x06,0x08,0x06,0x00,0x64,0x00,0x01,0x00,0x01,0x00,0x00,0x00]).tostring()
	 
	# Disabling all NMEA sentences
	self.serialcom.write("$PUBX,40,GLL,0,0,0,0*5C\n")
	self.serialcom.write("$PUBX,40,GSA,0,0,0,0*4E\n")
	self.serialcom.write("$PUBX,40,GSV,0,0,0,0*59\n")
	self.serialcom.write("$PUBX,40,VTG,0,0,0,0*5E\n")
	
	#Change rate and baudrate
	self.serialcom.write(rate10hz.encode('utf-8'))

    def is_fix(self) :
	self.data = self.serialcom.readline()
	gpsfix = false
	while (gpsfix == false) :
	    if (self.data.startswith("$GPRMC")) :
		msg = pynmea2.parse(self.data)
		gpsfix = msg.is_valid
		return gpsfix
		
    def read_datetime(self):
	self.data = self.serialcom.readline()
	if (self.data.startswith("$GPRMC")) :
	    msg = pynmea2.parse(self.data)
	    gps_datetime = msg.datetime
	    gprmcok = msg.is_valid
	    if (gprmcok == 1):
		gps_lat = round(msg.latitude,5)
		gps_lon = round(msg.longitude,5)
		gps_tz = self.tf.timezone_at(lng = self.lon, lat = self.lat)
		tz = timezone(gps_tz)
		gps_datetime_aware = self.datetime.replace(tzinfo=utc)
		gps_datetime_local = gps_datetime_aware.astimezone(tz)
		self.datetime = gps_datetime_local.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
		return self.datetime

    def read_data(self,counter) :
	#Pembacaan data GPS
	self.data = self.serialcom.readline()
	#self.data ="$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
	#print data
	if (self.data.startswith("$GPRMC")):
	    msggps = pynmea2.parse(self.data)
	    #print repr(msg)
	    self.datetime = msggps.datetime
	    self.lat = round(msggps.latitude,5)
	    self.lon = round(msggps.longitude,5)
	    #self.tz = self.tf.timezone_at(lng=self.lon, lat=self.lat)
	    self.speed = msggps.spd_over_grnd
	    self.course = msggps.true_course
	    self.gprmc_status = msggps.is_valid
	elif self.data.startswith("$GPGGA"):
	    msggps = pynmea2.parse(self.data)
	    self.alt = msggps.altitude
	    self.sats = msggps.num_sats
	    self.gpgga_status = msggps.is_valid
	else:
	    pass
		
	if ((self.gprmc_status == 1) and (self.gpgga_status == 1 )):
	    '''gps_tz = self.tf.timezone_at(lng=self.lon, lat=self.lat)
	    tz = timezone(gps_tz)
	    gps_datetime_aware = self.datetime.replace(tzinfo=utc)
	    gps_datetime_local = gps_datetime_aware.astimezone(tz)
	    self.datetime = gps_datetime_local.strftime('%Y-u%m-%d %H:%M:%S.%f')[:-4]'''
	    
	    datalist = []
	    datalist.append(str(self.datetime))
	    #self.datalistgps.append(localtime)
	    #self.datalistgps.append(str(gps_datetime_local.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]))
	    #datalist.append(str(gps_tz))
	    datalist.append(str(self.lat))
	    datalist.append(str(self.lon))
	    datalist.append(str(self.alt))
	    datalist.append(str(self.course))
	    datalist.append(str(self.speed))
	    datalist.append(str(self.sats))
	    self.dataline = ','.join(datalist)
		
	#Array replacing process
	self.array_dataline[counter]=self.dataline

    def write_data(self,file):
	file.write(self.dataline)
	file.write("\n")

    def write_array(self,file, counter):
	file.write(self.array_dataline[counter])
	file.write("\n")
