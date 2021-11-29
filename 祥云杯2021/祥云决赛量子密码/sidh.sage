import sys
import secrets
import hashlib
import base64
#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
assert(sys.version_info.major >= 3)

flag = b"flag{**********REDACTED**********}"

def xADD(xP,xQ,xR):
    return (xP*xQ-1)^2/(xP-xQ)^2/xR

def xDBL(x,a):
	return (x^2-1)^2/(4*x*(x^2+a*x+1))

def xTPL(x,a):
	return (x^4-6*x^2-4*a*x-3)^2*x/(3*x^4+4*a*x^3+6*x^2-1)^2

def ladder3pt(xP,xQ,xR,k,A):
    bits=k.bits()
    R0=xQ
    R1=xP
    R2=xR
    for i in range(0,len(bits)-1):
        if bits[i] == 1:
            R1=xADD(R0,R1,R2)
        else:
            R2=xADD(R0,R2,R1)
        R0=xDBL(R0,A)
    R1=xADD(R0,R1,R2)
    return R1

def iso2(alpha,pts):
    image_pts=[]
    for x in pts:
        image_pts.append(x*(alpha*x-1)/(x-alpha))
    return 2*(1-2*alpha^2),image_pts

def iso3(beta,a,pts):
    image_pts=[]
    for x in pts:
        image_pts.append(x*(beta*x-1)^2/(x-beta)^2)
    return (6-6*beta^2+a*beta)*beta,image_pts

def iso4(alpha,pts):
    image_pts=[]
    for x in pts:
        image_pts.append(x*(alpha^2*x-2*alpha+x)*(alpha*x-1)^2/((alpha^2-2*alpha*x+1)*(alpha-x)^2))
    return 2*(2*alpha^4-1),image_pts

def jInv(a):
    return 256*(a^2-3)^3/(a^2-4)

def MontFromPoints(xP,xQ,xR):
    return (1-xP*xQ-xP*xR-xQ*xR)^2/(4*xP*xQ*xR)-xP-xQ-xR

e2=257;  e3=11;      file=open('out.txt','w')

p=2^e2*3^e3-1

Fp=GF(p)
Fp2.<i> = GF(p^2, modulus=x^2+1)
A=6
E0=EllipticCurve(Fp2,[0,A,0,1,0])

def square_root(s):
    assert is_square(s)
    if s != 0:
        if s != 1:
            r=sqrt(Fp2(s))
            r=r.polynomial().list()
            alpha=r[0]
            beta=r[1]
            if alpha == 0:
                if is_odd(Integer(beta)):
                    beta=-beta
            else:
                if is_odd(Integer(alpha)):
                    alpha=-alpha
                    beta=-beta
            assert (alpha+beta*i)^2 == s
            return alpha+beta*i
        else:
            return 1
    else:
        return 0

c=-1

while True:
    while True:
        c = c + 1
        X = i + c
        fX = X^3+A*X^2+X
        if is_square(fX):
            break
    P2=3^e3*E0(X,square_root(fX))
    T=2^(e2-1)*P2
    if (T[0]+3)^2 == 8 and T[1] == 0:
        break

c=-1

while True:
    while True:
        c = c + 1
        X = i + c
        fX = X^3+A*X^2+X
        if is_square(fX):
            break
    Q2=3^e3*E0(X,square_root(fX))
    T=2^(e2-1)*Q2
    if T == E0(0,0):
        break

c=-1
while True:
    while True:
        c = c + 1
        fc = c^3+A*c^2+c
        if is_square(Fp(fc)):
            break
    P3=2^(e2-1)*E0(c,sqrt(Fp(fc)))
    if P3.order() == 3^e3:
        break

c=-1
while True:
    while True:
        c = c + 1
        fc = c^3+A*c^2+c
        if not is_square(Fp(fc)):
            break
    Q3=2^(e2-1)*E0(c,square_root(Fp2(fc)))
    if Q3.order() == 3^e3:
        break

R2 = P2-Q2
R3 = P3-Q3

