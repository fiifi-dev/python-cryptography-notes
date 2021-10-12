from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(16)

aesCipher = Cipher(algorithms.AES(key), modes.ECB(), default_backend())

encryptor = aesCipher.encryptor()
decryptor = aesCipher.decryptor()

ecrypted_data = encryptor.update(b"the dog is going to school")
print(decryptor.update(ecrypted_data))



