#!/usr/bin/env python
from Crypto.Util.number import *
from hashlib import sha512,md5
from os import urandom
import random

def hash(message):
	return int(sha512(message).hexdigest(), 16)

def key_gen():
	q = getPrime(256)
	while True:
		p = random.getrandbits(256)*q + 1
		if isPrime(p):
			print(p.bit_length())
			break
	while True:
		g = pow(random.randrange(1, p-1), (p-1)/q, p)
		if g != 1:
			break
	x = random.randrange(1, q)
	y = pow(g, x, p)
	pubkey = (p, q, g, y)
	privkey = x
	return pubkey, privkey

def sign(message, pubkey, privkey):
	p, q, g, y = pubkey
	x = privkey
	k = pow(y, x, g) * random.randrange(1, 512) % q
	r = pow(g, k, p) % q
	s = inverse(k, q) * (hash(message) + x * r) % q
	return r, s

def verify(message, signature, pubkey):	
	
	p, q, g, y = pubkey
	r, s = signature
	if not (0 < r < q) or not (0 < s < q):
		return False
	w = inverse(s, q)
	u1 = (hash(message) * w) % q
	u2 = (r * w) % q
	v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
	return v == r

pubkey, privkey = key_gen()
print(pubkey)

message1 = urandom(16).encode('hex')
signature1 = sign(message1, pubkey, privkey)
print(message1,signature1)
print(verify(message1, signature1, pubkey))

message2 = urandom(16).encode('hex')
signature2 = sign(message2, pubkey, privkey)
print(message2,signature2)
print(verify(message2, signature2, pubkey))

flag = 'flag{'+md5(long_to_bytes(privkey)).hexdigest()+'}'
