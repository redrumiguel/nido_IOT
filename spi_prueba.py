#! /usr/bin/python3
import spidev
import time

SPI_BUS = 1          # spidev1
SPI_SS  = 1          # spidev1.1
SPI_CLOCK = 100000  # 1 Mhz

# setup SPI
spi = spidev.SpiDev(SPI_BUS, SPI_SS)
spi.max_speed_hz = SPI_CLOCK

# transfer 2 bytes at a time, ^C to exit
try:
	"""    v = 0
    while True:
        send = [v, v+1]
        print("")
        print("TX:", send)
        print("RX:", spi.xfer(send))
        time.sleep(0.5)
        if v >= 254:
            v = 0
        else:
            v = (v+2)
	"""
	# values = spi.xfer3([<list of bytes to write>], <number of bytes to read>)
	readVals = spi.xfer3([0x9F], 3)
	print(readVals)

finally:
    spi.close()
