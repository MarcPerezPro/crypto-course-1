#! /usr/bin/env python3

import hashlib

from tqdm.contrib.concurrent import process_map
from numba.misc.special import prange
from Cryptodome.Cipher import AES
from numba import jit
import binascii
from tqdm import tqdm
from itertools import product
from multiprocessing import RLock


PLAINTEXT = "I was lost, but now I'm found...".encode()
assert len(PLAINTEXT) == 32

KEY = hashlib.sha256("omgwtfbbq".encode()).digest()
iv = 'h4ppyh4ppya5canB'.encode()
assert len(iv) == 16

cipher = AES.new(KEY, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(PLAINTEXT)

if __name__ == '__main__':
    print('cipher text:')
    print(binascii.hexlify(ciphertext))

ENCODED = bytes([
    # Unknown
    0x00,  # 0x02
    0xf3, 0x74, 0xa8, 0x2d, 0xb5, 0x0b, 0x23,
    # Unknown
    0x00, 0x00, 0x0b,  # 0xa7, 0xd0, 0x9b
    0x88, 0xf1, 0xd9, 0x76, 0xdd, 0xc1, 0xcf, 0x6d, 0xb4, 0x52, 0x4a, 0xac, 0x04, 0xe2, 0x22, 0x85, 0x39, 0x69, 0x36, 0x7e, 0x0d
])
assert len(ENCODED) % 16 == 0
assert len(ENCODED) == 32

if __name__ == '__main__':
    print('ENCODED (with holes):')
    print(binascii.hexlify(ENCODED))


@jit(nopython=True)
def byte_xor(b1, b2):  # use xor for bytes
    result = list()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return result


def encrypt_with_cbc_cipher(iv):
    cbc_cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return cbc_cipher.encrypt(PLAINTEXT)


@jit(nopython=True)
def check_against_encoded_cipher(new_cipher_text) -> bool:
    for i in prange(1, 8):
        if new_cipher_text[i] != ENCODED[i]:
            return False
    for i in prange(11, 32):
        if new_cipher_text[i] != ENCODED[i]:
            return False
    return True


# IV=𝑃1⊕𝐷𝑒𝑐(𝐾,𝐶1)
# Where 𝑃1 is the first plaintext and 𝐶1 its encryption of 𝑃1 with the key 𝐾 under the CBC mode of operation.
ecbCipher = AES.new(KEY, AES.MODE_ECB)
# We need to bruteforce the hidden encoded bytes
# and then check if the IV encodes the plaintext back into the encoded bytes
# ENCODED[0], ENCODED[8] and ENCODED[9] may be any byte
byte_range = [bytes([x]) for x in range(0xff + 1)]
# ENCODED[10] finishes with a B
byte_range_10 = [bytes([x * 0x10 + 0xB]) for x in range(0xF + 1)]


def bruteforce_encoded_bytes(encoded_0: bytes):
    for (encoded_8, encoded_9, encoded_10) in product(byte_range, byte_range, byte_range_10):
        bruteforced_encoded = encoded_0 + ENCODED[1:8] + \
            encoded_8 + encoded_9 + encoded_10 + ENCODED[11:]
        decrypted_text = ecbCipher.decrypt(bruteforced_encoded)
        found_iv = bytearray(byte_xor(PLAINTEXT, decrypted_text))[:16]

        # Let's cipher it with the foundIV and to check if we get the original encoded string
        new_cipher_text = encrypt_with_cbc_cipher(found_iv)
        if (check_against_encoded_cipher(new_cipher_text)):
            return ({
                'new_cipher_text': new_cipher_text,
                'bruteforced_encoded': bruteforced_encoded,
                'found_iv': found_iv  # h4ppyh4ppya5canB
            })


if __name__ == '__main__':
    tqdm.set_lock(RLock())
    results = process_map(bruteforce_encoded_bytes, byte_range)
    print(results)
