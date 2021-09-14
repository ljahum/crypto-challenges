#!/usr/bin/env sage
import struct
from random import SystemRandom

p = 10000000000000001119
R.<x> = GF(p)[]
y=x
f = y + y^7
C = HyperellipticCurve(f, 0)
J = C.jacobian()

es = [SystemRandom().randrange(p**3) for _ in range(3)]
Ds = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]
q = []

def clk():
	global Ds,es
	Ds = [e*D for e,D in zip(es, Ds)]
	return Ds

def generate():
    
    u,v = sum(clk())
    rs = [u[i] for i in range(3)] + [v[i] for i in range(3)]
    assert 0 not in rs and 1 not in rs
    q = struct.pack('<'+'Q'*len(rs), *rs)
    return q


# flag = "flag{xx/xxxxx}"
# text = 'a'*62
text = 'Hello! The flag is: hxp{ez_P4rT_i5_ez__tL0Cm}'
t = b''
keys = generate()
# keys = b'\xa0\x8c\xf9\x1c\x02\xb2M5\xd5k\xad\xbb\x06\x9c+}\x8f\xa4\xfb;D\x1aQ\x15\xc0c\n\xdc\t\xfb\xdd\x16\xa2\x90u\x8b\r\xa9\x923\xd1K\x9a\xe9q\x01\xb2['

leng = len(keys)
i = 0
for x in text:
    a = keys[i%leng]
    b = ord(x)
    print(a,b)
    t += bytes([a^^b])
    i+=1
print(t.hex())
#for x,y in zip(RNG(),flag):

# e8e995706d936d61bd0e8ddd6afd4c5de6d7c11b2c62216ea519558c3d898949cba52aee77f6cd479d7bd9840c



