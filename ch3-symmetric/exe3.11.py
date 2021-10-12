from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(16)

aesCipher = Cipher(algorithms.AES(key), modes.ECB(), default_backend())

encryptor = aesCipher.encryptor()
decryptor = aesCipher.decryptor()

# Encoding
with open("./secret.jpg", "rb") as fi:
    with open("encrypted_secret.jpg", "ab") as fo:
        while True:
            chunk = fi.read(16)
            if chunk == b'':
                break
            
            fo.write(encryptor.update(chunk + b"\x00"*(-len(chunk) % 16)))


# Decoding
with open("./encrypted_secret.jpg", "rb") as fi:
    with open("decrypted_secret.jpg", "ab") as fo:
        while True:
            chunk = fi.read(16)
            if chunk == b'':
                break
            
            fo.write(decryptor.update(chunk + b"\x00"*(-len(chunk) % 16)))
