

# This file was *autogenerated* from the file ruan师傅.sage
from sage.all_cmdline import *   # import sage library

_sage_const_816358673 = Integer(816358673); _sage_const_214551389 = Integer(214551389); _sage_const_683509053 = Integer(683509053); _sage_const_377954927 = Integer(377954927); _sage_const_461648693 = Integer(461648693); _sage_const_819009687 = Integer(819009687); _sage_const_833612683 = Integer(833612683); _sage_const_246393449 = Integer(246393449); _sage_const_258952137 = Integer(258952137); _sage_const_592274653 = Integer(592274653); _sage_const_439857687 = Integer(439857687); _sage_const_164289531 = Integer(164289531); _sage_const_138621939 = Integer(138621939); _sage_const_626982035 = Integer(626982035); _sage_const_733582939 = Integer(733582939); _sage_const_561376076 = Integer(561376076); _sage_const_206910526 = Integer(206910526); _sage_const_470721180 = Integer(470721180); _sage_const_1105393379 = Integer(1105393379); _sage_const_848577580 = Integer(848577580); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_6545130222 = Integer(6545130222); _sage_const_2 = Integer(2)

M = [_sage_const_816358673 , _sage_const_214551389 , _sage_const_683509053 , _sage_const_377954927 , _sage_const_461648693 , _sage_const_819009687 , _sage_const_833612683 , _sage_const_246393449 , _sage_const_258952137 , _sage_const_592274653 , _sage_const_439857687 , _sage_const_164289531 , _sage_const_138621939 , _sage_const_626982035 , _sage_const_733582939 , _sage_const_561376076 , _sage_const_206910526 , _sage_const_470721180 , _sage_const_1105393379 , _sage_const_848577580 ]
msg = [_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ]
S = _sage_const_6545130222 

n = len(M)
L = matrix.zero(n + _sage_const_1 )

for row, x in enumerate(M):
    L[row, row] = _sage_const_2 
    L[row, -_sage_const_1 ] = x

L[-_sage_const_1 , :] = _sage_const_1 
L[-_sage_const_1 , -_sage_const_1 ] = S

res = L.LLL()
print(res)
# for i in range(len(msg)):
#     ans = list(res[i])
#     print(ans)


