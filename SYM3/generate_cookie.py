#! /usr/bin/env python3

import base64
import json


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        print(myjson)
        print(e)
        return False
    return True


# URL: https://noflag-2.crypto.blackfoot.io/
originalCookie = "q09Iqdiu3besuxfdBiXssIBk6QKKJ6iDIg+1kA7tbD6rcrzWelLPJGl5VfNMd///1zJM46D8eB7FOn/Vl+dfJQ=="
originalIV = base64.b64decode(originalCookie)[:16]
originalCookieData = base64.b64decode(originalCookie)[16:]
originalPlainText = "{'password': '', 'username': '', 'admin': 0}"
# We can only manipulate the first block, so admin has to go first
# Should be 16 "################"
newFirstBlock = "{'admin':1,     "
assert len(
    newFirstBlock) <= 16, f"newFirstBlock invalid length: {len(newFirstBlock)}"

expectedCookieData = newFirstBlock + originalPlainText[len(newFirstBlock):]
print(f"Expected cookie data: {expectedCookieData}")
assert is_json(expectedCookieData.replace("'", '"'))


decrypt = [a ^ ord(b) for (a, b) in zip(originalIV, originalPlainText)]
newIV = bytes([a ^ ord(b) for (a, b) in zip(decrypt, newFirstBlock)])
assert originalIV != newIV
print(f'new IV: {newIV}')
assert len(newIV) == 16, f"newIV invalid length: {len(newIV)}"

newCookie = base64.b64encode(newIV + originalCookieData)
print(f'patched cookie:\t{newCookie}')
