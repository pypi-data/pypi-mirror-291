import random

def get_one_number():
    return random.randint(1, 45)

def get_one_set():
    numbers = set()
    while len(numbers) < 6:
        numbers.add(random.randint(1, 45))
    return list(numbers)

def get_one_set_sorted():
    numbers = get_one_set()
    numbers.sort()
    return numbers

def get_one_set_string():
    numbers = get_one_set_sorted()
    return ', '.join(str(n) for n in numbers)

def get_one_set_string_bracket():
    numbers = get_one_set_sorted()
    return '[' + ', '.join(str(n) for n in numbers) + ']'

def get_some_sets(count=5):
    return [get_one_set() for _ in range(count)]