xP2=P2[0].polynomial().list()
xP20 = xP2[0]; xP21 = xP2[1]
yP2=P2[1].polynomial().list()
yP20 = yP2[0]; yP21 = yP2[1]
xQ2=Q2[0].polynomial().list()
xQ20 = xQ2[0]; xQ21 = xQ2[1]
yQ2=Q2[1].polynomial().list()
yQ20 = yQ2[0]; yQ21 = yQ2[1]
xP3=P3[0].polynomial().list()
xP30 = xP3[0]; xP31 = 0
yP3=P3[1].polynomial().list()
yP30 = yP3[0]; yP31 = 0
xQ3=Q3[0].polynomial().list()
xQ30 = xQ3[0]; xQ31 = 0
yQ3=Q3[1].polynomial().list()
yQ30 = yQ3[0]; yQ31 = yQ3[1]
xR2=R2[0].polynomial().list()
xR20 = xR2[0]; xR21 = xR2[1]
yR2=R2[1].polynomial().list()
yR20 = yR2[0]; yR21 = yR2[1]
xR3=R3[0].polynomial().list()
xR30 = xR3[0]; xR31 = xR3[1]
yR3=R3[1].polynomial().list()
yR30 = yR3[0]; yR31 = yR3[1]

file.write("Public parameters \n \n")

file.write("p = ")
file.write(p.hex())
file.write("\n")
file.write("e2 = ")	
file.write(e2.hex())
file.write("\n")
file.write("e3 = ")
file.write(e3.hex())
file.write("\n")
file.write("xQ20 = ")
file.write(Integer(xQ20).hex())
file.write("\n")
file.write("xQ21 = ")
file.write(Integer(xQ21).hex())
file.write("\n")
file.write("yQ20 = ")	
file.write(Integer(yQ20).hex())
file.write("\n")
file.write("yQ21 = ")	
file.write(Integer(yQ21).hex())
file.write("\n")
file.write("xP20 = ")
file.write(Integer(xP20).hex())
file.write("\n")
file.write("xP21 = ")
file.write(Integer(xP21).hex())
file.write("\n")
file.write("yP20 = ")	
file.write(Integer(yP20).hex())
file.write("\n")
file.write("yP21 = ")	
file.write(Integer(yP21).hex())
file.write("\n")
file.write("xR20 = ")	
file.write(Integer(xR20).hex())
file.write("\n")
file.write("xR21 = ")	
file.write(Integer(xR21).hex())
file.write("\n")
file.write("xQ30 = ")
file.write(Integer(xQ30).hex())
file.write("\n")
file.write("xQ31 = ")
file.write(Integer(xQ31).hex())
file.write("\n")
file.write("yQ30 = ")	
file.write(Integer(yQ30).hex())
file.write("\n")
file.write("yQ31 = ")	
file.write(Integer(yQ31).hex())
file.write("\n")
file.write("xP30 = ")
file.write(Integer(xP30).hex())
file.write("\n")
file.write("xP31 = ")
file.write(Integer(xP31).hex())
file.write("\n")
file.write("yP30 = ")	
file.write(Integer(yP30).hex())
file.write("\n")
file.write("yP31 = ")	
file.write(Integer(yP31).hex())
file.write("\n")
file.write("xR30 = ")	
file.write(Integer(xR30).hex())
file.write("\n")
file.write("xR31 = ")	
file.write(Integer(xR31).hex())
file.write("\n")

Q2=E0(xQ20+xQ21*i,yQ20+yQ21*i)     
P2=E0(xP20+xP21*i,yP20+yP21*i)
R2=E0(xR20+xR21*i,yR20+yR21*i)

Q3=E0(xQ30+xQ31*i,yQ30+yQ31*i)
P3=E0(xP30+xP31*i,yP30+yP31*i)
R3=E0(xR30+xR31*i,yR30+yR31*i)

k_Alice = Integer(secrets.randbits(e2))
k_Bob = Integer(secrets.randbits(floor(log(3^e3,2))))

A_Alice = A
xS=ladder3pt(P2[0],Q2[0],R2[0],k_Alice,A_Alice)
pts=[xS,P3[0],Q3[0],R3[0]]

if is_odd(e2):
    x_ker=pts[0]
    for i in range(0,e2-1):
        x_ker=xDBL(x_ker,A_Alice)
    A_Alice,pts=iso2(x_ker,pts)

for e in range(floor(e2/2)-1,0,-1):    
    x_ker=pts[0]
    for i in range(0,e):
        x_ker=xDBL(x_ker,A_Alice)
        x_ker=xDBL(x_ker,A_Alice)
    A_Alice,pts=iso4(x_ker,pts)

A_Alice,PK_Alice=iso4(pts[0],[pts[1],pts[2],pts[3]])

