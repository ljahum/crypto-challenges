#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nc 118.190.62.234 61139
import string
import random
import socketserver
import signal
import codecs
from os import urandom
from hashlib import sha256
from Crypto.Util.number import bytes_to_long
from Crypto.PublicKey import RSA
from pwnlib import flag
# from flag import FLAG
FLAG = "syc123123"

BANNER = rb"""
 __   __              ___                _   _    
 \ \ / /__ _ _ _  _  / __|_ __  ___  ___| |_| |_  
  \ V / -_) '_| || | \__ \ '  \/ _ \/ _ \  _| ' \ 
   \_/\___|_|  \_, | |___/_|_|_\___/\___/\__|_||_|
               |__/                                  
"""

MENU = rb"""
[1] Encrypt
[2] Get Public Key
[3] Hint
[4] Exit
"""

# with open('public.key', 'rb') as f:
#     public_key_bytes = f.read()
# public_key = RSA.import_key(public_key_bytes)
# N = public_key.n
# E = public_key.e


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        random.seed(urandom(128))
        alphabet = string.ascii_letters + string.digits
        proof = ''.join(random.choices(alphabet, k=16))
        hash_value = sha256(proof.encode('ascii')).hexdigest()
        self.send(('sha256(XXXX+%s) == %s' % (proof[4:], hash_value)).encode('ascii'))
        nonce = self.recv(prompt=b'Give me XXXX > ')
        if len(nonce) != 4 or sha256(nonce + proof[4:].encode('ascii')).hexdigest() != hash_value:
            return False
        return True

    def timeout_handler(self, signum, frame):
        self.send(b'\nTimeout!')
        raise TimeoutError

    def handle(self):
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(60)
        
        # if not self.proof_of_work():
        #     self.send(b'\nWrong!')
        #     self.request.close()
        #     return

        self.send(BANNER)

        signal.alarm(60)

        while True:
            self.send(MENU, newline=False)
            try:
                choice = int(self.recv(prompt=b'Enter option > '))
            except:
                self.send(b'Error!')
                break

            # Encrypt
            if choice == 1:
                try:
                    m = codecs.decode(self.recv(prompt=b'Enter your plaintext in hex > '), 'hex')
                except:
                    self.send(b'Error!')
                    break
                p = 153968892947561463433130910423126323410759636799165591389021702114666437683510051206900761184633470419355462926916540639944555392206506829613740817510569576986545547574394809985660769692935776819932389075804470955472534182563238918204213763251507569224571263085966892123989281512467636480262709943578085892103
                q = 91078337678788550380856113732590002161874591614690595506559987177756245962650830963620403229409535451650232074394902844825597202615000630379066130521140029284364601588474180552761103144048543088960529768426961392543703204873801718580269061850734541250785817836516377844270925100422275408733401835903199851667
                N = 14023230823907247942396340028004707932519323183968497524130483604995999062968885731644541966639320594662789588975044372129504873342371047208270998920922245958303004506996998092835375365132299872653508303041197925180204616779936131722402385391560305291748653430205392345612729769555702424770184273957064495853340465359759727531686594494442722086204848727180576260675823078202435969964625274066530459134773598953608230644036987075895187116090743057750228521054236086523343088098655253261017029597441231872853788104094106921929022550457025418037807451274109578146589804187920439764975120051110556311125325984214966685701
                N= 153968892947561463433130910423126323410759636799165591389021702114666437683510051206900761184633470419355462926916540639944555392206506829613740817510569576986545547574394809985660769692935776819932389075804470955472534182563238918204213763251507569224571263085966892123989281512467636480262709943578085892103
                   
                E = 0xb0c9850f9011fff3
                m = bytes_to_long(m)
                c = hex(pow(m, E, N))[2:]
                # e=0xb0c9850f9011fff3
                self.send(b'Here is your ciphertext in hex: ')
                self.send(c.encode('ascii'))

            # Get Public Key
            elif choice == 2:
                pass
                # fake_n = int('f' * 1030, 16)
                # rsa = RSA.construct((fake_n, E))
                # fake_public_key = rsa.exportKey()
                # self.send(b'\n' + fake_public_key + b'\n')
                # encrypted_flag = pow(bytes_to_long(FLAG.encode('ascii')), E, N)
                # e=0xb0c9850f9011fff3
                # self.send(hex(encrypted_flag)[2:].encode('ascii'))

            # Hint
            elif choice == 3:
                pass
                # with open('init_public_key.py', 'rb') as f:
                #     self.send(b'\n' + f.read())

            # Exit
            elif choice == 4:
                break

            else:
                self.send(b'Error!')
                break

        self.send(b'Bye!\n')
        self.request.close()


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 30002
    print(HOST, PORT)
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
'''
from random import choice
from Crypto.Util.number import isPrime, getPrime, sieve_base as primes

def get_prime(bits):
    while True:
        p = 1
        while p.bit_length() < bits:
            p *= choice(primes)
        if isPrime(p + 1):
            return p + 1

def init_public_key():
    N = get_prime(2048) * get_prime(2048)
    E = getPrime(64)
    rsa = RSA.construct((N, E))
    with open('public.key', 'wb') as f:
        f.write(rsa.exportKey())
'''