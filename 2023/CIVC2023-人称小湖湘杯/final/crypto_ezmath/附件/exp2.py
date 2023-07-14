from Crypto.Util.number import *
from icecream import *
import json
from random import *
p = getPrime(128)
seed = randint(2, p - 1)
p = 187118872649000152449935854468312651603
seed = 132465115999257321177856804960428863037
# ic(p,seed)
class prng:
    n = p
    # a,b = [randint(2, p - 1) for _ in range(2)]
    a = 33506786636243071520088178746093728280
    b = 164097689542794851499819197760160907707
    
    def __init__(self,seed):
        self.state = seed
    def next(self):
        self.state = (self.state * self.a + self.b) % self.n
        return self.state

    
def main():
    gen = prng(seed)
    s = [seed]
    s.append(gen.next())
    s.append(gen.next())
    s.append(gen.next())
    s.append(gen.next())
    s.append(gen.next())
    s.append(gen.next())
    f = open("output1.txt",'w')
    json.dump(s,f)
    f.close()
    flag = "flag{"+str(gen.next())+"}"
    print(flag)
    # return flag
main()
# flag{169478446215114801205986337930790905381}