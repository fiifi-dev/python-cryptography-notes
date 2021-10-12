from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


key = os.urandom(32)
iv = os.urandom(16)


aesCipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())

encryptor = aesCipher.encryptor()
decryptor = aesCipher.decryptor()

padder = padding.PKCS7(128).padder()
unpadder = padding.PKCS7(128).unpadder()


msg = b"""
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOB
RE: Meeting
DATE: 2001-1-1
Meet me today at the docks at 2300.
"""

# Encryption
padded_msg = padder.update(msg)
ciphertext = encryptor.update(padded_msg)
ciphertext += encryptor.update(padder.finalize())
print(ciphertext.hex())

# Decryption
padded_msg = decryptor.update(ciphertext)
msg = unpadder.update(padded_msg)
msg += unpadder.finalize()
print(msg)
