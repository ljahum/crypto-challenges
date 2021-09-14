from os import X_OK
from Crypto.Util.number import *
p = getPrime(1024)
t = getPrime(1024)
x = getPrime(1024)
key = getPrime(256)
y = (key + t*x )%p