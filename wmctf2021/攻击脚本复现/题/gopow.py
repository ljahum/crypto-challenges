from pwn import *  
from itertools import product
# from MyRE import *
import string

# nc 47.104.85.225 49803
# nc 47.104.85.225 49823
io = remote('47.104.243.99',10001)

def pow1():
    String = string.ascii_letters+string.digits
    io.recvuntil('[+] sha256(XXXX+')
    s2 = io.recvuntil(') == ')[:-5]
    HASH = io.recvuntil('\n')[:-1]
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
            print(io.recvuntil('[+] Plz tell me XXXX:'))
            print(s1)
            io.sendline(s1)
            return
pow1()
io.interactive()

