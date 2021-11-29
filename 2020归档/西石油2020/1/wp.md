# happy

exp

```python
from gmpy2 import *
from Crypto.Util.number import *
#q + q*p^3 =467962068718552895211162459665195309477537820950314984120501297653251626108029252766706321468050831941604717101473973050
#qp + q *p^2 = 565793545980404021917176171737381087790180558655380403750360123494827821905901954270664682
x1 = 1285367317452089980789441829580397855321901891350429414413655782431779727560841427444135440068248152908241981758331600586

x2 = 1109691832903289208389283296592510864729403914873734836011311325874120780079555500202475594


x3 = x1+3*x2
x4 = x2**3
x5 = x4//x3
a = 1
b = -x1
c = x5
delta = iroot(b**2-4*a*c, 2)[0]
q = (-b-delta)//(2*a)
q = 827089796345539312201480770649
x5 = x5//(q**2)
p = iroot(x5, 3)[0]

c = 0x7a7e031f14f6b6c3292d11a41161d2491ce8bcdc67ef1baa9e
e = 0x872a335

n = p*q
phi = (p-1)*(q-1)
d = invert(e, phi)
print(long_to_bytes(pow(c, d, n)))
```

# Yusa的密码学课堂 CBC第一课


```python
from pwn import *
from Crypto.Util.number import *
io = remote('das.wetolink.com', 42888)
name = bytes_to_long(b'admin===========')
m1 = bytes_to_long(b'yusa'*4)

m2 = bytes_to_long(b'================')

s = io.recv(1024)
io.sendline(b'1')
io.sendline(b'=================')
io.recvuntil(b'token(in hex): ')
token = io.recvline(b'\n')[:-1]

print(token)
token = bytes.fromhex(token.decode())
iv = bytes_to_long(token[:16])
c1 = bytes_to_long(token[16:32])
c2 = bytes_to_long(token[32:])
c3 = name ^ (c1 ^ m2)
c = long_to_bytes(c1)+long_to_bytes(c3)
token2 = long_to_bytes(iv) + c
print('token2 = ', token2.hex())  # write
io.sendline(b'2')
s = io.recv(1024)
print(s)
io.sendline(bytes(token2.hex(),encoding='utf-8'))
s = io.recv(1024)
print(s)
s = io.recvuntil(b'Hello, ')
print(s)
m3 = io.recvline(b'\n\n1. ')[:-1]
print(m3)
m3 = bytes_to_long(m3)


iv3 = long_to_bytes(m1 ^ (c1 ^ m3))

c = long_to_bytes(c3)+long_to_bytes(c2)

token3 = iv3 + c
# print(token3)
print('---------------------------------------')
print('token3 = ', token3.hex())
s = io.recv(1024)
print(s)
io.sendline(b'2')
# input()
io.recvuntil(b'Your token(in hex): ')
io.sendline(bytes(token3.hex(), encoding='utf-8'))

s = io.recv(1024)
print(s)
s = io.recv(1024)
print(s)

```