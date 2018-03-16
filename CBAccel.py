#File name : Accelerometer.py
#Source code module for accelerometer device.

#Import library
import smbus
import math
import time

#Function to conduct accelerometer reading process
def BacaByte(adr) :
    return bus.read_byte_data(address, adr)

def BacaData(adr) :
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def BacaData1(adr) :
    val = BacaData(adr)
    if (val >= 0x8000) :
        return -((65535 - val) + 1)
    else:
        return val

def InitAkselero() :
	#Power management for turning on the accelerometer
	Daya1 = 0x6b
	Daya2 = 0x6c
	bus = smbus.SMBus (1)
	address = 0x68

	#Configure the sensitivity of the accelerometer
	bus.write_byte_data(address, Daya1, 0)
	bus.write_byte_data(address, 0x1c, 0x10)
	
	ArrayAccelX = [0] * 300
	ArrayAccelY = [0] * 300
	ArrayAccelZ = [0] * 300

def BacaAkselero(Counter) :	
	#Accelerometer data reading process
	AccelX = BacaData1(0x3b)
	AccelY = BacaData1(0x3d)
	AccelZ = BacaData1(0x3f)
	
	AccelXScaled = round((AccelX / 4096.0), 5)
	AccelYScaled = round((AccelY / 4096.0), 5)
	AccelZScaled = round((AccelZ / 4096.0), 5)
	
	#Array replacing process
	ArrayAccelX[Counter] = AccelXScaled
	ArrayAccelY[Counter] = AccelYScaled
	ArrayAccelZ[Counter] = AccelZScaled

def TulisAkselero(file) :
	#Opening file for external write process
	#file = open(NamaFile, "w")
	
	#Writing process
	file.write(localtime)
        file.write("\tX: ")
        file.write("%.5f\t"  % (AccelXScaled))
        file.write("Y: ")
        file.write("%.5f\t"  % (AccelYScaled))
        file.write("Z: ")
        file.write("%.5f\n"  % (AccelZScaled))
