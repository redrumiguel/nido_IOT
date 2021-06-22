/* --COPYRIGHT--,BSD
 * Copyright (c) 2017, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * --/COPYRIGHT--*/
//******************************************************************************
//!  MSP430FR4133 Demo - USCI_B0 I2C Master RX multiple bytes from MSP430 Slave
//!
//!  Description: This demo connects two MSP430's via the I2C bus. The master
//!  reads 5 bytes from the slave. This is the MASTER CODE. The data from the slave
//!  transmitter begins at 0 and increments with each transfer.
//!  The USCI_B0 RX interrupt is used to know when new data has been received.
//!  ACLK = n/a, MCLK = SMCLK = BRCLK =  DCO = ~1MHz
//!
//!                                /|\  /|\
//!               MSP430FR4133      10k  10k     MSP430FR4133
//!                   slave         |    |        master
//!             -----------------   |    |   -----------------
//!           -|XIN  P5.2/UCB0SDA|<-|----+->|P5.2/UCB0SDA  XIN|-
//!            |                 |  |       |                 | 32kHz
//!           -|XOUT             |  |       |             XOUT|-
//!            |     P5.3/UCB0SCL|<-+------>|P5.3/UCB0SCL     |
//!            |                 |          |             P1.0|--> LED
//!
//! This example uses the following peripherals and I/O signals.  You must
//! review these and change as needed for your own board:
//! - I2C peripheral
//! - GPIO Port peripheral (for I2C pins)
//! - SCL2
//! - SDA
//! - CS
//!
//! This example uses the following interrupt handlers.  To use this example
//! in your own application you must add these interrupt handlers to your
//! vector table.
//! - USCI_B0_VECTOR
//******************************************************************************
#include "driverlib.h"
#include<stdint.h>
#include "eusci_b_i2c_nido.h"
#include "Calendar.h"
#include "eusci_a_uart_general_main.h"



#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=USCI_B0_VECTOR
__interrupt
#elif defined(__GNUC__)
__attribute__((interrupt(USCI_B0_VECTOR)))
#endif
void USCIB0_ISR(void)
{
    static uint8_t count = 0;
    switch(__even_in_range(UCB0IV, USCI_I2C_UCBIT9IFG))
    {
        case USCI_NONE:             // No interrupts break;
            break;
        case USCI_I2C_UCALIFG:      // Arbitration lost
            break;
        case USCI_I2C_UCNACKIFG:    // NAK received (master only)
            EUSCI_B_I2C_masterReceiveStart(EUSCI_B0_BASE);
            EUSCI_B_I2C_clearInterrupt(EUSCI_B0_BASE,
                EUSCI_B_I2C_NAK_INTERRUPT
                );
            break;
        case USCI_I2C_UCSTTIFG:     // START condition detected with own address (slave mode only)
            break;
        case USCI_I2C_UCSTPIFG:     // STOP condition detected (master & slave mode)
            break;
        case USCI_I2C_UCRXIFG3:     // RXIFG3
            break;
        case USCI_I2C_UCTXIFG3:     // TXIFG3
            break;
        case USCI_I2C_UCRXIFG2:     // RXIFG2
            break;
        case USCI_I2C_UCTXIFG2:     // TXIFG2
            break;
        case USCI_I2C_UCRXIFG1:     // RXIFG1
            break;
        case USCI_I2C_UCTXIFG1:     // TXIFG1
            break;
        case USCI_I2C_UCRXIFG0:     // RXIFG0
            // Get RX data
            RXData_rtc[count++] = EUSCI_B_I2C_masterReceiveSingle(
                                    EUSCI_B0_BASE);

            EUSCI_B_I2C_clearInterrupt(EUSCI_B0_BASE,
                EUSCI_B_I2C_RECEIVE_INTERRUPT0
                );
            break; // Vector 24: RXIFG0 break;
        case USCI_I2C_UCTXIFG0:     // TXIFG0
            break;
        case USCI_I2C_UCBCNTIFG:    // Byte count limit reached (UCBxTBCNT)

            temp = (RXData_rtc [0] << 8 | RXData_rtc [1]) & 0xFFFC;
            count = 0;

            EUSCI_B_I2C_masterReceiveMultiByteFinish(EUSCI_B0_BASE);

            hora_fecha = RTC_C_getCalendarTime(RTC_C_BASE);
            pointer = save_temperatura(hora_fecha, pointer, temp);

             GPIO_setOutputLowOnPin(
                        GPIO_PORT_P7, sensor);
            sensor = 0;
            EUSCI_B_I2C_clearInterrupt(EUSCI_B0_BASE,
                EUSCI_B_I2C_BYTE_COUNTER_INTERRUPT
                );


            break;
        case USCI_I2C_UCCLTOIFG:    // Clock low timeout - clock held low too long
            break;
        case USCI_I2C_UCBIT9IFG:    // Generated on 9th bit of a transmit (for debugging)
            break;
        default:
            break;
    }
}



