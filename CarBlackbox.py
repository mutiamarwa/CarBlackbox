from libcoba2 import Gps

if __name__ == '__main__':
	gps = Gps()
	gps.read()
	file_gps=open('hasilcobagps.txt',"w")
	print gps.data
	gps.write_to_file(file_gps)