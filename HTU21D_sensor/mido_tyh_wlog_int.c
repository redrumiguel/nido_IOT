#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "HTU21D.h"
#include "wiringPII2C.h"
#include "wiringPI.h"

char *time_stamp(){

	char *timestamp = (char *)malloc(sizeof(char) * 16);
	time_t ltime;
	ltime=time(NULL);
	struct tm *tm;
	tm=localtime(&ltime);

	sprintf(timestamp,"%2.2d-%2.2d-%.4d %02d:%02d:%02d", tm->tm_mday, tm->tm_mon+1, tm->tm_year+1900, tm->tm_hour, tm->tm_min, tm->tm_sec);

	return timestamp;
}
char *fecha(){

        char *timestamp = (char *)malloc(sizeof(char) * 16);
        time_t ltime;
        ltime=time(NULL);
        struct tm *tm;
        tm=localtime(&ltime);

        sprintf(timestamp,"%2.2d-%2.2d-%.4d", tm->tm_mday, tm->tm_mon+1, tm->tm_year+1900);

        return timestamp;
}
int fd;
FILE *fp;
int main ()
{
	wiringPiSetup();
	fd = wiringPiI2CSetup(HTU21D_I2C_ADDR);
	char file_name[30];
	if ( 0 > fd )
	{
		fprintf (stderr, "Unable to open I2C device: %s\n", strerror (errno));
		exit (-1);
	}
	sprintf(file_name,"temperaturas-%s.txt",fecha());
	fp = fopen ( file_name, "a" );
	if (fp==NULL) 
		{fputs ("File error",stderr); 
		 exit (1);
	}else{
	fprintf(fp,"\n%s,",time_stamp());
	fprintf(fp," %5.1fC, ", getTemperature(fd));
	}
	fclose ( fp );


}
