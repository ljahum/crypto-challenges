

# This file was *autogenerated* from the file 生成数据.sage
from sage.all_cmdline import *   # import sage library

_sage_const_75 = Integer(75); _sage_const_150 = Integer(150); _sage_const_10 = Integer(10); _sage_const_126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109 = Integer(126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109); _sage_const_2 = Integer(2); _sage_const_15 = Integer(15); _sage_const_16 = Integer(16)
from sage.modules.free_module_integer import IntegerLattice
from base64 import b64encode
from hashlib import *
import signal

n = _sage_const_75 
m = _sage_const_150 
r = _sage_const_10 
N = _sage_const_126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109 

def gen(n, m, r, N):
    t1 = [ZZ.random_element(-_sage_const_2 **_sage_const_15 , _sage_const_2 **_sage_const_15 ) for _ in range(n*m)]
    t2 = [ZZ.random_element(N) for _ in range(r*n)]
    B = matrix(ZZ, n, m, t1)
    L = IntegerLattice(B)
    A = matrix(ZZ, r, n, t2)
    save(B,'orignal_b.sobj')
    C = (A * B) % N
    return L,B, C

def pad(s):
    return s + (_sage_const_16  - len(s) % _sage_const_16 ) * b"\x00"

output = open("output.txt","w")

#token = input("team token:").strip().encode()
L, B,C = gen(n, m, r, N)
print(C,file = output)
save(C,"output.sobj")
save(L,"L.sobj")
LL = load("L.sobj")
print(LL==L)
CC = load("output.sobj")
print(CC==C)
OB = load("orignal_b.sobj")
print(OB==B)

