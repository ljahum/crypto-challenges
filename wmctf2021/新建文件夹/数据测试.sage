#!sage
from icecream import *
from sage.all import *
from Crypto.Util.number import *
N = 78783023222142579402299
e1 = 20339472065400293617
e2 = 16071808231974749459

list1 = continued_fraction(Integer(e1)/Integer(e2))
conv = list1.convergents()

time=0
for i in conv:
    time+=1
    if(time==40):
        break
    k = i.numerator()
    qi = i.denominator()
    print(time)
    print(k,qi)
a = 3889559329731
b = 3073445144167
'''
sage: factor(3889559329731)
3^3 * 229 * 6079 * 103483
sage: factor(3073445144167)
41 * 43 * 71 * 1693 * 14503
sage:
'''
a = 71092821*54711
b =  211917889 * 14503

x1 = 211917889
y1  = 54711
x2=71092821
y2=14503
S = N+1-(e1*x1)//y1

D = int((S^2-4*N)^(1/2))
ic(S)
ic(D)
hp = (S+D)//2
R.<x> = PolynomialRing(Zmod(N), implementation='NTL')
p = hp + x
x0 = p.small_roots(X = 2^15, beta = 0.1)[0]
P = int(p(x0))
print(P)
# 395718860549
