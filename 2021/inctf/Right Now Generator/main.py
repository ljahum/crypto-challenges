from icecream import *

import random, hashlib, os, gmpy2, pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# FLAG = open('flag.txt', 'rb').read()
# FLAG

class RNG():
	pad = 0xDEADC0DE
	sze = 64
	mod = int(gmpy2.next_prime(2**sze))
	#  18446744073709551629

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

	def next(self,ans):
		a, b, c, d = (self.seed[self.ctr^i] for i in range(4))
		mod = self.mod
		k = 1 if self.ctr%2 else 2 # 1 和 2 交替出现,可控
		a, b, c, d = (k*a-b)%mod, (b-c)%mod, (c-d)%mod, (d-a)%mod
		self.ctr += 1
		if self.ctr==64:
			self.wrap(pr=False)
		ans.append(a)
		return a

def encrypt(key: bytes, pt: bytes) -> bytes:
	key = hashlib.sha256(key).digest()[:16]
	cipher = AES.new(key, AES.MODE_CBC, os.urandom(16))
	return {'cip': cipher.encrypt(pad(pt, 16)).hex(), 'iv': cipher.IV.hex()}

def main():
	r = 188013210689069300476163527325290628371
	obj = RNG(r)
	# o	bj = RNG(random.getrandbits(128))
	ans=[]
	ic(obj.seed[:10])
	out1 = ''.join([format(obj.next(ans), '016x') for i in range(64)])
	print(out1)
	ic(ans[:10])
	ans=[]
	ic(obj.seed[:10])
	out2 = ''.join([format(obj.next(ans), '016x') for i in range(64)])
	ic(ans[:10])
	print(out2)

	
	
	# cip = encrypt(bytes.fromhex(out1), FLAG)
	cip = {}
	cip['leak'] = out2
	return cip

if __name__ == '__main__':
	cip = main()
	# pickle.dump(cip, open('enc2.pickle', 'wb'))