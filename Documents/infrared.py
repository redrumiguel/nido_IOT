#!/usr/bin/python
##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 08-02-21
# Descripcion: Script que permite habilitar led infrarrojo
###############################################################################################

import RPi.GPIO as GPIO

PIN_ENA_INFRARED = 21


def infrared_init(pin_infrared):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin_infrared,GPIO.OUT)
        GPIO.output(pin_infrared, GPIO.LOW)

def infrared_on(pin_infrared):
    GPIO.output(pin_infrared, GPIO.HIGH)

def infrared_off(pin_infrared):
    GPIO.output(pin_infrared, GPIO.LOW)


