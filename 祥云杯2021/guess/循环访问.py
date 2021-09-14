from Crypto.Util.number import (
    bytes_to_long,
    getPrime,
    long_to_bytes,
    getRandomNBitInteger,
)
import random
import hashlib
from math import gcd
from pwn import *  
from icecream import *
from MyRE import CatNum
from itertools import product
# from MyRE import *
# from rich import *
from rich.traceback import install
install()
# -----------------------------------

String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz" 
# nc 47.104.85.225 57811



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
        
def enc(n, g, m):
    while 1:
        r = random.randint(2, n - 1)
        if gcd(r, n) == 1:
            break
    c = (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)
    return c
def init():
    # pow1()
    # io.interactive()
    print(io.recvuntil('Step 1 - KeyGen. This is my public key.'))

    buf = io.recvuntil('Step ')
    ans = CatNum(buf)
    n,g = int(ans[0]),int(ans[1])
    ic(n)
    ic(g)
    
    return n,g
# =====================================
key0={132, 134, 264, 266, 403, 921, 666, 922, 158, 291, 419, 805, 167, 169, 810, 299, 309, 697, 570, 827, 444, 189, 830, 957, 449, 967, 715, 338, 980, 981, 731, 603, 352, 993, 618, 885, 374, 504, 379}
key1={898, 132, 261, 773, 134, 264, 393, 266, 525, 142, 145, 403, 149, 666, 154, 922, 158, 415, 291, 421, 805, 807, 167, 937, 810, 299, 553, 169, 430, 819, 821, 951, 953, 698, 570, 444, 957, 827, 189, 447, 449, 962, 322, 830, 582, 967, 200, 712, 715, 716, 588, 591, 340, 980, 981, 471, 731, 603, 349, 352, 353, 738, 993, 618, 110, 751, 879, 367, 885, 374, 504}

def get_index(k):
    if(k in key0):
        return '0'
    else:
        return '1'

def oracle(n,g):
    buf = io.recvuntil('round')
    round = io.recvuntil('Step 1')
    ic(round)
    print(io.recvuntil('Please give me one decimal ciphertext.\n'))
    c = enc(n,g,123321123321)
    io.sendline(str(c))
    print(io.recvuntil('Step 3'))
    print(io.recvline())
# s3
    m1 =  787
    m2 =  929
    io.sendline(str(m1))
    print(io.recvline())
    io.sendline(str(m2))
    print(io.recvline())
    print(io.recvuntil('This is a ciphertext.\n'))
    buf = io.recvline()
    ans = CatNum(buf)
    c1 = int(ans[0])
    # print(buf,c1)
    # init


    x1 = enc(n,g,787)
    c1x1 = pow(c1,m1,n**2)
    # ic(c1x1)
    io.sendline(str(c1x1))

    print(io.recvuntil('This is the corresponding plaintext.\n'))
    buf = io.recvline()
    print(ans)
    ans = CatNum(buf)
    tmp = int(ans[0])
    print(io.recvuntil('-> c0 , m1 -> c1)?\n'))
    k = (tmp)//(m1*m2*m1)
    ic(k)
    _01 = get_index(k)
    io.sendline(_01)
    res = io.recvline()
    print(res)
    # io.interactive()
    return res,k
    
time=0
io = remote('0.0.0.0',10001)      
for i in range(100):
    
    
    
    n,g = init()
    res,k = oracle(n,g)

    if(b'Sorry' in res):
        print(f'{k}:0')
        key0.add(k)
        time=0
        io.close()
        io = remote('0.0.0.0',10001)        
    else:
        print(f'{k}:1')
        key1.add(k)
        time+=1
    if(time==32):
        print('get it')
        io.recv(2048)    
        exit()
    
    # sleep(1)
    print(f'key0={key0}')
    print(f'key1={key1}')
    print(time)
    # (key1)
    
        
    # input()
    
