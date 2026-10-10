from base64 import b32decode
def solve():
    s = 'AJCS6JDDHFPPG4TOAVJSOJDM2BKU'
    dic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    msg = ''.join([dic[(5 * dic.find(x) + 12) % 32] for x in s])
    return b32decode(msg + '=' * (8 - len(msg) % 8))
if __name__ == '__main__':
    print(solve())