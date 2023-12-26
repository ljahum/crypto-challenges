import random
import time
from tqdm import tqdm
from Crypto.Util.number import *
# About 3 seconds to run
def AMM(o, r, q):
    start = time.time()
    print('\n----------------------------------------------------------------------------------')
    print('Start to run Adleman-Manders-Miller Root Extraction Method')
    print('Try to find one {:#x}th root of {} modulo {}'.format(r, o, q))
    g = GF(q)
    o = g(o)
    p = g(random.randint(1, q))
    while p ^ ((q-1) // r) == 1:
        p = g(random.randint(1, q))
    print('[+] Find p:{}'.format(p))
    t = 0
    s = q - 1
    while s % r == 0:
        t += 1
        s = s // r
    print('[+] Find s:{}, t:{}'.format(s, t))
    k = 1
    while (k * s + 1) % r != 0:
        k += 1
    alp = (k * s + 1) // r
    print('[+] Find alp:{}'.format(alp))
    a = p ^ (r**(t-1) * s)
    b = o ^ (r*alp - 1)
    c = p ^ s
    h = 1
    for i in range(1, t):
        d = b ^ (r^(t-1-i))
        if d == 1:
            j = 0
        else:
            print('[+] Calculating DLP...')
            j = - discrete_log(d, a)
            print('[+] Finish DLP...')
        b = b * (c^r)^j
        h = h * c^j
        c = c^r
    result = o^alp * h
    end = time.time()
    print("Finished in {} seconds.".format(end - start))
    print('Find one solution: {}'.format(result))
    return result

def onemod(p,r): 
    t=random.randint(2,p)
    while pow(t,(p-1)//r,p)==1: 
        t=random.randint(2,p)
    return pow(t,(p-1)//r,p) 
 
def solution(p,root,e):  
    while True:
        g=onemod(p,e) 
        may=[] 
        for i in tqdm(range(e)): 
            may.append(root*pow(g,i,p)%p)
        if len(may) == len(set(may)):
            return may


def solve_in_subset(ep,p):
    cp = int(pow(c,inverse(int(e//ep),p-1),p))
    com_factors = []
    while GCD(ep,p-1) !=1:
        com_factors.append(GCD(ep,p-1))
        ep //= GCD(ep,p-1)
    com_factors.sort()

    cps = [cp]
    for factor in com_factors:
        mps = []
        for cp in cps:
            mp = AMM(cp, factor, p)
            mps += solution(p,mp,factor)
        cps = mps
    for each in cps:
        assert pow(each,e,p)==c%p
    return cps

n = 6249734963373034215610144758924910630356277447014258270888329547267471837899275103421406467763122499270790512099702898939814547982931674247240623063334781529511973585977522269522704997379194673181703247780179146749499072297334876619475914747479522310651303344623434565831770309615574478274456549054332451773452773119453059618433160299319070430295124113199473337940505806777950838270849
e = 641747
c = 730024611795626517480532940587152891926416120514706825368440230330259913837764632826884065065554839415540061752397144140563698277864414584568812699048873820551131185796851863064509294123861487954267708318027370912496252338232193619491860340395824180108335802813022066531232025997349683725357024257420090981323217296019482516072036780365510855555146547481407283231721904830868033930943
p = 91027438112295439314606669837102361953591324472804851543344131406676387779969
ep = 641747
# eq = 3

m_p = solve_in_subset(49,p)
# m_q = solve_in_subset(3,q)

for mpp in m_p:
    for mqq in m_q: 
        m = crt([int(mpp),int(mqq)],[p,q])
        flag = long_to_bytes(m)
        if b'CTF' in flag:
            print(flag)
            break

# b'DASCTF{C0nsTruct!n9_Techn1qUe2_f0r_RSA_Pr1me_EnC2ypt10N}'
