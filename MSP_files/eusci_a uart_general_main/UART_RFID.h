#ifndef UART_RFID_H
#define UART_RFID_H

#include "driverlib.h"

#define GET_TRAMA 0x01
#define POOLING_TRAMA 0x00



uint8_t trama_rx[14];
uint8_t tag_RFID[];

void init_uart_rfid();
void Des_RFID();
void Act_RFID();

#endif
