#! /usr/bin/sage
from icecream import *
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
import gmpy2
import hashlib
import socketserver
import os,random,string
from hashlib import sha256
from Crypto.Util.number import bytes_to_long
from libnum import invmod
# from SECRET import FLAG

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
xG = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
yG = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
h = 1
zero = (0,0)
G = (xG, yG)
kbits = 8

def add(p1, p2):
    if p1 == zero:
        return p2
    if p2 == zero:
        return p1
    (p1x,p1y),(p2x,p2y) = p1,p2
    if p1x == p2x and (p1y != p2y or p1y == 0):
        return zero
    if p1x == p2x:
        tmp = (3 * p1x * p1x + a) * gmpy2.invert(2 * p1y , p) % p
    else:
        tmp = (p2y - p1y) * gmpy2.invert(p2x - p1x , p) % p
    x = (tmp * tmp - p1x - p2x) % p
    y = (tmp * (p1x - x) - p1y) % p
    return (int(x),int(y))

def mul(n, p):
    r = zero
    tmp = p
    while 0 < n:
        if n & 1 == 1:
            r = add(r,tmp)
        n, tmp = n >> 1, add(tmp,tmp)
    return r

def sha256(raw_message):
    return hashlib.sha256(raw_message).hexdigest().encode()

def _sha256(raw_message):
    return bytes_to_long(hashlib.sha256(raw_message).digest())


def main():
    _r=[]
    _s=[]
    _kp=[]
    _hash=[]
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    dA = random.randrange(n)
    Public_key = mul(dA, G)
    for _ in range(100):
        
        msg = str(_)
        hash = _sha256(msg.encode())
        k = random.randrange(n)
        kp = k % (2 ** kbits)
        P = mul(k, G)
        r = P[0]
        k_inv = gmpy2.invert(k, n)
        s = int((k_inv * (hash + r * dA)) % n)
        _r.append(r)
        _s.append(s)
        _kp.append(kp)
        _hash.append(hash)
    # fr = open('./data.py','w')
    # print(f"r={_r}",file=fr)
    # print(f"s={_s}",file=fr)
    # print(f"a={_kp}",file=fr)
    # print(f"H={_hash}",file=fr)
    # # print(f"da={dA}",file=fr)
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    l=8
    LEN=len(_kp)
    tt=[]
    uu=[]
    for i in range(LEN):
        tmp1 = (_r[i]*invmod(_s[i]*2^l,n))%n
        tt.append(tmp1)
        tmp2 = ((_kp[i]*_s[i]-_hash[i])*invmod(_s[i]*2^l,n))%n
        uu.append(tmp2)
    M=[[0 for i in range(102)] for j in range(102)]

    for i in range(LEN):
        M[i][i]=n
    for i in range(LEN):
        M[LEN][i]=tt[i]
        M[LEN+1][i]=uu[i]

    ct= 1
    cu= 1
    M[LEN][LEN]=ct
    M[LEN+1][LEN+1]=cu

    print("start LLL....")
    M = matrix(M)
    M = [list(i) for i in M]
    fakeX = M[LEN][LEN]
    ic(fakeX)
    ic(dA)
    return fakeX == dA

for i in range(10000):
    if(main()==false):
        print("no",i)
    else:
        print("yes")
        break

