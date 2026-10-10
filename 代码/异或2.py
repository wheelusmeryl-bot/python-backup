dict=[i for i in range(0,65)]+[i for i in range(91,97)]+[i for i in range(123,128)]

a=''
b=''
ddd=['a','s','s','e','r','t','P','O','S','T']
for s in ddd:
    for i in dict:
        for j in dict:
            if chr(i^j)==s and len(hex(i)[2:])==2 and len(hex(j)[2:])==2:
                print("('%"+hex(i)[2:]+"'^'"+"%"+hex(j)[2:]+"')")
                break
        else:
            continue
        break
        