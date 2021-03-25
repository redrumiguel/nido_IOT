#!/usr/bin/python
##############################################################################################
# File:  main.nido.py
# Autor: Miguel Redruello Garcia
# Version:V 1.1
# Fecha: 06-02-21
# Descripcion: Programa principal del proyector para la monitorizacion de aves. Esta aplicacion
#	       permite la gestion de dos pulsadores con los cuales se detecta la entrada o sali-
#	       da de las aves al nido. Una vez que uno de ellos es pulsado se activa el lector
#	       del puerto serie donde se reciben una serie de tramas, una de las cuales ofrece
#	       el identificador unico del ave. Una vez procesado el identificador se procede a
#	       leer un fichero dado por el cliente donde se especifica a cada identificador la 
#	       la necesidad o no de capturarlo. Esta accion sera realizada una vez se haya accio-
#	       nado el segundo pulsador. Si se diera esta situacion se proceede a grabar un video
#	       asi como, la notificacion por email del hecho. Tanto en el caso de captura o no,
#   	       se procedera a dejar reflejado en un arhivo txt toda la actividad que se recoja
#	       anotandose la fecha,hora, identificador, y si ha salido o entrado del nido. 
#	       Programa hara pooling a los pulsadores constantemete hasta que se produce una cap-
#	       tura. En ese momento, sera necesario un reset del sistema.
###############################################################################################

import time
import serial
import os, time
import RPi.GPIO as GPIO
from datetime import date
from time import sleep
from eleciman import *
from infrared import *
from datetime import datetime
import subprocess
## Metodos para realizar registros de Logs
import logging
FORMATO = '%(asctime)s - %(levelname)s - %(script)s - %(message)s'
logging.basicConfig(filename='/home/pi/Nido_IoT_'+datetime.now().strftime('%d-%m-%y.log'), filemode='a', level=logging.DEBUG, format=FORMATO, datefmt='%m/%d/%Y %H:%M:%S')
d = {'script':'main_nido.py'}

GPIO.setmode(GPIO.BCM)
## Pin infrarrojo
PIN_ENA_INFRARED = 21
## Pines para el electroiman
PIN_ENA_ELECIMAN = 6
## Pines asociados a las interrupciones de los pulsadores
PIN_FUERA = 5
PIN_DENTRO = 12
## Pin habilitar lector RFID.
PIN_RFID = 27
## Estados  maquina principal
POOLING = 0b00
LECTURA = 0b01
## Variables globales
trama_leida = b'\x00'
contador = 0
flagteiner = 0b0000  #variable encargada de monitorizar estados pulsadores(dos posiciones mas bajas), si es desconocido(tercera posicion)
		     # y si hay algun ave dentro (cuarta posicion), todas ellas a nivel alto.
