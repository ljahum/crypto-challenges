from Crypto.Util.number import *
from icecream import *

def next_prime(a):
    while not isPrime(a):
        a += 2
    return a
def get_prime(a):
    suffix = getPrime(368)
    return next_prime(a ** 2 + suffix + 1)


a = getPrime(512)
p = get_prime(a)
q = get_prime(getPrime(512))

ic(p)
ic(q)