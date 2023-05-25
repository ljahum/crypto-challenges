from Crypto.Util.number import bytes_to_long,long_to_bytes
from secret import N,e,p,q,a,b
import os
flag = open('flag','r').read().strip()
assert N == p*q

def padding(msg):
    num = bytes_to_long(msg)
    msg = long_to_bytes(num^^p)
    res = msg
    if len(res) < 128:
        res = res + os.urandom(128-len(res))
    return res

def transfer(msg):
    assert len(msg) < 128
    while True:
        m = padding(msg)
        Mx = Integer(bytes_to_long(m))
        if Mx > N:
            continue
        u = R(pow(Mx,3,N)+a*Mx+b)
        if kronecker(u,p) == 1 and kronecker(u,q) == 1:
            mp = Ep.lift_x(Mx)
            mq = Eq.lift_x(Mx)
            My = crt([Integer(mp[1]),Integer(mq[1])],[p,q])
            return E(Mx,My)

def Stone_Curse(heart):
    stone = e*heart
    return stone

def Lifting_Curse(stone):
    p_order = Ep.order()
    q_order = Eq.order()
    d = inverse_mod(e,lcm(p_order,q_order))
    heart = d*stone
    return heart

if __name__ == "__main__":
    R = Zmod(N)
    E = EllipticCurve(R,[a,b])
    Ep = EllipticCurve(GF(p),[a,b])
    Eq = EllipticCurve(GF(q),[a,b])
    Heart = transfer(flag)
    Stone = Stone_Curse(Heart)
    print Stone
    print N,e
    print a,b

