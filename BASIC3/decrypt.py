def xor(data, key):
    l = len(key)
    return bytearray((
        (data[i] ^ key[i % l]) for i in range(0, len(data))
    ))


data = bytearray(open('ch2.bmp', 'rb').read())

# gitgud
key = bytearray([0x67, 0x69, 0x74, 0x67, 0x75, 0x64])

xored = xor(data, key)

newFile = open("solved.bmp", "wb")
newFile.write(xored)

newFile.close()
