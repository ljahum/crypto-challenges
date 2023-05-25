
import struct
from random import SystemRandom
# from icecream import *

from rich import *
# ----------------------------
p = 10000000000000001119
R.<x> = GF(p)[]
y=x
f = y + y^7
print(f)
C = HyperellipticCurve(f, 0)
J = C.jacobian()

es = [SystemRandom().randrange(p**3) for _ in range(3)]


Ds = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]
q = []
print(es)
print(Ds)


def clk():
	global Ds,es
	Ds = [e*D for e,D in zip(es, Ds)]
	return Ds

def generate():
    print('=========generate=')
    u,v = sum(clk())
    print(u)
    print()
    print(v)
    for i in range(3):
        print(u[i])
    rs = [u[i] for i in range(3)] + [v[i] for i in range(3)]
    
    q = struct.pack('<'+'Q'*len(rs), *rs)
    print(q[0],q[1:])
    print(q)
    return rs
keys = generate()
print(len(keys))
print(keys)