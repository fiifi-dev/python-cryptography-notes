import hashlib

bob = hashlib.md5(b'bob').hexdigest()
cob = hashlib.md5(b'cob').hexdigest()

print(f"{bin(int(bob,16))}\n{bin(int(cob,16))}")