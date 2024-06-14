#include <stdio.h>
#include <math.h>

int liters(double time)
{
    return(int)floor(time*0.5); //floor used to round result
}

int main()
{
    printf("%d\n", liters(3));
    printf("%d\n", liters(6.7));
    printf("%d\n", liters(11.8));
    return 0;
}