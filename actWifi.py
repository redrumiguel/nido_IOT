#!/usr/bin/python
##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# Descripcion: Script que permite la conexion a una red wifi determinada por su SSID.
#              Ademas permite la actualizacion de fecha y hora a traves de un servidor NTP.
#              Sin parametros de entrada. Devuelve el valor 1 si no se ha conseguido la co-
#              nexion despues de 10 intentos espaciados 1 segundo cada intento. Si exito, devuelve 0
###############################################################################################
import subprocess
from time import sleep
import socket
import sys
import time
import logging
from datetime import datetime
FORMATO = '%(asctime)s - %(levelname)s - %(script)s - %(message)s'
d = {'script':'actWifi.py'}


                        ## Declaracion de variables globales del script ##
#mySSID = "nestbox" + '\n'
#mySSID = "Mi_casa_2.4" + '\n'
#mySSID = "i2a2-INSTRUMENT" + '\n'
#myIP = "127.0.0.1" + '\n'
#myIP = "192.168.1.51" + '\n'
logging.basicConfig(filename='/home/pi/Nido_IoT_'+datetime.now().strftime('%d-%m-%y.log'), filemode='a', level=logging.DEBUG, format=FORMATO, datefmt='%m/%d/%Y %H:%M:%S')
                        ## Declaracion de funciones del script ##
def get_ssid():
        proc_ssid = subprocess.Popen(["sudo","iwgetid","-r"], stdout=subprocess.PIPE)
     #  proceso proc_ssid -->  obtiene el SSID en la conexion wifi
        output,err = proc_ssid.communicate()
        return output

def check_ssid(NET):
        file1 = open('/etc/wpa_supplicant/wpa_supplicant.conf', "r")
        lineas = file1.readlines()
        file1.close()
        for i, item in enumerate(lineas,0):
                if NET in item:
			return True
	return False

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
                response = client.request('hora.rediris.es')
                clock = time.strftime(time_format,time.localtime(response.tx_time))
                date = time.strftime(date_format,time.localtime(response.tx_time))
                print "sincronizado con ntp server"
                logging.info('Date&Time NTP update', extra=d)
        except:
                # if internet if not available, get clock from host
                import datetime
                clock = datetime.datetime.now().strftime(time_format)
                date = datetime.datetime.now().strftime(date_format)
                print "hora del host"
                logging.warning('Date&Time host update', extra=d)
        return clock, date

                                ## Inicio del programa ##
print "wifi ON"
logging.info('Wifi Connection started', extra=d)
proc_unblock_wlan0 = subprocess.Popen(["sudo","rfkill","unblock","0"], stdout=subprocess.PIPE)
  
proc_wlna_ena = subprocess.Popen(["sudo","ifconfig","wlan0","up"], stdout=subprocess.PIPE)
reintentos = 0
print get_ssid()
while check_ssid(get_ssid()[0:len(get_ssid())-1]) == False or get_ssid() == "":
        if reintentos < 20:
                sleep(2)
                reintentos = reintentos + 1
		logging.warning("..", extra=d)
                print "."
        else:
                sys.exit(-1)
                logging.error('Failed to conenect to wifi')

SSID = get_ssid()[0:len(get_ssid())-1]
IP=get_IP()[0:len(get_IP())-1]
logging.debug('IP - {0}'.format(IP), extra = d)
logging.debug('SSID - {0}'.format(SSID), extra = d)
print "Sincronizando con NTP"
hora = get_datetime()
print "hora ="+hora[0]+" fecha= " +hora[1]

try:
        proc_set_hour = subprocess.Popen(["sudo","date","-s", hora[1] + "-" + hora[0]], stdout=subprocess.PIPE)
        subprocess.Popen.wait(proc_set_hour)
        print "Completada actualizacion de hora"
        logging.debug('Date&Time updated', extra=d)
except:
        print "Error actualizacion"

sys.stdout.write("0\n")

                                        ###### Fin de programa ######





