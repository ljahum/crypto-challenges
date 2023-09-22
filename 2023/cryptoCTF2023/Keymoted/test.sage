from icecream import *
from Crypto.Util.number import *
nbit = 256//2
# def gen_koymoted(nbit):
# 	p = getPrime(nbit)
 
# 	a, b = [randint(1, p - 1) for _ in '__']
# 	Ep = EllipticCurve(GF(p), [a, b])
# 	tp = p + 1 - Ep.order()
# 	_s = p ^^ ((2 ** (nbit - 1)) + 2 ** (nbit // 2))
# 	q = next_prime(2 * _s + 1)

# 	Eq = EllipticCurve(GF(q), [a, b])
# 	n = p * q
# 	tq = q + 1 - Eq.order()
# 	e = 65537
# 	while True:
# 		if gcd(e, (p**2 - tp**2) * (q**2 - tq**2)) == 1:
# 			break
# 		else:
# 			e = next_prime(e)
# 	pkey, skey = (n, e, a, b), (p, q)
# 	return pkey, skey

# tmp = gen_koymoted(nbit)



p = getPrime(nbit)
_s = p ^^ ((2 ** (nbit - 1)) + 2 ** (nbit // 2))
q = next_prime(2 * _s + 1)
print(bin(p)[2:].rjust(128,'0'))
print(bin(_s)[2:].rjust(128,'0'))
print(bin(q)[2:].rjust(128,'0'))
