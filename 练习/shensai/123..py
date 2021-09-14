from libnum import *

def invp(a,b,c):
    x = (invmod(a,b)*c)%b
    return x
    