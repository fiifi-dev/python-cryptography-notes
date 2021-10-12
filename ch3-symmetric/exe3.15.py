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

msg2 = b"""
<XML>
<CreditCardPurchase>
<Merchant>Fiifi Dev</Merchant>
<Buyer>John Doe</Buyer>
<Date>11/01/2011</Date>
<Amount>$500.00</Amount>
<CCNumber>444-555-555-555</CCNumber
</CreditCardPurchase>
</XML>
"""

aesContext = Cipher(algorithms.AES(preshared_key), modes.CTR(
    preshared_iv), backend=default_backend())

encryptor = aesContext.encryptor()
encrypted_msg1 = encryptor.update(msg1)
encrypted_msg1 += encryptor.finalize()

encryptor = aesContext.encryptor()
encrypted_msg2 = encryptor.update(msg2)
encrypted_msg2 += encryptor.finalize()


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


key_chain = b''

for (x, y) in zip(encrypted_msg1, msg1):
    key_chain += int_to_bytes(x ^ y)

plaintext = b''

for (x, y) in zip(key_chain, encrypted_msg2):
    plaintext += int_to_bytes(x ^ y)

print(plaintext)
