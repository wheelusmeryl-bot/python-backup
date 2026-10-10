import os
import base64
a = r"C:/Users/29120/Desktop/1"
for i in os.listdir(a):
    b = os.path.join(a, i)
    if os.path.isfile(b):
        try:
            with open(b, 'r') as f:
                x = f.read()
                c = base64.b16decode(x)
                d = base64.b16decode(c)
                e = base64.b32decode(d)
                f = base64.b32decode(e)
                print( {i})
                print( {f[:100]})
        except:
            continue