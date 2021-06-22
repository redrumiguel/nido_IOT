#include "driverlib.h"
#include "string.h"
#include "stdio.h"
#include "eusci_b_i2c_nido.h"
#include "UART_RPI.h"
#include "UART_RFID.h"
#include "calendar.h"
#include "eusci_a_uart_general_main.h"

uint16_t temp_size;
uint32_t pointer = 0x5000;
uint32_t pointer_mov = 0x9000;

uint8_t rpi_action;

uint32_t temperature;
Calendar FechayHora;
uint32_t data;
uint8_t estado_main = FUERA;
uint8_t inputs = 0x00;
uint8_t num_aves = 0x00;
uint8_t id_nido = 0x00;
uint8_t prueba;
static uint8_t imagen;
uint32_t smclk, aclk;
const uint8_t transmit_data[]="Hello World. I'm UART Module of MSP430F5529 Microcontroller !!!\r\n";
const uint8_t trama_tx[] = {"\xFF\x10\x02\x17\xFF\x57\x38\x30\x37\x6D\x48\x10\x03\xAE"};
bool capturado = false;
bool innout;
extern uint8_t trama_rx[14];
uint8_t trama[] = {"\x10\x02\x17\xFF\x20\x00\x07\xC1\x21\x52\x10\x03\x7C"};

uint8_t tag_rfid[] = {"\x00\x07\xC1\x20\xE5"};


void main(void)

