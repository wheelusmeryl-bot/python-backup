from Crypto.Util.number import *

c = [748044282, 2053864743, 734492413, 675117672, 1691099828, 1729574447, 1691102180, 657669994, 1741780405, 842228028, 1909206003, 1797919307]
IV = bytes_to_long(b'cbc!')
K = (IV ^ bytes_to_long(b'moec')) ^ c[0]
plain_nums = [IV ^ c[0] ^ K] + [c[i-1] ^ c[i] ^ K for i in range(1, len(c))]
flag = b''.join(long_to_bytes(num, 4) for num in plain_nums).rstrip(b'\x00')
print(flag.decode())