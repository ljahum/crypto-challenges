

# This file was *autogenerated* from the file test.sage
from sage.all_cmdline import *   # import sage library

_sage_const_256 = Integer(256); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_128 = Integer(128)
from icecream import *
from Crypto.Util.number import *
nbit = _sage_const_256 //_sage_const_2 
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
_s = p ^ ((_sage_const_2  ** (nbit - _sage_const_1 )) + _sage_const_2  ** (nbit // _sage_const_2 ))
q = next_prime(_sage_const_2  * _s + _sage_const_1 )
print(bin(p)[_sage_const_2 :].rjust(_sage_const_128 ,'0'))
print(bin(_s)[_sage_const_2 :].rjust(_sage_const_128 ,'0'))
print(bin(q)[_sage_const_2 :].rjust(_sage_const_128 ,'0'))

