from icecream import *
import random, hashlib, os, gmpy2, pickle
import libnum
from libnum.modular import invmod
from Crypto.Util.number import *

from Crypto.Cipher import AES

# -----------------------------------

pad = 0xDEADC0DE
sze = 64
mod = 18446744073709551629

def inv_wrap(seed):
	
	for i in range(32):
		
		r2 = seed[i]
		r1 = ((seed[i+32]*libnum.invmod(r2,mod))%mod)^pad
		seed[i+32]=r1
	for i in range(32):
		r2 = seed[i+32]
		r1 = ((seed[i]*libnum.invmod(r2,mod))%mod)^pad
		seed[i] = r1
	return seed

def from_aa_get_seed(aa):
	seed=[]
	for i in range(0,63,4):
		tmp = aa[i:i+4]
		
		a1,a2,a3,a4 = tmp
		s0 = (a1+a2)%mod
		s1 = (2*a2+a1)%mod
		s2 = (a3+a4)%mod
		s3 = (2*a4+a3)%mod
		seed = seed + [s0,s1,s2,s3]
	return seed
def from_leak_get_aa(leak):
	aa =[]
	for i in range(0,1024,16):
		
		tmp  =leak[i:i+16]
		s = bytes.fromhex(tmp)
		tmp = bytes_to_long(s)
		
		aa.append(tmp)
	return aa
def next(seed1,i):
	ctr = i
	a, b, c, d = (seed1[ctr^i] for i in range(4))
	mod = 18446744073709551629
	k = 1 if ctr%2 else 2 # 1 和 2 交替出现,可控
	a, b, c, d = (k*a-b)%mod, (b-c)%mod, (c-d)%mod, (d-a)%mod
	
	return a
enc = {'cip': '71d39d37d3c03e08b82d81ae3b4be658e2dbdaee6a73d73a3e88271f423db30f0422d4fb9475ceef281a746afa86eaee', 'iv': 'cbf411655acfd7f670968ccf44d74e05', 'leak': '3aeba43302ab9ad0df898103fc0223be23f5ec10f62ad48744c2ec06bc4ac9b2290aff5f5d17fc2ff2a1115e657ddced0f12238ca12b076bf85fed0ce621202d159c014907e39ba7373ada78a4dea3a76bfb9ff09a8f10705cd95a47edd743fde25f32ab545bf98bba1344bed511b0c095ddede11b4a35bc02acb34d3aef46c56bfc9b668c82c0d3da76307dd87016e1a7df478cdefb98d4fe991088f478f24390fac3d4f0d0673d2801f37df421ab17cb72af64a8b21ebf9d73c3ef35a8bd5fe98c62a910ef8b859b86a58bf670fe544266bc37a36d3828e7397bac0b817f41522e76a68661b3e9952ed3d2eb7846b2f9cd2c1cc44eda2ac536eb826ce922afaa4c7d61ff3db9023cf2fff8fb34791954fbb1541f043fe26e92fb79f119fbe175bd1b551dd1225275a457580bef4301505f474060f39caad6d3172f17a9a21f68e66b59a13e817b0201dbdbcc1e6c1d80ab2e8d38f7f0a62d0bb3577da845643273b1743f5aac064422bdbd85358f6da726f9114c5553432d4f4e2f43f997975add7ea3b6a56b689ff84f7635815879e28d8c7421b979449f5bccb29cce745862610af8c99379c60e1205d5e1eda9d2f5243d4da4325ac142bd196d1777bd2d4f61eb355b7fca3e16295d05e8a21e75f010272ce159afb49fa3d4b97bd242304e34599f7bc8edf5b4430bb42b12437b7c27583d303043311afd56fae70a7d6b'}

leak  = enc['leak']
aa = from_leak_get_aa(leak)
seed = from_aa_get_seed(aa)
seed_prev = inv_wrap(seed)
out1 = ''.join([format(next(seed_prev,i), '016x') for i in range(64)])
key = bytes.fromhex(out1)
key = hashlib.sha256(key).digest()[:16]
cip = enc['cip']
iv = enc['iv']
cip = bytes.fromhex(cip)
iv = bytes.fromhex(iv)
ic(key)
ic(iv)
aes = AES.new(key, AES.MODE_CBC, iv)
flag = aes.decrypt(cip)
print(flag)


# b'inctf{S1mpl3_RN65_r_7h3_b35t!_b35e496b4d570c16}\x01'







