#! /usr/bin/sage


from tqdm import tqdm
from rich.progress import track
from rich.traceback import install
install()
# -----------------------------------
from icecream import *
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *

from Crypto.Util.number import *
import gmpy2
import hashlib

import os,random,string
from hashlib import sha256
from Crypto.Util.number import bytes_to_long
from sage.misc.functional import order
from libnum import *
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


dA = random.randrange(n)
# print(type(dA))
# dA = int(32703019445086741813420098481380379496870768336466025291166428319868396091971)

Public_key = mul(dA, G)


def sha256(raw_message):
    return hashlib.sha256(raw_message).hexdigest().encode()

def _sha256(raw_message):
    return bytes_to_long(hashlib.sha256(raw_message).digest())
kk =[]
rr =[]
ss = []
hh = []

order = n
# 1
msg1 = str(1)
hash = _sha256(msg1.encode())
k = random.randrange(2**128)
kp = k % (2 ** kbits)
k=k
print(hex(k))
P = mul(k, G)
r1 = P[0]
k_inv1 = gmpy2.invert(k, n)
s1 = (k_inv1 * (hash + r1 * dA)) % n
s1_inv = int(invmod(s1, order))
msg1=hash

# 2
msg2 = str(2)
hash = _sha256(msg2.encode())
k = random.randrange(2**128)
kp = k % (2 ** kbits)
k=k
print(hex(k))
P = mul(k, G)
r2 = P[0]
k_inv2 = gmpy2.invert(k, n)
s2 = (k_inv2 * (hash + r2 * dA)) % n
s2_inv = int(invmod(s2, order))
msg2=hash

m = [
[order, 0, 0, 0], 
[0, order, 0, 0],
[r1*s1_inv, r2*s2_inv, (2**128) / order, 0],
[msg1*s1_inv, msg2*s2_inv, 0, 2**128]]
M = matrix(m)
B = M.LLL()


r1_inv =invmod(r1, order)
ic(Public_key)
for row in B:
    potential_nonce_1 = row[0]
    potential_priv_key = r1_inv * ((potential_nonce_1 * s1) - msg1)
    # ic(potential_nonce_1)
    # ic(dA)
    P = mul(int(potential_nonce_1), G)
    ic(P)