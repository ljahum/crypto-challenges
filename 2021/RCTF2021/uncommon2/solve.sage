#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
from Crypto.Util.number import *
with open("lN.bin","rb") as f:
    data = f.read()

f1 = open("./data","wb")
size = 64
print('size',size)
nn=[]  
for i in range(size):
    nn.append((bytes_to_long(data[i*64:(i+1)*64])))
B = [[0 for i in range(size)] for _ in range(size)]
x0 = nn[0]
B[0][0]=2^304
for i in range(1,size):
    B[0][i]=nn[i]
    # B[0][i]=i
# print(B)
# print(x0)
print('start LLL....')
for i in range(1,size):
    B[i][i]=-x0
B = Matrix(B)
V = B.LLL()
q = abs(V[0][0])

q = q>>304
print(x0-q)
p = x0//q
print(long_to_bytes(p))


# flag{Simpl3_LLL_TrIck}