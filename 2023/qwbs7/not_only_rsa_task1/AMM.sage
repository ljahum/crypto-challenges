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

n = 20289788565671012003324307131062103060859990244423187333725116068731043744218295859587498278382150779775620675092152011336913225797849717782573829179765649320271927359983554162082141908877255319715400550981462988869084618816967398571437725114356308935833701495015311197958172878812521403732038749414005661189594761246154666465178024563227666440066723650451362032162000998737626370987794816660694178305939474922064726534186386488052827919792122844587807300048430756990391177266977583227470089929347969731703368720788359127837289988944365786283419724178187242169399457608505627145016468888402441344333481249304670223
e = 11079917583
p = 3891889986375336330559716098591764128742918441309724777337583126578227827768865619689858547513951476952436981068109005313431255086775128227872912287517417948310766208005723508039484956447166240210962374423348694952997002274647622939970550008327647559433222317977926773242269276334110863262269534189811138319
q = 5213351003420231819415242686664610206224730148063270274863722096379841592931572096469136339538500817713355302889731144789372844731378975059329731297860686270736540109105854515590165681366189003405833252270606896051264517339339578167231093908235856718285980689179840159807651185918046198419707669304960745217
c = 13354219204055754230025847310134936965811370208880054443449019813095522768684299807719787421318648141224402269593016895821181312342830493800652737679627324687428327297369122017160142465940412477792023917546122283870042482432790385644640286392037986185997262289003477817675380787176650410819568815448960281666117602590863047680652856789877783422272330706693947399620261349458556870056095723068536573904350085124198592111773470010262148170379730937529246069218004969402885134027857991552224816835834207152308645148250837667184968030600819179396545349582556181916861808402629154688779221034610013350165801919342549766


ep = 49
eq = 3

m_p = solve_in_subset(49,p)
m_q = solve_in_subset(3,q)

for mpp in m_p:
    for mqq in m_q: 
        m = crt([int(mpp),int(mqq)],[p,q])
        flag = long_to_bytes(m)
        if b'CTF' in flag:
            print(flag)
            break

# b'DASCTF{C0nsTruct!n9_Techn1qUe2_f0r_RSA_Pr1me_EnC2ypt10N}'
