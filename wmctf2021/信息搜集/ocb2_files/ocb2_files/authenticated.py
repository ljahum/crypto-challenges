#!/usr/bin/env python3

import os, ctypes, json
from random import randint

lib = ctypes.CDLL('./libocb.so')
lib.ocb_init.restype = ctypes.c_void_p
lib.ocb_encrypt.argtypes = [ctypes.c_void_p] * 6
lib.ocb_decrypt.argtypes = [ctypes.c_void_p] * 6

key = os.urandom(16)
ocb_state = lib.ocb_init(key, 16, 16, 0)

users = set()
nonces = set()
flag = open('flag.txt', 'rb').read().strip()

def encrypt(nonce, message):
    if type(nonce) is not bytes:
        nonce = bytes.fromhex(nonce)
    if type(message) is not bytes:
        message = bytes.fromhex(message)
    if len(nonce) != 16 or nonce in nonces:
        raise Exception
    if b'admin' in message:
        raise Exception 
    nonces.add(nonce)
    c = bytes(len(message))
    t = bytes(16)
    lib.ocb_encrypt(ocb_state, nonce, message, len(message), c, t)
    return nonce.hex(), c.hex(), t.hex()

def decrypt(nonce, ciphertext, tag):
    n = bytes.fromhex(nonce)
    c = bytes.fromhex(ciphertext)
    t = bytes.fromhex(tag)
    if len(n) != 16 or len(t) != 16:
        print('wrong length')
        raise Exception
    m = bytes(len(c))
    if not lib.ocb_decrypt(ocb_state, n, c, len(c), t, m):
        print('decryption fail')
        raise Exception
    if m == flag:
        print('Sorry, flag decryptions are not allowed!')
        raise Exception
    return nonce, m.hex()

def create_new_user():
    user_id = randint(a=1, b=1<<64)
    users.add(user_id)
    credentials = {"user_id": user_id, "permissions": "user"}
    return encrypt(os.urandom(16), json.dumps(credentials).encode('utf-8'))

def get_flag(args):
    if args['user_id'] in users and args['permissions'] == "admin":
        return encrypt(os.urandom(16), flag)
    exit()  

if __name__=='__main__':
    print('We heard that there were some attacks against OCB2 recently, so rather than do expensive updates to our flag-sharing service we simply restricted flag access to admins only!')
    
    for i in range(100):
        print('1: Register a new user\n2: Get flag\n3: Encrypt a message\n4: Decrypt a message')
        i = input('Your choice (1-4): ')
        if i == '1':
            print(create_new_user())
        if i == '2':
            args = input('Please submit your encrypted credentials: ').strip().split(' ')
            try:
                credentials = json.loads(bytes.fromhex(decrypt(args[0], args[1], args[2])[1]).decode())
                print(get_flag(credentials))
            except json.JSONDecodeError:
                print('Invalid!')
                break 
        if i == '3':
            args = input('Please submit your fresh nonce and message: ').strip().split(' ')
            try:
                if len(args) != 2:
                    raise Exception
                print(encrypt(args[0], args[1]))
            except:
                print('Invalid!')
                break
        if i == '4':
            args = input('Please submit your nonce, ciphertext, and tag: ').strip().split(' ')
            try: 
                if len(args) != 3:
                    print('wrong number of arguments')
                    raise Exception
                print(decrypt(args[0], args[1], args[2]))
            except:
                print('Invalid!')
                break

