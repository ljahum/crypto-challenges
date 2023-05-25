#!/usr/bin/python3
# encoding: utf-8
import random
import string
import sys
import os
from hashlib import sha256
import uuid
from Crypto.Util.number import *

password = # Hidden
flag = ('flag{' + str(uuid.uuid4()) + '}').encode()

def proof_of_work():
    random.seed(os.urandom(8))
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)]).encode()
    digest = sha256(proof).hexdigest()
    printf("sha256(XXXX+%s) == %s" % (proof[4:].decode(),digest))
    printf('Give me XXXX:')
    x = read_str()
    if len(x) != 4 or sha256(x.encode()+proof[4:]).hexdigest() != digest: 
        return False
    return True

def printf(message):
    sys.stdout.write('{0}\n'.format(message))
    sys.stdout.flush()
    sys.stderr.flush()

def read_str():
    return sys.stdin.readline().strip()

def read_int():
    return int(sys.stdin.readline().strip())

def next_prime(a):
    while not isPrime(a):
        a += 2
    return a

def get_prime(a):
    suffix = getPrime(368)
    return next_prime(a ** 2 + suffix + 1)

def generate_pubkey(key):
    p, q = get_prime(getPrime(512)), get_prime(key)
    n = p * q
    return n

def airdrop(a):
    n = generate_pubkey(a)
    printf('gift: {}'.format(n))
    return

def hint(n, e, c):
    printf('n = {}'.format(n))
    printf('e = {}'.format(e))
    printf('c = {}'.format(c))
    return

def leak():
    p = get_prime(getPrime(512))
    e = 0x1000
    c = pow(bytes_to_long(flag), e, p)
    
    hint(p, e, c)
    return

def backdoor():
    printf('Input your password:')
    user_input = read_str()
    if user_input.encode() == password:
        leak()
    else:
        printf('Wrong')
        exit(0)

if __name__ == '__main__':
    if not proof_of_work():
        exit(0)
    
    a = getPrime(512)
    p = get_prime(a)
    q = get_prime(getPrime(512))
    n = p * q
    e = 0x10001
    max_time = 5
    password_enc = pow(bytes_to_long(password), e, n)
    
    printf('====================================',)
    printf('1. Airdrop                          ',)
    printf('2. Backdoor                         ',)
    printf('3. Hint                             ',)
    printf('4. Exit                             ',)
    printf('====================================',)
    
    try:
        while True:
            printf('Your choice:')
            choice = read_int()
            if choice == 1:
                if max_time > 1:
                    airdrop(a)
                    max_time -= 1
                    printf('Done!')
                else:
                    printf('Greed will destroy you!')
                continue
            elif choice == 2:
                backdoor()
                printf('Done!')
                continue
            elif choice == 3:
                hint(n, e, password_enc)
                printf('Done!')
                continue
            elif choice == 4:
                printf('bye~')
                exit(0)
                continue
            else:
                printf('Invalid!')
                continue
    except:
        exit(-1)
