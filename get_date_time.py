#!/usr/bin/python

from datetime import datetime
import serial
ser = serial.Serial('/dev/ttyS0',baudrate = 9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout = 5)
def get_datetime():
        now = datetime.now() # current date and time
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        min = now.strftime("%M")
        sec = now.strftime("%S")
        trama1 = bytearray([int(sec),int(min),int(hour),int(day),int(month),int(year[0:2]),int(year[2:4])])
        return trama1

ser.write(get_datetime())
