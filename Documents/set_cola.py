#!/usr/bin/python
############################################################################################################################
# File: set_cola.py
# Autor: Miguel Redruello Garcia
# Fecha: 29-03-20
# Version:
# Descripcion: Script que permite encolar archivos que recibe por parametros [python set_cola.py <archivo a encolar>].
#	     Para ello, lo busca en primer luegar, para conocer su PATH completo y si existe, lo adjunta junto con la fecha 
#	     de modificacion en un archivo txt.
#	     Este archivo sera despues utilizador por el script sync_rclone.py para enviarlos a la cuenta de drive asocialda 
############################################################################################################################

import subprocess
import sys
import logging
from datetime import datetime

FORMATO = '%(asctime)s - %(levelname)s - %(script)s - %(message)s - %(file)s '
d = {'script':'set_cola.py', 'file': sys.argv[1]}
logging.basicConfig(filename='/home/pi/Nido_IoT_'+datetime.now().strftime('%d-%m-%y.log'), filemode='a', level=logging.DEBUG, format=FORMATO, datefmt='%m/%d/%Y %H:%M:%S')

					### Definicion de funciones ###
def grabar_file(name_file):
	logging.info('set into the out buffer', extra=d)
	#proc_find = subprocess.Popen(["sudo", "find", "/home/pi", "-iname", name_file], stdout=subprocess.PIPE)
	proc_find = subprocess.Popen(["find", "/home/pi", "-iname", name_file], stdout=subprocess.PIPE)
	output,errno = proc_find.communicate()
	if (output != ""):
		file2 = open("/home/pi/Documents/rclone_copy.txt","a") #Archivo a crear /abir para intruducir el archivo a encolar
		file2.write(output[0:len(output)-1])
		file2.write(",")
		proc_date_lastmod = subprocess.Popen(["date", "+%d-%m-%y", "-r", output[0:len(output)-1]], stdout=subprocess.PIPE)
        	output_fecha,errno_fecha = proc_date_lastmod.communicate()
		print output_fecha[0:len(output_fecha)-1]
		file2.write(output_fecha[0:len(output_fecha)-1].replace("/","-")) ## cambio de / por - en el formato
		file2.write("\n")
		file2.close()
	else:
		print "no existe el archivo"
		logging.warning('file coudn\'t be found', extra=d)
						### Inicio Script ###
print sys.argv[1]
grabar_file(sys.argv[1])
						### Fin Script ###
