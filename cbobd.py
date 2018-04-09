#File name : modobd.py
#Source code module for OBD device.

#Import library
import time
import obd

class Obd(object):
	def __init__(self) :
    		self.array_rpm = [''] * 300
		self.array_speed = [''] * 300
		self.array_throttle = [''] * 300
		self.array_load = [''] * 300
		self.array_coolant = [''] * 300
		self.connection = obd.OBD()
		self.rpm_before = 0
		self.throttle_before = 0
    
	def read_data(self,counter) :
    		#Assign variables for each of the OBD data
  	  	cmd1 = obd.commands.RPM
    		cmd2 = obd.commands.SPEED
    		cmd3 = obd.commands.THROTTLE_POS
    		cmd4 = obd.commands.ENGINE_LOAD
    		cmd5 = obd.commands.COOLANT_TEMP
	
    		self.rpm = self.connection.query(cmd1)
    		self.speed = self.connection.query(cmd2)
    		self.throttle = self.connection.query(cmd3)
    		self.load = self.connection.query(cmd4)
    		self.coolant = self.connection.query(cmd5)
    
    		self.array_rpm[counter]=self.rpm.value.to("rpm")
    		self.array_speed[counter]=self.speed.value.to("kph")
    		self.array_throttle[counter]=self.throttle.value.to("percent")
    		self.array_load[counter]=self.load.value.to("percent")
    		self.array_coolant[counter]=self.coolant.value.to("celsius")
	
	def driver_category(self, counter) :		
		#Develop initial variable
		self.array_rpm[counter] = rpm_now
		self.array_speed[counter] = speed_now
		self.array_throttle[counter] = throttle_now
		
		#Calculation process for further categorization
		rpm_change = abs(rpm_now - self.rpm_before)
		throttle_change = abs(throttle_now - self.throttle_before)
		ratio_speed_rpm = (speed_now/220)/(rpm_now/8000)
		ratio_throttle_rpm = (throttle_change/max(self.array_throttle))/(rpm_change/max(self.array_rpm))
										 
		#Decide between good or bad driver
		if (ratio_speed_rpm > 0.9) and (ratio_speed_rpm < 1.3) and (ratio_throttle_rpm > 0.9) and (ratio_throttle_rpm < 1.3) and (load > 20) and (load < 50):
			print('Good Driver')
		else:
			print('Bad Driver')
		
		#After process configuration
		self.rpm_before = rpm_now
		self.throttle_before = throttle_now
	
	def driver_behavior(self, counter) :
		#Develop initial variable
		self.array_speed[counter] = speed_now
		self.array_rpm[counter] = rpm_now
		
		#Overspeed
		if (speed_now > 100):
			self.counter_speed = self.counter_speed + 1
		else:
			self.counter_speed = 0
		if (self.counter_speed == 50):
			print("Overspeed")
		
		#High RPM
		if (rpm_now > 4000):
			print("High RPM")
		
		#Idle time
		if (speed_now == 0):
			self.counter_speed = self.counter_speed + 1
		else:
			self.counter_speed = 0
		if (self.counter_speed == 3000):
			print("Idle")
		
	
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
