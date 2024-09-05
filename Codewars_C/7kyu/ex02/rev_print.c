#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Helper function to reverse a portion of the string in place
void reverse(char* start, char* end) {
    while (start < end) {
        char temp = *start;
        *start = *end;
        *end = temp;
        start++;
        end--;
    }
}

char* reverseWords(const char* text) {
    if (!text) return NULL;  // Handle null input
    
    int len = strlen(text);
    char* result = (char*)malloc(len + 1);  // Allocate memory for the result
    if (!result) return NULL;  // Handle allocation failure

    strcpy(result, text);  // Copy the input text to the result buffer
    
    char* word_start = NULL;
    
    for (int i = 0; i <= len; i++) {
        if (!isspace(result[i]) && word_start == NULL) {
            word_start = &result[i];  // Mark the beginning of a word
        } else if ((isspace(result[i]) || result[i] == '\0') && word_start != NULL) {
            reverse(word_start, &result[i - 1]);  // Reverse the word
            word_start = NULL;  // Reset for the next word
        }
    }
    
    return result;  // Return the new string with reversed words
}
