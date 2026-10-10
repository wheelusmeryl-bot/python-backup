from hashlib import md5
import string
import itertools
a = 'e9032'
b = 'TASC%sO3RJMV%sWDJKX%sZM'
for i in (itertools.product(string.ascii_letters + string.digits, repeat=3)):
    flag = b % i
    if md5(flag.encode()).hexdigest()[:5] == a:
        print(flag)
        break