#File name : modaccel.py
#Source code module for accelerometer device.

#Import library
import smbus
import math
import time

class Accel(object):
    def __init__(self):
        #Power management for turning on the accelerometer
		self.status=0
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68       # This is the address value read via the i2cdetect command
        self.resultan_before = 0

        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)#wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, 0x1c,0x10) #penulisan register untuk sensitivitas akselerometer
        
        duration = 60/2 #minutes
        rate_accel = 100 #Hz
        self.array_x = [0] * duration * rate_accel
        self.array_y = [0] * duration * rate_accel
        self.array_z = [0] * duration * rate_accel
        
    #Function to conduct accelerometer reading process
    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def read_data(self,counter) :	
        #Accelerometer data reading process
        if (self.status==0):
			self.xraw = self.read_word_2c(0x3b)
			self.yraw = self.read_word_2c(0x3d)
			self.zraw = self.read_word_2c(0x3f)
		else:
			self.xraw = 0
			self.yraw = 0
			self.zraw = 0
            
        self.x_scaled = round((self.xraw / 4096.0), 5)
        self.y_scaled = round((self.yraw / 4096.0), 5)
        self.z_scaled = round((self.zraw / 4096.0), 5)
            
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
        file.write("%.5f\t"  % self.array_x[counter])
        file.write("Y: ")
        file.write("%.5f\t"  % self.array_x[counter])
        file.write("Z: ")
        file.write("%.5f\n"  % self.array_x[counter])
        
    def driver_behavior_accel(self,counter):
        x_now = self.array_x[counter]
        y_now = self.array_y[counter] 
        self.resultan = math.sqrt((x_now*x_now)+(y_now*y_now))
        if (self.resultan-self.resultan_before)>0.33:
            print("Aggresive Start")
            self.condition_accel = "Aggresive Start"
        elif (self.resultan-self.resultan_before)<-0.5:
            print("Hard Braking")
            self.condition_accel = "Hard Braking"
        else:
            self.condition_accel = ""
      
        self.resultan_before = self.resultan
        
