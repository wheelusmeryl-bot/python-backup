import hashlib
a = "8881088410842088810810842042108108821041010882108881"
a = a.split("0")
flag = ''
for substr in a:
    if not substr:
        continue
    total = 0
    for char in substr:
        total += int(char)
    flag += chr(total + 64)
print(flag)
md5_hash = hashlib.md5(flag.encode('utf-8')).hexdigest()
print(f"MD5加密后的结果: {md5_hash}")
