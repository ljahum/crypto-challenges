

# This file was *autogenerated* from the file /mnt/c/Users/16953/Desktop/RCTF2021/uncommon2/solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_64 = Integer(64); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_304 = Integer(304)#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
from Crypto.Util.number import *
with open("lN.bin","rb") as f:
    data = f.read()

f1 = open("./data","wb")
size = _sage_const_64 
print('size',size)
nn=[]  
for i in range(size):
    nn.append((bytes_to_long(data[i*_sage_const_64 :(i+_sage_const_1 )*_sage_const_64 ])))
B = [[_sage_const_0  for i in range(size)] for _ in range(size)]
x0 = nn[_sage_const_0 ]
B[_sage_const_0 ][_sage_const_0 ]=_sage_const_2 **_sage_const_304 
for i in range(_sage_const_1 ,size):
    B[_sage_const_0 ][i]=nn[i]
    # B[0][i]=i
# print(B)
# print(x0)
print('start LLL....')
for i in range(_sage_const_1 ,size):
    B[i][i]=-x0
B = Matrix(B)
V = B.LLL()
q = abs(V[_sage_const_0 ][_sage_const_0 ])

q = q>>_sage_const_304 
print(x0-q)
p = x0//q
print(long_to_bytes(p))


# flag{Simpl3_LLL_TrIck}

