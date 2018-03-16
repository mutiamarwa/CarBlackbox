#File name : OBD.py
#Source code module for OBD device.

#Import library
import time
import obd

class Obd:
	def init_obd :
    		ArrayOBDRPM = [''] * 300
		ArrayOBDSpeed = [''] * 300
		ArrayOBDThrottle = [''] * 300
		ArrayOBDLoad = [''] * 300
		ArrayOBDCoolant = [''] * 300
		connection = obd.OBD()
    
	def baca_obd(Counter) :
    		#Assign variables for each of the OBD data
  	  	cmd1 = obd.commands.RPM
    		cmd2 = obd.commands.SPEED
    		cmd3 = obd.commands.THROTTLE_POS
    		cmd4 = obd.commands.ENGINE_LOAD
    		cmd5 = obd.commands.COOLANT_TEMP
	
    		response1 = connection.query(cmd1)
    		response2 = connection.query(cmd2)
    		response3 = connection.query(cmd3)
    		response4 = connection.query(cmd4)
    		response5 = connection.query(cmd5)
    
    		ArrayOBDRPM[Counter]=response1.value.to("rpm")
    		ArrayOBDSpeed[Counter]=response2.value.to("kph")
    		ArrayOBDThrottle[Counter]=response3.value.to("percent")
    		ArrayOBDLoad[Counter]=response4.value.to("percent")
    		ArrayOBDCoolant[Counter]=response5.value.to("celsius")
	
	def tulis_data_obd(file) :
    		#Opening file for external write process
    		#file = open(NamaFile, "w")
	
    		#Writing process
    		file.write(localtime)
    		file.write("\tRPM: ")
    		file.write(str(response1.value.to("rpm")))
    		file.write("\tSpeed: ")
    		file.write(str(response2.value.to("kph")))
    		file.write("\tThrottle Position: ")
    		file.write(str(response3.value.to("percent")))
    		file.write("\tEngine Load: ")
    		file.write(str(response4.value.to("percent")))
    		file.write("\tCoolant Temperature: ")
    		file.write(str(response5.value.to("celsius")))
    		file.write("\n")
