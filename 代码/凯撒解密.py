b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
q = 'OoDVP4LtFm7lKnHk+JDrJo2jNZDROl/1HH77H5Xv'
for i in range(64):
    ans=""
    for c in q:
        ans+=b[(b.index(c)+i)%64]
    print(ans)
