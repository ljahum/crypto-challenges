#! /usr/bin/sage

from tqdm import tqdm
from rich.progress import track
from rich.traceback import install
install()
# -----------------------------------
from data import *
# from sage.all import *
from libnum import invmod
#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *

# from Crypto.Util.number import *
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
tt=[]
uu =[]
for i in range(len(ss)):
    tt.append(rr[i]*invmod(256*ss[i],n))
    uu.append((kk[i]-hh[i])*invmod(256*ss[i],n))
l=8
print('ok')

ct = (2**256)/n
cu = 2**256
print(ct)
print( cu)
M = [[0 for i in range(102)] for j in range(102)]
for i in range(100):
    for j in range(100):
        M[i][j] = n
for i in range(100):
    M[100][i] = tt[i]
    M[101][i] = uu[i]
TT = vector(M[100])
UU =vector(M[101])
M[100][100] = ct
M[101][101] = cu
M = matrix(M)
print('start LLLing.....')
B = M.LLL()


f = open('./data','w')
for i in B[-3:]:
    f.write(str(list(i))+'\n')
