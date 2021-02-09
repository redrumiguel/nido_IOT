#! /bin/bash
##############################################################################################
# File: main.sh
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-04-20
# Descripcion: Script que permite lanzar el programa principal ejecutado por crontab
###############################################################################################
./desWifi.py

cd Documents

#sudo ./main_nido.py & ../wifi_interrupcion.py
./main_nido.py & ../wifi_interrupcion.py

cd
