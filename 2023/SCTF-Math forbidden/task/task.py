from Crypto.Util.number import *
from Crypto.Cipher import AES
import os
from flag import flag

secret = os.urandom(16)*2
sysKEY = os.urandom(8)
aeskey = os.urandom(16)
iv = os.urandom(16)

p = getPrime(256)
q = getPrime(256)
e = 0x10001
d = inverse(e,(p-1)*(q-1))

n = p*q

def aes_enc(m,key,iv):
    aes = AES.new(key,AES.MODE_CBC,iv)
    c =  aes.encrypt(m)
    return c
def aes_dec(c,key,iv):
    aes = AES.new(key,AES.MODE_CBC,iv)
    m =  aes.decrypt(c)
    return m
def add_to_16(key):
    padding = 16 - (len(key) % 16)
    key += bytes([padding])*padding
    return(key)

def unpadding(key):
    padding = key[-1]
    if(padding==0):
        return key,False
    for i in range(padding):
        if key[-i-1]!=padding:
            return key,False
    key = key[:-padding]
    return key,True

def check_token():
    print("input your token")
    print("key")
    print(">",end='')
    enc_key = input()
    
    print("IV")
    print(">",end='')
    iv = input()
    enc_key =  bytes.fromhex(enc_key)
    iv =  bytes.fromhex(iv)
    key_padding = aes_dec(enc_key,aeskey,iv)    
    
    dec_key,flag= unpadding(key_padding)
    
    if(flag==False):
        print("fake token")
    else:
        if(dec_key == sysKEY):
            print("0.0")
            print('N',hex(n))
            print('E',hex(e))
            print('c',pow(bytes_to_long(secret),e,n))
        else:
            print("0.0??")

def adminadmin():
    print("input n:")
    print(">",end='')
    n = input()
    print("input c:")
    print(">",end='')
    c = input()
    n = bytes.fromhex(n)
    c = bytes.fromhex(c)
    n = bytes_to_long(n)
    c = bytes_to_long(c)
    
    secret = pow(c,d,n)
    print("only admin can touch the answer[yes/no]")
    op1 = input()
    if(op1=='yes'):
        print("input admin password:")
        print(">",end='')
        password = input()
        
        adminKEY = bytes.fromhex(password)
        
        if adminKEY==sysKEY:    
            m = long_to_bytes(secret,64)
            
            print(m[:2].hex())

key_padding = add_to_16(sysKEY)
enc_key = aes_enc(key_padding,aeskey,iv)
print('your token',enc_key.hex(),iv.hex())


menu = """
1.check
2.admin
3.getflag
"""

while 1:
    print(menu)
    print(">",end='')
    op = input()
    
    if(op=='1'):
        check_token()
        continue
    if(op=='2'):
        adminadmin()
        continue
    if(op=='3'):
        print("oops! I forget to hide the backdoor!\n>",end='')
        
        tmp = bytes.fromhex(input())
        if(tmp==secret):
            print(flag)
        continue
    
    print("try again")
        
