

# This file was *autogenerated* from the file test.sage
from sage.all_cmdline import *   # import sage library

_sage_const_251 = Integer(251); _sage_const_108960799213330048807537253155955524262938083957673388027650083719597357215238547761557943499634403020900601643719960988288543702833581456488410418793239589934165142850195998163833962875355916819854378922306890883033496525502067124670576471251882548376530637034077 = Integer(108960799213330048807537253155955524262938083957673388027650083719597357215238547761557943499634403020900601643719960988288543702833581456488410418793239589934165142850195998163833962875355916819854378922306890883033496525502067124670576471251882548376530637034077); _sage_const_3359917755894163258174451768521610910491402727660720673898848239095553816126131162471035843306464197912997253011899806560624938869918893182751614520610693643690087988363775343761651198776860913310798127832036941524620284804884136983215497742441302140070096928109039 = Integer(3359917755894163258174451768521610910491402727660720673898848239095553816126131162471035843306464197912997253011899806560624938869918893182751614520610693643690087988363775343761651198776860913310798127832036941524620284804884136983215497742441302140070096928109039); _sage_const_72201537621260682675988549650349973570539366370497258107694937619698999052787116039080427209958662949131892284799148484018421298241124372816425123784602508705232247879799611203283114123802597553853842227351228626180079209388772101105198454904371772564490263034162 = Integer(72201537621260682675988549650349973570539366370497258107694937619698999052787116039080427209958662949131892284799148484018421298241124372816425123784602508705232247879799611203283114123802597553853842227351228626180079209388772101105198454904371772564490263034162); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_256 = Integer(256); _sage_const_0p4 = RealNumber('0.4'); _sage_const_39217838246811431279243531729119914044224429322696785472959081158748864949269 = Integer(39217838246811431279243531729119914044224429322696785472959081158748864949269); _sage_const_69367143733862710652791985332025152581988181 = Integer(69367143733862710652791985332025152581988181); _sage_const_5 = Integer(5); _sage_const_4 = Integer(4)
from Crypto.Util.number import *
import itertools




hint = _sage_const_251 
n = _sage_const_108960799213330048807537253155955524262938083957673388027650083719597357215238547761557943499634403020900601643719960988288543702833581456488410418793239589934165142850195998163833962875355916819854378922306890883033496525502067124670576471251882548376530637034077 
e = _sage_const_3359917755894163258174451768521610910491402727660720673898848239095553816126131162471035843306464197912997253011899806560624938869918893182751614520610693643690087988363775343761651198776860913310798127832036941524620284804884136983215497742441302140070096928109039 
c = _sage_const_72201537621260682675988549650349973570539366370497258107694937619698999052787116039080427209958662949131892284799148484018421298241124372816425123784602508705232247879799611203283114123802597553853842227351228626180079209388772101105198454904371772564490263034162 
e //= hint
RP = PolynomialRing(Zmod(n), names=('x',)); (x,) = RP._first_ngens(1)
f = e*x -_sage_const_1 
f = f.monic()
x0 = f.small_roots(X = _sage_const_2 **_sage_const_256 ,beta = _sage_const_0p4 )
print(x0)

x0 = _sage_const_39217838246811431279243531729119914044224429322696785472959081158748864949269 

p4 = GCD(x0*e-_sage_const_1 ,n)
# 23153425300889483483553551112335873301449089474555179592930187730428387181422112282990079197590872977617830286073037301064978277511828551780538222539198674709759058026997715121

# print(gmpy2.iroot(int(p4),int(4)))
# (mpz(69367143733862710652791985332025152581988181), True)
p = _sage_const_69367143733862710652791985332025152581988181 
q = n // p ** _sage_const_5 

phi = p ** _sage_const_4  * (p - _sage_const_1 ) * (q - _sage_const_1 )
d=  inverse(e,phi)
# 39217838246811431279243531729119914044224429322696785472959081158748864949269


cp = c % p**_sage_const_5 
cq = c % q

e = e*hint

def decrypt2(p,c,e):
    phip = p ** _sage_const_4  * (p - _sage_const_1 ) 
    
    w = GCD(e,phip)
    p1 = phip // w
    b = inverse(e,p1)
    
    g = get_oneroot2(p,w)    
    m = pow(c,b,p**_sage_const_5 )
    mps = [ZZ(m*g**i) for i in range(w)]
    return mps

def get_oneroot2(p,w):
    while _sage_const_1 :
        Zp = Zmod(p**_sage_const_5 )
        g = Zp.random_element()
        g = g**(p**_sage_const_4 *(p-_sage_const_1 )//w)
        for i in divisors(w):
            if(i != w):
                g2 = g**i
                if(g2 ==_sage_const_1 ):
                    break
        else:
            # break
            return g


mps = decrypt2(p,cp,e)




def get_oneroot(p,w):

    while _sage_const_1 :
        Zp = Zmod(p)
        g = Zp.random_element()
        g = g**((p-_sage_const_1 )//w)
        for i in divisors(w):
            if(i != w):
                g2 = g**i
                if(g2 ==_sage_const_1 ):
                    break
        else:
            return g

def decrypt(p,c,e):
    phip = p-_sage_const_1 
    w =  GCD(e,phip)
    p1 = phip//w
    b = inverse(e,p1)
    
    g = get_oneroot(p,w)
    m = pow(c,b,p)
    return [ZZ(m*g**i) for i in range(w)]

mqs = decrypt(q,cq,e)


            
for mp, mq in itertools.product(mps, mqs):
    m = crt([mp, mq], [p**_sage_const_5 , q])
    msg = long_to_bytes(int(m))
    if (b'flag' in msg):
        print(msg)

