import itertools
import struct

p = 10000000000000001119

R.<x> = GF(p)[]; y=x
f = y + y^7
C = HyperellipticCurve(f, 0)
J = C.jacobian()
Ds = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]

enc = bytes.fromhex('66def695b20eeae3141ea80240e9bc7138c8fc5aef20532282944ebbbad76a6e17446e92de5512091fe81255eb34a0e22a86a090e25dbbe3141aff0542f5')
known_pt = ('a'*20+'flag').encode()

rng_output = bytes(e^^m for e,m in zip(enc, known_pt))
print(len(rng_output))
blocks = [rng_output[i:i+8] for i in range(0, len(rng_output), 8)]
ui = [int.from_bytes(r, 'little') for r in blocks]
u = x^3 + ui[2]*x^2 + ui[1]*x + ui[0]

L = GF(p).algebraic_closure()
roots = [r[0] for r in u.change_ring(L).roots()]

RR.<zz> = PolynomialRing(L)
v = RR.lagrange_polynomial([(xi, f(xi).sqrt()) for xi in roots])
vi = [v.coefficients()[i].as_finite_field_element()[1] for i in range(3)]
vi = [(int(-c), int(c)) for c in vi]

for rs in itertools.product(*vi):
    q = struct.pack('<'+'Q'*len(rs), *rs)
    print(len(rng_output+q))
    flag = bytes(k^^m for k,m in zip(rng_output+q, enc))
    print(flag)