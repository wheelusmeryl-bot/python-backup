import pandas as pd
x = ''
q = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
p = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
df = pd.read_excel(r"C:\Users\29120\Desktop\查找错误数据(1)\test.xlsx")
for _, row in df.iterrows():
    id = str(row['id'])
    b = str(row['idcard']).strip()
    if len(b)!=18 or not b[:17].isdigit():
        x += id + ','
        continue
    s = 0
    for i in range(17):
        s += int(b[i]) * p[i]
    k = s % 11
    if b[-1].upper() != str(q[k]):
        x += id + ','
print(x)