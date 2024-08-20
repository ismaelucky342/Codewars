#include <stdbool.h>
#include <stdio.h>

bool zero_fuel(double distance_to_pump, double mpg, double fuel_left)
{   
    if (distance_to_pump <= fuel_left*mpg)
    {
        return true;
    }
    return false;
}

int main(zero_fuel, should_pass_example_tests)
{
    printf(50, 25, 2, true);
    printf(60, 30, 3, true);
    printf(70, 25, 1, false);
    printf(100, 25, 3, false);
}
