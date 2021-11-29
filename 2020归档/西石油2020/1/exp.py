from gmpy2 import *
from Crypto.Util.number import *
#q + q*p^3 =467962068718552895211162459665195309477537820950314984120501297653251626108029252766706321468050831941604717101473973050
#qp + q *p^2 = 565793545980404021917176171737381087790180558655380403750360123494827821905901954270664682

f1 = 467962068718552895211162459665195309477537820950314984120501297653251626108029252766706321468050831941604717101473973050
f2 = 565793545980404021917176171737381087790180558655380403750360123494827821905901954270664682

# print(gcd(f1, f2))
    
q = 827089796345539312201480770649
p = 827089796345539312201480770649
print(q+q*(p**3))
print(q*p+q*(p**2))
print(f1%q)

print('------------------------------')
# ------------------------------
print(f2%q)
print(f1 % q)
a = f1//q -1
print(gcd(a,f2//q))
'''
c= 0x7a7e031f14f6b6c3292d11a41161d2491ce8bcdc67ef1baa9e
e= 0x872a335
phi = (p-1)*(q-1)
n=p*q
d = invert(e,phi)
print(long_to_bytes(pow(c,d,n)))

'''
