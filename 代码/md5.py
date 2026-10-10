# 已知的目标字符串
target = "Z3hI5Psu1bH0F3"

def reverse_transform(c):
    # 处理大写字母
    if 65 <= ord(c) <= 90:
        # 逆向计算: (original - 51) % 26 + 65 = c
        # => original = (ord(c) - 65 + 51) % 26 + 65
        return chr((ord(c) - 65 + 51) % 26 + 65)
    # 处理小写字母
    elif 97 <= ord(c) <= 122:
        # 逆向计算: (original - 83) % 26 + 97 = c
        # => original = (ord(c) - 97 + 83) % 26 + 97
        return chr((ord(c) - 97 + 83) % 26 + 97)
    # 非字母字符不变
    else:
        return c

# 计算原始输入
original_input = ''.join([reverse_transform(c) for c in target])
print(f"正确的输入应该是: {original_input}")

# 验证我们的结果是否正确
def forward_transform(c):
    if 65 <= ord(c) <= 90:
        return chr((ord(c) - 51) % 26 + 65)
    elif 97 <= ord(c) <= 122:
        return chr((ord(c) - 83) % 26 + 97)
    else:
        return c

transformed = ''.join([forward_transform(c) for c in original_input])
print(f"验证变换结果: {transformed} (应该等于目标字符串 {target})")
