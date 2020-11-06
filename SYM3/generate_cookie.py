#! /usr/bin/env python3

import base64
import requests

originalCookie = "4lgJhqe1Pf/8CTCHUyTNiYMshNOqa7tmdIyUcN099xpQ3z1tCuVR5FxEyawRnxUt0l3IA+i4jgjWcf7krV9yoA=="
originalPlainText = "{'password': '', 'username': '', 'admin': 0}"

print(f'original cookie: {base64.b64decode(originalCookie)}')

for i in range(1, len(base64.b64decode(originalCookie))):
    originalIV = str(base64.b64decode(originalCookie)[:i])
    decrypt = bytes(ord(a) ^ ord(b)
                    for (a, b) in zip(originalIV, originalPlainText[:len(originalIV)]))
    newPlainText = "{'admin': 1, 'password': '', 'username': ''}"
    newIV = bytes(a ^ ord(b) for (a, b) in zip(decrypt, newPlainText))
    #print(f'new IV: {newIV}')

    newCookie = base64.b64encode(
        newIV + base64.b64decode(originalCookie)[len(newIV):])
    print(f'patched cookie:\t{newCookie}')
    # response = requests.get("https://noflag-2.crypto.blackfoot.io/flag",
    #                         headers={
    #                             "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #                             "accept-language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
    #                             "authority": "noflag-2.crypto.blackfoot.io",
    #                             "cache-control": "max-age=0",
    #                             "dnt": "1",
    #                             "sec-fetch-dest": "document",
    #                             "sec-fetch-mode": "navigate",
    #                             "sec-fetch-site": "same-origin",
    #                             "sec-fetch-user": "?1",
    #                             "upgrade-insecure-requests": "1",
    #                             "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4315.6 Safari/537.36"
    #                         },
    #                         cookies={
    #                             "cookie": str(newCookie)
    #                         },
    #                         )
    # print(response)
    # print(response.content)
