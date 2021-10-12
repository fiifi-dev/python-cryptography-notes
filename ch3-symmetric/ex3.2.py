from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class CustomCipher:
    key = os.urandom(16)

    def __init__(self):

        self.aesCipher = Cipher(
            algorithms.AES(CustomCipher.key),
            modes.ECB(),
            default_backend()
        )
        self.encryptor = self.aesCipher.encryptor()
        self.decryptor = self.aesCipher.decryptor()

    def encrypt(self, plaintext: bytes):
        length = len(plaintext) % 16
        return self.encryptor.update(b"\x00"*length + plaintext)
        

    def decrypt(self, ciphertext: bytes):
        length = len(ciphertext) % 16
        return self.encryptor.update(b"\x00"*length + ciphertext)

aesCipher = CustomCipher()
print(aesCipher.encrypt(b"hello"))