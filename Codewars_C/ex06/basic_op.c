#include <stdlib.h>
#include <stdio.h>

int basic_op(char op, int value1, int value2)
{
    switch (op)
    {

    case '+':
        return value1 + value2;
    case '-':
        return value1 - value2;
    case '*':
        return value1 * value2;
    case '/':
        if (value2 == 0)
        {
            fprintf(stderr, "Error: Division by zero is not allowed\n");
            exit(EXIT_FAILURE);
        }
        return value1 / value2;
    default:
        fprintf(stderr, "Error: Invalid operation\n");
        exit(EXIT_FAILURE);
    }
    return 0;
}