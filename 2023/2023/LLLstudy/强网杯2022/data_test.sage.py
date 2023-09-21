

# This file was *autogenerated* from the file data_test.sage
from sage.all_cmdline import *   # import sage library

_sage_const_75 = Integer(75); _sage_const_150 = Integer(150); _sage_const_10 = Integer(10); _sage_const_126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109 = Integer(126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0); _sage_const_12 = Integer(12)
n = _sage_const_75 
m = _sage_const_150 
r = _sage_const_10 
N =_sage_const_126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109 
def kernelLLL(M):
    n = M.nrows()
    m = M.ncols()
    if m < _sage_const_2  * n:
        return M.right_kernel().matrix()
    K = _sage_const_2  ** (m // _sage_const_2 ) * M.height()
    MB = Matrix(ZZ, m + n, m)
    MB[:n] = K * M
    MB[n:] = identity_matrix(m)
    MB2 = MB.T.LLL().T
    assert MB2[:n, : m - n] == _sage_const_0 
    Ke = MB2[n:, : m - n].T
    return Ke

with open('output.txt', 'r') as f:
  data = f.readlines()
  for i in range(len(data)):
    data[i] = data[i].replace('[', '').replace(']', '').split(' ')
    tmp = []
    for x in data[i]:
      if x != '':
        tmp.append(int(x))
    data[i] = tmp
C = matrix(ZZ, data)
"""
CC = load("output.sobj")
print(C==CC)
A = matrix(ZZ,m+r,m+r)
for i in range(m):
  A[i,i] = 1
for i in range(r):
  for j in range(m):
    A[j,i+m] = C[i,j]<<200
  A[i+m,i+m] = N<<200
print("start LLL")
ans = A.LLL()
print("END LLL")
save(ans,"ALLL.sobj")
B = matrix(ZZ,n,m)
for i in range(n):
  assert list(ans[i][m:]) == [0]*r
  B[i] = ans[i][:m]
ans = B.right_kernel().basis()
save(ans,"ans.sobj")
"""

ans = load("ALLL.sobj")

B = matrix(ZZ,n,m)
for i in range(n):
  assert list(ans[i][m:]) == [_sage_const_0 ]*r
  B[i] = ans[i][:m]
print("may be (B*C^T) mod N = 0")
print((B*C.transpose())%N)
print("="*_sage_const_150 )


ke = kernelLLL(B)
print("This is the kernelLLL of B")
print(ke[_sage_const_0 ])
print("="*_sage_const_150 )


print("This is BKZ(block_size=12) of the kernelLLL of B")
print(kernelLLL(B).BKZ(block_size=_sage_const_12 )[_sage_const_0 ])
print("="*_sage_const_150 )

print("This is LLLof the kernelLLL of B")
print(kernelLLL(B).LLL()[_sage_const_0 ])
print("="*_sage_const_150 )

print("This is the BKZ of right_kernel basis of B")
ans = load("ans.sobj")
D = matrix(ZZ,ans)
res = D.BKZ(block_size=_sage_const_12 )[_sage_const_0 ]
print(res)
print("="*_sage_const_150 )

print("This is the LLL of right_kernel basis of B")
res = D.LLL()[_sage_const_0 ]
print(res)
print("="*_sage_const_150 )


OB = load("orignal_b.sobj")
print("This is the answer we search for")
print(OB.LLL()[_sage_const_0 ])
print("="*_sage_const_150 )

