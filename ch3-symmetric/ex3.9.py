import os

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

msg = b'qwertyuiopasdfgh'
key = os.urandom(16)

result = b''

for (x, y) in zip(msg, key):
    result += int_to_bytes(x^y)

final = b''

for (x, y) in zip(result, key):
    final += int_to_bytes(x^y)

print(final)