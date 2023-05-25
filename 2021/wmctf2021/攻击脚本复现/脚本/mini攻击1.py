from base64 import b64decode,b64encode
from hashlib import blake2b
from pwn import *

from itertools import product
from block import *
import string
io = remote('0.0.0.0',10002)
def green(text):
    return f'\033[92m{text}\033[0m'
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
            print(io.recvuntil('[+] Can you find the secret through the easy encryption system?\n'))
            return



def menu():
    print(green(io.recvuntil('[-] ').decode()))
    




def getflagenc():
    menu()
    io.sendline('3')
    io.recvuntil('ciphertext: ')
    cip = io.recvline()[:-1]
    io.recvuntil('tag: ')
    tag = io.recvline()[:-1]
    cip = b64decode(cip)
    tag = b64decode(tag)
    C = Block(cip)
    T = Block(tag)
    return C,T

def encrypt(N:Block,M):
    
    menu()
    A = b'from baby'
    N = N.data
    M = M.data
    # io.interactive()
    M = b64encode(M).decode()
    N = b64encode(N).decode()
    
    io.sendline('1')
    
    
    print(io.recvuntil('[+] Please input your nonce\n[-] '))
    io.sendline(N)
    
    print(io.recvuntil('[+] Please input your message\n[-] '))
    io.sendline(M)
    
    io.recvuntil('ciphertext:')
    cip = io.recvline()[:-1]
    io.recvuntil('tag: ')
    tag = io.recvline()[:-1]
    cip = b64decode(cip)
    tag = b64decode(tag)
    cip = Block(cip)
    tag = Block(tag)
    return cip,tag

def decrypt(N,C,T,A):
    menu()
    io.sendline('2')
    N = N.data
    C = C.data
    T = T.data
    A = A.data
    N = b64encode(N)
    C = b64encode(C)
    T = b64encode(T)
    A = b64encode(A)
    print(io.recvuntil('[+] Please input your nonce\n[-] '))
    io.sendline(N)
    io.recvuntil('[+] Please input your ciphertext\n[-] ')
    io.sendline(C)
    io.recvuntil('[+] Please input your tag\n[-] ')
    io.sendline(T)
    io.recvuntil('[+] Please input your associate data\n[-] ')
    io.sendline(A)
    io.recvuntil('plaintext: ')
    msg = io.recvline()[:-1]
    msg = b64decode(msg)
    msg = Block(msg)
    return msg

# 以上为模板函数
# 以下为poc函数
def randomMapping(n):
    N = Block(b'a'*16)
    M = Block(b'b'*16) + Block.len(16) + Block(b'c'*16)
    C, T = encrypt(N, M)
    S = Block.zero()
    C_ = Block()
    T_ = M[n + 1] ^ C[n + 1]
    for i in range(n):
        C_ += C[i]
        S ^= M[i]
    C_ += (S ^ C[n] ^ Block.len(16))
    A = Block(b'')

    M_ = decrypt(N, C_, T_,A)

    # print(green(auth))
    S = Block.zero()
    for i in range(n):
        S ^= M[i]
    print(n)
    print(M_[n].data)
    L = (S ^ M_[n] ^ Block.len(16)).half(n + 1) 
    mappings = []
    for i in range(n):
        mappings.append((M[i] ^ L.double(i + 1), C[i] ^ L.double(i + 1)))

    return mappings

def specificMapping(Is):
    N, L = randomMapping(1)[0]

    n = len(Is)
    M = Block()
    for i in range(n):
        M += (Is[i] ^ L.double(i + 1))
    M += Block.zero()
    C, T = encrypt(N, M)
    Os = []
    for i in range(n):
        Os.append(C[i] ^ L.double(i + 1))
    return Os

def recovery(N,  C, T):
    L = specificMapping([N])[0]
    print(green(L.data))
    n = C.blocksize()
    L_ = L.double() ^ L.double(2)
    C[0], C[1] = C[1] ^ L_, C[0] ^ L_
    A = Block(b'')
    auth, M_ = decrypt(N, C, T,A)

    M_[0], M_[1] = M_[1] ^ L_, M_[0] ^ L_
    print(green(M_.data))


# pow1()
# def encrypt(N,M):
# def decrypt(N,C,T,A):

# N = Block(b'\x00'*16)
# C,T = getflagenc()
# recovery(N, C, T)




# welcome
# print(io.recvuntil('[+] Can you find the secret through the easy encryption system?\n'))



# N = Block(b'a'*16)
# M = Block(b'b'*16) + Block.len(16) + Block(b'c'*16)
N = Block.random(16)
M = Block.len(16) + Block(b'1'*15)

C,T = encrypt(N,M)
# ========================
M = Block.len(16) + Block(b'1'*15+b'\x01')

C_ = C[0] ^ Block.len(16)
T_ = M[1] ^ C[1]

A = Block(b'')

# =========================
M = decrypt(N,C_,T_,A)


print(M.data)
