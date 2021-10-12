# Symmetric Encryption

One key is used to encrypt and decrypt documents. There are two types of symmetric ciphers: **block ciphers** and **stream ciphers**.  A block cipher gets its name from the fact that it works on blocks of data: you have to give it a certain amount of data before it can do anything, and larger data must be broken down into block-sized chunks (also, every block must be full). Stream ciphers, on the other hand, can encrypt data one byte at a time. **AES** is fundamentally a symmetric key, block cipher algorithm. It (like many other block ciphers) can be used in a way that makes it behave like a stream cipher.An example is **AES** (Advance Encryption Standard). It has many modes:

1. Electronic code book (ECB) (WARNING! DANGEROUS!) (Raw AES)
2. Cipher block chaining (CBC)
3. Counter mode (CTR)

For testing purposes the KATS used which contains a list of plaintext and cyphertext. ECB is usually used for testing purposes
[List of KATS](https://csrc.nist.gov/CSRC/media/Projects/)

How to do encryption (ECB)

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Step 1 - Create key - 16 bytes (128 bits)
key = os.urandom(16)

# Step 2 - Create Cipher
aesCipher = Cipher(algorithms.AES(key),
    modes.ECB(),
    backend=default_backend())

# Step 3 - Generate encryptors or decryptors
aesEncryptor = aesCipher.encryptor()
aesDecryptor = aesCipher.decryptor()

# Step 4 - Start Encrypting or Decrypting
ecrypted_data = encryptor.update(b"the dog is going to school")
decryptor.update(ecrypted_data) # Decrypted data

```

*NB: There's **update method** for updating encryptor and decryptor data*

## Understanding the update method

The update functions for both encryption and decryption always work on **16 bytes** at a time.  Calling update with fewer than **16 bytes** produces no immediate result. Instead, it accumulates data until it has at least **16 bytes** to work with.

## Why is ECB not secure

ECB ouputs are deterministic: An encryption output should be:

1. Encrypt the same message differently each time.
2. Eliminate predictable patterns between blocks.

We solve this problem with **initialization vector (IV)**
An IV is typically a random string that is used as a third input—in addition to the key and plaintext. Unlike the key, the **IV** is public. **IV** prevents repeatablility.

In ECB avalanche effect depends on the block length. This implies a change in the first block will affect just the first block. To make make this effect affect the other blocks-When encrypting, for example, one can **XOR** the encrypted output of a block with the unencrypted input of the next block. To reverse this while decrypting, the ciphertext is decrypted and then the XOR operation is again applied to the previous ciphertext block to obtain the plaintext.
This is called **cipher block chaining (CBC) mode**.
$$(A XOR B) XOR B = A$$

for encryption:
$$P'[n] = P[n]*C[n-1]$$ where Co=IV

for decryption:
$$P[n] = P'[n]*C[n-1]$$ where Co=IV

### Implementation of CBC

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Step 1 - Create key (32 bytes bigger than iv)) and iv (16 bytes (128 bits))
key = os.urandom(32)
iv = os.urandom(16)

# Step 2 - Create Cipher
aesCipher = Cipher(algorithms.AES(key),
    modes.CBC(iv),
    backend=default_backend())

# Step 3 - Generate encryptors or decryptors
aesEncryptor = aesCipher.encryptor()
aesDecryptor = aesCipher.decryptor()

# Step 4 - Start Encrypting or Decrypting
ecrypted_data = encryptor.update(b"the dog is going to school")
decryptor.update(ecrypted_data) # Decrypted data

```

## Proper Padding

The cryptography module provides two schemes, one following what is known as the **PKCS7 specification** and the other following **ANSI X.923**. PKCS7 appends n bytes, with each padding byte holding the value n: if 3 bytes of padding are needed, it appends **\x03\x03\x03**. Similarly, if 2 bytes of padding are needed, it appends **\x02\x02**. ANSI X.923 is slightly different. All appended bytes are 0, except for the last byte, which is the length of the total padding. In this example, 3 bytes of padding is **\x00\x00\x03**, and two bytes of padding is **\x00\x02**.

*Note* that the padding also **update** and **finalized** method. only finalized method returns full blocks. When finalize() is called, all remaining bytes are returned along with enough bytes of padding to make a full block size.

*Note* that the padding must match the block size in case of AES is 128bits.

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Step 1 - Create key (32 bytes bigger than iv)) and iv (16 bytes (128 bits))
key = os.urandom(32)
iv = os.urandom(16)

