#!/usr/bin/python
""" 
################################################################################################################
Fecha: 29-03-20
Autor: Miguel Redruello Garcia
Version
File: mail.py
Descripcion: Script para el envio de emails de notificacion al cliente en tiempo real que existe 
	     un individuo capturado. Este script necesita introducir un parametro con identificacion 
	     del numero del nido donde se ha producido la captura, asi como, la identificacion del sujeto 
	     capturado.
#################################################################################################################
"""
import sys
# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
						### Inicio Scrit ### 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Esta es una prueba de mail con identificacion de nido ["+sys.argv[1]+"], cuya identificacion es ["+sys.argv[2]+"] con python que sera utilizada para enviar mensajes una vez que un pajaro sea capturado.\n Miguel"
 
# setup the parameters of the message
password = "#hwiot33"
msg['From'] = "dtehwiot1@gmail.com"
msg['To'] = "jeremiaco@gmail.com"
msg['Subject'] = "prueba py"
 
# add in the message body
msg.attach(MIMEText(message, 'plain'))
 
#create server
server = smtplib.SMTP('smtp.gmail.com: 587')
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print "successfully sent email to %s:" % (msg['To'])
## para que esto funcione bien hay que permitir en la cuenta de google a usar el permiso para
## utilizar cuentas no seguras.
					### Fin Scrit ### 
