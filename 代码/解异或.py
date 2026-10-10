import hashlib
import itertools
f = 'abcdefghijklmnopqrstuvwxyz0123456789'
m = '496603d6953a15846cd7cc476f146771'
a1 = 'LitCTF{md5can'
a2 = '3de'
a3 = 'rypt213thoughcr'
a4 = 'sh}'
for i, j, k, o in itertools.product(f, repeat=4):
    flag = a1 + i + o + a2 + j + a3 + k + a4
    if hashlib.md5(flag.encode()).hexdigest() == m:
        print(flag)
        break
#郑义