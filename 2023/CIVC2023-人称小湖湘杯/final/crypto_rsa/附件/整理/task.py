from Crypto.Util.number import *
from flag import flag

p1 = getPrime(512)
q1 = getPrime(512)
n1 = p1 * q1

e = 65537

p2 = getPrime(1024)
q2 = getPrime(1024)
n2 = p2 * q2

leak1 = (p2+q2) >> 400
leak2 = (p1 & ((1 << 350) - 1)) >> 5

enc = pow(leak2,e,n2)
c = pow(bytes_to_long(flag),e,n1)
f = open(f'output.txt','w')
f.write(f'n1 = {n1}\n')
f.write(f'n2 = {n2}\n')
f.write(f'leak1 = {leak1}\n')
f.write(f'enc = {enc}\n')
f.write(f'c = {c}')
f.close()