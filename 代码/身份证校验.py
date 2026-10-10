import csv
import re
from datetime import datetime


def p(e):
    return bool(re.match(r'^1[3-9]\d{9}$', str(e)))


def i(b):
    s = str(b).strip()
    if not re.match(r'^(\d{17}[\dXx])$', s):
        return False
    try:
        datetime.strptime(s[6:14], '%Y%m%d')
        return True
    except:
        return False


def g(d, b):
    s = str(d).strip()
    t = str(b).strip()
    if s not in ['男', '女']:
        return False
    return (int(t[16]) % 2 == 1 and s == '男') or (int(t[16]) % 2 == 0 and s == '女')


try:
    with open(r'C:\Users\29120\Downloads\数据校验\data.csv', 'r', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            a = r.get('id', '').strip()
            b = r.get('身份证', '').strip()
            c = r.get('姓名', '').strip()
            d = r.get('性别', '').strip()
            e = r.get('手机号', '').strip()
            if p(e) and i(b) and g(d, b):
                print(f"{a},{b},{c},{d},{e}")

except:
    print('error')