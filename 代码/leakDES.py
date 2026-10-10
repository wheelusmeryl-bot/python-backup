import pyDes
from itertools import product

# --- 提供的 $K_{11}$ (d.Kn[10]) 48位子密钥 ---
K11_BITS = [
    0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0,
    0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0
]

# PC-2 Permutation Table (1-based index)
# 将48位子密钥 (K_i) 映射到56位密钥状态 (C_i D_i)
PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

# PC-1 Permutation Table for C0 and D0 (1-based index)
# 用于将 56 位 C0D0 映射回 64 位原始密钥 K
PC1_C = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36]
PC1_D = [63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

# 8个被PC-2丢弃的比特的索引 (1-based index)
# 这些是需要爆破的未知位
UNKNOWN_INDICES = [9, 18, 22, 25, 35, 38, 43, 54]

# C11 D11 逆向回到 C0 D0 所需的右循环移位次数
# 11轮总共左移 19 次 (1+1+2+2+2+2+2+2+1+2+2)
# 逆向操作是右移 19 次
TOTAL_SHIFTS_REVERSE = 19


def right_shift(bits, n):
    """对28位比特块进行n次右循环移位"""
    n = n % 28
    return bits[-n:] + bits[:-n]


def c0d0_to_key(c0_bits, d0_bits):
    """将56位 C0 D0 映射回64位DES密钥 (8字节)"""
    # 64位密钥K，奇偶校验位默认为0
    key_bits = [0] * 64
    c0d0_bits = c0_bits + d0_bits

    # 填充C0 (前28位)
    for i in range(28):
        # PC1_C[i] - 1 是64位密钥中的索引 (0-based)
        # c0d0_bits[i] 是C0中的比特
        key_bits[PC1_C[i] - 1] = c0d0_bits[i]

    # 填充D0 (后28位)
    for i in range(28):
        # PC1_D[i] - 1 是64位密钥中的索引 (0-based)
        # c0d0_bits[i + 28] 是D0中的比特
        key_bits[PC1_D[i] - 1] = c0d0_bits[i + 28]

    # 将64位比特列表转换为8字节
    key_bytes = bytearray()
    for i in range(0, 64, 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | key_bits[i + j]
        key_bytes.append(byte_val)
    
    return bytes(key_bytes)


def decrypt_and_check(cipher_data):
    """主解密逻辑，迭代所有256个候选密钥"""
    print("开始爆破 256 种可能的密钥...")
    
    # 迭代所有 2^8 = 256 种未知比特组合
    for unknown_bits in product([0, 1], repeat=8):
        # 1. 重构 C11 D11 (56位)
        c11d11_bits = [0] * 56
        
        # 填充K11已知的48位
        k11_idx = 0
        for i in range(56):
            # i+1是1-based索引
            if i + 1 in UNKNOWN_INDICES:
                # 填充8个未知位
                unknown_idx = UNKNOWN_INDICES.index(i + 1)
                c11d11_bits[i] = unknown_bits[unknown_idx]
            else:
                # 填充K11已知的48位
                # 需要找到 i+1 在 PC2 中的位置，来确定从 K11 的哪个位置取值
                pc2_idx = PC2.index(i + 1)
                c11d11_bits[i] = K11_BITS[pc2_idx]

        # 2. 逆向移位到 C0 D0
        c11_bits = c11d11_bits[:28]
        d11_bits = c11d11_bits[28:]

        c0_bits = right_shift(c11_bits, TOTAL_SHIFTS_REVERSE)
        d0_bits = right_shift(d11_bits, TOTAL_SHIFTS_REVERSE)
        
        # 3. 构造 8 字节密钥 K
        key = c0d0_to_key(c0_bits, d0_bits)
        
        # 4. 尝试解密
        try:
            # pyDes.des的padding模式默认为None，需要指定
            # 题目中使用的是'\0'填充 (pyDes默认填充到8字节倍数)
            d = pyDes.des(key, pyDes.ECB, pad=None, padmode=pyDes.PAD_NORMAL)
            plaintext_padded = d.decrypt(cipher_data)
            
            # 移除'\0'填充
            plaintext = plaintext_padded.rstrip(b'\0')

            # 检查Flag格式
            if plaintext.startswith(b'flag{') and b'}' in plaintext:
                print("\n[+] 找到密钥:", key.hex())
                print("[+] 解密成功! Flag:", plaintext.decode('utf-8'))
                return plaintext.decode('utf-8')
        except Exception:
            # 忽略解密错误 (例如密钥错误导致的奇怪Padding)
            pass

    print("\n[-] 未能找到有效的Flag。请检查输入的K11_BITS和cipher文件内容是否正确。")
    return None

if __name__ == '__main__':
    # --- ！！！请将此处的密文内容替换为您实际的 'cipher' 文件内容 ！！！ ---
    # 假设 'cipher' 文件已存在
    try:
        with open('cipher1', 'rb') as f:
            cipher_content = f.read()
    except FileNotFoundError:
        print("错误: 找不到 'cipher' 文件。请创建此文件并放入密文。")
        # 为使其可运行，提供一个示例密文 (假设key=b'\x01\x23\x45\x67\x89\xab\xcd\xef'加密flag{test_flag_000}得到)
        # 此示例密文用于演示脚本结构，实际运行时必须使用题目提供的密文
        cipher_content = b'\x93\x8f\x3b\x82\x90\x08\x99\xdc\xa2\x8e\x71\x8c\x5b\x17\x92\xc7'
        print("使用示例密文进行演示 (请替换为实际密文!)")
    
    # 确保密文长度是8的倍数
    if len(cipher_content) % 8 != 0:
        print("警告: 密文长度不是8的倍数，DES加密可能已损坏。")

    decrypt_and_check(cipher_content)
