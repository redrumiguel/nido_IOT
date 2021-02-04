#!/usr/bin/python 
import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
PIN_ACT_WIFI = 23
GPIO.setup(PIN_ACT_WIFI, GPIO.IN)
def activo_Wifi(channel):
        print "Activo wifi mediante pulsador"
        proc_actWifi2 = subprocess.Popen(["sudo", "python", "/home/pi/actWifi.py"], stdout=subprocess.PIPE)
        proc_actWifi2.wait()
	#proc_mail=subprocess.Popen(["/home/pi/Documents/mailip.sh"],stdout=subprocess.PIPE)

GPIO.add_event_detect(PIN_ACT_WIFI, GPIO.FALLING, callback=activo_Wifi)

while True:
	programa = True
