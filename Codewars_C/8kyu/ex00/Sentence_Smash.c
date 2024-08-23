#include <stdlib.h>
#include <string.h>
#include <stdio.h>

char *smash(const char *const words[], size_t count)
{
    if (count == 0)
    {
        // If there are no words, return an empty string
        char *empty = (char *)malloc(1);
        if (empty == NULL)
        {
            return NULL; // Handle allocation failure
        }
        empty[0] = '\0';
        return empty;
    }

    // Calculate the total len needed
    size_t total_len = 0;
    for (size_t i = 0; i < count; ++i)
    {
        total_len += strlen(words[i]);
    }
    total_len += (count - 1); // Add spaces between words

    // Allocate memory for the resulting string
    char *result = (char *)malloc(total_len + 1); // +1 for the null terminator
    if (result == NULL)
    {
        return NULL; // Handle allocation failure
    }

    // Concatenate the words with spaces
    result[0] = '\0'; // Start with an empty string
    for (size_t i = 0; i < count; ++i)
    {
        strcat(result, words[i]);
        if (i < count - 1)
        {
            strcat(result, " ");
        }
    }

    return result;
}

int main()
{
    const char *words[] = {"hello", "world", "this", "is", "great"};
    size_t count = sizeof(words) / sizeof(words[0]);
    char *sentence = smash(words, count);

    if (sentence)
    {
        printf("%s\n", sentence);
        free(sentence);
    }
    else
    {
        printf("Memory allocation failed\n");
    }

    return 0;
}
