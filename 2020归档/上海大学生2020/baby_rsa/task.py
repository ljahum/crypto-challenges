#!/usr/bin/env python
from Crypto.Util.number import *
from secret import FLAG,BIT
p = getPrime(BIT)
q = getPrime(BIT)
n = p*q

m = bytes_to_long(FLAG)
n=p*q
e = 65537
c = pow(m,e,n)

print('n={}'.format(n))
print('c={}'.format(c))


p1 = getPrime(BIT)
q1 = getPrime(BIT)
n1 = p1*q1
e1 = 264769
c1 = pow(p,e1,n1)
print('n1={}'.format(n1))
print('c1={}'.format(c1))
hint1 = pow(233*p1+q1,123,n1)
hint2 = pow(p1+q1,321,n1)
print('hint1={}'.format(hint1))
print('hint2={}'.format(hint2))


p2 = getPrime(BIT)
q2 = getPrime(BIT)
n2 = p2*q2
e2 = 467237
c2 = pow(p,e2,n2)
hint3 = (p2^q2+23333)*(p2**2+q2**2)
print('n2={}'.format(n2))
print('c2={}'.format(c2))
print('hint3={}'.format(hint3))