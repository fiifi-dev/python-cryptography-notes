from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

preshared_key = bytes.fromhex('00112233445566778899AABBCCDDEEFF')
preshared_iv = bytes.fromhex('00000000000000000000000000000000')

msg1 = b"""
<XML>
<CreditCardPurchase>
<Merchant>Acme Inc</Merchant>
<Buyer>John Smith</Buyer>
<Date>01/01/2001</Date>
<Amount>$100.00</Amount>
<CCNumber>555-555-555-555</CCNumber
</CreditCardPurchase>
</XML>
"""

known_msg1 = b"""
<XML>
<CreditCardPurchase>
<Merchant>Acme Inc</Merchant>
"""

aesContext = Cipher(algorithms.AES(preshared_key), modes.CTR(
    preshared_iv), backend=default_backend())

encryptor = aesContext.encryptor()
encrypted_msg1 = encryptor.update(msg1)
encrypted_msg1 += encryptor.finalize()

size_kown_msg1 = len(known_msg1)
truncated_encrypted_msg1 = encrypted_msg1[:size_kown_msg1]


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


keystream = b''

for (x, y) in zip(truncated_encrypted_msg1, known_msg1):
    keystream += int_to_bytes(x ^ y)

modified_msg1 = b"""
<XML>
<CreditCardPurchase>
<Merchant>fii Inc</Merchant>
"""


new_encryted = b''

for (x, y) in zip(keystream, modified_msg1):
    new_encryted += int_to_bytes(x ^ y)

new_cipher = new_encryted + encrypted_msg1[len(modified_msg1):]

decryptor = aesContext.decryptor()

plaintext = decryptor.update(new_cipher)
plaintext += decryptor.finalize()

print(plaintext)
