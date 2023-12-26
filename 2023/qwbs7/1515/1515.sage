from para import m, n, q, v, flag
import json

Zq = IntegerModRing(q)

A0 = random_matrix(Zq, m-n, n)
A1515 = matrix.block(Zq, [[identity_matrix(ZZ, n)], [A0]])
u = random_vector(Zq, n)

print(A0)
print(u)

x = vector(ZZ, json.loads(input("Give me a list of numbers: ")))

if x * A1515 != u:
    print("Failed!", x * A1515)
    exit(0)
if x.norm().n() >= v:
    print("Failed!", v)
    exit(0)

print(flag)