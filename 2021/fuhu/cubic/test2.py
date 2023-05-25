from datatot import x,y,z
from data4 import x4,y4,z4
from data5 import x5,y5,z5
from data6 import x6, y6, z6
from fractions import Fraction as Frac
from pwn import *
sh = remote('0.0.0.0',10000)
for i in range(3):
    print(f"answer{i+1}")
    X=x[i]
    Y=y[i]
    Z=z[i]
    sh.sendline(str(X))
    sh.sendline(str(Y))
    sh.sendline(str(Z))
    print(Frac(X, Y+Z) + Frac(Y, Z+X) + Frac(Z, X+Y))

print("ans 4 ")
X = x4
Y = y4
Z = z4
sh.sendline(str(X))
sh.sendline(str(Y))
sh.sendline(str(Z))
print(Frac(X, Y+Z) + Frac(Y, Z+X) + Frac(Z, X+Y))

print("ans 5 ")
X = x5
Y = y5
Z = z5
sh.sendline(str(X))
sh.sendline(str(Y))
sh.sendline(str(Z))
print(Frac(X, Y+Z) + Frac(Y, Z+X) + Frac(Z, X+Y))

print("ans 6 ")
X = x6
Y = y6
Z = z6
sh.sendline(str(X))
sh.sendline(str(Y))
sh.sendline(str(Z))
print(Frac(X, Y+Z) + Frac(Y, Z+X) + Frac(Z, X+Y))
print(sh.recv(1024))