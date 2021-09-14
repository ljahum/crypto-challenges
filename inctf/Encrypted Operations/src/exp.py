from pwn import *
from pwnlib.util.iters import random_permutation
#  crypto.challenge.bi0s.in 1221

data = """9 0 0 0
*
1
y

189 0 0 0
+
1
n

189 0 0 0
+
1
n
+

20 0 0 0
*
1
y

830 0 0 0
+
1
n

0 0 0 0 0
>
1
n

-1 -1 -1 -1 -1
*
1
n

-1 -1 -1 -1 -1
*
1
n

"""
io = remote('crypto.challenge.bi0s.in',1221)
io.sendline(data)
io.recvuntil('flag')
io.recvuntil('flag')
buf = io.recv(2048)
if(b'inctf' in buf):
    print(buf)
    exit(0)
# inctfi{m4st3r_0f_Encrypt3d_0p3r4t1on5_B3c0m3_u_H4v3!!}