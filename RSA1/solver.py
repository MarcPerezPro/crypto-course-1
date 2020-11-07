#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import _modinv
from base64 import b64decode

# First factor of the RSA modulus
p = 11901234461494228310064076121482038286429650089208969229876184007349956782094248940290427800597817633601014470221576037327691902428151823981665392121868907

public_key = RSA.import_key(
    """-----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCG3rk7v9MWOhAkkqZoXBP2CLMx
        pVswwYSYmm1GArDf7ys4tQ0kk/iBS55Shu1h0Ld5nM5xSg8YHmthmPSjeaK/WkBy
        /Qjabol5Sfg30J4ksV0JsR0dK2mQSExs5hlQuLcgl9leIukzsUs7uXg2KvZ4ZWoh
        fnoqzEujTvkaXhhfgwIDAQAB
        -----END PUBLIC KEY-----""")
n = public_key.n
e = public_key.e

q = int(n // p)
assert p * q == n

# Phi
ϕ = (p - 1) * (q - 1)
d = _modinv(e, ϕ)
assert (e * d) % ϕ == 1

print(f'RSA modulus: {n}')
print(f'RSA public exponent: {e}')
print(f'First factor of the RSA modulus: {p}')
print(f'Second factor of the RSA modulus: {q}')
print(f'RSA private exponent: {d}')

# I suck at reading files in python, so I base64'd it
raw_cipher = b64decode(
    'U0JUONM2neF4/SksiQsBjybSLlJ/HbHrtM9iesDJWFlN/9y1N1OqouihxVqWpliUdAc8608bkxNXAz9DCdMG6myABK9H6Fd1+diVKktMWw+FbhV95MouJdvXRXR0VBOxc5RefLUL/ntTXoTZ3uR2oDthD8f+nB4Ky00y3DHOFuE=')

private_key = RSA.construct((n, e, d, p, q))
cipher = PKCS1_OAEP.new(private_key)

message = cipher.decrypt(raw_cipher)

print(message)  # [Good job! Next chall: /rsa2ez4me.zip]'
