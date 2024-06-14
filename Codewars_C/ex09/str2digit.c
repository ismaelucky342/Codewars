#include <stddef.h>
#include <inttypes.h>

void digitize(uint64_t n, uint8_t digits[], size_t *length_out)
{
    size_t length = 0;

    if (n == 0)
    {
        digits[length++] = 0;
    }
    else
    {
        while (n > 0)
        {
            digits[length++] = n % 10; // extract the last digit
            n /= 10;                   // remove the last digit from n
        }
    }
    *length_out = length;
}