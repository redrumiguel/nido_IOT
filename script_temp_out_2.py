#!/usr/bin/python
##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# File: mido_tyh_wlog_int.py
# Descripcion: Script que permite la medida de temperatura del sensor interno del nido.
#
###############################################################################################
import subprocess
import time
import RPi.GPIO as GPIO
					### Inicio Script ###
PIN_SENSOR_TEMP_EXT2 = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SENSOR_TEMP_EXT2, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.output(PIN_SENSOR_TEMP_EXT2, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(PIN_SENSOR_TEMP_EXT2, GPIO.LOW)
time.sleep(6.5)
tmp=subprocess.call ("./mido_tyh_wlog_ext")
GPIO.output(PIN_SENSOR_TEMP_EXT2, GPIO.HIGH)

					### Fin Script ###
