#! /usr/bin/env python3

import requests
import base64
import json
from bs4 import BeautifulSoup


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
# Should be 16  "################"
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

newCookie = str(base64.b64encode(newIV + originalCookieData), "utf-8")
print(f'patched cookie:\t{newCookie}')


def test_cookie(cookie):
    headers = {
        'authority': 'noflag-2.crypto.blackfoot.io',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4328.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
        'cookie': f'cookie={cookie}',
    }

    response = requests.get(
        'https://noflag-2.crypto.blackfoot.io/flag', headers=headers)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.body.find('div', attrs={'id': 'myAlert'}).text)


test_cookie(newCookie)
