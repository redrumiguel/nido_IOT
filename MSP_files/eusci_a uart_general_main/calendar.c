#include "driverlib.h"
#include "calendar.h"
#include "eusci_b_i2c_nido.h"

uint16_t minutes;

void set_date_and_time(uint8_t * rxtrama, Calendar calendario){
    uint16_t year = ((year | dectobcd(rxtrama[6]) << 8)) & 0xFF00;
    year = year | dectobcd(rxtrama[7]);

    calendario.Seconds    = dectobcd(rxtrama[0]);
    calendario.Minutes    = dectobcd(rxtrama[1]);
    calendario.Hours      = dectobcd(rxtrama[2]);
    calendario.DayOfMonth = dectobcd(rxtrama[3]);
    calendario.DayOfWeek  = dectobcd(rxtrama[4]);
    calendario.Month      = dectobcd(rxtrama[5]);
    calendario.Year       = year;

    //Initialize Calendar Mode of RTC
    /*
     * Base Address of the RTC_A
     * Pass in current time, intialized above
     * Use BCD as Calendar Register Format
     */
    RTC_C_initCalendar(RTC_C_BASE,
        &calendario,
        RTC_C_FORMAT_BCD);


}

void set_alarm(uint8_t hora, uint8_t min){


     RTC_C_configureCalendarAlarmParam alarmas = {0};
     alarmas.minutesAlarm = min;
     alarmas.hoursAlarm = hora;
     alarmas.dayOfWeekAlarm = RTC_C_ALARMCONDITION_OFF;
     alarmas.dayOfMonthAlarm = RTC_C_ALARMCONDITION_OFF;
     RTC_C_configureCalendarAlarm(RTC_C_BASE, &alarmas);


}

void set_event(uint8_t evento){
    RTC_C_setCalendarEvent(RTC_C_BASE,
        evento);

     /*  uint8_t evento:
      *
      *  RTC_C_CALENDAREVENT_MINUTECHANGE
         RTC_C_CALENDAREVENT_HOURCHANGE
         RTC_C_CALENDAREVENT_NOON
         RTC_C_CALENDAREVENT_MIDNIGHT   */

    RTC_C_enableInterrupt(RTC_C_BASE,
        RTC_C_CLOCK_READ_READY_INTERRUPT +
        RTC_C_TIME_EVENT_INTERRUPT +
        RTC_C_CLOCK_ALARM_INTERRUPT);
    RTC_C_clearInterrupt(RTC_C_BASE,
     RTC_C_CLOCK_READ_READY_INTERRUPT +
     RTC_C_TIME_EVENT_INTERRUPT +
     RTC_C_CLOCK_ALARM_INTERRUPT);


}

#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=RTC_VECTOR
__interrupt
#elif defined(__GNUC__)
__attribute__((interrupt(RTC_VECTOR)))
#endif
void RTC_ISR (void)
{
        switch (__even_in_range(RTCIV, 16)) {
        case RTCIV_NONE: break;  //No interrupts
        case RTCIV_RTCOFIFG: break;  //RTCOFIFG
        case RTCIV_RTCRDYIFG:         //RTCRDYIFG
                //Toggle P1.0 every second
            //newTime = RTC_C_getCalendarTime(RTC_C_BASE);
                break;
        case RTCIV_RTCTEVIFG:         //RTCEVIFG  events
                //Interrupts every minute
                // realizar medidas de temperatura
                start_temp_sensor(2);
                newTime = RTC_C_getCalendarTime(RTC_C_BASE);

                minutes = RTC_C_convertBCDToBinary(RTC_C_BASE,newTime.Minutes);

                //Read out New Time a Minute Later BREAKPOINT HERE
                break;
        case RTCIV_RTCAIFG:         //RTCAIFG   alarms
                //Interrupts 5:00pm on 5th day of week
                //levantar la rpi.
                Act_RPI();
                rpi_action = SYNC;
                break;
        case RTCIV_RT0PSIFG: break; //RT0PSIFG
        case RTCIV_RT1PSIFG: break; //RT1PSIFG
        default: break;
    }
}
