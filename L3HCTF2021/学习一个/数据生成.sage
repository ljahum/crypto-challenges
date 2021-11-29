
# from sage.all import *
# from sage.groups.generic import bsgs
from Crypto.Util.number import *
import gmpy2
import hashlib
import socketserver
import os,random,string
from hashlib import sha256
from Crypto.Util.number import bytes_to_long

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


# dA = random.randrange(n)
# print(type(dA))
dA = int(32703019445086741813420098481380379496870768336466025291166428319868396091971)

Public_key = mul(dA, G)


def sha256(raw_message):
    return hashlib.sha256(raw_message).hexdigest().encode()

def _sha256(raw_message):
    return bytes_to_long(hashlib.sha256(raw_message).digest())
kk =[]
rr =[]
ss = []
hh = []
for _ in range(100):
    
    msg = str(_)
    hash = _sha256(msg.encode())
    k = random.randrange(n)
    kp = k % (2 ** kbits)
    k=k -kp
    print(hex(k))
    P = mul(k, G)
    r_sig = P[0]
    k_inv = gmpy2.invert(k, n)
    s_sig = (k_inv * (hash + r_sig * dA)) % n
    kk.append(kp)
    ss.append(int(s_sig))
    rr.append(r_sig)
    hh.append(hash)


fr = open("./data.py",'w+')
print(f'kk={kk}',file=fr)
print(f'ss={ss}',file=fr)
print(f'rr={rr}',file=fr)
print(f'hh={hh}',file=fr)
    

# tt=[]
# uu =[]
# for i in range(len(ss)):
#     tt.append(r*inverse_mod(256*ss[i],n))
#     uu.append(hh[i]*inverse_mod(256*ss[i],n))
# l=8


# ct = 1/2^l
# cu = n/2^l
# M = [[0 for i in range(102)] for j in range(102)]
# for i in range(100):
#     for j in range(100):
#         M[i][j] = n
# for i in range(100):
#     M[100][i] = tt[i]
#     M[101][i] = uu[i]
# M[100][100] = ct
# M[101][101] = cu
# M = matrix(M)
# print('start LLLing.....')
# B = M.LLL()
# # A = matrix([[1,2,3],[1,2,3],[1,2,34]])
# # A.LLL()
# f = open('./data','w+')
# for i in B:
#     f.write(str(list(i))+'\n')
