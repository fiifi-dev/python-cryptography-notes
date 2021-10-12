import hashlib

with open("dog.jpg","rb") as fo:
    md5_hasher = hashlib.md5(fo.read())
    print(md5_hasher.hexdigest())