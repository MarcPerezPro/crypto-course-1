import base64
import hashlib
from Crypto.Cipher import AES

plaintext = "I was lost, but now I'm found000"

bs = AES.block_size
key = hashlib.sha256("omgwtfbbq".encode()).digest()
iv = "16bit00000000000".encode()

cipher = AES.new(key, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(plaintext.encode())

print(''.join(format(x, '02x') for x in ciphertext))
