CC=gcc
CFLAGS=-I. -Wall
DEPS = 
OBJ = HTU21D.o mido_tyh_wlog_int.o
EXTRA_LIBS=-lwiringPi

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

mido_tyh_wlog_int: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(EXTRA_LIBS)

.PHONY: clean

clean:
	rm -f HTU21D $(OBJ) 
