##############################################################################################
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# File: desWifi.py
# Descripcion: Script que permite deshabilitar la interfaz wifi numero 0.
#
###############################################################################################
import subprocess

proc_des_wlan0 = subprocess.Popen(["sudo","iwconfig","wlan0","txpower","off"], stdout=subprocess.PIPE)

print "wifi Off"

				#### Fin script  ####
