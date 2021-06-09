#!/usr/bin/python3

import subprocess
PATRONFINAL = 15
ID_TRAMA = 2
## Funcoon para lectura de archivo de acciones del cliente. Devuelve si hay que capturar el ave.
def leer_file():
        proc_find = subprocess.Popen(["find", "-iname", 'Acciones.inst'], stdout=subprocess.PIPE) 
        file, filerror = proc_find.communicate()
        file1 = open(file[0:len(file)-1], "r")
        #file1 = open('Acciones.inst')
        lineas = file1.readlines()
        file1.close()
        indice = 0
        cadena = ""
        trama = []
        x = 2
        for j, item in enumerate(lineas,0):
                if not '#' in item:
                        list_item = item.split(', ')
                        #cadena += (item[0:10]+item[22:27]+item[29:34]).replace(':','')
                        cadena += (list_item[0]+list_item[2].replace(':','')+list_item[3]).replace(':','')
                        #if 'capturar' in item:
                        if 'No_capturar' in list_item[1]:
                                cadena += '0'
                        else:
                                cadena += '1'
                        #if 'imagen' in item:
                        if 'No_imagen' in list_item[4]:
                                cadena += '0'
                        else:
                                cadena += '1'

        newlist = [cadena[i: i + x] for i in range(0, len(cadena), x)]
        print (newlist)
        for j in range(0,len(newlist)):
                newlist[j] = int(newlist[j],16)
        len_newlist = len(newlist)
        if len_newlist > 255:
            byte0 = (len_newlist/256)   
            byte1 = (len_newlist%256)
            newlist.insert(0,int(byte1))
            newlist.insert(0,int(byte0))
        else:
            newlist.insert(0,len(newlist))

        newlist.insert(0,ID_TRAMA)
        newlist.append(PATRONFINAL)
        print (newlist)
        return bytearray(newlist)

#print(leer_file())
