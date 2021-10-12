from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

nist_kats = []


def get_value(item: str) -> str:
    return line.split("=")[1].strip()


with open("./kats/ECBGFSbox128.rsp") as fo:
    kat = []
    for line in fo.readlines():
        if line.startswith("KEY"):
            kat.append(get_value(line))
        elif line.startswith("PLAINTEXT"):
            kat.append(get_value(line))
        elif line.startswith("CIPHERTEXT"):
            kat.append(get_value(line))

        if len(kat) == 3:
            nist_kats.append(tuple(kat))
            kat = []

for kat in nist_kats:
    key, plaintext, ciphertext = kat

    aesCipher = Cipher(
        algorithms.AES(bytes.fromhex(key)),
        modes.ECB(),
       backend=default_backend()
    )

    encryptor = aesCipher.encryptor()
    decryptor = aesCipher.decryptor()

    my_ciphertext = encryptor.update(bytes.fromhex(plaintext))

    print(f"my_ciphertext: {my_ciphertext.hex()}")
    print(f"expected_ciphertext: {ciphertext}")
    
    result ="[PASS]" if my_ciphertext.hex() == ciphertext else "[FAIL]"
    print(result)

