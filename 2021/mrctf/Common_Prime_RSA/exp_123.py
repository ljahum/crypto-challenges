from Crypto.Util.number import *
from gmpy2 import *
from icecream import *
n1 = 0x48b11209b62c5bc580d00fc94886272b92814ce35fcd265b2915c6917a299bc54c2c0603c41f8bf7c8f6f2a545eb03d38f99ec995bf6658bb1a2d23056ee21c7230caa2decec688ea9ee00b0d50b39e8cd23eb2c3ddeb20f5ab26777b80052c171f47b716e72f6aee9cece92776fc65119046f9a1ad92c40e2094d7ed7526d49
c1 = 0x27d8d7249643668ffc115be8b61775c60596e51f6313b47ad5af8493526922f5e10026a2cdaef74e22c3eec959dd8771abe3495b18d19f97623f5a3f65f22ff8fc294fc37ceb3b43ebbbf8a9bcf622922e22c5520dbd523483b9dc54fdffcd1a1b3f02ca1f53b75413fb79399ca00034f2acf108ac9a01bd24d2b9df6e27d156
e1 = 3

'''
kbits = int(1024*0.2247)
m0 =  0x436f6d6d6f6e207072696d652052534120697320612076617269616e74206f66205253410000000000000000000000000000000000000000000000000000000000416e642074686520636f6d6d6f6e20666163746f722067206973206c61726765207072696d6520616e6420703d3267612b3120713d3267622b31
PR.<x> = PolynomialRing(Zmod(n))
f = ((m0 + x*2**464)^e1) - c1
f = f.monic()
g1 = f.small_roots(X=2^kbits,beta=1)[0]
print(g1)
'''

g1 = 1328458990599515056771144217738449144496664370133586446617480019409757
v1 = ((n1 - 1) // (2*g1)) % (2*g1)
u1 = ((n1 - 1) // (2*g1)) // (2*g1)
# left = (((2 * iroot(n1, 2)[0]) // (2*g1)) - v1) // (2*g1)
# right = (((3 * iroot(2*n1, 2)[0]) // (4*g1)) - v1) // (2*g1)
aa = g1 ** 2
bb = 2 * g1 ** 2 + 1
cc = g1 ** 2 - u1
left = (-bb + iroot(bb ** 2 - 4 * cc * aa, 2)[0]) // (2 * aa)

right = (u1 * 1.125)**0.5 // g1


b = pow(114514, 2*g1, n1)
Y_c_min = pow(b, left, n1)
oneStep = iroot(int(right - left), 2)[0]
ic(oneStep)
ic(left,right)

#  2146990465019381
#  2024202022610750
# ic| oneStep: mpz(11080995)

# 压缩了范围的大步小步 ================================
Baby_step_list = {}
Babystep = pow(b, oneStep, n1)
Y = Y_c_min
print("start to baby step")
for i in range(oneStep):
    if i % (oneStep >> 10) == 1:
        print('\r%.2f%% of giant step' % ((i + 1) / (oneStep + 1) * 100), end='')
    Baby_step_list[Y] = i
    Y = Y * Babystep % n1
print("baby step ready")

Y_u = pow(b, u1, n1)
Y = Y_u
giant_step = inverse(b, n1)
for i in range(oneStep):
    if i % (oneStep >> 10) == 1:
        print('\r%.2f%% of giant step' % ((i + 1) / (oneStep + 1) * 100), end='')
    if(Y in Baby_step_list):
        print("ans found!")
        print(i, Baby_step_list[Y])
        c = left + i + oneStep * Baby_step_list[Y]
        break
    Y = Y * giant_step % n1
# =====================================================

# g2 > a+b 直接解
A = u1 - c
B = v1 + c * 2 * g1
C = iroot(B**2 - 4*A, 2)[0]
x = (B+C) // 2
y = B-x
p1 = x*g1*2+1
q1 = y*g1*2+1

phi1 = (p1-1) * (q1-1)
e1 = 65537
d1 = inverse(e1, phi1)
c1 = 0xeaf06b9050a809659f962251b14d6b93009a7010f0e8d8f0fa4d71591757e98243b8ff50ec98a4e140fd8a63bbb4b8bb0a6d302a48845b8b09d1e40874fcb586ddccbb0bbf86d21540ec6c15c1d2bf925942f6f384fdc1baae7f8e06150ccd9459eb65d0f07eea16a911fa0a17e876a145dbfec83537ca2bee4641897b9f7f5

g2 = pow(c1, d1, n1)

n2 = 0x6d457110d6044472d786936acbd3cd93c7728daa3343b35ccaa5c55eba6b35c28c831bb245b8cdd8fc8cb67a72f57e62a0e1259f5e804c487a8478f6895b302d39277bd73947598a5f8ec0a535be9e9a4d34df91df948ee44cc3d13d14e23b9651089e4767c7f0e7245df55619c92fe24483225d35f5f3ee6f74375065766ffd
c2 = 0x15be2b0eaef8837a753587c47d3f31696a7d239d88837a9b7d903cd0d0648ef8e225ea555402693a23f305d19e7e13905be61b44c651dba5b26614bcf876234e765a724e0ed8af4a4e408e6a233c48ab9cc63e9c552ef9cd1999512aa0aca830fe6cbcbcc3c6bb354903124a2c3a12d442cdbdefdae6576f4bbc1515051b7111
e2 = 65537

A = ((n2 - 1) // (2*g2)) // (2*g2)
B = ((n2 - 1) // (2*g2)) % (2*g2)
C = iroot(B**2 - 4*A, 2)[0]
x = (B+C) // 2
y = B-x
p2 = x*g2*2+1
q2 = y*g2*2+1

phi2 = (p2-1) * (q2-1)
d2 = inverse(e2, phi2)
m = pow(c2, d2, n2)
flag = long_to_bytes(m)
print(flag)
