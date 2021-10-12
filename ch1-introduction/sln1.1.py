from string import ascii_uppercase


def create_shift_substitions(n: int):
    encoding = {}
    decoding = {}

    alphabet_size = len(ascii_uppercase)

    for i in range(len(ascii_uppercase)):
        letter = ascii_uppercase[i]
        subt_letter = ascii_uppercase[(i+n) % alphabet_size]
        encoding[letter] = subt_letter
        decoding[subt_letter] = letter

    return encoding, decoding


shift_cypher = create_shift_substitions(10)
encoder= shift_cypher[0]
decoder= shift_cypher[1]


def encode(msg: str,  encoder=encoder):
    return "".join(encoder.get(x,x) for x in msg.upper())

def decode(cypher: str,  decoder=decoder):
    return "".join(decoder.get(x,x) for x in cypher.upper())

# Testing
print(encode("Hello World"))
print(decode("ROVVY GYBVN"))
