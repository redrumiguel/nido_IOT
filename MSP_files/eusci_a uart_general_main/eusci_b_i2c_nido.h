#ifndef EUSCI_B_I2C_MAIN_H
#define EUSCI_B_I2C_MAIN_H

#include "driverlib.h"

#define HTU21D_I2C_ADDR 0x40

//*****************************************************************************
//
//Specify HTU21D TEMP REGISTER.
//
//*****************************************************************************

#define   HTU21D_TEMP     0xF3


#define HTU21_RESET_COMMAND                                 0xFE

//*****************************************************************************
//
//Specify Expected Receive data count.
//
//*****************************************************************************
#define RXCOUNT 4



//*****************************************************************************
//
//Target frequency for SMCLK in kHz
//
//*****************************************************************************
#define CS_SMCLK_DESIRED_FREQUENCY_IN_KHZ   1000

//*****************************************************************************
//
//SMCLK/FLLRef Ratio
//
//*****************************************************************************
#define CS_SMCLK_FLLREF_RATIO   30

#define ADDRESS_MASK 0x7F


 uint8_t RXData_rtc[RXCOUNT];
 extern void init_i2c (void);
 extern uint8_t dectobcd (const uint8_t val);
 extern uint8_t bcdtodec (const uint8_t val);
 extern uint8_t inp2toi (char *cmd, const uint16_t seek);
 extern uint32_t save_temperatura(Calendar calendario, uint32_t address, uint16_t temperatura);
 extern uint32_t pointer ;
 bool start_temp_sensor(uint8_t pin);
 uint8_t EUSCI_B_I2C_getSlaveAddress (uint16_t baseAddress);
 unsigned int temp;
 uint8_t sensor;
 Calendar hora_fecha;




#endif
