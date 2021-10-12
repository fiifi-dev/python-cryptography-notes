msg1 = b'qwerty'
msg2 = b'asdfgh'


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

result = b''

for (x, y) in zip(msg1, msg2):
    result += int_to_bytes(x ^ y)

print(result)