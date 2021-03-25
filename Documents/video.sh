
#! /bin/bash
##############################################################################################
# File: video.sh
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# Descripcion: Script de bash que permite grabacion de 15 seg de video con una resolucion 
#	       640x480
#	       El video sera guardada con formato .h264 pero se realiza una conversion a mp4 
#	       y el nombre se compondra por la fecha.
#	      
###############################################################################################
DATE=$(date +"%d-%m-%Y")
raspivid -t 15000 -w 640 -h 480 -o /home/pi/Documents/$DATE.h264

#MP4Box -add /home/pi/$DATE.h264 /home/pi/Documents/$DATE.mp4

#sudo rm /home/pi/Documents/$DATE.h264
