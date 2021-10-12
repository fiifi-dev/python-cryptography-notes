from string import ascii_lowercase
import hashlib


def generate(alphabets, max_length):
    if max_length <= 0:
        return

    for x in alphabets:
        yield x

    for y in alphabets:
        for z in generate(alphabets, max_length-1):
            yield y + z


preimage = "preimage seed"
test_hash = "test hash"

text_hash_hex = hashlib.md5(test_hash[0:5].encode("utf-8")).hexdigest()


for x in generate(ascii_lowercase, 5):
    if hashlib.md5(x.encode("utf-8")).hexdigest() == text_hash_hex:
        print(x)
        print(text_hash_hex)
        break
