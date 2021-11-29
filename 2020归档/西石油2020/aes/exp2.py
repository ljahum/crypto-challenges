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
