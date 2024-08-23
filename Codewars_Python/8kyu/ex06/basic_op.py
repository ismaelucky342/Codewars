def basic_op(op, value1, value2):
    if op == '+':
        return value1 + value2
    elif op == '-':
        return value1 - value2
    elif op == '*':
        return value1 * value2
    elif op == '/':
        if value2 == 0:
            raise ValueError("Error: Division by zero is not allowed")
        return value1 / value2
    else:
        raise ValueError("Error: Invalid operation")