{
    //Stop Watchdog Timer
    WDT_A_hold(WDT_A_BASE);


    // LFXT Setup
    //Set PJ.4 and PJ.5 as Primary Module Function Input.
    /*

    * Select Port J
    * Set Pin 4, 5 to input Primary Module Function, LFXT.
    */
    GPIO_setAsPeripheralModuleFunctionInputPin(
        GPIO_PORT_PJ,
        GPIO_PIN4 + GPIO_PIN5,
        GPIO_PRIMARY_MODULE_FUNCTION
    );

    //Set DCO frequency to 1 MHz
    CS_setDCOFreq(CS_DCORSEL_0,CS_DCOFSEL_0);
    //Set external clock frequency to 32.768 KHz
    CS_setExternalClockSource(32768,0);
    //Set ACLK=LFXT
    CS_initClockSignal(CS_ACLK,CS_DCOCLK_SELECT,CS_CLOCK_DIVIDER_1);
    //Set SMCLK = DCO with frequency divider of 1
    CS_initClockSignal(CS_SMCLK,CS_LFXTCLK_SELECT,CS_CLOCK_DIVIDER_1);
    //Set MCLK = DCO with frequency divider of 1
    smclk = CS_getSMCLK();
    aclk = CS_getACLK();

    CS_initClockSignal(CS_MCLK,CS_DCOCLK_SELECT,CS_CLOCK_DIVIDER_1);
    //Start XT1 with no time out
    CS_turnOnLFXT(CS_LFXT_DRIVE_0); //PARAM POWER COMSUMPTION

    //Configure ID_MICROS pins
    GPIO_setAsInputPin(GPIO_PORT_P1, GPIO_PIN0 + GPIO_PIN1 + GPIO_PIN2 + GPIO_PIN3);
    GPIO_setAsInputPin(GPIO_PORT_P9, GPIO_PIN4 + GPIO_PIN5 + GPIO_PIN6 + GPIO_PIN7);
    //Configure Pulsadores ext pins
    GPIO_setAsInputPinWithPullUpResistor(GPIO_PORT_P3, GPIO_PIN3);
    //Configure Pulsadores ext pins
    GPIO_setAsInputPinWithPullUpResistor(GPIO_PORT_P1, GPIO_PIN5);


    id_nido = ((!GPIO_getInputPinValue(GPIO_PORT_P9, GPIO_PIN7) << 0) | (!GPIO_getInputPinValue(GPIO_PORT_P9, GPIO_PIN6) << 1)
            | (!GPIO_getInputPinValue(GPIO_PORT_P9, GPIO_PIN5) << 2) | (!GPIO_getInputPinValue(GPIO_PORT_P9, GPIO_PIN4) << 3)
            | (!GPIO_getInputPinValue(GPIO_PORT_P1, GPIO_PIN0) << 4) | (!GPIO_getInputPinValue(GPIO_PORT_P1, GPIO_PIN1) << 5)
            | (!GPIO_getInputPinValue(GPIO_PORT_P1, GPIO_PIN2) << 6) | (!GPIO_getInputPinValue(GPIO_PORT_P1, GPIO_PIN3) << 7));

    //setup pin ena_rpi as output.
    GPIO_setAsOutputPin(
            GPIO_PORT_P1, GPIO_PIN4);


    //setup pulsador manual RPI as input

    GPIO_setAsInputPinWithPullUpResistor(GPIO_PORT_P2, GPIO_PIN0);
    GPIO_selectInterruptEdge( GPIO_PORT_P2, GPIO_PIN0, GPIO_HIGH_TO_LOW_TRANSITION);
    GPIO_enableInterrupt(GPIO_PORT_P2, GPIO_PIN0);
    GPIO_clearInterrupt(GPIO_PORT_P2, GPIO_PIN0);

    // setup interrupcion rpi ready.
    GPIO_setAsInputPinWithPullUpResistor(GPIO_PORT_P3, GPIO_PIN1);
    GPIO_selectInterruptEdge( GPIO_PORT_P3, GPIO_PIN1, GPIO_HIGH_TO_LOW_TRANSITION); //rpi encendida y ready
    GPIO_enableInterrupt(GPIO_PORT_P3, GPIO_PIN1);
    GPIO_clearInterrupt(GPIO_PORT_P3, GPIO_PIN1);

    //RPI No activa
    Des_RPI();

    init_uart_rpi();

    init_uart_rfid();

    // Configura periferico i2c en modo master.
    init_i2c();

    RTC_C_setTemperatureCompensation(RTC_C_BASE,RTC_C_COMPENSATION_UP1PPM,20);
    set_alarm(3, 30);
    set_event(RTC_C_CALENDAREVENT_MINUTECHANGE);

    //Start RTC Clock
    RTC_C_startClock(RTC_C_BASE);
    /*
     * Disable the GPIO power-on default high-impedance mode to activate
     * previously configured port settings
     */
    PMM_unlockLPM5();

    // Enable global interrupts
    __enable_interrupt();
    //For debugger
    __no_operation();

    Act_RPI();
    rpi_action = INIT;


    send_UART_data(COMMAND_INIT);

    __delay_cycles(300000);

    // leo fecha y hora
    //FechayHora = RTC_C_getCalendarTime(RTC_C_BASE);
    //capturo?? con un delay
   // capturado = buscar_capturado(Acciones, len_Acciones, tag_rfid, FechayHora, &imagen);
   // pointer_mov = save_movimiento(FechayHora, trama, pointer_mov, capturado, innout);

   // send_UART_data(COMMAND_SYNC);

 // quizas delay

    while (1){

        switch(__even_in_range(estado_main,NUM_ESTADOS)){

            case FUERA:

                if (inputs >> 0 & 1){
                    inputs = inputs & 0xFC;;
                    //activo RFID
                    Act_RFID();

                    estado_main =  ENTRANDO;

                }
                else if (inputs >> 1 & 1 && num_aves > 0){
                    inputs = inputs & 0xFC;
                    //activo RFID
                    Act_RFID();

                    estado_main =  SALIENDO;

                }
                __bis_SR_register(CPUOFF+GIE);
                break;

            case ENTRANDO:

                if (inputs >> 1 & 1){
                    inputs = inputs & 0xFC;
                    //Disable RFID
                    Des_RFID();

                    innout = ENTRA;

                    // leo fecha y hora
                    FechayHora = RTC_C_getCalendarTime(RTC_C_BASE);
                    //capturo?? con un delay
                    capturado = buscar_capturado(Acciones, len_Acciones, tag_rfid, FechayHora, &imagen);
                    pointer_mov = save_movimiento(FechayHora, trama_rx, pointer_mov, capturado, innout);

                    if (capturado){
                        Act_RPI();
                        rpi_action = CAPTURE;
                    }
                    num_aves++;
                    estado_main = DENTRO;
                }
                else if (inputs >> 0 & 1){

                    inputs = inputs & 0xFC;;
                    estado_main =  FUERA;
                }
                __bis_SR_register(CPUOFF+GIE);
                break;

            case DENTRO:
                if (inputs >> 1 & 1){
                    inputs = inputs & 0xFC;;
                    //activo RFID
                    Act_RFID();
                    estado_main = SALIENDO;
                }
                else if (inputs >> 0 & 1){
                    inputs = inputs & 0xFC;;
                    //activo RFID
                    Act_RFID();
                    estado_main = ENTRANDO;
                }
                __bis_SR_register(CPUOFF+GIE);
                break;

            case SALIENDO:

                if (inputs >> 0 & 1){
                    inputs = inputs & 0xFC;;
                    //Disable RFID
                    Des_RFID();

                    innout = SALE;
                    // leo fecha y hora
                    FechayHora = RTC_C_getCalendarTime(RTC_C_BASE);

                    pointer_mov = save_movimiento(FechayHora, trama_rx, pointer_mov, capturado, innout);

                    num_aves--;
                    estado_main = FUERA;
                }
                else if (inputs >> 1 & 1){

                    inputs = inputs & 0xFC;;

                    estado_main =  DENTRO;
                }
                __bis_SR_register(CPUOFF+GIE);
                break;

        }
        __bis_SR_register(CPUOFF+GIE);
    }
}

