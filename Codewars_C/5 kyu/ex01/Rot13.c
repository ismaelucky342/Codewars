#include <stddef.h>
#include <stdlib.h>

char *rot13(const char *src)
{
    if (src == NULL) return NULL; // Handle null input

    size_t len = 0;
    while (src[len] != '\0') len++; // Calculate the length of the input string
    
    char *result = (char *)malloc(len + 1); // +1 for the null terminator
    if (result == NULL) return NULL; // Handle memory allocation failure

    for (size_t i = 0; i < len; i++) {
        char c = src[i];

        if (c >= 'a' && c <= 'z') {
            result[i] = ((c - 'a' + 13) % 26) + 'a'; // Shift by 13 positions in the alphabet
        }
        else if (c >= 'A' && c <= 'Z') {
            result[i] = ((c - 'A' + 13) % 26) + 'A'; // Shift by 13 positions in the alphabet
        }
        else {
            result[i] = c;
        }
    }

    result[len] = '\0'; // Null-terminate the output string
    return result;
}