# Possible Magic bytes at offset 0:

52 49 46 46
?? ?? ?? ??
57 45 42 50

Google WebP image file, where ?? ?? ?? ?? is the file size.

# Actual bytes at offset 0:
0000000 25 76 30 7b 11 91 51 61 07 17 70 1e

We are going to calculate the ASCII key by XORing the magic bytes with the actual bytes.

# Possible XOR for 1st block (ACTUAL^POSSIBLE)=KEY:

0x25 ^ R = w

0x76 ^ I = ?

0x30 ^ F = v

0x7b ^ F = =

w?v=

# Possible XOR for 2nd block:

0x11 ^ 0xe2 = 0xF3

0x91 ^ 0x64 = 0xF5

0x51 ^ 0x00 = Q

0x61 ^ 0x00 = a

0xF3 0xF5 Qa

# Possible XOR for 3rd block:

0x07 ^ W = P

0x17 ^ E = R

0x70 ^ B = 2

0x1e ^ P = N

PR2N
