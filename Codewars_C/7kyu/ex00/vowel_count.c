#include <stddef.h>

size_t get_count(const char *s)
{
    int i = 0; 
    int count = 0; 
    
    while(s[i])
    {
        if(s[i] == 'a' || s[i] == 'e' || s[i] == 'i' || s[i] == 'o' || s[i] == 'u')
            count += 1; 
        i++; 
    }
  
    return count;  // Retorna el número de vocales contadas
}