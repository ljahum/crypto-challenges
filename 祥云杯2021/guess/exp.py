
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
    buf = io.recvuntil('round')
    round = io.recvuntil('Step 1')
    ic(round)
    io.recvuntil('KeyGen. This is my public key.')

    buf = io.recvuntil('Step ')
    ans = CatNum(buf)
    n,g = int(ans[0]),int(ans[1])
    ic(n)
    ic(g)
    
    return n,g
# =====================================

key0={130, 899, 903, 521, 142, 783, 530, 148, 416, 288, 550, 939, 427, 299, 558, 942, 685, 307, 566, 313, 577, 585, 718, 983, 349, 355, 611, 995, 614, 746, 751, 114, 498, 885, 119, 637, 638, 639}
key1={128, 129, 646, 647, 521, 780, 396, 526, 653, 400, 783, 530, 148, 918, 281, 158, 286, 416, 548, 550, 936, 810, 939, 427, 299, 558, 942, 944, 430, 307, 309, 566, 313, 186, 577, 201, 585, 461, 718, 333, 977, 727, 216, 983, 860, 355, 613, 614, 232, 745, 746, 877, 237, 241, 113, 114, 244, 885, 119, 888, 121, 123, 637, 638, 639}
def get_index(k):
    if(k in key0):
        return '0'
    else:
        return '1'

def oracle(n,g):
    
    io.recvuntil('Please give me one decimal ciphertext.\n')
    c = enc(n,g,123321123321123321123321)
    io.sendline(str(c))
    io.recvuntil('Step 3')
    io.recvline()
# s3
    m1 =  787
    m2 =  929
    io.recvuntil('Give me m0.\n')
    io.sendline(str(m1))
    io.recvuntil('Give me m1.\n')
    io.sendline(str(m2))
    
    io.recvuntil('This is a ciphertext.\n')
    buf = io.recvline()
    ans = CatNum(buf)
    c1 = int(ans[0])
    # print(buf,c1)
    # init


    x1 = enc(n,g,787)
    c1x1 = pow(c1,m1,n**2)
    # ic(c1x1)
    io.sendline(str(c1x1))

    io.recvuntil('This is the corresponding plaintext.\n')
    buf = io.recvline()
    # print(ans)
    ans = CatNum(buf)
    tmp = int(ans[0])
    io.recvuntil('-> c0 , m1 -> c1)?\n')
    k = (tmp)//(m1*m2*m1)
    ic(k)
    _01 = get_index(k)
    io.sendline(_01)
    res = io.recvline()
    print(res)
    # io.interactive()
    return res,k
    
time=0
# nc 47.104.85.225 57811
io = remote('47.104.85.225',57811)     
pow1() 
for i in range(100):
    
    
    
    n,g = init()
    res,k = oracle(n,g)

    if(b'Sorry' in res):
        print(f'{k}:0')
        key0.add(k)
        time=0
        io.close()
        io = remote('47.104.85.225',57811)   
        pow1()      
    else:
        sleep(0.25)
        print(f'{k}:1')
        key1.add(k)
        time+=1
    if(time==32):
        print('get it')
        print(io.recv(2048))
        exit()
    
    
    print(f'key0={key0}')
    print(f'key1={key1}')
    print(time)
    
    # (key1)
    
        
    # input()
    
