

# This file was *autogenerated* from the file 数据测试.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF = Integer(0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF); _sage_const_3 = Integer(3); _sage_const_0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B = Integer(0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B); _sage_const_0 = Integer(0); _sage_const_515 = Integer(515)
import os, hashlib, pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
p = _sage_const_0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF 
a = p - _sage_const_3 
b = _sage_const_0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B 
EC = EllipticCurve(GF(p), [a, b])
G = EC.gens()[_sage_const_0 ] # 固定的点
print(G)
key = b'\x96\xec\x12o'
print(key)

def gen_key(G, pvkey):
    tmp = sum([i for i in pvkey])
    print(tmp)
    print(tmp*G)
    G = sum([i*G for i in pvkey])
    return G
P = gen_key(G, key)
print(P)
P = _sage_const_515 *G
print(P)

