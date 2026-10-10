from hashlib import sha256
import string
import itertools
a = 'c22a563acc2a587afbfaaaa6d67bc6e628872b00bd7e998873881f7c6fdc62fc'
b = '861709%s%s%s%s%s%s%s'
combinations = itertools.product(string.digits, repeat=7)
for combination in combinations:
    flag = b % combination
    if sha256(flag.encode()).hexdigest() == a:
        print(flag)
        break