from sage.modules.free_module_integer import IntegerLattice
from Crypto.Cipher import AES
from base64 import b64encode
from hashlib import *
# from secret import flag
import signal

flag = b'ljahum.no.1'
n = 75
m = 150
r = 10
N = 126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109

def gen(n, m, r, N):
    t1 = [ZZ.random_element(-2^15, 2^15) for _ in range(n*m)]
    t2 = [ZZ.random_element(N) for _ in range(r*n)]
    B = matrix(ZZ, n, m, t1)
    L = IntegerLattice(B)
    A = matrix(ZZ, r, n, t2)
    # print(B)
    C = (A * B) % N
    return L, C

def pad(s):
    return s + (16 - len(s) % 16) * b"\x00"

output = open("output.txt","w")
#token = input("team token:").strip().encode()
L, C = gen(n, m, r, N)
print(C,file = output)
key = sha256(str(L.reduced_basis[0]).encode()).digest()
aes = AES.new(key, AES.MODE_ECB)
ct = b64encode(aes.encrypt(pad(flag))).decode()
print(ct,file = output)
# vd3NeTpW5OgS7vTz6ApK+A==