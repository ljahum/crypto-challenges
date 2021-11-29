#!/use/bin/env sage
from icecream import *
from sys import exit
from hashlib import sha256
from Crypto.Util.number import *
from secret import FLAG

ec = EllipticCurve(GF(2**255-19), [0, 486662, 0, 1, 0])
p = ec.order()
ZmodP = Zmod(p)
G = ec.lift_x(9)

ha = lambda x: product(x.xy()) if type(x)==type(G) else x
hashs = lambda *x: int.from_bytes(sha256(b'.'.join([b'%X' % ha(x) for x in x])).digest(), 'little') % p


def hashp(x):
    x = hashs((x))
    while True:
        try:
            return ec.lift_x(x)
        except:
            x = hashs((x))


def keygen():
    x = randint(1, p-1)
    P = x * G
    return x, P


def verify(signature, P, m):
    I, e, s = signature
    tmp = hashs(m, s*G + e*P, s*hashp(P) + e*I)
    return e == tmp

menu="""
[1] log in
[2] gifts to you :-)
[3] get secret"""

if __name__ == "__main__":
    m = randint(1, p-1)
    x, P = keygen()
    spent = set()
    while 1:
        print(menu)
        op = input('>')
        if(op=='1'):
            
            Ix = int(input('I (x): '))
            Iy = int(input('I (y): '))
            I = ec(Ix, Iy)
            e = int(input('e: '))
            s = int(input('s: '))
            
            if verify((I, e, s), P, m) and I not in spent:
                print('ok')
                spent.add(I)
            else:
                print('nope')
        if(op=='2'):
            print(x, P,m)
        if(op=='3'):
            print(f'Completion:{len(spent)}/8')
            if(len(spent)==8):
                print('You have a great understanding on signature !')
                print(FLAG)
            else:
                print('You don\'t have enough permissions')
    