uint8_t dectobcd(const uint8_t val)
{
    return ((val / 10 * 16) + (val % 10));
}

uint8_t bcdtodec(const uint8_t val)
{
    return ((val / 16 * 10) + (val % 16));
}

uint8_t inp2toi(char *cmd, const uint16_t seek)
{
    uint8_t rv;
    rv = (cmd[seek] - 48) * 10 + cmd[seek + 1] - 48;
    return rv;
}


void init_i2c(){
    // Configure Pins for I2C
    /*
    * Select Port 5
    * Set Pin 2, 3 to input with function, (UCB0SIMO/UCB0SDA, UCB0SOMI/UCB0SCL).
    */
    GPIO_setAsPeripheralModuleFunctionInputPin(
        GPIO_PORT_P1,
        GPIO_PIN6 + GPIO_PIN7,
        GPIO_PRIMARY_MODULE_FUNCTION
    );

    //setup pin stemp_ext2 stemp_ext y stemp_int as output.
     GPIO_setAsOutputPin(
             GPIO_PORT_P7, GPIO_PIN0 +  GPIO_PIN1 + GPIO_PIN2);

     //set pin stemp_ext2 stemp_ext y stemp_int low. desactivo.
     GPIO_setOutputLowOnPin(
                 GPIO_PORT_P7, GPIO_PIN0 + GPIO_PIN1 + GPIO_PIN2);
     //GPIO_setOutputLowOnPin(
      //           GPIO_PORT_P7, GPIO_PIN0 + GPIO_PIN1 + GPIO_PIN2);

    /*
     * Disable the GPIO power-on default high-impedance mode to activate
     * previously configured port settings
     */
    PMM_unlockLPM5();

    EUSCI_B_I2C_initMasterParam param = {0};
    param.selectClockSource = EUSCI_B_I2C_CLOCKSOURCE_ACLK;
    param.i2cClk = CS_getACLK();
    param.dataRate = EUSCI_B_I2C_SET_DATA_RATE_400KBPS;
    param.byteCounterThreshold = RXCOUNT;
    param.autoSTOPGeneration = EUSCI_B_I2C_SEND_STOP_AUTOMATICALLY_ON_BYTECOUNT_THRESHOLD;
    EUSCI_B_I2C_initMaster(EUSCI_B0_BASE, &param);

    //Specify slave address
    EUSCI_B_I2C_setSlaveAddress(EUSCI_B0_BASE,
        HTU21D_I2C_ADDR
        );

    //Set Master in receive mode
    EUSCI_B_I2C_setMode(EUSCI_B0_BASE,
                        EUSCI_B_I2C_RECEIVE_MODE
        );

    //Enable I2C Module to start operations
    EUSCI_B_I2C_enable(EUSCI_B0_BASE);

    EUSCI_B_I2C_clearInterrupt(EUSCI_B0_BASE,
        EUSCI_B_I2C_RECEIVE_INTERRUPT0 +
        EUSCI_B_I2C_BYTE_COUNTER_INTERRUPT +
        EUSCI_B_I2C_NAK_INTERRUPT
        );

    //Enable master Receive interrupt
    EUSCI_B_I2C_enableInterrupt(EUSCI_B0_BASE,
        EUSCI_B_I2C_RECEIVE_INTERRUPT0 +
        EUSCI_B_I2C_BYTE_COUNTER_INTERRUPT +
        EUSCI_B_I2C_NAK_INTERRUPT
        );
}

uint8_t EUSCI_B_I2C_getSlaveAddress (uint16_t baseAddress)
{
    //Read the I2C RX slave address
    return ((HWREG16(baseAddress + OFS_UCBxADDRX) & ADDRESS_MASK));

}

bool start_temp_sensor(uint8_t pin){

    sensor |= (0x1 << pin);

    //set pin stemp_int. Activo.
    GPIO_setOutputHighOnPin
                (GPIO_PORT_P7, sensor);

    __delay_cycles(150000);

    if (EUSCI_B_I2C_masterSendSingleByteWithTimeout(EUSCI_B0_BASE, HTU21D_TEMP, EUSCI_B_I2C_TIMEOUT_34_MS)== STATUS_SUCCESS){

        EUSCI_B_I2C_masterReceiveStart(EUSCI_B0_BASE);
        return STATUS_SUCCESS;
    }
    else{

        GPIO_setOutputLowOnPin(
                    GPIO_PORT_P7, sensor);
        sensor = 0;
        return STATUS_FAIL;}

}