PA=PK_Alice[0].polynomial().list()
QA=PK_Alice[1].polynomial().list()
RA=PK_Alice[2].polynomial().list()
PA0 = PA[0]; PA1 = PA[1]
QA0 = QA[0]; QA1 = QA[1]
RA0 = RA[0]; RA1 = RA[1]

print("\nAlice's public key - PA0||PA1||QA0||QA1||RA0||RA1:\n")
print(Integer(PA0).hex())
print(Integer(PA1).hex())
print(Integer(QA0).hex())
print(Integer(QA1).hex())
print(Integer(RA0).hex())
print(Integer(RA1).hex())

file.write("\nAlice's public key - PA0||PA1||QA0||QA1||RA0||RA1:\n\n")
file.write(Integer(PA0).hex())
file.write("\n")
file.write(Integer(PA1).hex())
file.write("\n")
file.write(Integer(QA0).hex())
file.write("\n")
file.write(Integer(QA1).hex())
file.write("\n")
file.write(Integer(RA0).hex())
file.write("\n")
file.write(Integer(RA1).hex())
file.write("\n")

A_Bob = A
xS=ladder3pt(P3[0],Q3[0],R3[0],k_Bob,A_Bob)
pts=[xS,P2[0],Q2[0],R2[0]]

for e in range(e3-1,0,-1):
    x_ker=pts[0]
    for i in range(0,e):
        x_ker=xTPL(x_ker,A_Bob)
    A_Bob,pts=iso3(x_ker,A_Bob,pts)

A_Bob,PK_Bob=iso3(pts[0],A_Bob,[pts[1],pts[2],pts[3]])

PB=PK_Bob[0].polynomial().list()
QB=PK_Bob[1].polynomial().list()
RB=PK_Bob[2].polynomial().list()
PB0 = PB[0]; PB1 = PB[1]
QB0 = QB[0]; QB1 = QB[1]
RB0 = RB[0]; RB1 = RB[1]

print("\nBob's public key - PB0||PB1||QB0||QB1||RB0||RB1:\n")
print(Integer(PB0).hex())
print(Integer(PB1).hex())
print(Integer(QB0).hex())
print(Integer(QB1).hex())
print(Integer(RB0).hex())
print(Integer(RB1).hex())

file.write("\nBob's public key - PB0||PB1||QB0||QB1||RB0||RB1:\n\n")
file.write(Integer(PB0).hex())
file.write("\n")
file.write(Integer(PB1).hex())
file.write("\n")
file.write(Integer(QB0).hex())
file.write("\n")
file.write(Integer(QB1).hex())
file.write("\n")
file.write(Integer(RB0).hex())
file.write("\n")
file.write(Integer(RB1).hex())
file.write("\n")

A_Alice = MontFromPoints(PK_Bob[0],PK_Bob[1],PK_Bob[2])
xS=ladder3pt(PK_Bob[0],PK_Bob[1],PK_Bob[2],k_Alice,A_Alice)

pts=[xS]

if is_odd(e2):
    x_ker=pts[0]
    for i in range(0,e2-1):
        x_ker=xDBL(x_ker,A_Alice)
    A_Alice,pts=iso2(x_ker,pts)

for e in range(floor(e2/2)-1,0,-1):    
    x_ker=pts[0]
    for i in range(0,e):
        x_ker=xDBL(x_ker,A_Alice)
        x_ker=xDBL(x_ker,A_Alice)
    A_Alice,pts=iso4(x_ker,pts)

A_Alice=2*(2*pts[0]^4-1)

shared_Alice=jInv(A_Alice)

j = shared_Alice.polynomial().list()
j0 = "% s" % j[0]
j1 = "% s" % j[1]
key_Alice = (j0+j1).encode()

key = hashlib.sha256(key_Alice).digest()
cipher = AES.new(key, AES.MODE_ECB)
message = cipher.encrypt(pad(b"Hi there, can you hear me?",16))

print("\nEncrypted message 1:\n")
print(base64.b64encode(message).decode())

file.write("\nEncrypted message 1:\n\n")
file.write(base64.b64encode(message).decode())
file.write("\n")

message = cipher.encrypt(pad(b"Here is your flag: " + flag, 16))

print("\nEncrypted message 2:\n")
print(base64.b64encode(message).decode())

file.write("\nEncrypted message 2:\n\n")
file.write(base64.b64encode(message).decode())
file.write("\n")

file.close()

