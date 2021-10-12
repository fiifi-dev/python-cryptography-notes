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

added_msg = "a8ff0ed2ca9b80908757f8c3ecbc9b0d"


message += b"E"* (-len(message)%16)

message_hex = message.hex()

last_block = message_hex[-32:]
new_msg= message_hex.replace(last_block, added_msg)
print(new_msg)


ciphertext = encryptor.update(bytes.fromhex(new_msg))
plaintext = decryptor.update(ciphertext)
print(f"decoded: {plaintext}")