from Crypto.Util.number import *
from Crypto.Cipher import AES
from secrets import flag
from math import ceil
from binascii import unhexlify
from os import urandom

BLOCKSIZE = 16

def pad(s):
    length = BLOCKSIZE - len(s) % BLOCKSIZE
    return s + b"\x00" * length

def rsa_pad(m, size):
    return b"\x00" * 2 + m + urandom(size - 2 - len(m))

def genkey(bits):
    e = 65537
    p = getPrime(bits)
    q = getPrime(bits)
    if p > q:
        p, q = q, p
    d = inverse(e, (p - 1) * (q - 1))
    n = p * q
    u = inverse(q, p)
    dp = d % (p - 1)
    dq = d % (q - 1)
    sk = (n, e, d, p, q, dp, dq, u)
    pk = (n, e)
    return sk, pk

def rsa_encrypt(m, pk):
    n, e = pk
    m_padded = rsa_pad(m, ceil(n.bit_length() / 8))
    c = pow(bytes_to_long(m_padded), e, n)
    return long_to_bytes(c)

def rsa_decrypt(c, sk):
    c = bytes_to_long(c)
    n, e, d, p, q, dp, dq, u = sk
    mp = pow(c, dp, p)
    mq = pow(c, dq, q)
    t = (mp - mq) % p
    h = (u * t) % p
    m = (h * q + mq) % n
    m = long_to_bytes(m)
    m = m.rjust(ceil(n.bit_length() / 8), b"\x00")
    return m[2:]

def encrypt_sk(sk, kM):
    n, e, d, p, q, dp, dq, u = sk
    lp = long_to_bytes(ceil(p.bit_length() / 8) * 8)
    lq = long_to_bytes(ceil(q.bit_length() / 8) * 8)
    ld = long_to_bytes(ceil(d.bit_length() / 8) * 8)
    lu = long_to_bytes(ceil(u.bit_length() / 8) * 8)
    s = lq + long_to_bytes(q) + lp + long_to_bytes(p) + ld + long_to_bytes(d) + lu + long_to_bytes(u)
    s = pad(s)
    return aes_encrypt(s, kM)

def aes_encrypt(pt, key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(pt)

def aes_decrypt(ct, key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(ct)

def decrypt_sk(sk_enc, kM):
    sk = aes_decrypt(sk_enc, kM)

    lq = sk[:2]
    sk = sk[2:]
    q = bytes_to_long(sk[:bytes_to_long(lq) // 8])
    sk = sk[bytes_to_long(lq) // 8:]

    lp = sk[:2]
    sk = sk[2:]
    p = bytes_to_long(sk[:bytes_to_long(lp) // 8])
    sk = sk[bytes_to_long(lp) // 8:]

    ld = sk[:2]
    sk = sk[2:]
    d = bytes_to_long(sk[:bytes_to_long(ld) // 8])
    sk = sk[bytes_to_long(ld) // 8:]

    lu = sk[:2]
    sk = sk[2:]
    u = bytes_to_long(sk[:bytes_to_long(lu) // 8])
    return p, q, d, u

def query(sk_enc, c):
    p, q, d, u = decrypt_sk(sk_enc, master_key)
    dp = d % (p - 1)
    dq = d % (q - 1)
    phi = (p - 1) * (q - 1)
    n = p * q
    e = inverse(d, phi)
    sk = (n, e, d, p, q, dp, dq, u)
    return rsa_decrypt(c, sk)[:43]

query_times = 0
sk, pk = genkey(1024)
n, e, d, p, q, dp, dq, u = sk
master_key = urandom(16)
wrapped_key = encrypt_sk(sk, master_key)

print(f"my pk: {pk}")
print(f"wrapped_key: {wrapped_key.hex()}")
while query_times < 16:
    ct = unhexlify(input("ct:").strip().encode())
    wkey = unhexlify(input("wkey:").strip().encode())
    result = query(wkey, ct)
    print(f"result: {result.hex()}")
    query_times += 1

user_input = int(input("p = ").strip())
if user_input == p:
    print(flag)