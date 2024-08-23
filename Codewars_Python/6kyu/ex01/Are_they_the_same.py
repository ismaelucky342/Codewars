def find_index(arr, value):
    try:
        return arr.index(value)
    except ValueError:
        return -1

def comp(a, b):
    if a is None or b is None:
        return False

    b_copy = b[:]

    for num in a:
        squared = num * num
        index = find_index(b_copy, squared)
        if index == -1:
            return False  
        b_copy[index] = -1  

return True