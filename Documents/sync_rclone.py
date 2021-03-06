"""
###############################################################################################################$
File:  sync_rclone.py
Autor: Miguel Redruello Garcia
Fecha: 29-03-20
Version:
Descripcion: Script que permite la sincronizacion de archivos encolados en un chichero txt. Para ello, leemos ese 
	     fichero y procedemos a la sincronizacion de estos ficheros uno tras otro. Si alguno fallara en su 
	     comunicacion se reescribe en el fihcero original para su posterior envio la siguiente vez que sea posible
	     El sistema de almacenamiento de ficheros se estructura por nido --> ano --> mes --> dia --> ficheros
###############################################################################################################$
"""
import subprocess
from datetime import date
from datetime import datetime
import time
import sys
import os.path
from os import path
import logging

FORMATO = '%(asctime)s - %(levelname)s - %(script)s - %(message)s'
logging.basicConfig(filename='/home/pi/Nido_IoT_'+datetime.now().strftime('%d-%m-%y.log'), filemode='a', level=logging.DEBUG, format=FORMATO, datefmt='%m/%d/%Y %H:%M:%S')

					  ### Definicion de funciones ###
def leer_file():
	### Variables locales ###
	today = date.today()
	fecha = today.strftime("%d-%m-%y")
	hora = time.strftime("%H:%M") 
	proc = []
	linea = []
	d = {'script':'sync_rclone.py'}
	try:
        	file1 = open("rclone_copy.txt","r+")
	except:
		file1.close()
#		print "excepcion"
		sys.exit("no exite el archivo")
		logging.error('Could\'n open rclone_copy.txt',extra=d)
        lineas = file1.readlines()
	proc_rm = subprocess.Popen(["rm", "./rclone_copy.txt"], stdout=subprocess.PIPE)
#	proc_rm = subprocess.Popen(["sudo", "rm", "./rclone_copy.txt"], stdout=subprocess.PIPE)
	file1.seek(0)
	file1.close()
	for i, item in enumerate(lineas,0):
		lineas[i] = lineas[i].split(",")
		print lineas[i]
		if path.exists(lineas[i][0]):
			proc.append(subprocess.Popen(["rclone", "copy", lineas[i][0], "drive:Nido1/20"+lineas[i][1][6:8]+ "/" + lineas[i][1][3:5]+"/"+lineas[i][1][0:2]], stdout=subprocess.PIPE))
			logging.info('Copied into Cloud - {0}'.format(lineas[i][0]), extra = d)
    			resp= proc[i].communicate()
			proc[i].wait()
			print lineas[i][0]
			if proc[i].returncode != 0:
				escrbir = lineas[i][0]+","+lineas[i][1]
				print ("error en " +  escrbir)
				try:
					file2 = open("rclone_copy.txt","a")
					file2.write(escrbir)
                                	file2.close()
				except:
					file2.close()
                			sys.exit("Error al abrir archivo")
			else:
				if hora == "23:59":
					proc_rm_2 = subprocess.Popen(["rm", lineas[i][0]], stdout=subprocess.PIPE)
					#proc_rm_2 = subprocess.Popen(["sudo", "rm", lineas[i][0]], stdout=subprocess.PIPE)
					#print "borrar"
					logging.info("File removed - time:  {0}".format(hora), extra=d)
				else:
					file_name, file_extension = os.path.splitext(lineas[i][0])
					proc_date_lastmod = subprocess.Popen(["date", "+%d-%m-%y", "-r", lineas[i][0]], stdout=subprocess.PIPE)
			        	output_fecha,errno_fecha = proc_date_lastmod.communicate()
					fecha_last = output_fecha[0:len(output_fecha)-1].replace("/","-") ## cambio de / por - en el formato
					if (file_extension != '.txt' and  file_extension != '.log') or fecha_last != fecha:
						logging.info("File removed - extension: {0}".format(file_extension), extra=d)
						proc_rm_3 = subprocess.Popen(["rm", lineas[i][0]], stdout=subprocess.PIPE)
		else:
			print ("El archivo a enviar no exite")
			logging.warning("File dosn\'n exist anymore - {0}".format(lineas[i][0]), extra=d)
					### Incio Script ###
leer_file()
					### Fin Script ###
