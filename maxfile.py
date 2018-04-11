#Buat ngebatesin jumlah file dalam 1 folder
# udah bisa jalan

import os
import time
pathfolder=[""]*5
pathfolder[0]="/home/pi/Desktop/Result/Normal/Accelero/"
pathfolder[1]="/home/pi/Desktop/Result/Normal/GPS/"
pathfolder[2]="/home/pi/Desktop/Result/Normal/OBD/"
pathfolder[3]="/home/pi/Desktop/Result/Normal/Frontcam/"
pathfolder[4]="/home/pi/Desktop/Result/Normal/Rearcam/"

'''
path1 = '/home/pi/Desktop/Result/Normal/Accelero/'
path2 = '/home/pi/Desktop/Result/Normal/GPS/'
path3 = '/home/pi/Desktop/Result/Normal/OBD/'
path4 = '/home/pi/Desktop/Result/Normal/Frontcam/'
path5 = '/home/pi/Desktop/Result/Normal/Rearcam/'
'''
while(1):
    for i in range (0,5):
        path=pathfolder[i]
        print path
        onlyfiles = next(os.walk(path)) [2]
        amount = len(onlyfiles)
        print (amount)
        while (amount>2):
            file=min(os.listdir(path), key = lambda p: os.path.getmtime(os.path.join(path,p)))
            print(file)
            newpath = path + file
            os.remove(newpath)
            onlyfiles = next(os.walk(path)) [2]
            amount = len(onlyfiles)
        else:
            print('File not removed')
    
    time.sleep(10)
