#File name : modobd.py
#Source code module for OBD device.

#Import library
import time
import obd

class OBD:
	def __init__(self) :
    		self.array_rpm = [''] * 300
		self.array_speed = [''] * 300
		self.array_throttle = [''] * 300
		self.array_load = [''] * 300
		self.array_coolant = [''] * 300
		connection = obd.OBD()
    
	def read_data(self,counter) :
    		#Assign variables for each of the OBD data
  	  	cmd1 = obd.commands.RPM
    		cmd2 = obd.commands.SPEED
    		cmd3 = obd.commands.THROTTLE_POS
    		cmd4 = obd.commands.ENGINE_LOAD
    		cmd5 = obd.commands.COOLANT_TEMP
	
    		self.rpm = connection.query(cmd1)
    		self.speed = connection.query(cmd2)
    		self.throttle = connection.query(cmd3)
    		self.load = connection.query(cmd4)
    		self.coolant = connection.query(cmd5)
    
    		self.array_rpm[counter]=self.rpm.value.to("rpm")
    		self.array_speed[counter]=self.speed.value.to("kph")
    		self.array_throttle[counter]=self.throttle.value.to("percent")
    		self.array_load[counter]=self.load.value.to("percent")
    		self.array_coolant[counter]=self.coolant.value.to("celsius")
	
	def write_data(self, file, localtime) :
    		#Opening file for external write process
    		#file = open(NamaFile, "w")
	
    		#Writing process
    		file.write(localtime)
    		file.write("\tRPM: ")
    		file.write(str(self.rpm.value.to("rpm")))
    		file.write("\tSpeed: ")
    		file.write(str(self.speed.value.to("kph")))
    		file.write("\tThrottle Position: ")
    		file.write(str(self.throttle.value.to("percent")))
    		file.write("\tEngine Load: ")
    		file.write(str(self.load.value.to("percent")))
    		file.write("\tCoolant Temperature: ")
    		file.write(str(self.coolant.value.to("celsius")))
    		file.write("\n")
    		
        def write_array(self, file, counter, localtime) :
    		#Opening file for external write process
    		#file = open(NamaFile, "w")
	
    		#Writing process
    		file.write(localtime)
    		file.write("\tRPM: ")
    		file.write(str(self.array_rpm[counter]))
    		file.write("\tSpeed: ")
    		file.write(str(self.array_speed[counter]))
    		file.write("\tThrottle Position: ")
    		file.write(str(self.array_throttle[counter]))
    		file.write("\tEngine Load: ")
    		file.write(str(self.array_load[counter]))
    		file.write("\tCoolant Temperature: ")
    		file.write(str(self.array_coolant[counter]))
    		file.write("\n")