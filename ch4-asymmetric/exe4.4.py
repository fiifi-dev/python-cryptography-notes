from string import ascii_lowercase
import gmpy2, os, binascii
import itertools

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def simple_rsa_encrypt(m, publickey):
    # Public_numbers returns a data structure with the 'e' and 'n' parameters.
    numbers = publickey.public_numbers()

    # Encryption is(m^e) % n.
    return gmpy2.powmod(m, numbers.e, numbers.n)


def simple_rsa_decrypt(c, privatekey):
    # Private_numbers returns a data structure with the 'd' and 'n' parameters.
    numbers = privatekey.private_numbers()

    # Decryption is(c^d) % n.
    return gmpy2.powmod(c, numbers.d, numbers.public_numbers.n)

def int_to_bytes(i):
    # i might be a gmpy2 big integer; convert back to a Python int
    i = int(i)
    return i.to_bytes((i.bit_length()+7)//8, byteorder='big')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

# Testings
privateKey = rsa.generate_private_key(
    public_exponent=65537,key_size=2024,backend=default_backend()
)

publicKey = privateKey.public_key()

# Encryption
plaintext = "test".encode()
plaintext_int = bytes_to_int(plaintext)

ciphertextInt = simple_rsa_encrypt(plaintext_int,publicKey)
ciphertext = int_to_bytes(ciphertextInt)

for i in itertools.product(ascii_lowercase, repeat=4):
    word = "".join(i).encode()
    wordInt = bytes_to_int(word)

    wordCiphertextInt = simple_rsa_encrypt(wordInt,publicKey)
    wordCiphertext = int_to_bytes(wordCiphertextInt)

    if wordCiphertext == ciphertext:
        print(word)
        break

    
        

    
