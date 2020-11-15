#!/usr/bin/env python3

from typing import List
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA
import itertools
from os import path
from math import gcd
from cryptography.hazmat.primitives.asymmetric.rsa import _modinv

DIR = path.dirname(__file__)

cipherText = open(path.join(DIR, "cipher.txt"), "rb").read()

# Import the 100 public keys
public_keys: List[RsaKey] = []
for i in range(101):
    key_path = path.join(DIR, "keys", f"pub{i}.pem")
    with open(key_path, "rb") as key:
        public_keys.append(RSA.importKey(key.read()))
assert len(public_keys) == 101


def get_private_key(public_key: RsaKey, prime_factor: int):
    n = public_key.n
    e = public_key.e
    p = prime_factor
    q = int(n // p)
    assert p * q == n

    # Phi
    ϕ = (p - 1) * (q - 1)
    d = _modinv(e, ϕ)
    assert (e * d) % ϕ == 1

    return RSA.construct((n, e, d, p, q))

# Common prime:
# We can compute gcd(𝑁𝑖,𝑁𝑗) for the 6 (𝑖,𝑗) with 𝑖<𝑗,
# and if any of these is not 1,
# we have factored 𝑁𝑖 and 𝑁𝑗 (for two-primes RSA).
# With a full factorization, we can decipher the normal way.


# I will do something like this but slower
# https://courses.csail.mit.edu/6.857/2017/project/11.pdf
for a_key, b_key in itertools.combinations(public_keys, 2):
    highest_common_factor = gcd(a_key.n, b_key.n)
    if highest_common_factor != 1:
        print(f"Found a common prime! {highest_common_factor}")
        # print(f"Key A: {a_key.export_key()}")
        print(f"Key B: {b_key.export_key()}")

        # Let's create the private key of public key A
        # private_key_a = get_private_key(a_key, highest_common_factor)
        # print(f"Private Key A = {private_key_a.export_key()}")
        # cipher = PKCS1_OAEP.new(private_key_a)
        # message = cipher.decrypt(cipherText)
        # print(message)

        # Let's create the private key of public key B
        private_key_b = get_private_key(b_key, highest_common_factor)
        print(f"Private Key B = {private_key_b.export_key()}")
        cipher = PKCS1_OAEP.new(private_key_b)
        message = cipher.decrypt(cipherText)
        print(message)  # Shared prime factors?! Impossible... Or improbable? ;)
