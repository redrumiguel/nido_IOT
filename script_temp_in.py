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
PIN_SENSOR_TEMP_INT = 17


def sensor_int_init(PIN_SENSOR_TEMP_INT):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN_SENSOR_TEMP_INT, GPIO.OUT)
	GPIO.setwarnings(False)
	GPIO.output(PIN_SENSOR_TEMP_INT, GPIO.LOW)
#time.sleep(0.5)
def sensor_int_mide(PIN_SENSOR_TEMP_INT):
	GPIO.output(PIN_SENSOR_TEMP_INT, GPIO.HIGH)
	time.sleep(3)
	tmp=subprocess.call ("./mido_tyh_wlog_int")
	GPIO.output(PIN_SENSOR_TEMP_INT, GPIO.LOW)
sensor_int_init(PIN_SENSOR_TEMP_INT)
sensor_int_mide(PIN_SENSOR_TEMP_INT)
					### Fin Script ###
