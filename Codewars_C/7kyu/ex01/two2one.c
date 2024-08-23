#include <stdlib.h>
#include <stdbool.h>

char *longest (const char *s1, const char *s2)
{
  bool letters[26] = {false}; 
  int i; 
  char *result; 
  
    for(i = 0; s1[i] ; i++) 
        letters[s1[i] - 'a'] = true;
    

    for (i = 0; s2[i] ; i++) 
        letters[s2[i] - 'a'] = true;
    
    int len = 0;
    
    for (i = 0; i < 26; i++) {
        if (letters[i]) {
            len++;
        }
    }

    if (!(result = (char *)malloc((len + 1) * sizeof(char))))
        return NULL;

    int pos = 0;
    
    for (i = 0; i < 26; i++) {
        if (letters[i]) {
            result[pos++] = 'a' + i;
        }
    }

    result[pos] = '\0'; 
    return result;
}