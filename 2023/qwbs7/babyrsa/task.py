from Crypto.Util.number import isPrime, inverse, bytes_to_long
from random import getrandbits, randrange
from collections import namedtuple


Complex = namedtuple("Complex", ["re", "im"])

def complex_mult(c1, c2, modulus):
    return Complex(
        (c1.re * c2.re - c1.im * c2.im) % modulus,
        (c1.re * c2.im + c1.im * c2.re) % modulus,
    )

def complex_pow(c, exp, modulus):
    result = Complex(1, 0)
    while exp > 0:
        if exp & 1:
            result = complex_mult(result, c, modulus)
        c = complex_mult(c, c, modulus)
        exp >>= 1
    return result

def rand_prime(nbits, kbits, share):
    while True:
        p = (getrandbits(nbits) << kbits) + share
        if p % 4 == 3 and isPrime(p):
            return p

def gen():
    while True:
        k = getrandbits(100)
        pp = getrandbits(400) << 100
        qq = getrandbits(400) << 100
        p = pp + k
        q = qq + k
        if isPrime(p) and isPrime(q):
            break
    if q > p:
        p, q = q, p

    n = p * q
    lb = int(n ** 0.675)
    ub = int(n ** 0.70)
    d = randrange(lb, ub)
    e = inverse(d, (p * p - 1) * (q * q - 1))
    sk = (p, q, d)
    pk = (n, e)
    return pk, sk


pk, sk = gen()
n, e = pk
with open("flag.txt", "rb")as f:
    flag = f.read()

m = Complex(bytes_to_long(flag[:len(flag)//2]), bytes_to_long(flag[len(flag)//2:]))
c = complex_pow(m, e, n)
print(n)
print(e)
print(c)