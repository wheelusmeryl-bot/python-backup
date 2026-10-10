import base64
k = " 23DfgabcQeEFh4pklmnojqGHIJKLMNOPdRSTUVWXYZrstuvwxyz0ABCi56789+/"
b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
c = "FbdbHqAUNzoiIDdUIDhSEnF54DHthDT5Hm05HVlREnoAhaF0Hn2dFBQVFC0"
flag = ""
for i in c:
    flag+=b[k.index(i)]#从k里面提取出来的字符下标，在b中寻找对应的字符。
for i in range(4):
    if len(flag)%4!=0:
        flag=flag+'='#确保 Base64 编码的字符串长度是 4 的倍数
print(base64.b64decode(flag))


import base64

str="e3nifIH9b_C@n@dH"
flag=""

for i in range(len(str)):
    flag+=chr(ord(str[i])-i)

print(base64.b64decode(flag))
