from Crypto.Util.number import *
from Crypto.Util.Padding import pad
flag = 'flag{d3b07b0d416ebb}'

assert len(flag) <= 45
assert flag.startswith('flag{')
assert flag.endswith('}')

m = bytes_to_long(pad(flag.encode(), 128))

p = 0xf6e82946a9e7657cebcd14018a314a33c48b80552169f3069923d49c301f8dbfc6a1ca82902fc99a9e8aff92cef927e8695baeba694ad79b309af3b6a190514cb6bfa98bbda651f9dc8f80d8490a47e8b7b22ba32dd5f24fd7ee058b4f6659726b9ac50c8a7f97c3c4a48f830bc2767a15c16fe28a9b9f4ca3949ab6eb2e53c3
g = 5

assert m < (p - 1)

c = pow(g, m, p)

with open('out.txt', 'w') as f:
    print(f"{p = }", file=f)
    print(f"{g = }", file=f)
    print(f"{c = }", file=f)
