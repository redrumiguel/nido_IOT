#!/usr/bin/python

from datetime import datetime
from desarmar_trama import *
import serial
import RPi.GPIO as GPIO
import subprocess
import struct
ser = serial.Serial('/dev/ttyS0',baudrate = 9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
PIN_RPI_READY = 6

def pin_init(PIN):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.output(PIN, GPIO.LOW)

def get_datetime():
        now = datetime.now() # current date and time
        year = now.strftime("%Y")
        month = now.strftime("%m")
	dow = now.strftime("%u")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        min = now.strftime("%M")
        sec = now.strftime("%S")
        trama1 = bytearray([b'\x01',int(sec),int(min),int(hour),int(day),int(dow),int(month),int(year[0:2]),int(year[2:4]),b'\x01'])
        return trama1

dato = b'\x00'

pin_init(PIN_RPI_READY)


while 1:
	if dato == b'\x0A': ## sincronizacion inicial. Hora y Archivo de acciones
		print (dato)
		dato = b'\x00'
		print (get_datetime(), 'utf-8')
		ser.write(get_datetime())
		print (leer_file(), 'utf-8')
                ser.write(leer_file())
	elif dato == b'\x0B':  ##Hora, realizar videos y apagar
		print (dato)
                dato = b'\x00'
		print (get_datetime(), 'utf-8')
                ser.write(get_datetime())
		## video
		get_video = subprocess.Popen(["./video.sh"], stdout=subprocess.PIPE)
		get_video.wait()
		## commando de apagar
		off = subprocess.Popen(["sudo", "poweroff"], stdout=subprocess.PIPE)
	elif dato == b'\x0C': ## hora , temperaturas, movimientos, foto, subo ficheros, sincronizo acciones y apago
#		print (dato, hex)
		ser.write(b'\x03')
                tam8 = ser.read(2)
		print ("tam8: ")
		print (tam8, hex)
		tam = struct.unpack("H", tam8)[0]
		print ("tam: ")
		print (tam)
		fecha = ser.read(4)
		print ("fecha: ")
		print (fecha, hex)
		temp = ser.read(tam)
		print ("temp: ")
		print (temp, hex)
		## procesado de temp y generacion de fichero de texto.
		lista_rx = list(temp)
		print (lista_rx, hex)

		for i in range(4,len(lista_rx)):
			if i % 4 == 0:
				iteracion = lista_rx[i-4:i]
				temp_medida = iteracion[0] + iteracion[1]
				min_str = iteracion[2]
				hora_str = iteracion[3]
				print ("temp: {0}".format(temp_medida), hex)
				print ("min: {0}".format(min_str), hex)
				print ("hora: {0}".format(hora_str), hex)
				temp_sin =struct.unpack("H", temp_medida)[0]
				min_sin = struct.unpack("B", min_str)[0]
				hora_sin = struct.unpack("B", hora_str)[0]
				print ("temp_sin: {0}".format(temp_sin), hex)
				temperatura = ((175.72 * temp_sin)/ 65536) - 46.85
				print ("temp: {0} C".format(temperatura))
				min = (min_sin/16*10)+(min_sin%16)
				print ("min: {0}".format(min))
				hora = (hora_sin/16*10)+(hora_sin%16)
                                print ("hora: {0}".format(hora))
		iteracion = lista_rx[len(lista_rx)-4:len(lista_rx)]
                temp_medida = iteracion[0] + iteracion[1]
                min_str = iteracion[2]
                hora_str = iteracion[3]
                print ("temp: {0}".format(temp_medida), hex)
                print ("min: {0}".format(min_str), hex)
                print ("hora: {0}".format(hora_str), hex)
                temp_sin =struct.unpack("H", temp_medida)[0]
                min_sin = struct.unpack("B", min_str)[0]
                hora_sin = struct.unpack("B", hora_str)[0]
                print ("temp_sin: {0}".format(temp_sin), hex)
                temperatura = ((175.72 * temp_sin)/ 65536) - 46.85
                print ("temp: {0} C".format(temperatura))
                min = (min_sin/16*10)+(min_sin%16)
                print ("min: {0}".format(min))
                hora = (hora_sin/16*10)+(hora_sin%16)
                print ("hora: {0}".format(hora)) 
		dato = b'\x00'
	else:
		dato = ser.read(1)
		data_left = ser.inWaiting()
		dato += ser.read(data_left)
		print (dato, hex)
