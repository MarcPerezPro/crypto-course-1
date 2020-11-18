#! /usr/bin/env python3

import requests
import base64
import json
from bs4 import BeautifulSoup

# URL: https://noflag-2.crypto.blackfoot.io/
originalCookie = "1MesXUfznEMYFaa9L8WQB7KuLRpyxa8Czae1cheXa6aD/RdOjYiupdpXPseP57ve3WFvk/dYn+cBSVUVw0ghcyRU7zEUxRWvpVCoJ2Qy07s="
originalIV = base64.b64decode(originalCookie)[:16]
originalCookieData = base64.b64decode(originalCookie)[16:]
# 16 bytes blocks:   1111111111111111222222222222222233333333333333334444444444444444
originalPlainText = "{'password': 'aa', 'username': 'aaaaaaaaaaaaaaaa', 'admin': 0}"
adminBooleanOffset = originalPlainText.find('0')
# We want to flip that 0 at offset adminBooleanOffset to a 1
# So basically to flip originalPlainText[adminBooleanOffset] we have to flip originalCookieData[adminBooleanOffset - 16]
# This will destroy the 3rd block, but switch a byte in the 4th block

newCookieData = bytearray(originalCookieData)
newCookieData[adminBooleanOffset - 16] += 1

newCookie = str(base64.b64encode(originalIV + newCookieData), "utf-8")
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
