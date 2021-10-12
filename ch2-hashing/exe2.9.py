import hashlib
import os


def generate():
    num = 0

    while True:
        yield num
        num += 1


target = 2**255

for num in generate():
    rand_num = os.urandom(4)

    num_hex = hashlib.sha256(num.to_bytes(
        (8 + (num + (num < 0)).bit_length()) // 8,
        byteorder='big')+ rand_num
    ).hexdigest()

    num_int = int(num_hex, 16)

    if num_int < target:
        print(num_int)
        print(target)
        break
