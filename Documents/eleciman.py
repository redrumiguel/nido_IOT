#!/usr/bin/python
##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 08-02-21
# Descripcion: Script que permite habilitar led infrarrojo
###############################################################################################

import RPi.GPIO as GPIO
import time

PIN_ENA_ELECIMAN = 6


def eleciman_init(pin_infrared):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin_infrared,GPIO.OUT)
        GPIO.output(pin_infrared, GPIO.LOW)

def eleciman_on(pin_infrared):
    GPIO.output(pin_infrared, GPIO.HIGH)

def eleciman_off(pin_infrared):
    GPIO.output(pin_infrared, GPIO.LOW)

eleciman_init(PIN_ENA_ELECIMAN)
eleciman_on(PIN_ENA_ELECIMAN)
time.sleep(0.5)
eleciman_off(PIN_ENA_ELECIMAN)
