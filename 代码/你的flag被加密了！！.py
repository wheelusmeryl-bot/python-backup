def custom_decrypt(ciphertext):
    decrypted = ""
    key = [3, 5, 2]
    key_index = 0
    for char in ciphertext:
        if 'a' <= char <= 'z':
            shift = key[key_index]
            new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            key_index = (key_index + 1) % len(key)
        elif 'A' <= char <= 'Z':
            shift = key[key_index]
            new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            key_index = (key_index + 1) % len(key)
        elif '0' <= char <= '9':
            num = int(char)
            new_num = (num - 7) % 10
            new_char = str(new_num)
        else:
            new_char = char
        decrypted += new_char
    return decrypted

encrypted = "iqcj{qafmgh89991}"
decrypted_flag = custom_decrypt(encrypted)
print("解密后的flag是:", decrypted_flag)