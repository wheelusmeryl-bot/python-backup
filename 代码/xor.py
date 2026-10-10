enflag =[ 105, 122, 119, 104, 114, 111, 122, 34, 34, 119,
  34, 118, 46, 75, 34, 46, 78, 105, 0]
flag = ""
for i in range(0,18,3):
    flag+=chr((18^enflag[i])-6)
    flag+=chr((18^enflag[i+1])+6)
    flag+=chr(18^enflag[i+2]^6)
print(flag)