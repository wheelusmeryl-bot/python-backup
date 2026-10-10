s = 'ComeChina'
flag = ''
key = 13
for i in s:
    x = ord(i) + key
    if i >= "A" and i <= "Z" and x > 90 :
        x -= 26
    if i >= "a" and i <= "z" and x > 122 :
        x -= 26
    flag += chr(x)
print(flag)
