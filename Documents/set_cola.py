"""
############################################################################################################################
File: set_cola.py
Autor: Miguel Redruello Garcia
Fecha: 29-03-20
Version:
Descripcion: Script que permite encolar archivos que recibe por parametros [python set_cola.py <archivo a encolar>].
	     Para ello, lo busca en primer luegar, para conocer su PATH completo y si existe, lo adjunta junto con la fecha 
	     de modificacion en un archivo txt.
	     Este archivo sera despues utilizador por el script sync_rclone.py para enviarlos a la cuenta de drive asocialda 
############################################################################################################################
"""
import subprocess
import sys
					### Definicion de funciones ###
def grabar_file(name_file):
	proc_find = subprocess.Popen(["sudo", "find", "/home/pi", "-name", name_file], stdout=subprocess.PIPE)
	output,errno = proc_find.communicate()
	if (output != ""):
		file2 = open("rclone_copy.txt","a") #Archivo a crear /abir para intruducir el archivo a encolar
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
						### Inicio Script ###
print sys.argv[1]
grabar_file(sys.argv[1])
						### Fin Script ###
