#! /bin/bash
##############################################################################################
# File: camara.sh
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# Descripcion: Script que permite la toma de una imagen con la camara de las raspberry pi
#	       La imagen sera guardada con formato jpg y el nombre se compondra por la fecha.
#	      
###############################################################################################
DATE=$(date +"%d-%m-%y-%H:%M:%S")
raspistill -o /home/pi/Documents/$DATE.jpg
