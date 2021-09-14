from base64 import b64decode,b64encode
from pwn import *

from itertools import product
# from MyRE import *
import string

# welcome



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
    buf = io.recvuntil('[-] ')


def getflag():
    menu()
    io.sendline('3')
    io.recvuntil('ciphertext: ')
    cip = io.recvline()[:-1]
    io.recvuntil('tag: ')
    tag = io.recvline()[:-1]
    cip = b64decode(cip)
    tag = b64decode(tag)
    print(io.recv(1024))
    return cip,tag

def enc(N,M):
    menu()
    A = b'from baby'

    N = b64encode(N)
    M = b64encode(M)
    io.sendline('1')
    
    
    print(io.recvuntil('[+] Please input your nonce\n[-] '))
    io.sendline(N)
    
    io.recvuntil('[+] Please input your message\n[-] ')
    io.sendline(M)
    io.recvuntil('ciphertext: ')
    cip = io.recvline()[:-1]
    io.recvuntil('tag: ')
    tag = io.recvline()[:-1]
    cip = b64decode(cip)
    tag = b64decode(tag)
    # print(len(cip))
    # print(len(tag))
    return cip,tag

def dec(N,C,T,A):
    menu()
    io.sendline('2')
    
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
    return msg



io = remote('47.104.243.99',10001)
pow1()

N = b'0'*16
M = b'0'*16
A = b'from baby'
C,T = enc(N,M)
M = dec(N,C,T,A)


print(M)
    
io.interactive()

'''

if(choice == b'1'):
                try:
                    self.send(b'[+] Please input your nonce')
                    nonce = b64decode(self.recv())
                    self.send(b'[+] Please input your message')
                    message = b64decode(self.recv())
                    associate_data = b'from baby'
                    ciphertext, tag = self.encrypt(nonce, message, associate_data)
                    self.send(b"[+] ciphertext: " + b64encode(ciphertext))
                    self.send(b"[+] tag: " + b64encode(tag))
                except:
                    self.send(b"[!] ERROR!")
            elif(choice == b'2'):
                try:
                    self.send(b'[+] Please input your nonce')
                    nonce = b64decode(self.recv())
                    self.send(b'[+] Please input your ciphertext')
                    ciphertext = b64decode(self.recv())
                    self.send(b'[+] Please input your tag')
                    tag = b64decode(self.recv())
                    self.send(b'[+] Please input your associate data')
                    associate_data = b64decode(self.recv())
                    if associate_data == b'from admin':
                        self.send(b'[!] You are not admin!')
                        break
                    message = self.decrypt(nonce, ciphertext, tag, associate_data)
                    self.send(b'[+] plaintext: ' + b64encode(message))
                except:
                    self.send(b"[!] ERROR!")
'''