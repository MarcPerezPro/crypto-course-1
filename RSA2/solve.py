#!/usr/bin/env python3

from Crypto.PublicKey import RSA
import itertools
from math import gcd

public_keys = [
]

# Common prime:
# We can compute gcd(𝑁𝑖,𝑁𝑗) for the 6 (𝑖,𝑗) with 𝑖<𝑗,
# and if any of these is not 1,
# we have factored 𝑁𝑖 and 𝑁𝑗 (for two-primes RSA).
# With a full factorization, we can decipher the normal way.

# I will do something like this but slower
# https://courses.csail.mit.edu/6.857/2017/project/11.pdf
for a, b in itertools.combinations(public_keys, 2):
    gcd(a_key.n, b_key.n)
    #print(a, b)
