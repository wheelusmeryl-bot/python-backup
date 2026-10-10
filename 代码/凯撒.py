encrypted = "OoDVP4LtFm7lKnHk+JDrJo2jNZDROl/1HH77H5Xv"
key = 13

decrypted = ''
for i in encrypted:
    if i.islower():
        decrypted += chr((ord(i) - 97 - key) % 26 + 97)
    elif i.isupper():
        decrypted += chr((ord(i) - 65 - key) % 26 + 65)
    else:
        decrypted += i
print("解密后的字符串:", decrypted)