#! /usr/bin/env python3

import hashlib
import sys
from Crypto.Cipher import AES
from itertools import product

plaintext = "I was lost, but now I'm found...".encode()
assert len(plaintext) == 32

bs = AES.block_size
key = hashlib.sha256("omgwtfbbq".encode()).digest()
iv = ''.encode() + bytes(16)
assert len(iv) == 16

cipher = AES.new(key, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(plaintext)

print('cipher text:')
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
print('encoded (with holes):')
print(''.join(format(x, '02x') for x in encoded))

# IV=𝑃1⊕𝐷𝑒𝑐(𝐾,𝐶1)
# Where 𝑃1 is the first plaintext and 𝐶1 its encryption of 𝑃1 with the key 𝐾 under the CBC mode of operation.
ecbCipher = AES.new(key, AES.MODE_ECB)

# We need to bruteforce the hidden encoded bytes
# and then check if the IV encodes the plaintext back into the encoded bytes
# encoded[0], encoded[8] and encoded[9] may be any byte
byte_range = [bytes([x]) for x in range(0xff + 1)]
# encoded[10] finishes with a B
byte_range_10 = [bytes([x * 0x10 + 0xB]) for x in range(0xF + 1)]
for (encoded_0, encoded_8, encoded_9, encoded_10) in product(byte_range, byte_range, byte_range, byte_range_10):
    sys.stdout.write(
        f' BRUTEFORCE PROGRESS: {encoded_0} {encoded_8} {encoded_9} {encoded_10}\r')
    sys.stdout.flush()
    bruteforced_encoded = encoded_0 + encoded[1:8] + \
        encoded_8 + encoded_9 + encoded_10 + encoded[11:]
    # assert len(bruteforced_encoded) % 16 == 0
    decryptedText = ecbCipher.decrypt(bruteforced_encoded)
    foundIV = bytes(a ^ b for (a, b) in zip(plaintext, decryptedText))
    # Let's cipher it with the foundIV and to check if we get the original encoded string
    cbcCipher = AES.new(key, AES.MODE_CBC, foundIV[:16])
    newCipherText = cbcCipher.encrypt(plaintext)
    if newCipherText[1:8] == encoded[1:8] and newCipherText[11:] == encoded[11:]:
        print('newCipherText:')
        print(''.join(format(x, '02x') for x in newCipherText))
        print('encoded (bruteforced):')
        print(''.join(format(x, '02x') for x in bruteforced_encoded))
        print(f"IV is \t{foundIV[:16]}")
