from sage.all import log


log2 = lambda val: f"{float(RR(log(abs(val),2))):.3f}"
proof.arithmetic(False)

from random import randint, seed
# seed(101)

p = q = 1
while p % 3 != 2:
    p = next_prime(randint(1,2**512))
while q % 3 != 2:
    q = next_prime(randint(1,2**512))

n = p*q
R = Zmod(p*q)
Mx = R.random_element()
My = R.random_element()
b = My**2 - Mx**3

Ep = EllipticCurve(GF(p), [0,b])
Eq = EllipticCurve(GF(q), [0,b])
E = EllipticCurve(R, [0,b])

Ecard = Ep.cardinality()*Eq.cardinality()

#r = random_prime((p^^q)>>100)
r = next_prime(randint(0, (p^^q)>>100))
s = inverse_mod(r, Ecard)

print("   s", log2(s))
print("   r", log2(r))
print("rmax", log2((p^^q)>>100))

spt = s*E(Mx, My)
randpt = randint(0, Ecard)*E(Mx, My)

from hashlib import sha256
from Crypto.Util.number import bytes_to_long, long_to_bytes
flag = b"RCTF{Copper5mith_M3thod_f0r_ECC}"
v = r^^(bytes_to_long(sha256(long_to_bytes(Mx)).digest())^^bytes_to_long(flag))<<256