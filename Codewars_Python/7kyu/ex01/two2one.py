def longest(s1, s2):
    letters = set()
    for char in s1:
        letters.add(char)
    for char in s2:
        letters.add(char)
    sorted_letters = sorted(letters)
    result = ''.join(sorted_letters)
    return result