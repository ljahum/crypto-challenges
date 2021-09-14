from itertools import product
import struct
p = 10000000000000001119

K = GF(p)
R.<x> = K[]; y=x
f = y + prod(map(eval, 'yyyyyyy'))
C = HyperellipticCurve(f, 0)
J = C.jacobian()

def get_u_from_out(output, known_input):
    res = []
    for i in range(24):
        res.append(output[i]^^known_input[i])
    res = bytes(res)
    u0, u1, u2 = struct.unpack("<QQQ", res)
    u = x^3+x^2*u2+x*u1+u0
    return u
def get_v_from_u(u):
    Kbar = GF(p^6)
    Rbar.<t> = Kbar["t"]
    u2 = u.change_ring(Rbar)
    roots = [x[0] for x in u2.roots()]
    ys = []
    for root in roots:
        ys.append(f(root).sqrt(0,1))
    res = []
    for perm in product(range(2), repeat=3):
        poly = Rbar.lagrange_polynomial([(roots[i], ys[i][perm[i]]) for i in range(3)])
        if poly[0] in K:
            res.append(R(poly))
    return res

def try_decode(output, u, v):
    rs = [u[0], u[1], u[2], v[0], v[1], v[2]]
    otp = struct.pack("<QQQQQQ", *rs)
    plain = []
    for i in range(len(output)):
        plain.append(output[i]^^otp[i%len(otp)])
    return bytes(plain)


output2 = bytes.fromhex("fca3dd468e9f6f0e5e70046af7a6e4355fd8b15f8523980933dd9d1385884929fd0a67517c30fa7af82c07c45769d5216dd5721898f1c219c4753021b7f1bc6db2ee5c450a9efa4da6c40df913fb113bcd5193ba3135351e55db3ba23c")
output2 = bytes.fromhex("66def695b20eeae3141ea80240e9bc7138c8fc5aef20532282944ebbbad76a6e17446e92de5512091fe81255eb34a0e22a86a090e25dbbe3141aff0542f5")

known_input = b"Hello! The flag is: hxp{"
known_input = b"aaaaaaaaaaaaaaaaaaaaflag"
u = get_u_from_out(output2, known_input)
vs = get_v_from_u(u)
for v in vs:
    print(try_decode(output2, u, v))

# aaaaaaaaaaaaaaaaaaaaflag{1b82f60a-43ab-4f18-8ccc-97d120aae6fc}