#! /usr/bin/env python3

import string
import hashlib
from Crypto.Cipher import AES

plaintext = "I was lost, but now I'm found...".encode()
assert len(plaintext) == 32

bs = AES.block_size
key = hashlib.sha256("omgwtfbbq".encode()).digest()
iv = ''.encode() + bytes(16)
assert len(iv) == 16

cipher = AES.new(key, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(plaintext)

print(''.join(format(x, '02x') for x in ciphertext))

encoded = bytes([
    # Unknown
    0x00,
    0xf3, 0x74, 0xa8, 0x2d, 0xb5, 0x0b, 0x23,
    # Unknown
    0x00, 0x00, 0x0b,
    0x88, 0xf1, 0xd9, 0x76, 0xdd, 0xc1, 0xcf, 0x6d, 0xb4, 0x52, 0x4a, 0xac, 0x04, 0xe2, 0x22, 0x85, 0x39, 0x69, 0x36, 0x7e, 0x0d
])
assert len(encoded) % 16 == 0

# IV=𝑃1⊕𝐷𝑒𝑐(𝐾,𝐶1)
# Where 𝑃1 is the first plaintext and 𝐶1 its encryption of 𝑃1 with the key 𝐾 under the CBC mode of operation.
ecbCipher = AES.new(key, AES.MODE_ECB)
# decryptedText = ecbCipher.decrypt(encoded)
# foundIV = bytes(a ^ b for (a, b) in zip(plaintext, decryptedText))
# print(foundIV)

# We need to bruteforce the first encoded byte and then check if the IV is ascii
printable_chars = set(bytes(string.printable, 'ascii'))
for i in range(0xff):
    newEncoded = bytes([i]) + encoded[1:]
    decryptedText = ecbCipher.decrypt(newEncoded)
    foundIV = bytes(a ^ b for (a, b) in zip(plaintext, decryptedText))
    printable = all(char in printable_chars for char in foundIV[:4])
    if printable:
        # Let's cipher it with the foundIV and to check if we get the original encoded string
        cbcCipher = AES.new(key, AES.MODE_CBC, foundIV[:16])
        newCipherText = cbcCipher.encrypt(plaintext)
        print(
            f"IV is printable for\t{hex(i)}\t{foundIV[:16]}\t{''.join(format(x, '02x') for x in newCipherText)}")
