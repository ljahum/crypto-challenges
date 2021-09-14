import struct
from random import SystemRandom

p = 10000000000000001119

# R.<x> = GF(p)[]; y=x
# f = y + prod(map(eval, 'yyyyyyy'))
# C = HyperellipticCurve(f, 0)
# J = C.jacobian()

class RNG(object):

    def __init__(self):
        self.es = [SystemRandom().randrange(p**3) for _ in range(3)]
        self.Ds = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]
        self.q = keys = b'\xa0\x8c\xf9\x1c\x02\xb2M5\xd5k\xad\xbb\x06\x9c+}\x8f\xa4\xfb;D\x1aQ\x15\xc0c\n\xdc\t\xfb\xdd\x16\xa2\x90u\x8b\r\xa9\x923\xd1K\x9a\xe9q\x01\xb2['

    def clk(self):
        self.Ds = [e*D for e,D in zip(self.es, self.Ds)]
        return self.Ds

    def __call__(self):
        
        r, self.q = self.q[0], self.q[1:]
        return r

    def __iter__(self): return self
    def __next__(self): return self()

# flag = open('flag.txt').read().strip()
# import re; assert re.match(r'hxp\{\w+\}', flag, re.ASCII)

# text = f"Hello! The flag is: {flag}"
text = 'Hello! The flag is: hxp{ez_P4rT_i5_ez__tL0Cm}'
# keys = b'\xa0\x8c\xf9\x1c\x02\xb2M5\xd5k\xad\xbb\x06\x9c+}\x8f\xa4\xfb;D\x1aQ\x15\xc0c\n\xdc\t\xfb\xdd\x16\xa2\x90u\x8b\r\xa9\x923\xd1K\x9a\xe9q\x01\xb2['
# print(keys)
print(bytes(k^^m for k,m in zip(RNG(), text.encode())).hex())
# e8e995706d936d61bd0e8ddd6afd4c5de6d7c11b2c62216ea519558c3d898949cba52aee77f6cd479d7bd9840c
