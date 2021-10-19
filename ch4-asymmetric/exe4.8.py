import gmpy2
import os
import binascii
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
    public_exponent=65537, key_size=2024, backend=default_backend()
)

publicKey = privateKey.public_key()


# Encryption
r = 2
m = "Hello World".encode()

print(m)


cipherR = simple_rsa_encrypt(r, publicKey)
cipherM = simple_rsa_encrypt(bytes_to_int(m), publicKey)


# Decryption
n = publicKey.public_numbers().n
cipherProduct = (cipherM*cipherR) % n
plainProductInt = simple_rsa_decrypt(cipherProduct, privateKey)
plainProductBytes = int_to_bytes(plainProductInt)

r_inv_modulo_n = gmpy2.powmod(r, -1, n)
resolvedPlaintextInt = plainProductInt * r_inv_modulo_n
resolvedPlaintextBytes = int_to_bytes(resolvedPlaintextInt)
print(resolvedPlaintextBytes)
