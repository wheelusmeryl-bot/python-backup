with open(r"C:\Users\29120\Desktop\数据脱敏\归档\person.txt", encoding="utf-8") as f1, \
     open(r'C:\Users\29120\Desktop\数据脱敏\归档\flag.txt', 'w', encoding="utf-8") as f2:
    for line in f1:
        s = line.split(',')
        name = s[0]
        if len(name) == 2:
            name = name[0] + '*'
        elif len(name) == 3:
            name = name[0] + '*' + name[-1]
        else:
            name = name[0] + '**' + name[-1]
        num = s[1]
        num = num[:7]+'********'+num[-4:]
        phone = s[2]
        phone = phone[:4]+'****'+phone[-5:]
        f2.write(f'{name},{num},{phone}')