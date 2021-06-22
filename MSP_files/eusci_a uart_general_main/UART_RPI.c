/*
 * uart_A.c
 *
 *  Created on: 14 abr. 2021
 *      Author: miguelredruello
 */

#include "UART_RPI.h"
#include "driverlib.h"
#include "calendar.h"
#include "eusci_a_uart_general_main.h"


uint8_t uart_A0_modo_rx = FIRST_BYTE;
uint8_t uart_A0_modo_tx = FIRST_BYTE;
uint16_t valor[400];
uint16_t size_temp;
uint8_t size_mov;
uint8_t * posi[41];

extern Calendar newTime;

void init_uart_rpi(void){

    GPIO_setAsPeripheralModuleFunctionInputPin(
            GPIO_PORT_P4,
            GPIO_PIN2 + GPIO_PIN3,
            GPIO_PRIMARY_MODULE_FUNCTION
    );

    // Configure UART
    EUSCI_A_UART_initParam param = {0};
    param.selectClockSource = EUSCI_A_UART_CLOCKSOURCE_SMCLK;
    param.clockPrescalar = 3;  //52
    param.firstModReg = 0;  //1
    param.secondModReg = 146;  //73
    param.parity = EUSCI_A_UART_NO_PARITY;
    param.msborLsbFirst = EUSCI_A_UART_LSB_FIRST;
    param.numberofStopBits = EUSCI_A_UART_ONE_STOP_BIT;
    param.uartMode = EUSCI_A_UART_MODE;
    param.overSampling = EUSCI_A_UART_LOW_FREQUENCY_BAUDRATE_GENERATION;  //EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION

    if (STATUS_FAIL == EUSCI_A_UART_init(EUSCI_A0_BASE, &param)) {
        return;
    }

    EUSCI_A_UART_enable(EUSCI_A0_BASE);

    EUSCI_A_UART_clearInterrupt(EUSCI_A0_BASE,
      EUSCI_A_UART_RECEIVE_INTERRUPT );

    // Enable USCI_A0 RX interrupt
    EUSCI_A_UART_enableInterrupt(EUSCI_A0_BASE,
      EUSCI_A_UART_RECEIVE_INTERRUPT );                     // Enable interrupt


}

void send_UART_data(uint8_t command){

    EUSCI_A_UART_transmitData(EUSCI_A0_BASE, command);
   // while(EUSCI_A_UART_queryStatusFlags(EUSCI_A0_BASE,EUSCI_A_UART_BUSY)==EUSCI_A_UART_BUSY);

}


//******************************************************************************
//
//This is the USCI_A0 interrupt vector service routine.
//
//******************************************************************************
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=USCI_A0_VECTOR
__interrupt
#elif defined(__GNUC__)
__attribute__((interrupt(USCI_A0_VECTOR)))
#endif
void USCI_A0_ISR(void)
{


    switch(__even_in_range(UCA0IV,USCI_UART_UCTXCPTIFG))
  {

    case USCI_NONE: break;
    case USCI_UART_UCRXIFG:
      switch (uart_A0_modo_rx)
      {
          case FIRST_BYTE:
              RXData = EUSCI_A_UART_receiveData(EUSCI_A0_BASE);
              i = 0;
              k = 0;
              l = 0;
              if (RXData == GET_TIME_DATE)

                  uart_A0_modo_rx = GET_TIME_DATE;
              else if (RXData == GET_ACCIONES)

                  uart_A0_modo_rx = GET_ACCIONES;
              else if (RXData == SEND_TEMPERATURAS)
              {
                  size_temp = pointer - FRAM_TEMP_START;

                  newTime = RTC_C_getCalendarTime(RTC_C_BASE);

                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) size_temp);
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) (size_temp >> 8));

                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) newTime.DayOfMonth);
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) newTime.Month);
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) (newTime.Year >> 8));
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) newTime.Year);

                  EUSCI_A_UART_enableInterrupt(EUSCI_A0_BASE,
                   EUSCI_A_UART_TRANSMIT_INTERRUPT);

                  EUSCI_A_UART_clearInterrupt(EUSCI_A0_BASE,
                    EUSCI_A_UART_TRANSMIT_INTERRUPT);
                  t = 0;
                  uart_A0_modo_tx = SEND_TEMPERATURAS;
              }

              else
                  size_mov = pointer - FRAM_MOV_START;

                  newTime = RTC_C_getCalendarTime(RTC_C_BASE);
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) size_mov);
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) newTime.DayOfMonth);
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) newTime.Month);
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) (newTime.Year >> 8));
                  EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t) newTime.Year);
                  EUSCI_A_UART_enableInterrupt(EUSCI_A0_BASE,
                     EUSCI_A_UART_TRANSMIT_INTERRUPT);

                    EUSCI_A_UART_clearInterrupt(EUSCI_A0_BASE,
                      EUSCI_A_UART_TRANSMIT_INTERRUPT);
                  s = 0;
                  uart_A0_modo_tx = SEND_MOVIMIENTOS;


                break;

          case GET_TIME_DATE:
              if (i >= 8){
                 RTC_C_holdClock(RTC_C_BASE);
                 set_date_and_time(RXTrama,newTime);
                 RTC_C_startClock(RTC_C_BASE);
                 uart_A0_modo_rx = FIRST_BYTE;
          //       send_UART_data(COMMAND_SYNC);
              }
              else
                  RXTrama[i++] = EUSCI_A_UART_receiveData(EUSCI_A0_BASE);
                break;
          case GET_ACCIONES:
              if (k > 1){
                  len_Acciones = (Acciones_2b[0] << 8) + Acciones_2b[1];
                  if (k > len_Acciones + 1){
                      uart_A0_modo_rx = FIRST_BYTE;
                      //Des_RPI();
                      // guardar fichero en ram
                  }
                  else
                      Acciones[l++] = EUSCI_A_UART_receiveData(EUSCI_A0_BASE);

              }
              else{
                  Acciones_2b[0] = Acciones_2b[1];
                  Acciones_2b[1] = EUSCI_A_UART_receiveData(EUSCI_A0_BASE);
                  k++;
              }
                break;
      }

      EUSCI_A_UART_clearInterrupt(EUSCI_A0_BASE,EUSCI_A_UART_RECEIVE_INTERRUPT);
              // __bic_SR_register_on_exit(CPUOFF); // Exit LPM0
      break;

    case USCI_UART_UCTXIFG:

        switch (uart_A0_modo_tx)
        {

        case SEND_TEMPERATURAS:
        {
            if (t < size_temp){
               // valor[t] =  (uint16_t) (FRAM_TEMP_START+t);
                EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t)*((uint16_t *)(FRAM_TEMP_START+t)));
                t++;
            }
            else
                uart_A0_modo_tx = FIRST_BYTE;


              break;
        }
        case SEND_MOVIMIENTOS:
            if (s < size_mov){
               // valor[t] =  (uint16_t) (FRAM_TEMP_START+t);
                EUSCI_A_UART_transmitData(EUSCI_A0_BASE, (uint8_t)*((uint16_t *)(FRAM_MOV_START+t)));
                s++;
            }
            else
                uart_A0_modo_tx = FIRST_BYTE;


              break;

        }

        EUSCI_A_UART_clearInterrupt(EUSCI_A0_BASE,EUSCI_A_UART_TRANSMIT_INTERRUPT);


      break;
    case USCI_UART_UCSTTIFG: break;
    case USCI_UART_UCTXCPTIFG: break;
  }
}
