import hashlib

target_prefix = "c4d038"
count = 5  # 生成5个匹配值
found = 0

# 遍历数字，生成匹配的明文和MD5
for i in range(100000, 10000000):
    plaintext = str(i)
    md5_val = hashlib.md5(plaintext.encode()).hexdigest()
    if md5_val[:6] == target_prefix:
        print(f"明文：{plaintext} → MD5：{md5_val}")
        found += 1
        if found >= count:
            break