from Crypto.Util.number import long_to_bytes

# 替换为题目给出的mask和c
mask = 9319439021858903464    # 题目输出的mask值
c = 8882504877732087312989345828667663333297225833982945014279010438327750150593504327259176959316943362605442206624947923157363187067410478202161873663103506  # 题目输出的c值


class myRNG():
    def __init__(self, seed, mask):
        self.seed = seed
        self.mask = mask

    def next(self):
        i = self.seed & self.mask
        Out = 0
        while i != 0:
            Out ^= (i & 1)
            i >>= 1
        self.seed = ((self.seed << 1) | Out) & ((1 << 64) - 1)
        return Out

    def get_myRNG_randbits(self, n):
        temp = 0
        for _ in range(n):
            temp = (temp << 1) | self.next()
        return temp


# 枚举初始seed（64位），由于flag是可打印字符，可快速验证
# 注：若mask有特殊特征（如稀疏位），可优化枚举范围，否则需暴力（64位枚举不现实，实际题目中mask大概率有规律）
def crack():
    # 实际场景中，可先分析mask的二进制特征，缩小seed范围
    # 此处假设mask是稀疏位（如只有少数几位为1），或seed有可利用特征
    for seed in range(0, 1 << 64):  # 注意：纯暴力64位不可行，需结合mask特征优化
        rng = myRNG(seed, mask)
        key = rng.get_myRNG_randbits(64 * 8)
        flag_long = key ^ c
        flag_bytes = long_to_bytes(flag_long)
        # 验证flag长度和可打印性
        if len(flag_bytes) == 64 and all(32 <= b <= 126 for b in flag_bytes):
            print(f"Found flag: DASCTF{{{flag_bytes.decode()}}}")
            return


if __name__ == "__main__":
    crack()