import gmpy2, os, binascii
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
plaintext = "Testing message".encode()
plaintext_int = bytes_to_int(plaintext)


ciphertextInt = simple_rsa_encrypt(plaintext_int,publicKey)
ciphertext = int_to_bytes(ciphertextInt)
ciphertext_hex = binascii.hexlify(ciphertext)
print(ciphertext_hex)

# Decryption
plaintext_int = simple_rsa_decrypt(ciphertextInt,privateKey)
plaintext = int_to_bytes(plaintext_int)
print(plaintext)