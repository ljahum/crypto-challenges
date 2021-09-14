from Crypto.Util.number import *
from secret import flag


def get_my_prime(nibt, gamma):
    g = getPrime(int(nibt * gamma))
    while True:
        p = 2 * g * getPrime(int(nibt * (0.5 - gamma))) + 1
        if isPrime(p):
            break

    while True:
        q = 2 * g * getPrime(int(nibt * (0.5 - gamma))) + 1
        if isPrime(q):
            break

    assert 2 * p > q and 2 * q > p
    return p, q, g


p1, q1, g1 = get_my_prime(1024, 0.2247)
# 230
p2, q2, g2 = get_my_prime(1024, 0.3247)
# 332
n1 = p1 * q1
n2 = p2 * q2

print(hex(n1))
# 0x48b11209b62c5bc580d00fc94886272b92814ce35fcd265b2915c6917a299bc54c2c0603c41f8bf7c8f6f2a545eb03d38f99ec995bf6658bb1a2d23056ee21c7230caa2decec688ea9ee00b0d50b39e8cd23eb2c3ddeb20f5ab26777b80052c171f47b716e72f6aee9cece92776fc65119046f9a1ad92c40e2094d7ed7526d49

print(hex(pow(bytes_to_long(b'Common prime RSA is a variant of RSA' + long_to_bytes(g1) + b'And the common factor g is large prime and p=2ga+1 q=2gb+1'), 3, n1)))
# 0x27d8d7249643668ffc115be8b61775c60596e51f6313b47ad5af8493526922f5e10026a2cdaef74e22c3eec959dd8771abe3495b18d19f97623f5a3f65f22ff8fc294fc37ceb3b43ebbbf8a9bcf622922e22c5520dbd523483b9dc54fdffcd1a1b3f02ca1f53b75413fb79399ca00034f2acf108ac9a01bd24d2b9df6e27d156

print(hex(pow(g2, 65537, n1)))
# 0xeaf06b9050a809659f962251b14d6b93009a7010f0e8d8f0fa4d71591757e98243b8ff50ec98a4e140fd8a63bbb4b8bb0a6d302a48845b8b09d1e40874fcb586ddccbb0bbf86d21540ec6c15c1d2bf925942f6f384fdc1baae7f8e06150ccd9459eb65d0f07eea16a911fa0a17e876a145dbfec83537ca2bee4641897b9f7f5

print(hex(n2))
# 0x6d457110d6044472d786936acbd3cd93c7728daa3343b35ccaa5c55eba6b35c28c831bb245b8cdd8fc8cb67a72f57e62a0e1259f5e804c487a8478f6895b302d39277bd73947598a5f8ec0a535be9e9a4d34df91df948ee44cc3d13d14e23b9651089e4767c7f0e7245df55619c92fe24483225d35f5f3ee6f74375065766ffd

print(hex(pow(bytes_to_long(flag.encode()), 65537, n2)))
# 0x15be2b0eaef8837a753587c47d3f31696a7d239d88837a9b7d903cd0d0648ef8e225ea555402693a23f305d19e7e13905be61b44c651dba5b26614bcf876234e765a724e0ed8af4a4e408e6a233c48ab9cc63e9c552ef9cd1999512aa0aca830fe6cbcbcc3c6bb354903124a2c3a12d442cdbdefdae6576f4bbc1515051b7111
