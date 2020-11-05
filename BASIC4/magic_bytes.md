# Possible Magic bytes at offset 0:

52 49 46 46
?? ?? ?? ??
57 45 42 50

Google WebP image file, where ?? ?? ?? ?? is the file size - 8 bits.

# Actual bytes at offset 0:
0000000 25 76 30 7b 11 91 51 61 07 17 70 1e

We are going to calculate the key by XORing the magic bytes with the actual bytes.

# Possible XOR for 1st block (ACTUAL^POSSIBLE)=KEY:

0x25 ^ R = w

0x76 ^ I = ?

0x30 ^ F = v

0x7b ^ F = =

w?v=

# Possible XOR for 2nd block:

```bash
ls -l basic4.webp
printf '%x\n' 57956-8
```

Size is e25c but we have to reverse the order and pad with zeros, so 0x5C 0xE2 0x00 0x00

0x11 ^ 0x5C = M

0x91 ^ 0xE2 = s

0x51 ^ 0x00 = Q

0x61 ^ 0x00 = a

MsQa

# Possible XOR for 3rd block:

0x07 ^ W = P

0x17 ^ E = R

0x70 ^ B = 2

0x1e ^ P = N

PR2N

# Full key

w?v=MsQaPR2N