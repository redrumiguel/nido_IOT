#include "eusci_a_uart_general_main.h"

#ifndef CALENDAR_H
#define CALENDAR_H




Calendar newTime;

extern uint8_t rpi_action;
extern void Act_RPI();

void set_date_and_time(uint8_t * rxtrama, Calendar calendario);
void set_alarm(uint8_t hora, uint8_t min);
void set_event(uint8_t evento);



#endif
