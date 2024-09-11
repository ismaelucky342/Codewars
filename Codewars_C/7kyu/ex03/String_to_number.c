int string_to_number(const char *src) //ft_atoi para los amigos
{
  int sign = 1;
  int result = 0; 
  
  while(*src == ' ' || *src == '\t')
      src++; 
    if (*src == '-')
      sign = -1; 
    if (*src == '-' || *src == '+')
      src++;
  while (*src)
    result = result * 10 + *src++ - '0';
  result = result * sign; 
  return result;
}