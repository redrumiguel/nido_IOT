#!/usr/bin/python
##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# File: mido_tyh_wlog_out.py
# Descripcion: Script que permite la medida de temperatura del sensor exterior del nido.
#
###############################################################################################
import subprocess
import time
import RPi.GPIO as GPIO
					### Inicio Script ###
PIN_SENSOR_TEMP_OUT = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SENSOR_TEMP_OUT, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.output(PIN_SENSOR_TEMP_OUT, GPIO.HIGH)
time.sleep(5)    ##tiempo necesario que esta medida se tome unos segundos despues de la otra medida ya que ambos script se lanzan al mismo tiempo
## no necesario cuando conf definita de hw
GPIO.output(PIN_SENSOR_TEMP_OUT, GPIO.LOW)
time.sleep(0.5)
tmp=subprocess.call ("./mido_tyh_wlog_ext")
GPIO.output(PIN_SENSOR_TEMP_OUT, GPIO.HIGH)
					### Fin Script ###
