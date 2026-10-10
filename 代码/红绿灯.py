with open(r'C:\Users\29120\Desktop\file\Traffic_Light\0.png', 'rb') as f1, open(r'C:\Users\29120\Desktop\file\Traffic_Light\2.png', 'rb') as f2:
    green = f1.read()
    red = f2.read()

flag = ''
for i in range(1167):
    file = rf'C:\Users\29120\Desktop\file\Traffic_Light\{i}.png'
    with open(file, 'rb') as f:
        s = f.read()
        if s == green:
            flag = flag + '0'
        elif s == red:
            flag = flag + '1'

print(flag)

for i in range(0, len(flag), 8):
    print(chr(int(flag[i:i + 8], 2)), end='')


