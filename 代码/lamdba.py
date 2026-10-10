key = 'adsfkndcls'
text = 'killshadow'
v5 = len(key)
flag = ''
for v3, text_char in enumerate(text):
    for v1 in range(65, 91):
        if (v1 - 39 - ord(key[v3 % v5]) + 97) % 26 + 97 == ord(text_char):
            flag += chr(v1)
print(flag)