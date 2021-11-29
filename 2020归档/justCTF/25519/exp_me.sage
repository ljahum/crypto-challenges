# sage
# -*- encoding: utf-8 -*-
'''
@File    :   exp_me.sage
@Time    :   2021/02/10 15:05:20
@Author  :   ljahum 
@Contact :   roomoflja@gmail.com
@Desc    :   None
'''

# code here

from os import environ
environ['PWNLIB_NOTERM'] = 'True'
from pwn import remote
from hashlib import sha256


ha = lambda x: x if isinstance(x, int) or isinstance(x, Integer) else product(x.xy())


hashs = lambda *x: int.from_bytes(
    sha256(b'.'.join([b'%X' % ha(x) for x in x])).digest(), 'little') % p


def hashp(x):
    x = hashs((x))
    while True:
        try:
            return E.lift_x(x)
        except:
            x = hashs((x))


E = EllipticCurve(GF(2 ^ 255 - 19), [0, 486662, 0, 1, 0])
p = E.order()
ZmodP = Zmod(p)
G = E.lift_x(9)
cn = remote('0.0.0.0', 10001)
data = cn.recvline().decode().strip()
print(data)
x = int(data.split()[0])
P = x*G
m = int(data.split()[-1])

tot =0 
while tot <8:
    a = randint(1, p)
    b = randint(1, p)
    aG = a*G
    bG = b*G
    e = hashs(m, aG, bG)
    if not e & 1: 
        print('try again')
        continue
    s =  a - e*x
    e_inv = inverse_mod(e,p)
    I = e_inv*(bG - s*hashp(P))
    Ix = I.xy()[0]
    Iy = I.xy()[1]
    cn.sendlineafter('I (x): ', str(Ix))
    cn.sendlineafter('I (y): ', str(Iy))
    cn.sendlineafter('e: ', str(e))
    cn.sendlineafter('s: ', str(s))
    cn.recvline()
    tot += 1
print(cn.recvall())
