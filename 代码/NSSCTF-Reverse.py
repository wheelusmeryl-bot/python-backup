import pyDes
import copy
Kn = [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]

# Despermuted[48]
PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
# DesRotations
movnum = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]#对应16轮中每一轮的循环左移位数

def gen_key(C1,D1,k):
    tempc=C1
    tempd=D1
    for i in range(k):
        tempc = tempc[1:] + tempc[:1]
        tempd = tempd[1:] + tempd[:1]
    tempCD1=tempc+tempd
    tempkey=[]
    for i in range(len(PC2)):
        tempkey.append(tempCD1[PC2[i]-1])
    return (tempkey,tempCD1)#轮运算得到下一轮子密钥

def re_gen_key(C1,D1):
    tempc=C1[-1:]+C1[:-1]
    tempd=D1[-1:]+D1[:-1]
    tempCD1=tempc+tempd
    return tempCD1 #轮运算得到上一轮CD

f=open('cipher','rb')
flag_enc=f.read()
d = pyDes.des("0"*8)

CD = ['*']*56
# 获得置换前的数据
for i in range(len(PC2)):
    CD[PC2[i]-1] = Kn[i]

for i in range(256):
    # 遍历2^8种可能
    temp = CD[::]
    bi = bin(i)[2:].zfill(8)
    tot = 0
    for j in range(len(temp)):
        if temp[j] == '*':
            temp[j] = int(bi[tot])
            tot += 1

    # 回到初始密钥
    for j in range(sum(movnum[:11])):
        temp = re_gen_key(temp[:28],temp[28:])

    tempK=[]
    Z = temp
    # 16轮迭代生成子密钥
    for j in range(16):
        tempx=gen_key(Z[:28],Z[28:],movnum[j])
        tempK.append(tempx[0])
        Z=tempx[1]
    d.Kn = tempK
    print(d.decrypt(flag_enc))


a = "NRQ@PAu;8j[+(R:2806.i"
flag = ''
for i in range(len(a)):
    b = chr(ord(a[i])+i)
    flag+=b
print(flag)