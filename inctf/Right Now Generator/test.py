from posixpath import abspath
from icecream import *
import random, hashlib, os, gmpy2, pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
class RNG():

    pad = 0xDEADC0DE
    sze = 64
    # mod = int(gmpy2.next_prime(2**sze))
    mod = 18446744073709551629

    def __init__(self, seed_val, seed=None):
        if seed == None:
            assert seed_val.bit_length() == 64*2, "Seed is not 128 bits!"
            self.seed = self.gen_seed(seed_val)
            self.wrap()
        else:
            self.seed = seed
            self.ctr = 0

    def gen_seed(self, val):
        ret = [val % self.mod]
        val >>= self.sze
        for i in range(self.sze - 1):
            val = pow(i ^ ret[i] ^ self.pad, 3, self.mod)
            ret.append(val % self.mod)
            val >>= self.sze
        return ret

    def wrap(self, pr=True):
        
        ic(self.seed[:10])
        
        
        hsze = self.sze//2 # 32
        # for i in range(64):
        #     ic(i)
        #     r1 = self.seed[i]
        #     r2 = self.seed[(i+hsze)%self.sze]
        #     self.seed[i] = ((r1^self.pad)*r2)%self.mod
        for i in range(32):
            r1 = self.seed[i]
            r2 = self.seed[i+32]
            self.seed[i] = ((r1^self.pad)*r2)%self.mod
        for i in range(32):
            r1 = self.seed[i+32]
            r2 = self.seed[i]
            self.seed[i+32] = ((r1^self.pad)*r2)%self.mod
        
        ic(self.seed[:10])
        input()
        self.ctr = 0

    def next(self,ans):
        index = [self.ctr^i for i in range(4)]

        ic(index)
        ic(len(self.seed))
        s0, s1, s2, s3 = (self.seed[self.ctr^i] for i in range(4))
        ic(s0, s1, s2, s3)
        mod = self.mod

        k = 1 if self.ctr%2 else 2
        ic(k)
        a, b, c, d = (k*s0-s1)%mod, (s1-s2)%mod, (s2-s3)%mod, (s3-s0)%mod
        self.ctr += 1
        if self.ctr==64:
            self.wrap(pr=False)
        ans.append(a)
        
        
        return a


def main():
    # r = random.getrandbits(128)
    r = 188013210689069300476163527325290628371
    obj = RNG(r)
    ans=[]
    out1 = ''.join([format(obj.next(ans), '016x') for i in range(64)])
    ic(ans)
    ic(len(ans))
    input()
    ans=[]
    out1 = ''.join([format(obj.next(ans), '016x') for i in range(64)])
    # 64个数
    ic(len(out1))

if __name__ == '__main__':
    cip = main()