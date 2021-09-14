from Crypto.Util.number import *
from libnum import *
from icecream import *
p2 = getPrime(512)
q2 = getPrime(512)
n2 = p2*q2
p=p2
q=q2
e2 = 65537

e1 = 202020
e2 = 212121

hint3 = pow(2020 * p2 + 2021 * q2, 202020, n2)
hint4 = pow(2021 * p2 + 2020 * q2, 212121, n2)
a = 2020
c1 = hint3
c2 = hint4
t = 202020*212121

c1e2 = pow(c1,e2,n2)
c2e1 = pow(c2,e1,n2)

ans = (c1e2+c2e1)%n2
ans2 = ((pow(a,t,n2)+pow((a+1),t,n2))*(pow(p,t,n2)+pow(q,t,n2)))%n2
tmp =pow(a,t,n2)+pow((a+1),t,n2)

invtmp = invmod(tmp,n2)
print(invtmp)
pt_qt = (ans2*invtmp)%n2
pt_qt2 = (pow(p,t,n2)+pow(q,t,n2))%n2
ic(pt_qt==pt_qt2)
ic(ans==ans2)