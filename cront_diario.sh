#! /bin/bash
##############################################################################################
# File: cront_diario.sh
# Autor: Miguel Redruello Garcia
# Version:
# Fecha: 29-03-20
# Descripcion: Script que permite realizar todas las rutinas previstas al finalizar el dia
#	       Este script sera ejecutado por la app crontab.
#	       Una vez al dia, tomara una fotografica del interior, encolara algunos ficheros
#	       e intentara conectarse a una red wifi. Si tiene exito sincronizara los datos
#	       con rclone a google drive.
#	       Ficheros a enviar: fotografia(jpg), datos de temperaturas recogidas (txt)
#				  logs con las entradas y salidas recogidas (txt)
###############################################################################################
cd Documents
./soloON.py
./camara.sh
./soloOFF.py
DATE=$(date +"%d-%m-%y")
DATE_T=$(date +"%d-%m-%Y")
#DATE_CAM=$(date +"%d-%m-%y-%H:%M:%S")
find /home/pi/ -name '*.jpg' | while read a;do /home/pi/Documents/set_cola.py $(basename $a);done
./set_cola.py "temperaturas-"$DATE_T.txt
./set_cola.py "Movimientos_nido1-"$DATE.txt
./set_cola.py "Nido_IoT_"$DATE.log
sudo chmod 666 /home/pi/Documents/rclone_copy.txt
#crontab -l > crontab.crtb
../actWifi.py
if [[ $? -eq 0 ]] 
then

	python /home/pi/Documents/sync_rclone.py
	rclone copy drive:Nido1/Acciones/ /home/pi/Documents/
	rclone copy drive:Nido1/Crontab/ /home/pi/
	FILE_CRTB=$(find /home/pi -iname '*.crtb') 
	crontab $FILE_CRTB
	../desWifi.py
fi

cd
