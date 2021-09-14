from icecream import *

import random, hashlib, os, gmpy2, pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

FLAG = b'syc{123123123123}'

class RNG():
	pad = 0xDEADC0DE
	sze = 64
	mod = int(gmpy2.next_prime(2**sze))

	def __init__(self, seed_val, seed=None):
		if seed == None:
			assert seed_val.bit_length() == 64*2, "Seed is not 128 bits!"
			self.seed = self.gen_seed(seed_val)
			self.wrap()
		else:
			self.seed = seed
			self.ctr = 0

	def gen_seed(self, val):
		ret = [val % self.mod]
		val >>= self.sze
		for i in range(self.sze - 1):
			val = pow(i ^ ret[i] ^ self.pad, 3, self.mod)
			ret.append(val % self.mod)
			val >>= self.sze
		return ret

	def wrap(self, pr=True):
		hsze = self.sze//2
		for i in range(self.sze):
			r1 = self.seed[i]
			r2 = self.seed[(i+hsze)%self.sze]
			self.seed[i] = ((r1^self.pad)*r2)%self.mod
		self.ctr = 0

	def next(self):
		a, b, c, d = (self.seed[self.ctr^i] for i in range(4))
		mod = self.mod
		k = 1 if self.ctr%2 else 2
		a, b, c, d = (k*a-b)%mod, (b-c)%mod, (c-d)%mod, (d-a)%mod
		self.ctr += 1
		if self.ctr==64:
			self.wrap(pr=False)
		return a

def encrypt(key: bytes, pt: bytes) -> bytes:
	key = hashlib.sha256(key).digest()[:16]
	
	iv = '120a0d814682a768128504c2fe28eb79'
	iv = bytes.fromhex(iv)
 
	ic(key)
	ic(iv)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciptxt = cipher.encrypt(pad(pt, 16)).hex()
	ic(ciptxt)
 
	cipher2 = AES.new(key, AES.MODE_CBC, iv)
	txt = cipher2.decrypt(bytes.fromhex(ciptxt))
	ic(txt)

	return {'cip': ciptxt, 'iv': cipher.IV.hex()}

def main():
	# obj = RNG(random.getrandbits(128))
	r = 188013210689069300476163527325290628371
	obj = RNG(r)
	out1 = ''.join([format(obj.next(), '016x') for i in range(64)])
	out2 = ''.join([format(obj.next(), '016x') for i in range(64)])
	# print(out1)
	cip = encrypt(bytes.fromhex(out1), FLAG)
	cip['leak'] = out2
	# print(out2)
	print(cip)
	return cip

if __name__ == '__main__':
	cip = main()
	pickle.dump(cip, open('enc2.pickle', 'wb'))