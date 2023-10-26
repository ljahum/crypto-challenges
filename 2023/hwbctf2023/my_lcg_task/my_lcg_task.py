from Crypto.Util.number import*
# from secret import flag

# assert(flag[0:5]==b"flag{" )
# assert(flag[-1:]==b"}" )
# flag = flag[5:-1]
flag = b'000000000000000000000000000000000000'
print(len(flag))


class LCG:
    def __init__(self):
        self.a = getRandomNBitInteger(32)
        self.b = getRandomNBitInteger(32)
        self.c = getRandomNBitInteger(32)
        self.m = getPrime(32)
        self.seed1 = getRandomNBitInteger(32)
        self.seed2 = getRandomNBitInteger(32)

    def next(self):
        tmp = self.seed2
        self.seed2 = (self.a*self.seed1+self.b*self.seed2 +self.c) % self.m
        self.seed1 = tmp
        return self.seed2 >> 16

    def output(self):
        print("m = {}".format(self.m))
        print("self.seed2= {}".format(self.seed2))

L = LCG()
L.output()
T = []
for i in range(9):
    tmp = bytes_to_long(flag[i*4:i*4+4])
    tt = L.next()
    T.append(tt)
    print(tmp^tt)
print(T)
print("Have a good time!")


# 909619317
# 912378641
# 761422938
# 841844503
# 1701111746
# 1701194992
# 959752815
# 892545567
# 1667598316
# [0,3180180532,86337434,1850726346,2970464585,3350124366]