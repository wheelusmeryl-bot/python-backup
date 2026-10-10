def xor_decrypt(ciphertext, key):
    """对密文进行异或解密"""
    return bytes([byte ^ key for byte in ciphertext])

def brute_force_decrypt(ciphertext):
    """尝试所有可能的密钥（0-255）进行爆破解密"""
    print("开始爆破解密...")
    for key in range(256):  # 尝试所有可能的密钥（0-255）
        print(f"正在尝试密钥 {key}")  # 调试信息
        decrypted = xor_decrypt(ciphertext, key)
        try:
            decrypted_text = decrypted.decode('utf-8')  # 尝试解码为字符串
            print(f"密钥 {key:03d}: {decrypted_text}")
        except UnicodeDecodeError:
            # 如果解码失败，跳过该密钥
            continue

def main():
    # 用户输入加密数据（十六进制字符串）
    ciphertext_hex = input("请输入加密数据（十六进制字符串）: ")
    
    # 将十六进制字符串转换为字节序列
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        print("输入的加密数据格式不正确，请输入有效的十六进制字符串。")
        return
    
    # 开始爆破解密
    brute_force_decrypt(ciphertext)

if __name__ == "__main__":
    main()
