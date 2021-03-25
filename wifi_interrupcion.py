#!/usr/bin/python
import RPi.GPIO as GPIO
import subprocess
import logging
from datetime import datetime

d = {'script':'wifi_interrupcion.py'}

logging.basicConfig(filename='/home/pi/Nido_IoT_'+datetime.now().strftime('%d-%m-%y.log'), filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(script)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
GPIO.setmode(GPIO.BCM)
PIN_ACT_WIFI = 23
GPIO.setup(PIN_ACT_WIFI, GPIO.IN)
def activo_Wifi(channel):
        print ("Activo wifi mediante pulsador")
        proc_actWifi2 = subprocess.Popen(["/home/pi/actWifi.py"], stdout=subprocess.PIPE)
        proc_actWifi2.wait()
	logging.info('Manual Wifi Switch pushed', extra=d)
	#proc_mail=subprocess.Popen(["/home/pi/Documents/mailip.sh"],stdout=subprocess.PIPE)


GPIO.add_event_detect(PIN_ACT_WIFI, GPIO.FALLING, callback=activo_Wifi)

while 1:
	#programa = True
	pass

