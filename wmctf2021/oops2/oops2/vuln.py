#!/usr/bin/env python3
import os, ctypes
from Crypto.Cipher import AES

key = os.urandom(16)
nonces = set()

lib = ctypes.CDLL('./ocb.so')
lib.ocb_init.restype = ctypes.c_void_p
lib.ocb_encrypt.argtypes = lib.ocb_decrypt.argtypes = [ctypes.c_void_p] * 6
ocb_state = lib.ocb_init(key, 16, 16, 0)
cbuf = ctypes.create_string_buffer
def enc(nonce, plain):
    if len(nonce) != 16 or nonce in nonces: return None
    cipher, tag = cbuf(len(plain)), cbuf(16)
    nonces.add(nonce)
    if not lib.ocb_encrypt(ocb_state, nonce, plain, len(plain), cipher, tag):
        raise Exception()
    return bytes(cipher), bytes(tag)
def dec(nonce, cipher, tag):
    if len(nonce) != 16 or len(tag) != 16: return None
    plain = cbuf(len(cipher))
    if not lib.ocb_decrypt(ocb_state, nonce, cipher, len(cipher), tag, plain):
        return None
    return bytes(plain),

flag = open('flag.txt', 'rb').read().strip()
flag = flag.ljust((len(flag)+15)//16*16, b'\0')
print(AES.new(key, AES.MODE_ECB).encrypt(flag).hex())
del flag

for _ in range(1000):
    try: q = input('> ').split(' ')
    except EOFError: break
    fun = {'enc': enc, 'dec': dec}[q[0]]
    r = fun(*map(bytes.fromhex, q[1:]))
    print(' '.join(map(bytes.hex, r)))

