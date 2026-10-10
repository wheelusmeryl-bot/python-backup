#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
with open(r"C:\Users\29120\Desktop\chall2\chall2\flag_cipher", "rb") as f:
    ct = f.read()
blocks = [ct[i:i+32] for i in range(0, len(ct), 32)]
if len(blocks) > 1:
    plain = b''.join([AES.new(blocks[i-1], AES.MODE_ECB).decrypt(blocks[i]) 
                     for i in range(1, len(blocks))])
    if b'flag{' in plain:
        start = plain.find(b'flag{')
        end = plain.find(b'}', start) + 1
        print(plain[start:end].decode() if end > start else plain.decode())
    else:
        print(plain.decode('utf-8', errors='ignore'))

