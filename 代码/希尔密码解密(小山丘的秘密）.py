import numpy as np
table=['z','a','b','c','d','e','f','g','h',
       'i','j','k','l','m','n','o','p','q',
       'r','s','t','u','v','w','x','y']
key_inv=np.matrix(np.array([[1,2,3],[0,1,4],[5,6,0]])).I%26
result=key_inv*np.array([[16,20,17],
                [12,7,8],
                [7,2,13]])%26
a=''
b=[]
for i in range(result.shape[0]):
    for j in range(result.shape[1]):
        b.append(round(result.T[i,j]))
for i in range(9):
    a+=table[b[i]]
print(a)

