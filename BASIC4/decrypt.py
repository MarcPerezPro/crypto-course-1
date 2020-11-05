def xor(data, key):
    l = len(key)
    return bytearray((
        (data[i] ^ key[i % l]) for i in range(0, len(data))
    ))


data = bytearray(open('basic4.webp', 'rb').read())

# w?v=MsQaPR2N
key = bytearray([
    0x77, 0x3F, 0x76, 0x3D,
    0x4D, 0x73, 0x51, 0x61,
    0x50, 0x52, 0x32, 0x4E
])

xored = xor(data, key)

newFile = open("solved.webp", "wb")
newFile.write(xored)

newFile.close()
