/*
 * UART_RFID.C
 *
 *  Created on: 14 abr. 2021
 *      Author: miguelredruello
 */

#include "driverlib.h"
#include "UART_RFID.h"
#include "string.h"

uint8_t estado_trama = 0;
uint8_t j = 2;

void init_uart_rfid(){

    GPIO_setAsPeripheralModuleFunctionInputPin(
            GPIO_PORT_P3,
            GPIO_PIN4 + GPIO_PIN5,
            GPIO_PRIMARY_MODULE_FUNCTION
    );

    GPIO_setAsOutputPin(
            GPIO_PORT_P2, GPIO_PIN1);



    //Configure UART
    //SMCLK = 1,048MHz, Baudrate = 9600
    //UCBRx = 8, UCBRFx = 0, UCBRSx = 0xD6, UCOS16 = 0
    // http://software-dl.ti.com/msp430/msp430_public_sw/mcu/msp430/MSP430BaudRateConverter/index.html
    // calculo de valoes para baudrate
    // Configure UART
    EUSCI_A_UART_initParam paramemtros = {0};
    paramemtros.selectClockSource = EUSCI_A_UART_CLOCKSOURCE_ACLK;
    paramemtros.clockPrescalar = 6;  //3
    paramemtros.firstModReg = 8;  //0
    paramemtros.secondModReg = 0;  //146
    paramemtros.parity = EUSCI_A_UART_NO_PARITY;
    paramemtros.msborLsbFirst = EUSCI_A_UART_LSB_FIRST;
    paramemtros.numberofStopBits = EUSCI_A_UART_ONE_STOP_BIT;
    paramemtros.uartMode = EUSCI_A_UART_MODE;
    paramemtros.overSampling = EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION; //0

    if (STATUS_FAIL == EUSCI_A_UART_init(EUSCI_A1_BASE, &paramemtros)) {
        return;
    }

    EUSCI_A_UART_enable(EUSCI_A1_BASE);

    EUSCI_A_UART_clearInterrupt(EUSCI_A1_BASE,
      EUSCI_A_UART_RECEIVE_INTERRUPT);

    // Enable USCI_A0 RX interrupt
    EUSCI_A_UART_enableInterrupt(EUSCI_A1_BASE,
      EUSCI_A_UART_RECEIVE_INTERRUPT);                     // Enable interrupt


}


//******************************************************************************
//
//This is the USCI_A0 interrupt vector service routine.
//
//******************************************************************************
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=USCI_A1_VECTOR
__interrupt
#elif defined(__GNUC__)
__attribute__((interrupt(USCI_A1_VECTOR)))
#endif
void USCI_A1_ISR(void)
{
  switch(__even_in_range(UCA1IV,USCI_UART_UCTXCPTIFG))
  {
    case USCI_NONE: break;
    case USCI_UART_UCRXIFG:
        switch(estado_trama)
         {
             case POOLING_TRAMA:
                 trama_rx[0] = trama_rx[1];
                 trama_rx[1] = EUSCI_A_UART_receiveData(EUSCI_A1_BASE);
                 if (trama_rx[0] == '\x10' && trama_rx[1] == '\x02' )
                 {
                     estado_trama = GET_TRAMA;
                 }
                 break;

             case GET_TRAMA:
                 if (trama_rx[j-2] == '\x10' && trama_rx[j-1] == '\x03')
                 {
                 trama_rx[j++] = EUSCI_A_UART_receiveData(EUSCI_A1_BASE);
                 j = 2;
                 estado_trama = POOLING_TRAMA;
                 //strcpy (tag_RFID, (trama_rx + 6));
                 //fin
                 // me despierto

                 }
                 else

                 trama_rx[j++] = EUSCI_A_UART_receiveData(EUSCI_A1_BASE);

                 break;
         }

         // Check value
         EUSCI_A_UART_clearInterrupt(EUSCI_A1_BASE,EUSCI_A_UART_RECEIVE_INTERRUPT);
        // __bic_SR_register_on_exit(CPUOFF); // Exit LPM0
         break;
    case USCI_UART_UCTXIFG: break;
    case USCI_UART_UCSTTIFG: break;
    case USCI_UART_UCTXCPTIFG: break;
  }
}

void Act_RFID(){
    GPIO_setOutputHighOnPin(
            GPIO_PORT_P2, GPIO_PIN1);
    // CLear USCI_A0 RX interrupt
    EUSCI_A_UART_clearInterrupt(EUSCI_A0_BASE,
       EUSCI_A_UART_RECEIVE_INTERRUPT);

   // Enable USCI_A0 RX interrupt
    EUSCI_A_UART_enableInterrupt(EUSCI_A0_BASE,
       EUSCI_A_UART_RECEIVE_INTERRUPT);

}

void Des_RFID(){
    GPIO_setOutputLowOnPin(
            GPIO_PORT_P2, GPIO_PIN1);
    // Disable USCI_A0 RX interrupt
    EUSCI_A_UART_disableInterrupt(EUSCI_A0_BASE,
               EUSCI_A_UART_RECEIVE_INTERRUPT);

}
