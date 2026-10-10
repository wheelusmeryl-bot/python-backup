import base64
import re
import libnum
n1 = 0x53a121a11e36d7a84dde3f5d73cf
n2 = 0x99122e61dc7bede74711185598c7
p1=38456719616722997
q1=44106885765559411
p2=49662237675630289
q2=62515288803124247
e = 0x10001
phi1 = (p1-1)*(q1-1)
phi2 = (p2-1)*(q2-1)
d1 = libnum.invmod(e, phi1)
d2 = libnum.invmod(e, phi2)

flag = ['0'] * 100
with open(r"C:\Users\29120\Desktop\base.txt") as f:
    for line in f:
        txt = base64.b64decode(line).decode()
        seq = int(re.split(r'[ ;]', txt)[2])
        c = int(re.split(r'[ ;]', txt)[6].strip('L'), 16)
        sig = int(re.split(r'[ ;]', txt)[-2].strip('L'), 16)
        try:
            m1 = libnum.n2s(pow(c, d1, n1)).decode()
        except:
            m1 = libnum.n2s(pow(c, d2, n2)).decode()
        try:
            m2 = libnum.n2s(pow(sig, e, n1)).decode()
        except:
            m2 = libnum.n2s(pow(sig, e, n2)).decode()
        if m1 == m2:
            flag[seq] = m1
print(''.join(flag))
