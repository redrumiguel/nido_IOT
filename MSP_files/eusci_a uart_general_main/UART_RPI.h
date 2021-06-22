
#ifndef UART_RPI_H
#define UART_RPI_H

#include "driverlib.h"

#define FIRST_BYTE 0x00
#define GET_TIME_DATE 0x01
#define GET_ACCIONES 0x02
#define SECOND_BYTE 0x01
#define SEND_TEMPERATURAS 0x03
#define SEND_MOVIMIENTOS 0x04

uint8_t RXData;
uint8_t i, k;
uint16_t len_Acciones, l, t;
extern uint8_t estado_main;
extern uint32_t  pointer, pointer_mov;
uint8_t RXTrama[8];
uint8_t Acciones_2b[2];
uint8_t Acciones[512];

void init_uart_rpi(void);
void send_UART_data(uint8_t command);


#endif