capturado = False
pool = True
NIDO = "1"
GPIO.setup(PIN_RFID, GPIO.OUT)
GPIO.setup(PIN_FUERA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_DENTRO, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
ESTADO = POOLING
## Funcion del API serial para configurar el puerto serie
ser = serial.Serial('/dev/ttyS0',baudrate = 9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout = 5)  ## ver cuanto tiempo estan en tubo para entrar y variar timeout si necesario
ser.close()
infrared_init(PIN_ENA_INFRARED)
						### Declaracion de funciones ###
""" Funcion que permite leer el puerto serie del lector de transponder y elaborar y filtrar tramas para devolver una valida"""
def lee_trama():
	print "leo trama"
	global flagteiner, ser
	## Variables locales
	acabado = False
	dato = b'\x00'
	trama = 0
	trama1 = 0
	trama2 = 0
	## Estados maquina de lectura
	LEE = 0b0
	GET_TRAMA = 0b1
	ESTADO_TRAMA = LEE
	while(acabado != True):
        	if ESTADO_TRAMA == LEE:
                	while dato != b'\x10\x02': ##patron inicial de trama valida
				try:
                        		dato = ser.read(1)
                        		dato = dato + ser.read(1)
                               		print (dato,hex)
					print len(dato)
					if len(dato)  == 0:
						trama = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
						flagteiner = flagteiner | 0b0100
						acabado = True
						ser.close()
						return trama
				except serial.SerialException: ## caputra si el puerto esta cerrado (default). Permite abortar lecturas 
							       ## accidentales
					acabado = True
					trama = "no valida"
					logging.warning("No valid data", extra=d)
					return trama
                	trama = dato
                	dato = b'\x00\x00'
                	ESTADO_TRAMA = GET_TRAMA
        	elif ESTADO_TRAMA == GET_TRAMA:
                	while dato != b'\x10\x03': ##patron final de trma buscada
                        	dato = ser.read(1)
                        	dato = dato + ser.read(1)
                        	trama = trama + dato
                	dato = b'\x00\x00'
                	trama = trama + ser.read(1)
                	print "la trama es:"
                	print trama.encode("hex")
			trama2 = trama1
                        trama1 = trama
			if trama2 == trama1:
				ser.close()
                                acabado = True
				print "return"
				flagteiner = flagteiner & 0b1011
                                return trama
			else:
				ESTADO_TRAMA = LEE
## Funcion para esritura de logs en archivo txt. Formto: fecha, hora, id, entra/sale, capturado/no capturado
def escribo_file(capturado, sale):
	print "escribo file"
	file_name = "Movimientos_nido1-"+fecha+".txt"
	file1 = open(file_name,"a")
	file1.write("Fecha: ")
        file1.write(fecha)
        file1.write(", Hora: ")
        file1.write(hora)
        file1.write(", Id: ")
        file1.write(id)
	if sale == 0b1:
                file1.write(", entra")
	else:
		file1.write(", sale")
	if capturado == True:
		file1.write(", capturado ")
	file1.write("\n")
        file1.close()
## Funcoon para lectura de archivo de acciones del cliente. Devuelve si hay que capturar el ave.
def leer_file(trama):
	proc_find = subprocess.Popen(["find", "-iname", 'Acciones.inst'], stdout=subprocess.PIPE) 
	file, filerror = proc_find.communicate()
	file1 = open(file[0:len(file)-1], "r")
	lineas = file1.readlines()
	file1.close()
	indice = 0
	for i, item in enumerate(lineas,0):
        	if trama in item:
                	print i
                	indice = i
	if "capturar" in lineas[indice]:
        	hora = time.strftime("%H:%M:%S")
        	linea =  lineas[indice].split(", ")
        	if linea[2] < hora and linea[3] > hora:
                	return True
        	else:
                	return False
	else:
		return False
""" Callback de interrupcion genereada por el switch mas externo al nido"""
def button_ext(channel):
	global flagteiner, pool, ESTADO, ser
	pool = True
        print("Button exterior pressed!")
	if flagteiner >> 0 & 1:
        	flagteiner = flagteiner & 0b1110
	else:
		flagteiner = flagteiner | 0b0001
	print "inter ext:"
	print bin(flagteiner)
        ESTADO = POOLING
""" Callback de interrupcion genereada por el switch mas interno al nido"""
def button_int(channel):
	global pool, flagteiner, ESTADO, ser
	pool = True
        print "Button interior pressed"
	if flagteiner >> 1 & 1:
                flagteiner = flagteiner & 0b1101
        else:
                flagteiner = flagteiner | 0b0010
		if flagteiner >> 0 & 1 == 0:
                        flagteiner = flagteiner | 0b1000
	print "inter int:"
        print bin(flagteiner)
        ESTADO = POOLING
					### Incio de la maquina de estados princiap ###
GPIO.add_event_detect(PIN_DENTRO, GPIO.FALLING, callback=button_int, bouncetime=500)
GPIO.add_event_detect(PIN_FUERA, GPIO.FALLING, callback=button_ext, bouncetime=500)
"""Algoritmo princpal que realiza la gestion de interrpcion de switches, lecturas y escritura de ficheros de texto, toma decision para atrapar
o no determinadas aves"""
print "Starting program"
flagteiner = 0b0000
PROGRAMA_ACTIVO = True
while PROGRAMA_ACTIVO == True:
	if ESTADO == POOLING:
        	while pool == True:
           		if flagteiner >> 3 & 1 == 0  and flagteiner >> 1 & 1 and flagteiner >> 0 & 1 :
                		#segundo switch, dentro analizar que hacer, con transponder
               			## analizo y tomo una accion
				if leer_file(id):
					capturado = True
					logging.info('Captured', extra = d)
					print "PAJARO ID CAPTURADO"
					GPIO.remove_event_detect(PIN_DENTRO)
                                        GPIO.remove_event_detect(PIN_FUERA)
					##capturo pajaro
					eleciman_init(PIN_ENA_ELECIMAN)
					eleciman_on(PIN_ENA_ELECIMAN)
					time.sleep(0.5)
					eleciman_off(PIN_ENA_ELECIMAN)
					#grabo video
					#infrared_on(PIN_ENA_INFRARED)
					#proc_record_video = subprocess.Popen(["raspivid", "-t", "10000","-w","640","-h","480","-o",id + "-" + fecha + "-"+ hora +".h264"], stdout=subprocess.PIPE)
                                        #proc_record_video.wait()
					#infrared_off(PIN_ENA_INFRARED)
                                       # print "viedo done"
                                       # o = subprocess.Popen([""./video.sh"], stdout=subprocess.PIPE)
                                       # proc_set_cola = subprocess.Popen(["/home/pi/Documents/set_cola.py", id + "-" + fecha + "-"+ hora +".h264"], stdout=subprocess.PIPE)
					#proc_set_cola.wait()
                                       # print "set_cola done"
					#arranco wifi
					PROGRAMA_ACTIVO = False
					proc_actWifi = subprocess.Popen(["/home/pi/actWifi.py"], stdout=subprocess.PIPE)
					proc_actWifi.wait()
                                        if proc_actWifi.returncode != 0:
                                        	print "No ha sido posible conectarse a la red"
                                        else:
                                        	#envio mail
                                                print "wifi activo"
                                                proc_mail = subprocess.Popen(["/home/pi/Documents/mail.py", NIDO, str(id)], stdout=subprocess.PIPE)
                                                proc_mail.wait()
                                                #apago wifi
                                                print "mail sent"
                                                proc_dis_wifi = subprocess.Popen(["/home/pi/desWifi.py"], stdout=subprocess.PIPE)
                                                proc_dis_wifi.wait()
                                                print "des wifi"
				else:
					#otras acciones
					#grabo video
                                        infrared_on(PIN_ENA_INFRARED)
                                        proc_record_video = subprocess.Popen(["raspivid", "-t", "60000","-w","640","-h","480","-o",id + "-" + fecha + "-"+ hora +".h264"], stdout=subprocess.PIPE)
                                        proc_record_video.wait()
                                        infrared_off(PIN_ENA_INFRARED)
                                        print "viedo done"
					proc_set_cola = subprocess.Popen(["/home/pi/Documents/set_cola.py", id + "-" + fecha + "-"+ hora +".h264"], stdout=subprocess.PIPE)
                                        proc_set_cola.wait()
                                        print "set_cola done"
				time.sleep(0.3)
				print "0b0011 piso segundo sw y entrando"
				flagteiner = flagteiner & 0b1100
                                flagteiner = flagteiner | 0b1000
				escribo_file(capturado, flagteiner >> 3 & 1)
			elif flagteiner == 0b0000:
				logging.info('tried to get in but left', extra = d)
                                #esta entrando
				print flagteiner
                                print "0b0000 piso 1 sw pero se fue"
            		elif flagteiner >> 1 & 1 == 0 and flagteiner >> 0 & 1:
                		#esta entrando
               			ESTADO = LECTURA
				flagteiner = flagteiner & 0b0011
				print "0b0001 entrando"
				logging.info('getting in', extra = d)
            		elif flagteiner >> 3 & 1  and flagteiner >> 1 & 1 and flagteiner >> 0 & 1 == 0:
                		#saliendo del nido
				print "0b1010 saliendo del nido sw interior"
				logging.info('getting out', extra = d)
				ESTADO = LECTURA
			elif flagteiner >> 3 & 1  and flagteiner >> 1 & 1 and flagteiner >> 0 & 1 == 1:
				print "0b1x11 ha salido "
				logging.info('Left', extra = d)
				escribo_file(capturado,0b0)
                                flagteiner = 0b0000
            		elif flagteiner >> 3 & 1  and flagteiner >> 1 & 1 == 0 and flagteiner >> 0 & 1 == 0:
				print "0b1x00 volvio a entrar"
				logging.info('tried to leeve but stayed', extra = d)
				time.sleep(0.3)
			pool = False
    	elif ESTADO == LECTURA:
		print "estado lectura"
		## Habilito lector RFID
		GPIO.output(PIN_RFID, GPIO.HIGH)
		## Habilito puerto serie
		try:
                        ser.open()
                except serial.SerialException:
                        print "cant open port"
                        logging.warning("Serial port can\'t opened", extra=d)
		trama_leida = lee_trama()
		## Deshabilito puerto serie
		try:
                        ser.close()
                except serial.SerialException:
                        print "cant close port"
                        logging.warning("Serial port can\'t be closed", extra=d)
		## Deshabilito lector RFID para ahorro de energia.
		GPIO.output(PIN_RFID, GPIO.LOW)
       			 ## guardo la informacion de hora fecha e id del pajaro en file
		today = date.today()
		fecha = today.strftime("%d-%m-%y")
		hora = time.strftime("%H:%M:%S") 
		print "flagteiner: "
		print bin(flagteiner)
		if trama_leida == "no valida":
			print "trama no valida"
		else:
        		if flagteiner == 0b0001 or flagteiner == 0b1010:
            			id = trama_leida[5:10].encode("hex")
				print "id es: "
            			print id
			elif flagteiner  >> 2 & 1:
                        	id = "0000000000"
                        	print id
				print bin(flagteiner)
				if flagteiner >> 2 & 1 and flagteiner >> 1 & 1 == 0  and flagteiner >> 0 & 1:
                                	print "flagsteiner "+ bin(flagteiner)
                                	flagteiner = flagteiner & 0b1000
                                	print "pulsacion erronea pulsador externo"
                        	elif flagteiner >> 2 & 1 and flagteiner >> 1 & 1  and flagteiner >> 0 & 1 == 0:
                                	flagteiner = flagteiner & 0b1000
                                	print "pulsacion erronea pulsador interno"
		ESTADO = POOLING
print "Pajara capturado. Necesito Reset"
						### Fin Maquina principal ###
