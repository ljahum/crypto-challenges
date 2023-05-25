from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
from hashlib import sha256

flag = b'flag{Copper5mith_M3thod_f0r_ECC}'

p=getStrongPrime(512)
q=getStrongPrime(512)
R=Zmod(p*q)

Mx=R.random_element()
My=R.random_element()
b=My^2-Mx^3
E=EllipticCurve(R, [0,b])
Ep=EllipticCurve(GF(p), [0,b])
Eq=EllipticCurve(GF(q), [0,b])
Ecard=Ep.cardinality()*Eq.cardinality()
r=random_prime((p^^q)>>100)
s=inverse_mod(r, Ecard)

print((s,b))
print(s*E(Mx,My))
print(randint(0,Ecard)*E(Mx,My))
print(r^^(bytes_to_long(sha256(long_to_bytes(Mx)).digest())^^bytes_to_long(flag))<<256)
