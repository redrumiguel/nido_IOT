#! /bin/bash
##############################################################################################
# File: rescue_old_file.sh
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 05-02-21
# Descripcion: Script de mantenimiento que permite encolar archivos antiguos que no han podido
#		ser encolados y por tanto no disponibles en cloud
###############################################################################################

find /home/pi/ -name 'temp*' | while read a;do /home/pi/Documents/set_cola.py $(basename $a);done
find /home/pi/ -name 'Mov*' | while read a;do  /home/pi/Documents/set_cola.py $(basename $a);done
find /home/pi/ -name '*.h264' | while read a;do /home/pi/Documents/set_cola.py $(basename $a);done
find /home/pi/ -name '*.jpg' | while read a;do /home/pi/Documents/set_cola.py $(basename $a);done
