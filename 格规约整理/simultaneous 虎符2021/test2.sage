def gen_prime(size):
    p = random_prime(1 << size, lbound=1 << (size-1))
    while p % 3 != 2:
        p = random_prime(1 << size, lbound=1 << (size-1))

    q = random_prime(1 << size, lbound=1 << (size-1))
    while q % 3 != 2:
        q = random_prime(1 << size, lbound=1 << (size-1))

    if q > p:
        p, q = q, p

    return ZZ(p), ZZ(q)


SIZE = 512
p, q = gen_prime(SIZE)
n = p * q
y = random_prime(floor(n**0.373), proof=False)
a = int(((p-q) * round(n ** 0.25) * y) // (3 * (p + q)))
b = (((p-q) * round(n ** 0.25) * y) / (3 * (p + q)))

zbound =  int(((p-q) * round(n ** 0.25) ) // (3 * (p + q)))
print(a)
print('================')
print(b-a)
print(zbound)
