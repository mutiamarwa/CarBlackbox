#File name : modaccel.py
#Source code module for accelerometer device.

#Import library
import smbus
import math
import time

#Function to conduct accelerometer reading process
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

class Accel(object):
    def __init__(self):
        #Power management for turning on the accelerometer
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        address = 0x68       # This is the address value read via the i2cdetect command

        bus.write_byte_data(address, power_mgmt_1, 0)#wake the 6050 up as it starts in sleep mode
        bus.write_byte_data(address, 0x1c,0x10) #penulisan register untuk sensitivitas akselerometer
        
        duration = 60/2 #minutes
        rate_accel = 100 #Hz
        self.array_x = [0] * duration * rate_accel
        self.array_y = [0] * duration * rate_accel
        self.array_z = [0] * duration * rate_accel

    def read_data(self,counter) :	
        #Accelerometer data reading process
        self.x = read_word_2c(0x3b)
        self.y = read_word_2c(0x3d)
        self.z = read_word_2c(0x3f)
            
        self.x_scaled = round((self.x / 4096.0), 5)
        self.y_scaled = round((self.y / 4096.0), 5)
        self.z_scaled = round((self.z / 4096.0), 5)
            
        #Array replacing process
        self.array_x[counter] = self.x_scaled 
        self.array_y[counter] = self.y_scaled 
        self.array_z[counter] = self.z_scaled 

    def write_data(self,file,localtime):
        #Opening file for external write process
        #file = open(NamaFile, "w")
            
        #Writing process
        file.write(localtime)
        file.write("\tX: ")
        file.write("%.5f\t"  % (self.x_scaled))
        file.write("Y: ")
        file.write("%.5f\t"  % (self.y_scaled))
        file.write("Z: ")
        file.write("%.5f\n"  % (self.z_scaled))
    
    def write_array(self,file,counter,localtime):
        #Opening file for external write process
        #file = open(NamaFile, "w")
            
        #Writing process
        file.write(localtime)
        file.write("\tX: ")
        file.write("%.5f\t"  % self.array_x[Counter])
        file.write("Y: ")
        file.write("%.5f\t"  % self.array_x[Counter])
        file.write("Z: ")
        file.write("%.5f\n"  % self.array_x[Counter])
