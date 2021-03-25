#!/usr/bin/python
##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 08-02-21
# Descripcion: Script que permite controlar el servo para cierre del nido
###############################################################################################


import RPi.GPIO as GPIO
import time
import logging
from datetime import datetime
d = {'script':'servo.py'}

logging.basicConfig(filename='/home/pi/Nido_IoT_'+datetime.now().strftime('%d-%m-%y.log'), filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(script)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')


PIN_ENA_SERVO = 6
SERVO = 7

# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one frequency is 20ms
# duty cycle for 0 degree = (1/20)*100 = 5%
# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
# duty cycle for 180 degree = (2/20)*100 = 10%

#p.start(5)# starting duty cycle ( it set the servo to 0 degree )
def servo_init(pin_servo, pin_pwm):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(pin_servo,GPIO.OUT)
	GPIO.setup(pin_pwm,GPIO.OUT)
	GPIO.output(pin_servo, GPIO.HIGH)
	time.sleep(0.6)
	p=GPIO.PWM(pin_pwm,50)# 50hz frequency
        p.start(5)# starting duty cycle ( it set the servo to 0 degree 
	time.sleep(1.9)
	GPIO.output(pin_servo, GPIO.LOW)
	return p
def release_trap(pin_servo, pin_pwm, pwm, posicion): 
    try:
        GPIO.output(pin_servo, GPIO.HIGH)
        time.sleep(0.6)
        pwm.ChangeDutyCycle(posicion)
	logging.debug('Moving servo..', extra=d)
	time.sleep(1.9) 
        GPIO.output(pin_servo, GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup()

