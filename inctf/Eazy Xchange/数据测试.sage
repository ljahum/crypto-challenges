import os, hashlib, pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = p - 3
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
EC = EllipticCurve(GF(p), [a, b])
G = EC.gens()[0] # 固定的点
print(G)
key = b'\x96\xec\x12o'
print(key)

def gen_key(G, pvkey):
    tmp = sum([i for i in pvkey])
    print(tmp)
    print(tmp*G)
    G = sum([i*G for i in pvkey])
    return G
for i in range(2048):
    SS = i*G
    cip = encrypt(FLAG, SS.xy()[0])