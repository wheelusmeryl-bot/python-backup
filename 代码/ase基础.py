from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes

def recover_flag(xor_int: int, enc_flag: bytes):
    key_high_int = xor_int >> 128
    key_high = long_to_bytes(key_high_int, 16)
    pattern = key_high[:2]
    if key_high != pattern * 8:
        raise ValueError("上半段不是 2 字节模式重复：密钥格式不符合预期")
    key = pattern * 16

    low_part = xor_int & ((1 << 128) - 1)
    key_low_int = bytes_to_long(key[16:])
    iv_int = key_low_int ^ low_part
    iv = long_to_bytes(iv_int, 16)

    aes = AES.new(key, AES.MODE_CBC, iv)
    flag = aes.decrypt(enc_flag)
    return key, iv, flag

xor_int = 91144196586662942563895769614300232343026691029427747065707381728622849079757
enc_flag = b"\x8c-\xcd\xde\xa7\xe9\x7f.b\x8aKs\xf1\xba\xc75\xc4d\x13\x07\xac\xa4&\xd6\x91\xfe\xf3\x14\x10|\xf8p"

key, iv, flag = recover_flag(xor_int, enc_flag)
print("flag:", flag)