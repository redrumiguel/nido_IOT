#!/usr/bin/python

from datetime import datetime
from desarmar_trama import *
import serial
import RPi.GPIO as GPIO
import subprocess
import struct
import logging

FORMATO = '%(asctime)s - %(levelname)s - %(script)s - %(message)s'
d = {'script':'get_date_time.py'}

ser = serial.Serial('/dev/ttyS0',baudrate = 9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
PIN_RPI_READY = 6

logging.basicConfig(filename='/home/pi/Get_tramas'+datetime.now().strftime('%d-%m-%y.log'), filemode='a', level=logging.DEBUG, format=FORMATO, datefmt='%m/%d/%Y %H:%M:%S')

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

def convert_dec_bcd_int_format(dec):
	return (dec/16*10)+(dec%16)

def get_temp_hora_from_trama(subtrama, fecha, files):
	temp_medida = subtrama[0] + subtrama[1]
        min_str = subtrama[2]
        hora_str = subtrama[3]
        print ("temp: {0}".format(temp_medida), hex)
        print ("min: {0}".format(min_str), hex)
        print ("hora: {0}".format(hora_str), hex)
        temp_sin =struct.unpack("H", temp_medida)[0]
        min_sin = struct.unpack("B", min_str)[0]
        hora_sin = struct.unpack("B", hora_str)[0]
        print ("temp_sin: {0}".format(temp_sin), hex)
        temperatura = ((175.72 * temp_sin)/ 65536) - 46.85
        print ("temp: {0} C".format(temperatura))
        min = convert_dec_bcd_int_format(min_sin)
        print ("min: {0}".format(min))
        hora = convert_dec_bcd_int_format(hora_sin)
        print ("hora: {0}".format(hora))
        files.write(fecha)
        files.write(" ")
        files.write(str("%.2d" %(hora)))
        files.write(":")
        files.write(str("%.2d" %(min)))
        files.write(", ")
        files.write(str("{:,.2f}".format(temperatura)))
        files.write(",\n")


dato = b'\x00'
print("conectando")
act_wifi = subprocess.Popen(["./actWifi.py"], stdout=subprocess.PIPE)
act_wifi.wait()
print("conected")
pin_init(PIN_RPI_READY)
temp = ""
while 1:
	if dato == b'\x0A': ## sincronizacion inicial. Hora y Archivo de acciones
		print (dato)
		dato = b'\x00'
		print (get_datetime(), 'utf-8')
		ser.write(get_datetime())
#		print (leer_file(), 'utf-8')
#                ser.write(leer_file())
#		off = subprocess.Popen(["sudo", "poweroff"], stdout=subprocess.PIPE)
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
		ser.write(b'\x03')
                tam8 = ser.read(2)
		print ("tam8: ")
		print (tam8, hex)
		tam = struct.unpack("H", tam8)[0]
		print ("tam: ")
		print (tam)
		logging.debug('Numero de bytes: {0}'.format(tam), extra=d)
		fecha = ser.read(4)
		print ("fecha: ")
		print (fecha, hex)
		logging.debug('Fecha: {0}'.format(fecha), extra=d)
	        dom  = convert_dec_bcd_int_format(struct.unpack("B", fecha[0])[0])
	        month  = convert_dec_bcd_int_format(struct.unpack("B", fecha[1])[0])
	        year = convert_dec_bcd_int_format(struct.unpack("B", fecha[2])[0])
		year1 = convert_dec_bcd_int_format(struct.unpack("B", fecha[3])[0])
		year = str(year) + str(year1) 
		print ("year: ")
		print (year)
		temp += ser.read(tam)
		print ("temp: ")
		print (temp, hex)
		## procesado de temp y generacion de fichero de texto.
		lista_rx = list(temp)
		print (lista_rx, hex)
		file2 = open("/home/pi/temperaturas-" + str("%.2d" %(dom)) + "-" + str("%.2d" %(month)) + "-" + str(year) + ".txt","a")
		for i in range(4,len(lista_rx)):
			if i % 4 == 0:
				iteracion = lista_rx[i-4:i]
				get_temp_hora_from_trama(iteracion, str("%.2d" % (dom)) + "-" + str("%.2d" % (month)) + "-" + str(year), file2)
		last_iteracion = lista_rx[len(lista_rx)-4:len(lista_rx)]
		get_temp_hora_from_trama(last_iteracion, str("%.2d" %(dom)) + "-" + str("%.2d" % (month)) + "-" + str(year), file2)
        	file2.close()
		dato = b'\x00'
	else:
		dato = ser.read(1)
#		print (dato, hex)
		data_left = ser.inWaiting()
		dato += ser.read(data_left)
		#print (dato, hex)
