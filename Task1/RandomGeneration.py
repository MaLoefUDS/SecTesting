import random
import string

def random_string():#length: int):
    length = random.randint(0, 4)
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def random_int():
    return random.randint(0, 1000)