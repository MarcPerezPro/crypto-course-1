#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from sympy.ntheory.modular import crt

# First factor of the RSA modulus
p = 11901234461494228310064076121482038286429650089208969229876184007349956782094248940290427800597817633601014470221576037327691902428151823981665392121868907

public_key = RSA.import_key(
    """-----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCG3rk7v9MWOhAkkqZoXBP2CLMx
        pVswwYSYmm1GArDf7ys4tQ0kk/iBS55Shu1h0Ld5nM5xSg8YHmthmPSjeaK/WkBy
        /Qjabol5Sfg30J4ksV0JsR0dK2mQSExs5hlQuLcgl9leIukzsUs7uXg2KvZ4ZWoh
        fnoqzEujTvkaXhhfgwIDAQAB
        -----END PUBLIC KEY-----""")

print(f'RSA modulus: {public_key.n}')
print(f'RSA public exponent: {public_key.e}')  # Useless
print(f'First factor of the RSA modulus: {p}')
print(f'Second factor of the RSA modulus: ??')

# If we get p and q, then we can deduct d and use that to decrypt the cipher
