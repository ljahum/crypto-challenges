from functools import reduce

from flag import flag


def encrypt(m, e, n):
    n = int(n)
    size = n.bit_length() // 2
    m_low = m & ((1 << size) - 1)
    m_high = (m >> size)

    b = (m_low**2 - m_high**3) % n
    EC = EllipticCurve(Zmod(n), [0, b])

    return (EC((m_high, m_low)) * e).xy()

def decrypt(c, d, n):
    n = int(n)
    size = n.bit_length() // 2

    c_high, c_low = c
    b = (c_low**2 - c_high**3) % n
    EC = EllipticCurve(Zmod(n), [0, b])
    m_high, m_low = (EC((c_high, c_low)) * d).xy()
    m_high, m_low = int(m_high), int(m_low)

    return (m_high << size) | m_low

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
HINTSIZE = 96

assert len(flag) == 42
flag = int.from_bytes(flag, "big")

masks = [randint(1 << (SIZE-1), 1 << SIZE) for _ in range(3)]
masked_flag = reduce(lambda a, b: a ^^ b, masks, flag)


count = 0
ciphertexts = []
x = random_prime(floor((1<<(2*SIZE-2))**0.373), proof=False)
while count < 3:
    try:
        p, q = gen_prime(SIZE)
        n = p * q

        y = random_prime(floor(n**0.373), proof=False)
        zbound = -1 * int(((p-q) * round(n ** 0.25) * y) // (3 * (p + q)))

        z_ = zbound + ((p + 1)*(q + 1)*y - zbound) % x
        e = ((p + 1) * (q + 1) * y - z_) // x

        assert (e*x - y*(p+1)*(q+1) == -z_)
        assert (abs(z_) < abs(zbound))
        assert (gcd(x, y) == 1)

        d = inverse_mod(e, (p+1)*(q+1))
        c = encrypt(masks[count], e, n)
        assert decrypt(c, d, n) == masks[count]

        ciphertexts.append({
            "n": n,
            "e": e,
            "c": c,
            "hint": p & ((1<<HINTSIZE)-1)
        })
        count += 1
    except KeyboardInterrupt:
        break
    except ZeroDivisionError:
        pass


print("masked_flag = ", masked_flag)
print("ciphertexts = ", ciphertexts)
