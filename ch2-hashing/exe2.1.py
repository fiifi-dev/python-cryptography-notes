import hashlib

"""Hasing various messages"""
alice = hashlib.md5(b'alice').hexdigest()
bob = hashlib.md5(b'bob').hexdigest()
balice = hashlib.md5(b'balice').hexdigest()
cob = hashlib.md5(b'cob').hexdigest()
a = hashlib.md5(b'a').hexdigest()
aa = hashlib.md5(b'aa').hexdigest()
aaaaaaaaaa = hashlib.md5(b'aaaaaaaaaa').hexdigest()
a_1000000_times = hashlib.md5(b'a'*1000000).hexdigest()


# Testing

# print(alice)
# print(bob)
# print(balice)
# print(cob)
# print(a)
# print(aa)
# print(aaaaaaaaaa)
# print(a_1000000_times)
