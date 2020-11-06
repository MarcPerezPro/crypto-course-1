#! /usr/bin/env python3

import base64
import hashlib
from Crypto.Cipher import AES

plaintext = "I was lost, but now I'm found...".encode()
assert len(plaintext) == 32

bs = AES.block_size
key = hashlib.sha256("omgwtfbbq".encode()).digest()
iv = bytes(16)

cipher = AES.new(key, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(plaintext)

print(''.join(format(x, '02x') for x in ciphertext))


encoded = bytes([
    # Unknown but I think it's 0x25 or 0x81
    0x00,
    0xf3, 0x74, 0xa8, 0x2d, 0xb5, 0x0b, 0x23,
    # Unknown
    0x00, 0x00, 0x0b,
    0x88, 0xf1, 0xd9, 0x76, 0xdd, 0xc1, 0xcf, 0x6d, 0xb4, 0x52, 0x4a, 0xac, 0x04, 0xe2, 0x22, 0x85, 0x39, 0x69, 0x36, 0x7e, 0x0d
])
assert len(encoded) % 16 == 0

decryptedText = cipher.decrypt(encoded)
print(''.join(format(x, '02x') for x in decryptedText))

xored = bytes(a ^ b for (a, b) in zip(plaintext, decryptedText))
print(xored)
