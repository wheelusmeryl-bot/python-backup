a = "bacoN is one of aMerICa'S sWEethEartS. it's A dARlinG, SuCCulEnt fOoD tHAt PaIRs FlawLE"
b = ""
for x in a:
    if ord('A') <= ord(x) and ord(x) <= ord('Z'):
        b += 'b'
    if ord('a') <= ord(x) and ord(x) <= ord('z'):
        b += 'a'

cipher1 = ['aaaaa', 'aaaab', 'aaaba', 'aaabb', 'aabaa', 'aabab', 'aabba', 'aabbb',
           'abaaa', 'abaaa', 'abaab', 'ababa', 'ababb', 'abbaa', 'abbab', 'abbba',
           'abbbb', 'baaaa', 'baaab', 'baaba', 'baabb', 'baabb', 'babaa', 'babab',
           'babba', 'babbb']

plain1 = [chr(ord('a') + i) for i in range(26)]

dict1 = dict(zip(cipher1, plain1))

txt = b
flag1 = ""

try:
    for i in range(0, len(txt), 5):
        group = txt[i:i + 5]
        flag1 += dict1.get(group, '')
    print("解密结果:", flag1)
except:
    flag1 = ""
    trans = str.maketrans('ab', 'ba')
    txt_swap = txt.translate(trans)
    for i in range(0, len(txt_swap), 5):
        group = txt_swap[i:i + 5]
        flag1 += dict1.get(group, '')
    print("交换a/b后解密结果:", flag1)
