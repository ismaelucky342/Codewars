#include <stddef.h>
#include <inttypes.h>

void digitize(uint64_t n, uint8_t digits[], size_t *len_out)
{
    size_t len = 0;

    if (n == 0)
    {
        digits[len++] = 0;
    }
    else
    {
        while (n > 0)
        {
            digits[len++] = n % 10; // extract the last digit
            n /= 10;                   // remove the last digit from n
        }
    }
    *len_out = len;
}