# Step 2 - Create Cipher
aesCipher = Cipher(algorithms.AES(key),
    modes.CBC(iv),
    backend=default_backend())

# Step 3 - Generate encryptors or decryptors
aesEncryptor = aesCipher.encryptor()
aesDecryptor = aesCipher.decryptor()

# Step 4 - Make a padder/unpadder pair for 128 bit block sizes (AES) .
padder = padding.PKCS7(128).padder()
unpadder = padding.PKCS7(128).unpadder()

# Step 5 - Start Encrypting or Decrypting and finalized
padded_msg = padder.update(b"the dog is going to school")
ecrypted_data = encryptor.update(padded_msg)
encryptor.update(padder.finalize()) # After msg has been exhausted

padded_msg = decryptor.update(ecrypted_data) # Decrypted data
msg = unpadder.update(padded_message)
encryptor.update(unpadder.finalize())
```

Note that individual calls to update() produce no padding. Only the finalize() operation will do that. For the cryptography library, always think about everything submitted to a sequence of encryption update() calls and one finalize() call as a single input. Similarly, think about everything that is recovered from a series of decryption update() alls and one finalize() call as a single output

Remember, the IV is supposed to be different each time you encrypt, preventing the same data from being encrypted to the same ciphertext! **This is not optional**.

Calling the update() method over and over is not reusing a key and IV because we are appending to the end of the CBC chain. Never give the same key and IV pair to an encryptor more than once

## Cross the Streams 

**Counter mode (CTR)** has a number of advantages to CBC mode and, in our opinion, is significantly easier to understand than CBC mode.

**AES-CTR** mimics this aspect of **OTP**. But instead of requiring the key to be the same size as the plaintext (a real pain when encrypting a 1TB file), it uses AES and a counter to generate a key stream of almost arbitrary length from an AES key as small as 128 bits.

Happily,**stream ciphers** do not require padding! It is quite simple to only XOR a partial block, discarding the later parts of the key that aren’t needed.

$$C[n] = P[n] ^ n<sub>k</sub>$$
$$C[n] = P[n] ^ (IV + n)<sub>k</sub>$$ *For encryption*

Where IV is the **nounce**: where the subscript k indicates *"encrypted with key k"*):

$$P[n] = C[n] ^ (IV + n)<sub>k</sub>$$ *For decryption*

Implementation of CTR

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Step 1 generate key and nonce
key = os.urandom(32)
nonce = os.urandom(16)

# Step 2 create cipher object
aes_context = Cipher(algorithms.AES(key),modes.CTR(nonce),backend=default_backend())

#Step for generate encryptor and decryptor
encryptor = aes_context.encryptor()
decryptor = aes_context.decryptor()

# Step 5: encrypt
encryptor.update(plaintext)
encryptor.finalize()

decryptor.update(ciphertext)
decryptor.finalize()

```

Because no padding is needed, the finalize methods are actually unnecessary except for “closing” the object. How do you choose between CTR and CBC modes? In almost all circumstances, counter mode (CTR) is recommended.12 Not only is it easier, but in some circumstances it is also more secure. As if that wasn’t enough, counter mode is also easier to parallelize because keys in the key stream are computed from their index, not from a preceding computation.

## Key and IV Management

We have already touched briefly on one of them: reuse of keys or IVs.

**Important** You must never reuse key and IV pairs. Doing so seriously compromises security and disappoints cryptography book authors. Just don’t do it. Always use a new key/IV pair when encrypting anything.

Reusing a key and IV in CBC mode is bad. Reusing a key and IV in counter mode, on the other hand, is much worse. Because  counter mode is a stream cipher, the plaintext is simply XORed with the key stream. If  you happen to know the plaintext, you can recover the key
