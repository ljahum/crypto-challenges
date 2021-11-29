#! /usr/bin/sage
import icecream


from icecream import *
# -----------------------------------
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
import ecdsa
import random
from libnum import invmod
from tqdm import tqdm
from rich.progress import track
from rich.traceback import install
install()
# -----------------------------------
gen = ecdsa.NIST256p.generator
order = int(gen.order())
secret = random.randrange(1,order)
 
pub_key = ecdsa.ecdsa.Public_key(gen, gen * secret)
priv_key = ecdsa.ecdsa.Private_key(pub_key, secret)
 
nonce1 = random.randrange(1, 2**127)
nonce2 = random.randrange(1, 2**127)
 
msg1 = random.randrange(1, order)
msg2 = random.randrange(1, order)

print(f'k1={nonce1}')
print(f'k2={nonce2}')
print(f'msg1={msg1}')
print(f'msg2={msg2}')
sig1 = priv_key.sign(msg1, nonce1)
sig2 = priv_key.sign(msg2, nonce2)
r1 = int(sig1.r)
s1_inv = int(invmod(sig1.s, order))
r2 = int(sig2.r)
s2_inv = int(invmod(sig2.s, order))
 
m = [
[order, 0, 0, 0], [0, order, 0, 0],
[r1*s1_inv, r2*s2_inv, (2**128) / order, 0],
[msg1*s1_inv, msg2*s2_inv, 0, 2**128]]
M = matrix(m)
B = M.LLL()
ans =[v for v in B]
print(ans)
 

r1_inv =invmod(sig1.r, order)
s1 = sig1.s
for row in B:
    potential_nonce_1 = row[0]
    potential_priv_key = r1_inv * ((potential_nonce_1 * s1) - msg1)
    pk = ecdsa.ecdsa.Public_key(gen, gen * potential_priv_key)
    # check if we found private key by comparing its public key with actual public key
    # if(pk==pub_key):
        # print('yes')
    