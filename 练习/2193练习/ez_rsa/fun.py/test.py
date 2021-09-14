from random import *
from hashlib import *
from Crypto.Util.number import *

def get_modulus(bits):
    
    base = getrandbits(bits)
    p,q = base,base
    
    while not isPrime(p):
        p+=getrandbits(bits//4)
        
    while not isPrime(q):
        q+=getrandbits(bits//8)
    print(len(bin(p-base))-2) # 
    print(len(bin(base))-2) # 2047
    return p,q,p*q

p,q,N=get_modulus(2048)
