import random
from gmpy2 import *
from Crypto.Util.number import *
FLAG = b'xxx'
f = open('output.txt', 'w+')
seed = random.getrandbits(32)
def _int32(x):
    return int(0xFFFFFFFF & x)
class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        self.mti = 0
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self):
        if self.mti == 0:
            self.twist()
        y = self.mt[self.mti]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        self.mti = (self.mti + 1) % 624
        return _int32(y)

    def twist(self):
        for i in range(0, 624):
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = (y >> 1) ^ self.mt[(i + 397) % 624]
            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
    
    def getrandbits(self, bits):
        if bits == 32:
            return self.extract_number()
        elif bits < 32:
            return self.extract_number() >> (32-bits)
        elif bits > 32:
            res = 0
            for i in range(bits//32):
                res |= self.extract_number()<<(32*i)
            return res

mt = MT19937(seed)

print(mt.mt[random.getrandbits(32)%624], file=f)
r = lambda x: bytes([mt.getrandbits(8)])
P = getPrime(1024, randfunc=r)
Q = getPrime(1024, randfunc=r)
N = P*Q

assert gcd(seed, (P-1)*(Q-1)) == 1

print(powmod(bytes_to_long(FLAG), seed, N), file=f)