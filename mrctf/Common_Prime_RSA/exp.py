from Crypto.Util.number import *
import time
from gmpy2 import iroot
from sys import getsizeof
from icecream import *

'''sage
e = 3
    0x436f6d6d6f6e207072696d652052534120697320612076617269616e74206f66205253410000000000000000000000000000000000000000000000000000000000416e642074686520636f6d6d6f6e20666163746f722067206973206c61726765207072696d6520616e6420703d3267612b3120713d3267622b31
b = 0x436f6d6d6f6e207072696d652052534120697320612076617269616e74206f66205253410000000000000000000000000000000000000000000000000000000000416e642074686520636f6d6d6f6e20666163746f722067206973206c61726765207072696d6520616e6420703d3267612b3120713d3267622b31
N = 0x48b11209b62c5bc580d00fc94886272b92814ce35fcd265b2915c6917a299bc54c2c0603c41f8bf7c8f6f2a545eb03d38f99ec995bf6658bb1a2d23056ee21c7230caa2decec688ea9ee00b0d50b39e8cd23eb2c3ddeb20f5ab26777b80052c171f47b716e72f6aee9cece92776fc65119046f9a1ad92c40e2094d7ed7526d49
c = 0x27d8d7249643668ffc115be8b61775c60596e51f6313b47ad5af8493526922f5e10026a2cdaef74e22c3eec959dd8771abe3495b18d19f97623f5a3f65f22ff8fc294fc37ceb3b43ebbbf8a9bcf622922e22c5520dbd523483b9dc54fdffcd1a1b3f02ca1f53b75413fb79399ca00034f2acf108ac9a01bd24d2b9df6e27d156
kbits = 240

PR.<x> = PolynomialRing(Zmod(N))
f = (x * 2^464 + b)^e-c
g = int(f.monic().small_roots(X=2^kbits, beta=0.5)[0])
hex(g)
'''
# b'Common prime RSA is a variant of RSA' + long_to_bytes(g1) + b'And the common factor g is large prime and p=2ga+1 q=2gb+1')

g1 = 0x314678eb7386e8c9dc7042bee9e565de53074e0575ca91c83d9d117b5d

n1 = 0x48b11209b62c5bc580d00fc94886272b92814ce35fcd265b2915c6917a299bc54c2c0603c41f8bf7c8f6f2a545eb03d38f99ec995bf6658bb1a2d23056ee21c7230caa2decec688ea9ee00b0d50b39e8cd23eb2c3ddeb20f5ab26777b80052c171f47b716e72f6aee9cece92776fc65119046f9a1ad92c40e2094d7ed7526d49
c1 = 0xeaf06b9050a809659f962251b14d6b93009a7010f0e8d8f0fa4d71591757e98243b8ff50ec98a4e140fd8a63bbb4b8bb0a6d302a48845b8b09d1e40874fcb586ddccbb0bbf86d21540ec6c15c1d2bf925942f6f384fdc1baae7f8e06150ccd9459eb65d0f07eea16a911fa0a17e876a145dbfec83537ca2bee4641897b9f7f5
n2 = 0x6d457110d6044472d786936acbd3cd93c7728daa3343b35ccaa5c55eba6b35c28c831bb245b8cdd8fc8cb67a72f57e62a0e1259f5e804c487a8478f6895b302d39277bd73947598a5f8ec0a535be9e9a4d34df91df948ee44cc3d13d14e23b9651089e4767c7f0e7245df55619c92fe24483225d35f5f3ee6f74375065766ffd
c2 = 0x15be2b0eaef8837a753587c47d3f31696a7d239d88837a9b7d903cd0d0648ef8e225ea555402693a23f305d19e7e13905be61b44c651dba5b26614bcf876234e765a724e0ed8af4a4e408e6a233c48ab9cc63e9c552ef9cd1999512aa0aca830fe6cbcbcc3c6bb354903124a2c3a12d442cdbdefdae6576f4bbc1515051b7111
e = 65537

a1 = 2464018258194586071142234478391390711406779702189308207403798067312099010206143579629
b1 = 2934675537985245252057592064251628026914110115755296316638506623629803734187164176349
c1 = a1 + b1

div = (n1 - 1) // (2 * g1)
u = div // (2 * g1)
v = div % (2 * g1)

aa = g1 ** 2
bb = 2 * g1 ** 2 + 1
cc = g1 ** 2 - u
c_min = (-bb + iroot(bb ** 2 - 4 * cc * aa, 2)[0]) // (2 * aa)

c_max = (u * 1.125)**0.5 // g1

#                 2146990465019381
#                                               2024202022610750
# ic | left: mpz(2024202022610750), right: mpz(2146990465019380)
ic(c_max,c_min)
ic(c_max-c_min)
# ?????
d = int(pow(c_max - c_min, 0.5)) + 1
# 11080995

print('d =', d)
input()
y = pow(getRandomRange(2, n1), 2 * g1, n1)
baby = {}
baby_start = pow(y, u - c_min, n1)
gian_start = 1
y_d = pow(y, d, n1)
inv = inverse(y, n1)


# baby step
start = time.time()

for i in range(d):
    if i % (d >> 10) == 1:
        print('\r%.2f%% of baby step' % ((i + 1) / (d + 1) * 100), end='')

    baby[baby_start] = i
    baby_start = (baby_start * inv) % n1

end = time.time()
print('\nbaby step : %s Seconds' % (end - start))

print('memory size of baby :', end=' ')
print(getsizeof(baby) + sum([getsizeof(i) for i in baby.values()]) + sum([getsizeof(i) for i in baby.keys()]))


# giant step
start = time.time()

for i in range(d):
    if i % (d >> 10) == 1:
        print('\r%.2f%% of giant step' % ((i + 1) / (d + 1) * 100), end='')

    if gian_start in baby:
        r, s = i, baby[gian_start]
        break
    gian_start = (gian_start * y_d) % n1
else:
    raise RuntimeError('d is too small')

end = time.time()
print('\ngiant step : %s Seconds' % (end - start))

c = (r * d + s) + c_min
print('c =', c)

aa = 1
bb = -(v + 2 * g1 * c)
cc = u - c
a1, b1 = (-bb - iroot(bb ** 2 - 4 * cc * aa, 2)[0]) // (2 * aa), (-bb + iroot(bb ** 2 - 4 * cc * aa, 2)[0]) // (2 * aa)
ic(a1,b1)
p1, q1 = 2 * g1 * a1 + 1, 2 * g1 * b1 + 1

g2 = pow(c1, inverse(e, (p1 - 1) * (q1 - 1)), n1)

M = (n2 - 1) // (2 * g2)
c = M % g2

aa = 2 * g2
bb = 2 * g2 * c
cc = (n2 - 1) // (2*g2) - c
a2, b2 = (-bb - iroot(bb ** 2 - 4 * cc * aa, 2)[0]) // (2 * aa), (-bb + iroot(bb ** 2 - 4 * cc * aa, 2)[0]) // (2 * aa)

p2, q2 = 2 * g2 * a2 + 1, 2 * g2 * b2 + 1
print(long_to_bytes(pow(c2, inverse(e, (p2 - 1) * (q2 - 1)), n2)).decode())

'''
d = 11080995
100.00% of baby step
baby step : 17.612889289855957 Seconds
memory size of baby : 2507419432
6.25% of giant step
giant step : 2.964820384979248 Seconds
c = 2031938446870488
MRCTF{k33p1ng_th3_C0mm0M_f@ct0r_g_C0ncea1ed_@t_A11_t1m3s_is_Imp0rtant}
'''
