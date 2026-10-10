import string
import re
import binascii
from openpyxl import load_workbook
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

with open(r"C:\Users\29120\Desktop\筛查弱口令\top1000.txt") as f:
    top = f.read()
top = top.split('\n')
top.pop()

wb = load_workbook(r"C:\Users\29120\Desktop\筛查弱口令\user_info.xlsx")
ws = wb['users']

for i in range(2, 436):
    password = binascii.unhexlify(ws[f'c{i}'].value)
    key = binascii.unhexlify(ws[f'd{i}'].value)
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(password)
    flag = unpad(flag, AES.block_size).decode()
    if flag not in top and re.search('[A-Z]', flag) and re.search('[a-z]', flag) and re.search('[0-9]', flag) and re.search('[' + re.escape(string.punctuation) + ']', flag) and len(flag) >= 6:
        continue
    else:
        print(ws[f'a{i}'].value, end='_')