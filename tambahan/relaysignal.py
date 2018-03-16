import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Dari 3.3V
GPIO.setup(5,GPIO.OUT) #Output signal dari raspi untuk ke relay
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pushbutton buat priority

GPIO.output(5,True) #awalnya ga ada tegangan outputnya
print("Jalan")
inputpriority = True #Awalnya keadaan priori
priority=False

while (1):
    inputpriority=GPIO.input(21)
    if (inputpriority==False): #button ditekan
        if(priority==False):
            priority=True
        else:
            priority=False
    print(priority)
    
    inputValue=True
    if (inputValue==False): #Gaada Tegangan
        # Keluarin Sinyal
        print (inputValue)
        if (priority==False):
            os.system("sudo shutdown now")
            GPIO.output(5,False)          
        print("Mati")
    else: #ada tegangan
        GPIO.output(5,True)
        print("Hidup") 
    time.sleep(0.1)
    