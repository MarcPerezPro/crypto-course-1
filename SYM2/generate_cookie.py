#! /usr/bin/env python3

import base64

originalCookie = "Q01pZXV4VW5JVlJhbmRvbbBNVUWTyb3i9ih6TPY9Ovq0YRsnNe8ulLlQSq6hvr3S8rtyevLBdsTPlUi4Z0qkyw=="
originalPlainText = "{'admin': 0, 'password': '', 'username': ''}"
originalIV = "CMieuxUnIVRandom"

print(f'original cookie: {base64.b64decode(originalCookie)}')

decrypt = bytes(ord(a) ^ ord(b)
                for (a, b) in zip(originalIV, originalPlainText[:16]))
newPlainText = "{'admin': 1, 'password': '', 'username': ''}"
newIV = bytes(a ^ ord(b)
              for (a, b) in zip(decrypt, newPlainText))
print(f'new IV: {newIV}')

newCookie = base64.b64encode(newIV + base64.b64decode(originalCookie)[16:])
print(f'patched cookie: {newCookie}')
