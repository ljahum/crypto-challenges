#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
from icecream import *
BITS = 512
p = getPrime(BITS//2)
q = getPrime(BITS//2)
n = p*q

m = b'SYC{123123123}0000000'
m = bytes_to_long(m)
ic(hex(m))
ic(hex(n))
# for i in range(512):
#     tmp = m*2**i
#     ic(hex(m))
#     ic(hex(n))
#     ic(hex(tmp%n),i)
#     if('00000' in hex(tmp%n)==false):
#         break
pl = 2**340
ph = 2**350
mid= (pl+ph)//2
for i in range(1024):
    tmp = m*mid
    ic(tmp-n)
    if(tmp>n):
        ph=mid-1
        mid = (mid+pl)//2
    else:
        pl=mid+1
        mid  =(mid+ph)//2
print(long_to_bytes( n//mid)    )

'''
346~512
'''