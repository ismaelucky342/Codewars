def get_count(s):
    count = 0
    vowels = 'aeiou'
    for char in s:
        if char in vowels:
            count += 1
    return count