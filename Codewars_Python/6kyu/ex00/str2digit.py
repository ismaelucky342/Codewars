def digitize(n):
    if n == 0:
        return [0], 1
    
    digits = []
    while n > 0:
        digits.append(n % 10)  
        n //= 10               
    
return digits, len(digits)