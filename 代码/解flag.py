a =  "Qsw3sj_lz4_Ujw@l"
flag = ""
for i in range(0,16):
    for j in range(0,127):
        b = j
        if  65 <= j <= 90:
            j = (j  - 51) % 26 + 65
        if  96 < j <= 122:
            j = (j  - 79) % 26 + 97
        if chr(j) == a[i]:
            flag += chr(b)
            break
print(flag)



a='Qsw3sj_lz4_Ujw@l'
#  Cae3ar_th4_Gre@t
#  Cae3aX_Zh4_GXe@Z
b=''
for i in a:
    if 65<=ord(i)<=90:
        b=b+chr((ord(i)-65+26)%26+51)
    elif 97<=ord(i)<=122:
        b=b+chr((ord(i)-97+26)%26+79)
    else:
        b=b+i
print(b)