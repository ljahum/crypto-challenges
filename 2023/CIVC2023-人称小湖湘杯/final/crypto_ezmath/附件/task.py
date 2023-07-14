from Crypto.Util.number import *
from icecream import *
import json
from random import *
p = getPrime(128)
seed = randint(2, p - 1)
# p =207669569439772486173239448051031663177
# seed = 187347920947732167502669966469089592988


# ic(p,seed)
class prng:
    n = p
    a,b = [randint(2, p - 1) for _ in range(2)]
    # a = 74082735081951230700921788552095623053/
    # b = 29653429384078010846399218642000625655
    # print(a,b)
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
# flag{54033510324291165820565145588068303166}