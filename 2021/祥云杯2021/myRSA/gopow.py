from pwn import *  
from itertools import product
# from MyRE import *

String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz" 
# nc 47.104.85.225 49803
# nc 47.104.85.225 49823
io = remote('47.104.85.225',49823)

def pow1():
    io.recvuntil('?+')
    s2 = io.recvuntil(') ')[:-2]
    HASH = io.recvuntil('\n')[3:-1]
    print(s2)
    print(HASH)
    for i in product(String,repeat=4):
        s1 = ''.join(i)
        # print(s1.encode())\
        s1 = s1.encode()
        s0 = s1+s2
        # print(s0)
        HASH1 = hashlib.sha256(s0).hexdigest().encode()
        # print(HASH1)
        # input()
        if(HASH==HASH1):
            print(s1)
            io.sendline(s1)
            return
pow1()
io.interactive()

