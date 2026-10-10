import hashlib
target_md5 = "158e64cfc9991940700acc5dc0f310e3"
suffix = "_heetian"
for i in range(10000):
    word = f"{i:04d}"
    combined = word + suffix
    md5_hash = hashlib.md5(combined.encode()).hexdigest()
    if md5_hash == target_md5:
        print(word)
