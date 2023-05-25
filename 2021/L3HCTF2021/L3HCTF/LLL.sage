#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
from libnum import invmod
from data import *
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
l=8
LEN=len(a)
tt=[]
uu=[]
for i in range(len(a)):
    tmp1 = (r[i]*invmod(s[i]*2^l,n))%n
    tt.append(tmp1)
    tmp2 = ((a[i]*s[i]-H[i])*invmod(s[i]*2^l,n))%n
    uu.append(tmp2)
M=[[0 for i in range(102)] for j in range(102)]

for i in range(LEN):
    M[i][i]=n
for i in range(LEN):
    M[LEN][i]=tt[i]
    M[LEN+1][i]=uu[i]

ct= 2^256
cu= 2^32 
M[LEN][LEN]=ct
M[LEN+1][LEN+1]=cu
print(ct)
print(cu)
print("start LLL....")
M = matrix(M)
M = [list(i) for i in M]
fr=open('./output','w')
for row in M:
    # if(ct in row[-1]):
    print(row,file=fr)
fr.close()
