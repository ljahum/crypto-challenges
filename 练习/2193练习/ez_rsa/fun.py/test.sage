#Sage
from sage.all import *
n = 
p4 = 
#p去0的剩余位
e =  
pbits = 1024
kbits = pbits - p4.nbits()
print(p4.nbits())
p4 = p4 << kbits
PR.<x> = PolynomialRing(Zmod(n))
f = x + p4
roots = f.small_roots(X=2^kbits, beta=0.4)
#经过以上一些函数处理后，n和p已经被转化为10进制
if roots:        
	p = p4+int(roots[0]) 
	print("n: "+str(n))
	print("p: "+str(p))
	print("q: "+str(n//p))