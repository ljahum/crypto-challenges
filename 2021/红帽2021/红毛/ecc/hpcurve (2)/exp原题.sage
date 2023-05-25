from binascii import unhexlify, hexlify
from itertools import permutations

p = 10000000000000001119
k = GF(p)
kc = k.algebraic_closure()

p = 10000000000000001119
R.<x> = GF(p)[]
y=x
f = y + y^7
C = HyperellipticCurve(f, 0)
J = C.jacobian()


msg_prefix = b"Hello! The flag is: hxp{"
# msg_prefix = b'aaaaaaaaaaaaaaaaaaaaflag'

# with open("output.txt") as f:
#     content = unhexlify(f.read().strip())
content = bytes.fromhex('9e6ab3ff11232e0c5d7ce94d3538fb73e5139749a1247b0b5c2221e2593efd58ddbdae697191781914c94f8d40')

bs = []
for c, m in zip(content, msg_prefix):
    # Do the XOR, obtain k
    b = c^^m
    print(b)
    bs.append(b)

u0 = int.from_bytes(bytes(bs[:8]), byteorder="little")
u1 = int.from_bytes(bytes(bs[8:16]), byteorder="little")
u2 = int.from_bytes(bytes(bs[16:24]), byteorder="little")
print(hex(u0), hex(u1), hex(u2))

ps = x^3 + u2 * x^2 + u1 * x + u0  # TODO: this ordering might be the other way around.
aps_roots = ps.roots(ring=kc, multiplicities=False)
x0, x1, x2 = aps_roots

A = Matrix(((x0^2, x0, kc(1)), (x1^2, x1, kc(1)), (x2^2, x2, kc(1))))
Y = vector((x0^7 + x0, x1^7 + x1, x2^7 + x2))
Ys = vector((-Y[0].sqrt(), -Y[1].sqrt(), -Y[2].sqrt())) # TODO: Maybe the other sqrt?

v = A.solve_right(Ys)
print(v)
v0 = int(str(v[0])).to_bytes(8, byteorder="little")
v1 = int(str(v[1])).to_bytes(8, byteorder="little")
v2 = int(str(v[2])).to_bytes(8, byteorder="little")

for a0, a1, a2 in permutations((v0, v1, v2)):
    cs = []
    q = bytes(bs) + a0 + a1 + a2
    print(q)
    for i in range(len(content)):
        b = content[i]^^q[i%len(q)]
        cs.append(chr(b))
    # for c, m in zip(content, q):
    #     # Do the XOR, obtain k
    #     b = c^^m
    #     cs.append(chr(b))
    print("".join(cs))