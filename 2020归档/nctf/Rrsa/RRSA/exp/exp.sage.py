

# This file was *autogenerated* from the file exp.sage
from sage.all_cmdline import *   # import sage library

_sage_const_30003 = Integer(30003); _sage_const_1 = Integer(1); _sage_const_5 = Integer(5); _sage_const_4 = Integer(4); _sage_const_2 = Integer(2); _sage_const_3 = Integer(3); _sage_const_0 = Integer(0); _sage_const_0p355 = RealNumber('0.355'); _sage_const_0p4 = RealNumber('0.4')
import ljahum
from itertools import product
from hashlib import sha256
import string
import re
tcp = ljahum.remote('42.192.180.50', _sage_const_30003 , timeout=_sage_const_1 )
# 42.192.180.50 30003

def pow_():
    table = string.ascii_letters + string.digits
    s = tcp.recv_until(b'+')
    s = tcp.recv_until(b')')
    hash2 = s[:-_sage_const_1 ].decode()
    # hash2 = 'M56q8kgsDbmXCeeX'
    s = tcp.recv_until(b'== ')
    shastr = tcp.recv_until(b'Give')[:-_sage_const_5 ]
    print('xxxx +', hash2, '=', shastr.decode())

    for _ in product(table, repeat=_sage_const_4 ):
        hash1 = ''.join(_)
        guess = hash1+hash2
        if (sha256(guess.encode()).hexdigest()) == shastr.decode():
            print('yes')
            print('xxxx =', hash1)
            tcp.sendline(bytes(hash1, encoding='utf-8'))


def LLL():
    s = tcp.recv_until(b'key: ')
    e1 = tcp.recv_until(b', ')[:-_sage_const_2 ]
    N = tcp.recv_until(b'\n\n1')[:-_sage_const_3 ]
    # ----------------------------------------------
    tcp.sendline(b'4')
    tcp.recv_until(b'encflag: ')
    cipher = tcp.recv_until(b'\n\n1')[:-_sage_const_3 ]
    # -----------------------------------------------
    tcp.sendline(b'3')
    tcp.recv_until(b'My new public key: ')
    e2 = tcp.recv_until(b',')[:-_sage_const_1 ]
    # -------------------------------------------------
    tcp.sendline(b'3')
    tcp.recv_until(b'My new public key: ')
    e3 = tcp.recv_until(b',')[:-_sage_const_1 ]
    e1 = int(e1)
    e2 = int(e2)
    e3 = int(e3)
    N = int(N)
    cipher = int(cipher)
    print('e1', e1)
    print('e2', e2)
    print('e3', e3)
    print('N',N)
    print('cipher',cipher)

    # -------------------------------------------
    B = Matrix([
        [_sage_const_1 , -N, _sage_const_0 , N ** _sage_const_2 , _sage_const_0 , _sage_const_0 , _sage_const_0 , -N ** _sage_const_3 ],
        [_sage_const_0 , e1, -e1, -e1*N, -e1, _sage_const_0 , e1*N, e1*N ** _sage_const_2 ],
        [_sage_const_0 , _sage_const_0 , e2, -e2*N, _sage_const_0 , e2 * N, _sage_const_0 , e2 * N ** _sage_const_2 ],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , e1*e2, _sage_const_0 , -e1*e2, -e1*e2, -e1*e2*N],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , e3, -e3*N, -e3*N, e3*N ** _sage_const_2 ],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , e1*e3, _sage_const_0 , -e1*e3*N],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , e2*e3, -e2*e3*N],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , e1*e2*e3],


    ])

    x2 = _sage_const_0p355 
    x3 = _sage_const_0p4 

    D = Matrix([
        [int(N ** (_sage_const_3 /_sage_const_2 )), _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 ],
        [_sage_const_0 ,   N, _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 ],
        [_sage_const_0 , _sage_const_0 , int(N ** (x2+(_sage_const_3 /_sage_const_2 ))), _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 ],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , int(N ** (_sage_const_1 /_sage_const_2 )), _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 ],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , int(N ** (x3+(_sage_const_3 /_sage_const_2 ))), _sage_const_0 , _sage_const_0 , _sage_const_0 ],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , int(N ** (x3+_sage_const_1 )), _sage_const_0 , _sage_const_0 ],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , int(N ** (x3+_sage_const_1 )), _sage_const_0 ],
        [_sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_0 , _sage_const_1 ]
    ])
    res = B*D
    print(type(res))
    lll = res.LLL()  # v2
    y = lll[_sage_const_0 ]
    inv = res.inverse()
    x = y*inv

    # ---------------------------------------
    phi = int(e1*int(x[_sage_const_1 ]))//int(x[_sage_const_0 ])
    print('phi', phi)
    print('-----------------------')

    bezout = xgcd(e1, phi)
    d1 = Integer(mod(bezout[_sage_const_1 ], phi))
    print('d1:', d1)
    plain1 = pow(cipher, d1, N)
    # -------------------------------------
    flag = (int(plain1))
    print("flag int ", flag)
    print(bytes.fromhex(hex(flag)[_sage_const_2 :]))
    print('---------------------------------')
    # ----------------------------------------------

    d = inverse_mod(e2, phi)
    flag = pow(cipher, d, N)
    print(flag)
    print(hex(flag))
    print(bytes.fromhex(hex(flag)[_sage_const_2 :]))


def main():
    pow_()
    LLL()
    return


if __name__ == '__main__':
    main()


'''
4f8c9bf9a612ebb7bfcc0fc2e3ba9739c8e43097e6f4ac5d82afe3194d5f2394
9b3fb9358019b7de093fe4690cc1478981c255b490137cfa73d3ef35bc5873e5
XXXX+RkURKfd2TW7pJAGD
     5zZ9YA5sngQSjEjg
     ssvaPxwkqD7ishiF
     LsqXbbiqbJQT4BC9


'''

