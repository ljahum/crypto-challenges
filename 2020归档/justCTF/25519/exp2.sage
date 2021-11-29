from os import environ
from icecream import *
environ['PWNLIB_NOTERM'] = 'True'
from pwn import remote
from hashlib import sha256

ha = lambda x: x if isinstance(x, int) or isinstance(x, Integer) else product(x.xy())
hashs = lambda *x: int.from_bytes(sha256(b'.'.join([b'%X' % ha(x) for x in x])).digest(), 'little') % p

def hashp(x):
    x = hashs((x))
    while True:
        try:
            return E.lift_x(x)
        except:
            x = hashs((x))

E = EllipticCurve(GF(2^255 - 19), [0, 486662, 0, 1, 0])
p = E.order()
ZmodP = Zmod(p)
G = E.lift_x(9)

conn = remote('0.0.0.0', 10001)

print(conn.recvuntil('>'))
conn.sendline('2')

data = conn.recvline().decode().strip()
x = int(data.split()[0])
P = x*G
m = int(data.split()[-1])
print(data)
ic(m)
# input()


wins = 0
while wins < 8:
    c = randint(1, p)
    e = hashs(m, c*G, c*G)
    if not e & 1: 
        print('try again')
        continue
    s = c - e*x
    I = inverse_mod(e, p)*(c*G - s*hashp(P))
    print(I.xy()[0])
    print(I.xy()[1])
    input()
    print(conn.recvuntil('>'))
    conn.sendline('1')
    
    conn.sendlineafter('I (x): ', str(I.xy()[0]))
    conn.sendlineafter('I (y): ', str(I.xy()[1]))
    conn.sendlineafter('e: ', str(e))
    conn.sendlineafter('s: ', str(s))
    print(conn.recvline())
    wins += 1
    input()

print(conn.recvuntil('>'))
conn.sendline('3')
print(conn.recv(1024))