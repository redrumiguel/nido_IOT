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
import time
import sys
					  ### Definicion de funciones ###
def leer_file():
	### Variables locales ###
	today = date.today()
	fecha = today.strftime("%d-%m-%y")
	proc = []
	linea = []
	try:
        	file1 = open("rclone_copy.txt","r+")
	except:
		file1.close()
		sys.exit("no exite el archivo")
        lineas = file1.readlines()
	proc_rm = subprocess.Popen(["sudo", "rm", "./rclone_copy.txt"], stdout=subprocess.PIPE)
	file1.seek(0)
	file1.close()
	for i, item in enumerate(lineas,0):
		lineas[i] = lineas[i].split(",")
		proc.append(subprocess.Popen(["rclone", "copy", lineas[i][0], "drive:Nido1/20"+lineas[i][1][6:8]+ "/" + lineas[i][1][3:5]+"/"+lineas[i][1][0:2]], stdout=subprocess.PIPE))
    		resp= proc[i].communicate()
		proc[i].wait()
		print lineas[i][0]
		if proc[i].returncode != 0:
			escrbir = lineas[i][0]+","+lineas[i][1]
			print "error en " +  escrbir
			try:
				file2 = open("rclone_copy.txt","a")
			except:
				file2.close()
                		sys.exit("Error al abrir archivo")
			file2.write(escrbir)
			file2.close()
		else:
			proc_rm_2 = subprocess.Popen(["sudo", "rm", lineas[i][0]], stdout=subprocess.PIPE)
			print "borrar"

					### Incio Script ###
leer_file()
					### Fin Script ###