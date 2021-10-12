from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


key = os.urandom(16)

aesCipher = Cipher(
    algorithms.AES(key), modes.ECB(),default_backend()
)

encryptor = aesCipher.encryptor()
decryptor = aesCipher.decryptor()


message = b"""
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOB
RE: Meeting
DATE: 2001-1-1
Meet me today at the docks at 2300.
"""

message += b"E"* (-len(message)%16)

ciphertext = encryptor.update(message)
plaintext = decryptor.update(ciphertext)
print(f"decoded: {plaintext}")