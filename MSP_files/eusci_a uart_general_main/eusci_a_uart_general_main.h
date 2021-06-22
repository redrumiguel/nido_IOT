#ifndef EUSCI_A_UART_GENERAL_MAIN_H
#define EUSCI_A_UART_GENERAL_MAIN_H

#include "driverlib.h"


#define FUERA 0x00
#define ENTRANDO 0x01
#define DENTRO 0x02
#define SALIENDO 0x03

#define COMMAND_INIT 0x0A
#define COMMAND_CAPT 0x0B
#define COMMAND_SYNC 0x0C
#define COMMAND_TEST 0x0D

#define SEND_DATA_MOV 0x05

#define INIT 0x01
#define CAPTURE 0x02
#define SYNC 0x04
#define TEST 0x08



#define NUM_ESTADOS 0x06

#define ENTRA 1
#define SALE  0

#define FRAM_TEMP_START (uint32_t) 0x5000
#define FRAM_MOV_START (uint32_t) 0x9000





void Act_RPI();
void Des_RPI();

extern uint8_t Acciones[512];
extern uint16_t len_Acciones;


uint32_t save_temperatura(Calendar calendario, uint32_t  address, uint16_t temperatura);
uint32_t save_movimiento(Calendar calendario, uint8_t* trama, uint32_t address,bool capt, bool dir);
bool buscar_capturado(uint8_t * acciones, uint16_t tam, uint8_t * buscado, Calendar calendario, uint8_t * grafico);

#endif
