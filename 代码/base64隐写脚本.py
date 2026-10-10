import base64
table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
bits = ""
with open(r"C:\Users\29120\Desktop\base64隐写\stego.txt") as f:
    for line in f:
        line = line.strip()
        if line.endswith("=="):
            bits += bin(table.index(line[-3]))[2:].zfill(6)[-4:]
        elif line.endswith("="):
            bits += bin(table.index(line[-2]))[2:].zfill(6)[-2:]
msg = ""
for i in range(0, len(bits), 8):
    msg += chr(int(bits[i:i+8], 2))
print(msg)