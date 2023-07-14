from Crypto.Util.number import *
from icecream import *
import json
from random import *
from data import A_list,B_list,seed_list,N_list

# s0 = [262511059665565542818742542680700347828, 287010904654436360145740056415861584813, 151812673943463405598104613454321947811, 154283457183801144036527862621937097062, 162169576764079744831218742042754936958, 237702446699526960097645789449246246726, 79991781927641983195598094004226339192]
s0 = [288530505749272642500730917886204398531, 63547143998110685331032679758907988154, 15151206512028268617888756820805603406, 268092204209244869520724955865278855216, 261067075335188593563542448889694952077, 138067838531633886698552659065694918861, 201319433320428898153580935653793106657]
# s0 =  [187347920947732167502669966469089592988, 172005321449729609569402112498877055039, 145497893129324793561010674772723412127, 7509141152031069488051378936726327124, 161799527734944103028691846155098689330, 17868038022722036141824368556075768437, 130935170227910213439548831640869043803]
def exp(p,seed,A,B):
    class prng:
        n = p
        # a,b = [randint(2, p - 1) for _ in range(2)]
        a = A
        b = B
        
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
        
        print(s)
        # f = open("output2.txt",'w')
        # json.dump(s,f)
        # f.close()
        flag = "flag{"+str(gen.next())+"}"
        print(s==s0,flag)

    main()


for i in range(len(A_list)):
    p = N_list[i]
    a = A_list[i]
    b = B_list[i]
    seed = seed_list[i]
    exp(p,seed,a,b)
    