from random import choice
from Crypto.Util.number import isPrime, getPrime, sieve_base as primes

def get_prime(bits):
    while True:
        p = 1
        while p.bit_length() < bits:
            p *= choice(primes)
        if isPrime(p + 1):
            return p + 1
'''
a*a*a...a  = p - 1
'''

def init_public_key():
    N = get_prime(2048) * get_prime(2048)
    E = getPrime(64)
    rsa = RSA.construct((N, E))
    with open('public.key', 'wb') as f:
        f.write(rsa.exportKey())
p = get_prime(32)
q = get_prime(64)
n = p*q
print(p)
print(q)
print(n)