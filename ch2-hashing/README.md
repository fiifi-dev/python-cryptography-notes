# Hashing

Hashing is used for message integrity.

Hasing works when the following are true:

1. They produce repeatable unique values for every input
2. The hash provide no clue about the input that produced it

Examples of hash functions are:

1. MD5 (not good)
2. SHA1 (not good)
3. SHA256 (good)

## MD5 - Message Digest (Fingerprint)

It converts any document of any size into a fixed small space. MD occupies **16 bytes** of memory.
They have the following features:

- Same document producing the same hash
- It feels random: No clues to the input
  
Hasing doesn't have to be inserted at once input can be added one after the other with the **update** method. eg

```python
md5_hasher.update(b'a')
md5_hasher.update(b'l')
```

Fundamental qualities of all hash functions:

1. Consistency
2. Compression
3. Lossiness

For hash functions to be secure these three (3) properties must be met:

1. Preimage Resistance
2. Second-Preimage Resistance
3. Collision Resistance

### Preimage Resistance

Preimage is a set of inputs that produce a set of specific output.
$$H(x) = k$$ all x's

Preimage resistance: It is hard to find a documents that produced hash. Because there are infintely many possible values.

### Second-preimage resistance

If you have the document that produced a particular hash it should be hard for you to find another document that produce the same hash.

### Collision Resistance

It should be hard for you to find any two inputs that produce the same output. It should have the avalache property.
$$E = 2^n$$ Takes for breaking where **n=128**
$$E = 2^\frac{n}{2}$$ Takes half to of n to break to find collision

Apparently, I has been determined that collision can be found in **MD5** even less than **n/2** making it not secure.
A technique have been found to get collision in less than and an hour.

## Password Hashers

Most websites store hashed passwords instead of the raw password (text)
$$H(password)$$
When you try to login your the hashed of the proposed is compared with the hashed password
$$H(proposed) == H(password)$$

Since hashes are deterministic, if you know a particular hash you can tell the input. This is bad
for passwords. To prevent people from using known hashes, we introduce **salt** into the persons passwords before hashing is done.

Salt must meet the following:

1. Sufficiently long
2. Unique `os.urandom`
3. Salt must be different for every user

So storage will look like this:
`username,salt,hash` instead of `username,hash`

Password storage is better achieve with algorithms like **scrypt** and **bcrypt**

Implementation of scrypt with cryptography

```python
 import os
 from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
 from cryptography.hazmat.backends import default_backend

 # step 1- generate salt
 salt = os.urandom(16)

 # step 2 - build Scrypt
 kdf = Scrypt(salt=salt, length=32,n=2**14, r=8, p=1,backend=default_backend())

 # step 3 - hash password
 key = kdf.derive (b"my great password")

 # step 4 - veryfy password
 kdf.verify(b"my great password", key)
```

### Parameters

1. backend: Enables low level storage for fast operations
2. length:  Determines how long the key should be
3. r,p,n:   Tunining parameters

### Hacking weak passwords

Hackers with GPU-enabled rigs are able to invert anything smaller than six characters, and most passwords under eight, so at a minimum, passwords should be that long

## Proof of work

Proof of work allows you to sign a document to state ownership
