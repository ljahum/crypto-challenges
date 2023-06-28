from Crypto.Util.number import *
from hashlib import md5
import random
def _int32(x):
    return int(0xFFFFFFFF & x)
class MT19937:
    def __init__(self, seed=0):
        self.mt = [0] * 624
        self.mt[0] = seed
        self.mti = 0
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)
    def getstate(self,op=False):
        if self.mti == 0 and op==False:
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
    def inverse_right(self,res, shift, mask=0xffffffff, bits=32):
        tmp = res
        for i in range(bits // shift):
            tmp = res ^ tmp >> shift & mask
        return tmp
    def inverse_left(self,res, shift, mask=0xffffffff, bits=32):
        tmp = res
        for i in range(bits // shift):
            tmp = res ^ tmp << shift & mask
        return tmp
    def extract_number(self,y):
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        return y&0xffffffff
    def recover(self,y):
        y = self.inverse_right(y,18)
        y = self.inverse_left(y,15,4022730752)
        y = self.inverse_left(y,7,2636928640)
        y = self.inverse_right(y,11)
        return y&0xffffffff
    def setstate(self,s):
        if(len(s)!=624):
            raise ValueError("The length of prediction must be 624!")
        for i in range(624):
            self.mt[i]=self.recover(s[i])
        #self.mt=s
        self.mti=0
    def predict(self,s):
        self.setstate(s)
        self.twist()
        return self.getstate(True)
    def invtwist(self):
        high = 0x80000000
        low = 0x7fffffff
        mask = 0x9908b0df
        for i in range(623,-1,-1):
            tmp = self.mt[i]^self.mt[(i+397)%624]
            if tmp & high == high:
                tmp ^= mask
                tmp <<= 1
                tmp |= 1
            else:
                tmp <<=1
            res = tmp&high
            tmp = self.mt[i-1]^self.mt[(i+396)%624]
            if tmp & high == high:
                tmp ^= mask
                tmp <<= 1
                tmp |= 1
            else:
                tmp <<=1
            res |= (tmp)&low
            self.mt[i] = res
def example():
    D=MT19937(48)
    print(D.getstate())
    # 生成32随机数 75120128
    print(D.mt[:5])
    print(D.recover(1353754603))
    print(D.extract_number(75120128)) # state -> random
    D.twist()
    print(D.mt[:5])
    D.invtwist()
    print(D.mt[:5])
#Main Below#
example()