# from os import environ
# environ['PWNLIB_NOTERM'] = 'True'
# from pwn import remote
from hashlib import sha256

ha = lambda x: x if isinstance(x, int) or isinstance(x, Integer) else product(x.xy())
hashs = lambda *x: int.from_bytes(sha256(b'.'.join([b'%X' % ha(x) for x in x])).digest(), 'little') % p
hashs = lambda *x: int.from_bytes(sha256(b'.'.join([b'%X' % ha(x) for x in x])).digest(), 'little') % p

def hashp(x):
    x = hashs((x))
    while True:
        try:
            return E.lift_x(x)
        except:
            x = hashs((x))
from Crypto.Util.number import *
E = EllipticCurve(GF(2^255 - 19), [0, 486662, 0, 1, 0])
p = E.order()
ZmodP = Zmod(p)
G = E.lift_x(9)
m0 = randint(1, p-1)
m=m0
m1 = b'admin'
m = m1.hex() + long_to_bytes(m).hex()[len(m1.hex()):]
print(bytes_to_long( bytes.fromhex(m))-p,m0)