//******************************************************************************
//
//This is the Port2 interrupt vector service routine.
//
//******************************************************************************
#pragma vector=PORT2_VECTOR
__interrupt

void P2_ISR(void)
{
    //rutina antirrebotes

    switch(__even_in_range(P2IV,P2IV_P2IFG7))
        {
        case P2IV_P2IFG0: //pulsador manual RPI
            GPIO_clearInterrupt( GPIO_PORT_P2, GPIO_PIN0);
            Act_RPI();
            rpi_action = TEST;
            break;
        case P2IV_P2IFG2: //interruptor interior
            GPIO_clearInterrupt( GPIO_PORT_P2, GPIO_PIN2);
            if (~inputs >> 1 & 1)
                inputs = inputs | 0x02;

            __delay_cycles(2000);
            break;
        case P2IV_P2IFG3: //interruptor exterior
            GPIO_clearInterrupt( GPIO_PORT_P2, GPIO_PIN3);
            if (~inputs >> 0 & 1)
                inputs = inputs | 0x01;

            __delay_cycles(2000);


            break;
        }
        __bic_SR_register_on_exit(LPM0_bits);
}

//******************************************************************************
//
//This is the Port2 interrupt vector service routine.
//
//******************************************************************************
#pragma vector=PORT3_VECTOR
__interrupt

void P3_ISR(void)
{
    switch(__even_in_range(P3IV,P3IV_P3IFG7))
        {
            case P3IV_P3IFG1: // RPI ON&Ready
                GPIO_clearInterrupt( GPIO_PORT_P3, GPIO_PIN1);

                static uint16_t reg;

                reg = P3IES & 0x0002;

                if (reg > 0)
                {
                    switch(__even_in_range(rpi_action,8))
                    {
                        case INIT:

                            send_UART_data(COMMAND_INIT);
                            GPIO_selectInterruptEdge( GPIO_PORT_P3, GPIO_PIN1, GPIO_LOW_TO_HIGH_TRANSITION);
                            break;
                        case CAPTURE:
                            send_UART_data(COMMAND_CAPT);
                            GPIO_selectInterruptEdge( GPIO_PORT_P3, GPIO_PIN1, GPIO_LOW_TO_HIGH_TRANSITION);
                            break;
                        case SYNC:
                            send_UART_data(COMMAND_SYNC);
                            GPIO_selectInterruptEdge( GPIO_PORT_P3, GPIO_PIN1, GPIO_LOW_TO_HIGH_TRANSITION);
                            break;
                        case TEST:
                            send_UART_data(COMMAND_TEST);
                            GPIO_selectInterruptEdge( GPIO_PORT_P3, GPIO_PIN1, GPIO_LOW_TO_HIGH_TRANSITION);
                            break;
                    }
                    GPIO_selectInterruptEdge( GPIO_PORT_P3, GPIO_PIN1, GPIO_LOW_TO_HIGH_TRANSITION);
               }
                else
                {
                    __delay_cycles(3000000);
                    Des_RPI();
                    GPIO_selectInterruptEdge( GPIO_PORT_P3, GPIO_PIN1, GPIO_HIGH_TO_LOW_TRANSITION);
                }
            break;
        }

}



