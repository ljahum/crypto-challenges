p = 199577891335523667447918233627928226021
E = EllipticCurve(GF(p), [1, 0, 0, 6745936378050226004298256621352165803, 27906538695990793423441372910027591553])
print(E)
G = E.gen(0)

priv = random_prime(2^128)
P1 = priv*G
flag = E.random_point()
key = random_prime(2^40)
P2 = key*G
key = key*P1
cipher = flag + key

with open('task.txt', 'w') as f:
    f.write("P1 = {}\n".format(P1))
    f.write("P2 = {}\n".format(P2))
    f.write("cipher = {}\n".format(cipher))

print("m", flag)
print("k", key)
print("(x2, y2)", key)