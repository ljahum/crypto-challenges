

# This file was *autogenerated* from the file asdasd.sage
from sage.all_cmdline import *   # import sage library

_sage_const_10000000000000001119 = Integer(10000000000000001119); _sage_const_0 = Integer(0); _sage_const_3 = Integer(3); _sage_const_1 = Integer(1); _sage_const_11 = Integer(11); _sage_const_22 = Integer(22); _sage_const_33 = Integer(33)
import struct
from random import SystemRandom

p = _sage_const_10000000000000001119 

R = GF(p)['x']; (x,) = R._first_ngens(1); y=x
f = y + prod(map(eval, 'yyyyyyy'))
C = HyperellipticCurve(f, _sage_const_0 )
J = C.jacobian()

class RNG(object):

    def __init__(self):
        self.es = [SystemRandom().randrange(p**_sage_const_3 ) for _ in range(_sage_const_3 )]
        self.Ds = [J(C(x, min(f(x).sqrt(_sage_const_0 ,_sage_const_1 )))) for x in (_sage_const_11 ,_sage_const_22 ,_sage_const_33 )]
        self.q = []

    def clk(self):
        self.Ds = [e*D for e,D in zip(self.es, self.Ds)]
        return self.Ds

    def __call__(self):
        if not self.q:
            u,v = sum(self.clk())
            rs = [u[i] for i in range(_sage_const_3 )] + [v[i] for i in range(_sage_const_3 )]
            assert _sage_const_0  not in rs and _sage_const_1  not in rs
            self.q = struct.pack('<'+'Q'*len(rs), *rs)
        print('q',self.q)
        r, self.q = self.q[_sage_const_0 ], self.q[_sage_const_1 :]
        print(r)
        return r

    def __iter__(self): return self
    def __next__(self): return self()

# flag = open('flag.txt').read().strip()
flag = 'hxp{ez_P4rT_i5_ez__tL0Cm}'
import re; assert re.match(r'hxp\{\w+\}', flag, re.ASCII)

text = f"Hello! The flag is: {flag}"

text = f"Hello! The flag is: {flag}"
print(bytes(k^m for k,m in zip(RNG(), text.encode())).hex())