uint32_t save_movimiento(Calendar calendario, uint8_t* trama, uint32_t address,bool capt, bool dir)
{
    uint8_t state_capt = (capt & 0x0F) << 4;
    state_capt = state_capt | (dir & 0xF);
    FRAMCtl_write8(&calendario.Hours, (uint8_t *) address,1);
    FRAMCtl_write8(&calendario.Minutes, (uint8_t *) address + 1,1);
    FRAMCtl_write8(trama + 5, (uint8_t *) address+2,5);
    FRAMCtl_write8(&state_capt, (uint8_t *) address+7,1);
    return (uint32_t) address + 8;

}

uint32_t save_temperatura(Calendar calendario, uint32_t address, uint16_t temperatura){

    data  = 0x00000000;
    //data = (calendario.Hours << 24) | (calendario.Minutes << 16) | temperatura;
    //data = (calendario.Minutes << 7) | (calendario.Hours << 15);
    data = data | (calendario.Hours << 8);
    data = data << 8;
    data = data | (calendario.Minutes << 8);
    data = data << 8;
    data = data | temperatura;
    FRAMCtl_fillMemory32(data, (uint32_t *) (uintptr_t)address, 1);
    return (uint32_t) address + 4;

}


void Des_RPI(){
    GPIO_setOutputLowOnPin(
            GPIO_PORT_P1, GPIO_PIN4);
}
void Act_RPI(){
    GPIO_setOutputHighOnPin(
            GPIO_PORT_P1, GPIO_PIN4);
}

bool buscar_capturado(uint8_t * acciones, uint16_t tam, uint8_t * buscado, Calendar calendario, uint8_t * grafico){
bool capturar = false;
uint8_t sub_tramas[10];
uint8_t hora_ini, hora_fin, min_ini, min_fin;
uint16_t inicial, actual, final, i, j, cont;
cont = 1;
j = 0;
for (i = 0; i < tam; i++){

    if (cont % 10 == 0){
        sub_tramas[j++] = acciones[i];
        j = 0;
        // comparo
        if (memcmp(sub_tramas, buscado, 5) == 0){
            hora_ini = sub_tramas[5];
            min_ini = sub_tramas[6];
            hora_fin = sub_tramas[7];
            min_fin = sub_tramas[8];
            inicial = (hora_ini << 8) + min_ini;
            final = (hora_fin << 8) + min_fin;
            actual = (calendario.Hours << 8) | calendario.Minutes;

            if (sub_tramas[9] & 0x10){ //capturar

                if (final > inicial){
                    if ((final > actual)&&(actual > inicial)){
                        *grafico = (sub_tramas[9] & 0xF);
                        capturar = true;
                    }
                    else
                        capturar =  false;
                }   //final > actual > inicial --> rango captura
                else{ //inicial > final
                          //eje: ini: 21h, fin:4h actual: 2h    eje: ini:20h , fin: 4h actual: 23 horas
                    if ((final > actual)&&(actual < inicial)||(final < actual)&&(actual > inicial)){
                        //capturo
                        *grafico = sub_tramas[9];
                        capturar =  true;
                    }
                    else
                        capturar = false;
                }
            }
        }
    }
    else
        sub_tramas[j++] = acciones[i];

    cont++;
}

return capturar;

}


