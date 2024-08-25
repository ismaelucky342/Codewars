#include <stdio.h>

char *human_readable_time(unsigned seconds, char *time_string) {
    unsigned int hours = seconds / 3600;
    unsigned int minutes = (seconds % 3600) / 60;
    unsigned int secs = seconds % 60;

    // Format the time string as HH:MM:SS
    sprintf(time_string, "%02u:%02u:%02u", hours, minutes, secs);

    return time_string;
}