import random
import string

def Random_Password_AF():
    password = ""
    lowerLetters = string.ascii_lowercase
    upperLetters = string.ascii_uppercase
    digits = string.digits
    symbols = "!@$%&*?"
    password = password + ''.join(random.choice(upperLetters) for i in range(1))
    password = password + ''.join(random.choice(lowerLetters) for i in range(1))
    password = password + ''.join(random.choice(digits) for i in range(1))
    password = password + ''.join(random.choice(symbols) for i in range(1))
    password = password + ''.join(random.choice(upperLetters+lowerLetters+digits+symbols) for i in range(8))
    return password


def Random_Name_AF():
    name = ""
    lowerLetters = string.ascii_lowercase
    upperLetters = string.ascii_uppercase
    digits = string.digits
    symbols = "!@$%&*?"
    name = name + ''.join(random.choice(upperLetters+lowerLetters) for i in range(8))
    return name


def Random_Number(size):
    num = ""
    digits = string.digits
    num = num + ''.join(random.choice(digits) for i in range(size))
    return num
