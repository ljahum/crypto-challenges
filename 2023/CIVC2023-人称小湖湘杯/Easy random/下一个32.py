def _int32(x):
    return int(0xFFFFFFFF & x)
class MT19937:
    # 根据seed初始化624的state
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        self.mti = 0
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)
 
    # 提取伪随机数
    def extract_number(self,i):
        print(i,self.mti)
        if self.mti == 0:
            print("开转")
            self.twist()
        y = self.mt[self.mti]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        self.mti = (self.mti + 1) % 624
        return _int32(y)

    # 对状态进行旋转
    def twist(self):
        
        for i in range(0, 624):
            # 第一位 + 后31位
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = (y >> 1) ^ self.mt[(i + 397) % 624]
            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
                
mt = MT19937(10)
for i in range(1250):
    m =mt.extract_number(i)
