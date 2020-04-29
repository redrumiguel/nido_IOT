##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# Descripcion: Script que permite la conexion a una red wifi determinada por su SSID.
#	       Ademas permite la actualizacion de fecha y hora a traves de un servidor NTP.
#	       Sin parametros de entrada. Devuelve el valor 1 si no se ha conseguido la co-
#	       nexion despues de 10 intentos espaciados 1 segundo cada intento. Si exito, devuelve 0
###############################################################################################
import subprocess
from time import sleep
import socket
import sys
import time

proc_unblock_wlan0 = subprocess.Popen(["sudo","rfkill","unblock","0"], stdout=subprocess.PIPE)

proc_wlna_ena = subprocess.Popen(["sudo","ifconfig","wlan0","up"], stdout=subprocess.PIPE)

			## Declaracion de variables globales del script ##
mySSID = "Mi_casa_2.4" + '\n'
myIP = "127.0.0.1" + '\n'
SSID = " "
IP = " "
			## Declaracion de funciones del script ##
def get_ssid():
	proc_ssid = subprocess.Popen(["sudo","iwgetid","-r"], stdout=subprocess.PIPE)
     #  proceso proc_ssid -->  obtiene el SSID en la conexion wifi
	output,err = proc_ssid.communicate()
	return output

def get_IP():
        proc_ip = subprocess.Popen(["hostname","-I"], stdout=subprocess.PIPE)
     #  proceso proc_ssid -->  obtiene la IP en la conexion wifi
        output,err = proc_ip.communicate()
	return output

def get_datetime(): 
        #format = "%H:%m - %A %-d %B %Y" # e.g. 20:15 - Tuesday 3 April 2015
        time_format = "%H:%M"
        date_format = "%A %-d %B %Y"
        try:
                # get clock from internet
                import ntplib
                client = ntplib.NTPClient()
                response = client.request('es.pool.ntp.org')
                clock = time.strftime(time_format,time.localtime(response.tx_time))
                date = time.strftime(date_format,time.localtime(response.tx_time))
                print "sincronizado con ntp server"
        except:
                # if internet if not available, get clock from host
                import datetime
                clock = datetime.datetime.now().strftime(time_format)
                date = datetime.datetime.now().strftime(date_format)
                print "hora del host"
        return clock, date

				## Inicio del programa ##
print "wifi ON"
reintentos = 0
while SSID != mySSID or IP == myIP:
	if reintentos < 10:
		sleep(1)
		SSID = get_ssid()
		IP = get_IP()
        	reintentos = reintentos + 1
	else:
	        sys.exit(1)

print SSID
print IP
print "Sincronizando con NTP"
hora = get_datetime()

try:
	proc_set_hour = subprocess.Popen(["sudo","date","--set=" + hora[0]], stdout=subprocess.PIPE)
	subprocess.Popen.wait(proc_set_hour)
	print "Completada sincronizacion de hora"
except:
	print "Error sincronizacion"

sys.stdout.write("0\n")

					###### Fin de programa ######
