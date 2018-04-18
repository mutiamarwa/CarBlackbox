#Filename : carblackbox.py
#Deskripsi : Perekaman data untuk ditulis di file utama dan file prioritas apabila trigger ditekan.
#Created by : Hans Christian, Mutia Marwa, Gregorius Henry
#Last Modified : 28 February 2018

#import library
import math
import time
import datetime
from multiprocessing import Process, Value, Array
import ctypes

def f(n):
	#print time.asctime(time.localtime(time.time()))
	n.value = 1
	#n.value = time.time()

def g(n):
	#print time.asctime(time.localtime(time.time()))
	if n.value==0:
		print ("on")
	else:
		print ("off")
	#n.value = time.time()
	
if __name__ == '__main__':
	num = Value(ctypes.c_int,0)
    #arr = Array('i', range(10))
	while (1):
		p = Process(target=f, args=(num,))
		q = Process(target=g, args=(num,))
		q.start()
		p.start()
		q.join()
		p.join()
		print num.value