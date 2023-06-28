import os
import random
from hashlib import md5
from Crypto.Util.number import *

rr = os.urandom(10)
rr = b'0'*10
flag = "flag{"+rr.hex()+"}"
flag_md5 = md5(flag.encode()).hexdigest()
print(flag)

m = bin(bytes_to_long(rr))[2:].zfill(8 * len(rr))

# 求 m
p = getPrime(256)
print(p)
p = 104751617715124365251106612526085291128968897297756686274482169490228962107431
def encrypt(m):
    # 80 bits
    pubkey = [random.randint(2,p - 2) for i in range(len(m))]
    # p0 64644155831251715361664070173320358480726025684876827235550363265240152582827
    print(len(pubkey),pubkey[0])
    enc = 0
    for k,i in zip(pubkey,m):
        print(k,i)
        input()
        enc += k * int(i)
        enc %= p
    return pubkey,enc

pubkey,c = encrypt(m)
f = open("output2.txt","w")
f.write(f"p = {p}\n")
f.write(f"pubkey = {pubkey}\n")
f.write(f"c = {c}\n")
f.write(f"flag_md5 = {flag_md5}\n")
f.close()